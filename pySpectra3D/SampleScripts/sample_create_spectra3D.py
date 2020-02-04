from Spectra3D import Spectra3D

file_3D_in = "SampleData/sample_room_scan_20000.ply"
file_spectral_list_in = "SampleData/sample_spectrum_list.csv"
file_labels_in = "SampleData/sample_spectrum_labels.csv"
file_out = "SampleData/sample_data_out.ply"

sp3D = Spectra3D()

# read point cloud data from PLY file
print("Reading 3D data...")
res, data_3D = sp3D.read_ply(file_3D_in)
data_3D = data_3D["vertex"]

# read list of substance labels from csv
res, data_labels = sp3D.read_spectra_labels(file_labels_in)

# read list of spectra from csv
res, xyzs, spectra_file_list = sp3D.read_spectra_list(file_spectral_list_in)

print("Reading Spectrometer data...")
data_spectra = []
for spectra_file, xyz in zip(spectra_file_list,xyzs):
    # Read spectra data from csv and convert it to format expected by 'createSpectra3D'
    res, data_spectra_n = sp3D.read_spectra(spectra_file,xyz)
    data_spectra.append(data_spectra_n)

print("Creating spectra3D data...")
res, plydata = sp3D.createSpectra3D(data_spectra,data_labels,data_3D)
print("Saving data...")
sp3D.write_ply(plydata,file_out)
print("Data saved sucessfully.")

res,plydata = sp3D.read_ply(file_out)
print("Plotting data...")
sp3D.plt_matplotlib(plydata)
print("Data plot ready.")