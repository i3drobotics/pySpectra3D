from Spectra3D import Spectra3D
import os

file_3D_in = "SampleData/sample_room_scan_20000.ply"
file_spectral_list_in = "SampleData/sample_spectrum_list.csv"
file_labels_in = "SampleData/sample_spectrum_labels.csv"
file_out = "SampleData/sample_data_out.ply"

sp3D = Spectra3D()

# generate example data for testing
# choose which data to generate and which data to read from file
# e.g. gen3D = true, genSpec = false: will generate random 3D data but read spectrum from file
gen3D = True
genSpec = True

if (gen3D):
    # generate 3D data
    x_range = (0,10)
    y_range = (0,10)
    z_range = (0,10)
    num_of_points = 1000
    file_3D = "SampleData/gen_3D_data.ply"
    print("Generating 3D test data...")
    ply3D = sp3D.generate_3D(x_range,y_range,z_range,num_of_points)
    # save 3D data to PLY
    sp3D.write_ply(ply3D,file_3D)
    file_3D_in = file_3D

# read point cloud data from PLY file
print("Reading 3D data...")
res, data_3D = sp3D.read_ply(file_3D_in)
data_3D = data_3D["vertex"]

# generate spectra
if (genSpec):
    if (not gen3D):
        x_range = (min(data_3D["x"]),max(data_3D["x"]))
        y_range = (min(data_3D["y"]),max(data_3D["y"]))
        z_range = (min(data_3D["z"]),max(data_3D["z"]))
    num_of_spectra = 20
    wavenumber_range = (0,2500)
    intensity_range = (0,100)
    num_of_points = 1000
    num_of_labels = 5
    file_labels = "SampleData/gen_labels.csv"
    file_spectra_list = "SampleData/gen_spectrum_list.csv"

    # generate label data
    data_labels = sp3D.generate_labels(num_of_labels)
    data_labels_formatted = []
    for d in data_labels:
        d_formatted = [d]
        data_labels_formatted.append(d_formatted)
    # save list of labels to csv
    sp3D.write_csv(file_labels,data_labels_formatted)
    file_labels_in = file_labels
    
    # generate spectrum data (xyz position and spectrum data)
    print("Generating spectral test data...")
    xyz_spectra = []
    for i in range(0,num_of_spectra):
        file_spectra = 'SampleData/gen_spectrum_data_{}.csv'.format(i)
        spectra_data, xyz_data = sp3D.generate_spectra(wavenumber_range,intensity_range,x_range,y_range,z_range,num_of_points,len(data_labels))
        # write spectral data to csv
        sp3D.write_csv(file_spectra,spectra_data)
        file_spectra_formatted = '\"{}\"'.format(file_spectra)
        xyz_spectra.append([xyz_data[0],xyz_data[1],xyz_data[2],file_spectra_formatted])
    # write xyz data with file name location of spectra to csv
    sp3D.write_csv(file_spectra_list,xyz_spectra)
    file_spectral_list_in = file_spectra_list

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

# clean up generated files
if (gen3D):
    os.remove(file_3D_in)
if (genSpec):
    os.remove(file_labels_in)
    os.remove(file_spectral_list_in)
    for i in range(0,num_of_spectra):
        file_spectra = 'SampleData/gen_spectrum_data_{}.csv'.format(i)
        os.remove(file_spectra)

print("Creating spectra3D data...")
res, plydata = sp3D.createSpectra3D(data_spectra,data_labels,data_3D)
print("Saving data...")
sp3D.write_ply(plydata,file_out)
print("Data saved sucessfully.")

res,plydata = sp3D.read_ply(file_out)
print("Plotting data...")
sp3D.plt_matplotlib(plydata)
print("Data plot ready.")