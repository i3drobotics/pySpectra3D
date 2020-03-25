from Spectra3D import Spectra3D
import os

file_spectra3D = "SampleData/sample_room_scan_spectra3D.ply"

os.chdir("../../")

sp3D = Spectra3D()

res,plydata = sp3D.read_ply(file_spectra3D)
print("Plotting data...")
sp3D.plt_matplotlib(plydata)
print("Data plot ready.")