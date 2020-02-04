from Spectra3D import Spectra3D

file_spectra3D = "Data/sample_room_scan_spectra3D.ply"

sp3D = Spectra3D()

res,plydata = sp3D.read_ply(file_spectra3D)
print("Plotting data...")
sp3D.plt_matplotlib(plydata)
print("Data plot ready.")