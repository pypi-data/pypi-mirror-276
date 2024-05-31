import matplotlib.pyplot as plt
from pydicom import dcmread
import numpy as np
import os
import pandas as pd
from numba import njit, jit
from numba.typed import List
from functools import wraps
import time


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function {func.__name__} executed in {execution_time:.4f} seconds")
        return result
    return wrapper

def show_slice(x, y, voxeldata, IPx, IPy, shapex, shapey, xw, yw, z):
    """shows a voxel array as a seaborn heatmap for troubleshooting

    Args:
        voxeldata (array): voxel array
    """

    import plotly.graph_objects as go

    x2 = x - IPx + xw/2
    y2 = y - IPy + yw/2
    xtw, ytw = (xw*shapex, yw*shapey)
    px, py = x2/xtw, y2/ytw
    ix, iy = int(np.floor(px*shapex).item()), int(np.floor(py*shapey).item())

    print(x, y, IPx, IPy, shapex, shapey, xw, yw, z)
    value_at_point = voxeldata[iy, ix]
    print(f"Value at ({ix}, {iy}): {value_at_point}")

    # Create heatmap with Plotly
    fig = go.Figure(data=go.Heatmap(
        z=voxeldata,
        colorscale='Greys',
        zmin=-2048,
        zmax=2048,
        hoverinfo='none',  # Disable hover info
    ))

    # Annotate the specified cell
    fig.add_annotation(x=ix, y=iy, text='*', showarrow=False, font=dict(color='red', size=20))

    # Update layout to invert y-axis
    fig.update_layout(
        yaxis=dict(
            autorange='reversed'
        ),
        xaxis=dict(
            scaleanchor='y',
            scaleratio=1
        ),
        autosize=False,
        width=600,
        height=600
    )

    print(get_voxel_value(x, y, voxeldata, IPx, IPy, shapex, shapey, xw, yw))

    # Save as PNG
    fig.show()#write_image("heatmap_plotly.png")

    # Read the DICOM file
    # dcmread reads the DICOM file and loads it into a dataset object
    #image = dcmread(dicom_file)

    # Extract the pixel data from the DICOM file
    # This is typically the image data contained in the DICOM file
    #voxeldata = image.pixel_array

def findfiles(directory: str):
    """Find all files in the specified directory.

    Args:
        directory (str): Directory path as a string.

    Returns:
        list: List of filenames with absolute paths.
    """

    files_list = []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            files_list.append(os.path.abspath(os.path.join(dirpath, f)))

    return files_list

def identify_bounds(inp_file: str):
    """identifies x, y, and z bounds of the ABAQUS mesh

    Args:
        inp_file (str): ABAQUS CAE input file as a string
    """

    # Initialize empty lists to store data for each section
    node_data = []
    element_data = []
    elset_data = []

    # Flag to identify the current section
    current_section = None
    # Read the file and process each line
    with open(inp_file, 'r') as file1:
        file = file1.name.split("\\")[-1]

        for line in file1:
            # Remove leading and trailing whitespaces
            line = line.strip()
            # Check for section headers
            if "*Node" in line:
                current_section = "node"
            elif "*Element" in line:
                current_section = "element"

            # Process lines based on the current section
            if current_section == "node" and not (line.startswith("*Node") or "*End " in line or "0.,           0.,           0." in line):
                # Split the line into columns and convert to NumPy array
                node_info = np.array(line.split(','), dtype=float)
                node_data.append(node_info)

            elif current_section == "element" and not ("*Element" in line or "*End" in line or "**" in line):
                # Split the line into columns and convert to NumPy array
                element_info = np.array(line.split(','), dtype=int)
                element_data.append(element_info)
            elif current_section == "elset" and not line.startswith("*ELSET, ELSET=ES_Volume 0_MAT0, GENERATE"):
                # Split the line into columns and convert to NumPy array
                elset_info = np.array(line.split(','), dtype=str)
                # Try to convert elements to integers, replace with NaN if not possible
                try:
                    elset_info = np.array([int(value) if value.isdigit() else np.nan for value in elset_info], dtype=float)
                except ValueError:
                    # Handle the ValueError (e.g., non-integer values)
                    elset_info = np.full_like(elset_info, np.nan, dtype=float)
                # Check if all elements in elset_info are valid integers (not NaN)
                if not np.any(np.isnan(elset_info)):
                    # Add the row only if all elements are valid integers
                    elset_data.extend(elset_info)
            
        node_data = np.vstack(node_data)
        node_data = node_data[:, 1:]  # Exclude the first column
        xrange, yrange, zrange = (np.min(node_data[:, 0]), np.max(node_data[:, 0])), (np.min(node_data[:, 1]), np.max(node_data[:, 1])), (np.min(node_data[:, 2]), np.max(node_data[:, 2])),
        return(xrange, yrange, zrange)

def check_for_zinvert(dc):
    """identifies if the DICOM image is inverted

    Args:
        dc (pydicom object): a pydicom dicom file

    Returns:
        int: boolean
    """

    key = (0x7005, 0x1043)
    if key in dc:
        if len(list(dc[key])) > 1:
            return dc[key][2]

    else:
        return 1

@measure_time
def createHU_matrix(directory, inp_file):
    """creates a cropped HU matrix for the bounds about the mesh inputted

    Args:
        directory (str): directory containing the DICOM files to be searched
        inp_file (str): path to the ABAQUS .inp file for mesh extraction
    """

    dcms = ([i for i in findfiles(directory)])

    dc = dcmread(dcms[0])

    zinv = (check_for_zinvert(dc))

    xrange, yrange, zrange = identify_bounds(inp_file)

    x_space, y_space, z_space, yshift, rescale = dc.PixelSpacing[0], dc.PixelSpacing[1], dc.SliceThickness, dc.PixelSpacing[1], dc.RescaleIntercept
    dataframe_list = []

    key = (0x0020, 0x0032)
    ImgPosPT = dc[key][2]
    try:
        TablePos = dc.TablePosition
    except:
        TablePos = 0

    zrange0 = zrange[0]
    zrange1 = zrange[1]

    for file in dcms:
        # Identify if the DICOM needs to be included 
        dc_file = dcmread(file, specific_tags=['SliceLocation'])

        slicelocation = dc_file.SliceLocation
        if zinv != None:
            slicelocation = slicelocation + ImgPosPT -TablePos

        if zrange0 <= slicelocation <= zrange1:
            # Read the entire DICOM image
            dc_file = dcmread(file)
            # Convert DICOM to numpy array
            image_array = dc_file.pixel_array
            slicelocation = dc_file.SliceLocation
            if zinv != None:
                slicelocation = slicelocation + ImgPosPT -TablePos

            dataframe_list.append([image_array, (dc.ImagePositionPatient)[0], (dc.ImagePositionPatient)[1], round(slicelocation,3), x_space, y_space])

    return(dataframe_list)

@njit
def calculate_centroid(element, node_data):
    nodes = element[1:]  # Exclude the first element which is the element number
    node_positions = node_data[np.isin(node_data[:,0], nodes)][:, 1:]  # Get positions of nodes in element
    centroid = np.mean(node_positions, axis=0)  # Calculate centroid
    elementdata = [element[0], centroid[0], centroid[1], centroid[2]]
    return elementdata

@jit
def calculate_centroid(element, node_data):
    # Calculate centroid of the element
    nodes = node_data[element - 1]
    num_nodes = len(nodes)
    centroid = np.zeros_like(nodes[0])  # Initialize centroid array

    # Compute mean along each dimension
    for i in range(nodes.shape[1]):
        total = 0.0
        for j in range(num_nodes):
            total += nodes[j, i]
        centroid[i] = total / num_nodes

    centroid[0] = element[0]

    return centroid

@jit
def extract_centroids_from_data(node_data, element_data):
    # Initialize empty list to store centroids
    centroids = []
    
    # Calculate centroids for each element
    for element in element_data:
        centroid = calculate_centroid(element, node_data)
        centroids.append(centroid)
    
    return centroids

def extract_centroids(inp_file, zinv, dc):
    # Read the file and process it
    node_data = []
    element_data = []

    with open(inp_file, 'r') as file1:
        file = file1.name.split("\\")[-1]
        current_section = None

        for line in file1:
            # Remove leading and trailing whitespaces
            line = line.strip()
            # Check for section headers
            if "*Node" in line:
                current_section = "node"
            elif "*Element" in line:
                current_section = "element"

            # Process lines based on the current section
            if current_section == "node" and not (line.startswith("*Node") or "*End " in line or "0.,           0.,           0." in line):
                # Split the line into columns and convert to NumPy array
                node_info = np.array(line.split(','), dtype=float)
                node_data.append(node_info)

            elif current_section == "element" and not ("*Element" in line or "*End" in line or "**" in line):
                # Split the line into columns and convert to NumPy array
                element_info = np.array(line.split(','), dtype=int)
                element_data.append(element_info)
                
    node_data = np.vstack(node_data)
    element_data = np.array(element_data)

    # Call the function to extract centroids
    centroids = np.array(extract_centroids_from_data(node_data, element_data))
    
    return centroids, element_data

@jit
def find_zindex(list: list, value: float, length: int):
    """find the index of the closest slice value, given a list of z slice positions and a target z position

    Args:
        list (list): list of voxel array z positions
        value (float): target z value of centroid
        length (int): length of voxel array list
    """

    mindiff = float(100)
    difference = float(100)
    minindex = int(0)
    for i in range(length):
        difference = np.abs(list[i] - value)
        if difference < mindiff:
            mindiff = difference
            minindex = i
    return(minindex)

@jit
def merge_on_first_col(arr1, arr2):
    """
    Merges two NumPy arrays based on the first column.

    Parameters:
    arr1 (np.ndarray): The first NumPy array.
    arr2 (np.ndarray): The second NumPy array.

    Returns:
    np.ndarray: The merged NumPy array.
    """
    # Extract the first columns
    col1_arr1 = arr1[:, 0]
    col1_arr2 = arr2[:, 0]

    # Find the indices of the matching elements
    indices = np.searchsorted(col1_arr2, col1_arr1)

    # Create a mask to filter valid indices (i.e., indices within bounds and matching values)
    mask = (indices < len(col1_arr2)) & (col1_arr1 == col1_arr2[indices])

    # Filter the data based on the mask
    filtered_arr1 = arr1[mask]
    filtered_arr2 = arr2[indices[mask]]

    # Concatenate the arrays on the columns
    merged_data = np.hstack((filtered_arr1, filtered_arr2[:, 1:]))

    return merged_data

@jit
def get_voxel_value(x: float, y: float, voxeldata, IPx: float, IPy: float, shapex: float, shapey: float, xw: float, yw: float):
    """gets voxel value at a particular x and y coordinate. This has been accelerated using numba, and is therefore not flexible with types.

    Args:
        x (float): query x - position
        y (float): query y - position
        voxeldata (ndarray): DICOM image array
        IPx (float): image position (patient) - x
        IPy (float): image position (patient) - y
        shapex (float): voxel data  - x shape
        shapey (float): voxel data  - y shape
        xw (float): voxel size - x 
        yw (float): voxel size - y
    """

    x2 = x - IPx + xw/2
    y2 = y - IPy + yw/2
    xtw, ytw = (xw*shapex, yw*shapey)
    px, py = x2/xtw, y2/ytw
    ix, iy = int(np.floor(px*shapex).item()), int(np.floor(py*shapey).item())
    voxelvalue = (voxeldata[iy, ix])

    return(voxelvalue)

@measure_time
def find_matprops(centroids, dataframe_list):

    element_w_mat = []
    
    #t = 1
    for i in centroids:

        zvalues = [zvalues[3] for zvalues in dataframe_list]
        nearestz_index = (find_zindex(List(zvalues), float(i[3]), len(zvalues)))

        voxeldata = dataframe_list[nearestz_index][0]
        IPx = dataframe_list[nearestz_index][1]
        IPy = dataframe_list[nearestz_index][2]
        xw = dataframe_list[nearestz_index][4]
        yw = dataframe_list[nearestz_index][5]
        x, y = i[1], i[2]

        shapex, shapey = float(voxeldata.shape[0]), float(voxeldata.shape[1])

        #if t == 31:
        #    show_slice(x, y, voxeldata, IPx, IPy, shapex, shapey, xw, yw, i[3])
        #    exit()
        #t = t+1

        cell_value = get_voxel_value(x, y, voxeldata, IPx, IPy, shapex, shapey, xw, yw)

        # Add the element with properties to our list
        element_w_mat.append([i[0], i[1], i[2], i[3], cell_value])

    return(element_w_mat)

def linear_equation(PD1: float, PD2: float, PHU1: float, PHU2: float):
    """ This function calculates the linear conversion between HU and density, given the HU and density values of two known phantoms.

    Args:
        PD1 (float): Phantom 1 density
        PD2 (float): Phantom 2 density
        PHU1 (float): Phantom 1 HU
        PHU2 (float): Phantom 2 HU

    Returns:
        float, float: the slope and y intercept of the linear equation.
    """

    # Calculate the slope (m)
    slope = (PD2 - PD1) / (PHU2 - PHU1)
    
    # Calculate the y-intercept (b) using one of the points
    b = PD2 - slope*PHU2

    return slope, b

@measure_time
def write_inp(element_modulus, elements, inp_file, output_filename, numberofmaterials, poisson):
    # Assign element modulus values to the node connectivity definition of the elements.
    mergeddata = merge_on_first_col(element_modulus, elements)

    # Sort by increasing modulus.
    mergeddata = mergeddata[mergeddata[:, 5].argsort()]

    # Add a new column with increasing order starting from 1
    new_column = np.arange(1, len(mergeddata) + 1)
    mergeddata = np.column_stack((new_column, mergeddata))

    # Write the header lines for the .inp file.
    result_lines = [
        "*HEADING\n",
        "Written by py_BMD_abaqus export filter\n",
        "** Units: mm\n",
        "\n",
        "*NODE\n"
    ]


    # 1. Copy the node data exactly as it is written.
    start = False
    with open(inp_file, 'r') as file:
        lines = file.readlines()

        for line in lines:
            
            if not start:
                if "*NODE" in line.upper():  # Using .upper() to make the search case-insensitive
                    start = True
                    continue
            
            if start:
                if "*ELEMENT" in line.upper():
                    break  # Using .upper() to make the search case-insensitive
                result_lines.append(f"\t{line.lstrip()}")


    # Add the element header. Currently, on C3D8 elements are supported. 
    result_lines.append(f"*ELEMENT, TYPE=C3D8\n")


    # 2. create a new element data portion for the .inp
    # Convert to integer format
    inp_data = np.concatenate((mergeddata[:, :1], mergeddata[:, 7:]), axis=1).astype(int)
    # Convert to the desired format
    lines_to_write = "\n".join(["\t" + ", ".join(map(str, row)) for row in inp_data])
    # Append the lines_to_write to result_lines
    result_lines.append(lines_to_write)


    # Identify the individual material sets
    
    # Extract the modulus column
    second_column = mergeddata[:, 6]

    # Identify the bin bounds 
    min_value = np.min(second_column)
    max_value = np.max(second_column)

    # Calculate the bin size
    binsize = (max_value - min_value) / numberofmaterials

    # Create bins
    bins = []
    for i in range(numberofmaterials + 1):
        bins.append(binsize * i + min_value)

    # Initialize a list to store binned data
    binned_data = []
    moduli = []
    densities = []

    # Iterate through each bin
    for i in range(numberofmaterials):
        # Initialize a list to store elements in the current bin
        binelements = []

        # Iterate through data and add values from the first column if the second column falls within [x1, x2]
        for row in mergeddata:
            if bins[i] <= row[6] <= bins[i + 1]:
                binelements.append(row[0])  # Add the first column value to the bin
                moduli.append([i, row[6]])  # Add the modulus to the list of included moduli
                densities.append([i, row[5]])   # Add the density to the list of included densities

        # Convert binelements to string (if needed)
        binelements = str(binelements)

        # Append the binned data for the current material to the binned_data list
        binned_data.append(["material" + str(i), [binelements]])

    result_lines.append(f"\n") # Add a new line character

    # Write the elset data for each material to the .inp file. 
    for i in range(numberofmaterials):
        # Convert string to list
        element_list = eval(binned_data[i][1][0]) 
        # Convert list to numpy array
        element_array = np.array(element_list)

        # Continue the loop if the bin is empty
        if len(element_list) < 1:
            continue

        # Add the starting text for the new element set
        result_lines.append(f"*ELSET, ELSET={binned_data[i][0]}, GENERATE\n")

        # Identify set element bounds
        first_value = int(element_array[0])
        last_value = int(element_array[-1])

        # Assign the bounds to the element set
        result_lines.append(f"{first_value},{last_value},1\n")

        # Add the footer text
        result_lines.append(f"*SOLID SECTION, ELSET={binned_data[i][0]}, MATERIAL=o1_material{i}\n")

    for i in range(numberofmaterials):
        # Add the header for each new material
        result_lines.append(f"*MATERIAL, NAME=o1_material{i}\n*DENSITY\n")

        # Filter the list to get  the values where the first element is part of the set
        filtered_moduli = [value[1] for value in moduli if value[0] == i]

        # Calculate the average modulus for the material set
        if filtered_moduli:
            average_modulus = sum(filtered_moduli) / len(filtered_moduli)
        else:
            average_modulus = 0

        # Filter the list to get  the values where the first element is part of the set
        filtered_densities = [value[1] for value in densities if value[0] == i]
        # Calculate the average density for the material set
        if filtered_densities:
            average_density = sum(filtered_densities) / len(filtered_densities)
        else:
            average_density = 0


        # Add the density, modulus, and poisson ratio value to the .inp file
        result_lines.append(f"{average_density}\n*ELASTIC\n{average_modulus}, {poisson}\n")

    # 3. open a file in write mode and write each line
    with open(output_filename, 'w') as file:
        for line in result_lines:
            file.write(line)

def extract_elementdata(dicomdirectory: str, inp_file: str, outputscale: str, phantom1HU=None, phantom2HU=None, phantom1density=None, phantom2density=None, output_filename = "output.inp", number_of_materials=20, poisson_ratio=0.3):
    """extrancts an array of elements [element number, centroid-x, centroid-y, centroid-z, value] which indicates the calibrated HU, density, or modulus values of those elements

    Args:
        dicomdirectory (str): directory of the DICOM images
        inp_file (str): path to .inp input file
        outputscale (str): ['HU', 'Density', 'Modulus']
        phantom1HU (float): calibrated hounsfield unit of phantom 1
        phantom2HU (float): calibrated hounsfield unit of phantom 2
        phantom1density (float): calibrated density unit of phantom 1 in g/cm^3
        phantom2density (float): calibrated density unit of phantom 2 in g/cm^3
        output_filename (str): path to .inp output file IF "Modulus" outputscale is selected
        number_of_materials (int): number of individual materials to create - default is 20
        poisson_ratio (float): constant poission ratio to assign to material - default is 0.3

    Returns:
        array: element material data. Output format is: HU: [element, x, y, z, <HU>], Density: [element, x, y, z, g/cm^3], Modulus: [element, x, y, z, g/cm^3, MPa]
        write: if "Modulus" selected: ABAQUS CAE .inp file with assigned material properties
    """

    dcms = findfiles(dicomdirectory)

    dc = dcmread(dcms[0])

    zinv = check_for_zinvert(dc)

    centroids, elements = extract_centroids(inp_file, zinv, dc)

    print("Identifying HU Matrix")

    dataframe_list = createHU_matrix(dicomdirectory, inp_file)

    print("Querying HU Matrix")

    elementHU = np.array(find_matprops(centroids, dataframe_list))

    if outputscale == 'HU':
        return elementHU
    
    elif (outputscale == "Density" or outputscale == 'Modulus'):
        element_density = elementHU

        # Apply the phantom calibration to convert from HU to density.
        m, b = linear_equation(phantom1density, phantom2density, phantom1HU, phantom2HU)
        element_density[:, -1] = m * element_density[:, -1] + b
        # Set all density values that are calculated to be less than zero to be zero.
        #element_density[element_density[:, -1] < 0, -1] = 0

        if outputscale == 'Modulus':
            print("Writing INP File")
            element_modulus = element_density

            # Compute the Young's Modulus according to DOI: 10.1016/s0021-9290(03)00071-x
            modulus_column = 8920 * (element_modulus[:, -1] ** 1.83)

            # Add the new column to the array
            element_modulus = np.column_stack((element_modulus, modulus_column))

            write_inp(element_modulus, elements, inp_file, output_filename, number_of_materials, poisson_ratio)
            
            return(element_modulus)

        else:
            return(element_density)
