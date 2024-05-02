# Blocksoft

## Description
Blocksoft is a Python based grafical user interface for shielding and apperture production in radiation therapy developed by the department of radiation oncology of the University Hospital Würzburg.<br>
With the tool the user is able to import treatmentplans in DICOM format, select the desired shieldings and appertures and export them in 3D objects in STL format. The 3D objects then are ready to be sliced and 3D printed with a 3D printer to a casting mold, which can be used to cast the desired shieldings and appertures for the treatment of a patient.<br>
The user has the ability to apply a point reduction algorithm for smoother contours in cases such as the presence of step like structures in the contour. After the rendering the use has the possibility to preview the 3D object and compare the orginal 2D contour with the point reduced version.

## Installation
The software package is provided as Python Version running on Windows. The tool makes use of `Python` and the opensource 3D modeling tool `openscad`, which have to be installed in the beginning with different subpackages.

### Python
The installed python version has to be 3.10.9 or higher and has to include the following packages:
* `numpy`
* `pydicom`
* `solid`
* `stl`
* `tkinter`
* `vtkplotlib`

### OpenSCAD
The Tool makes use of the opensource tool `openSCAD`, which has to be installed in Version 2021.01 or higher. The tool is provided under the following adress:
https://openscad.org/downloads.html

### Download and Configuration
To install the software tool clone the repository and follow the configuration instructions.
#### Configuration of the `setting.ini` file
* `blocksoft =`: provide path of the blocksoft installation folder
* `python =`: provide path of the python installation
* `openscad =`: provide path of the openSCAD installation
* `stl_def =`: provide default folder to save STL-files
* `dcm_def =`: provide default folder to load DICOM-files

#### Configuration of start by click option
To start the tool by click two files have to be configured: `blocksoft.bat` and `blocksoft.vbs`. After the configuration `blocksoft.vbs` can be moved to any location and the tool can be startet by double clicking on the file.
* `blocksoft.bat`:<br>
  The file has the folowing format:<br>
  ```
  python-path blocksoft-path
  ```
  Replace the python path with that of your python version and the second blocksoft one with the path of the `blocksoft.py` file seperated with a whitespace.<br>
  <br>
  For example:
  ```
  C:\Apps\WPy64-31090\python-3.10.9.amd64\python.exe C:\Apps\blocksoft\blocksoft.py
  ```
* `blocksoft.vbs`:<br>
  The file has the folowing format:<br>
  ```
  CreateObject("Wscript.Shell").Run "blocksoft-bat", 0, True
  ```
  Replace `blocksoft-bat` with the path to your `blocksoft.bat` file.<br>
  <br>
  For example:
  ```
  CreateObject("Wscript.Shell").Run "C:\Apps\blocksoft\blocksoft.bat", 0, True
  ```
