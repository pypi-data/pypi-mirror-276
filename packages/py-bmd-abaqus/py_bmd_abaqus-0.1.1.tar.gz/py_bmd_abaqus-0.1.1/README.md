# py_BMD_abaqus

## Features
- **Purpose:** Hello and welcome! This library was created in order to assign trabecular bone material property values to an ABAQUS CAE input mesh file (INP). This script uses the "Pooled" Morgan et al. Modulus-Density relationship - retrieved from DOI: 10.1016/s0021-9290(03)00071-x in order to calculate material modulus from density in g/cm^3. This tool also returns an array of element HU, density, or modulus values which can be used to easy evaluation of bone quality in the meshed region. 

## Features
- **Retains Node and Element Parameters:** When adding materials to an ABAQUS input file, sets, boundary conditions are currently NOT preserved. This may be added in the future.
- **Supported Element Types:**
  - Quadratic tetrahedral elements TYPE=C3D8

## Requirements
To run `py_BMD_abaqus`, you will need the following files:
1. An ABAQUS input file (`.inp`)
2. A CT scan (as a series of DICOM images in a folder. No other file types should be contained within the folder.)
3. An understanding of the phantom HU and density values for calibration of the DICOM HU density extraction

## Installation (this is not current)
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/py_BMD_abaqus.git
    ```
2. Navigate to the project directory:
    ```sh
    cd py_BMD_abaqus
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

<!-- ## Contact -->
<!-- For questions or issues, please contact [yourname](mailto:your.email@example.com). -->
