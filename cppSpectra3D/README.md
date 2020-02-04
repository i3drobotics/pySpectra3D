**[COMING SOON]**
# **SPECTRA 3D**
# C++ Library

C++ library for using spectroscopy data along side 3D by reading and writing the special ply format.

## **PLY HEADER**
A custom ply header is used to store the extra spectroscopy data. This includes text labels that identify the material that was scanned and x y z positioning of where the data was captured from. The spectroscopy data includes wavenumber and intensity.
It is advised to keep the comments in the header of all ply files of this type to avoid confusion by explaining the data format. 
```
ply
format ascii 1.0
comment -------------------------------------------------------
comment This data format is a varient of the ply format for use
comment combining 3D and spectrometer data.
comment -------------------------------------------------------
comment Developed by i3D Robotics and is-instruments (C)2020
comment -------------------------------------------------------
comment Care has been taken to make sure the 3D data is still viewable
comment in standard ply readers however using custom properties and elements
comment may cause issues so it is advised to use i3DR's ply tools.
comment See [INSERT GITHUB LINK] for tools to read and write this data format
comment -------------------------------------------------------
comment Define in vertex element 3D point cloud data.
comment Also included is label_index, a scalar that can be used
comment to identify different types of points.
comment A label_index of 0 will refer to an un-lablled point.
comment Label_index can be used as a Scalar field to quickly see
comment the labelled groups in a point cloud.
element vertex 8
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
comment -------------------------------------------------------
comment Define in spectrum the spectrometer data.
element spectrum 1
property float x
property float y
property float z
property list uchar int label_indices
property list uchar float similarity
property list int float wavenumber
property list int float intensity
comment -------------------------------------------------------
comment Define in label the labels used in this dataset.
comment Text is in ascii integer.
element label 5
property list uchar int label_text
comment -------------------------------------------------------
end_header
```
