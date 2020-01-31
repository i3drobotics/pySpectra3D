from plyfile import PlyData, PlyElement, PlyProperty, PlyListProperty
import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Spectra3D():
    def __init__(self):
        self.plydata = None

    def create_header(self,plydata):
        if (self.check_valid_plydata(plydata)):
            vertex_size = len(plydata["vertex"].data)
            spectrum_size = len(plydata["spectrum"].data)
            label_size = len(plydata["label"].data)            
            ply_header = ("ply\n"
                        "format ascii 1.0\n"
                        "comment -------------------------------------------------------\n"
                        "comment This data format is a varient of the ply format for use\n"
                        "comment combining 3D and spectrometer data.\n"
                        "comment -------------------------------------------------------\n"
                        "comment Developed by i3D Robotics and is-instruments (C)2020\n"
                        "comment -------------------------------------------------------\n"
                        "comment Care has been taken to make sure the 3D data is still viewable\n"
                        "comment in standard ply readers however using custom properties and elements\n"
                        "comment may cause issues so it is advised to use i3DR's ply tools.\n"
                        "comment See [INSERT GITHUB LINK] for tools to read and write this data format\n"
                        "comment -------------------------------------------------------\n"
                        "comment Define in vertex element 3D point cloud data.\n"
                        "comment Also included is label_index, a scalar that can be used\n"
                        "comment to identify different types of points.\n"
                        "comment A label_index of 0 will refer to an un-lablled point.\n"
                        "comment Label_index can be used as a Scalar field to quickly see\n"
                        "comment the labelled groups in a point cloud.\n"
                        "element vertex {}\n"
                        "property float x\n"
                        "property float y\n"
                        "property float z\n"
                        "property uchar red\n"
                        "property uchar green\n"
                        "property uchar blue\n"
                        "property uchar label_index\n"
                        "comment -------------------------------------------------------\n"
                        "comment Define in spectrum the spectrometer data.\n"
                        "comment MUST be the same size as the 3D data.\n"
                        "comment If the point does not have spectrometer data then it should\n"
                        "comment be set to 0 0\n"
                        "element spectrum {}\n"
                        "property list uchar float wavenumber\n"
                        "property list uchar float intensity\n"
                        "comment -------------------------------------------------------\n"
                        "comment Define in label the labells used in this dataset.\n"
                        "comment Text is in ascii integer.\n"
                        "comment Label_index 0 should be 0 0 to represent non labelled data\n"
                        "element label {}\n"
                        "property uchar label_index\n"
                        "property list uchar int label_text\n"
                        "comment -------------------------------------------------------\n"
                        "end_header\n").format(vertex_size,spectrum_size,label_size)
            return ply_header

    def check_element_properties(self,plydata_element_properties,required_properties):
        # initialise found array
        properties_found = []
        for p in required_properties:
            properties_found.append(False)
        # search for required properties in ply element properties
        for p in plydata_element_properties:
            i = 0
            for c_p in required_properties:
                # look for property name in required
                if (p.name == c_p.name):
                    # look for property type in required
                    if (p.val_dtype == c_p.val_dtype):
                        # check if property is a list
                        if hasattr(p, 'len_dtype'):
                            # check if required propety is a list
                            if (hasattr(c_p, 'len_dtype')):
                                # look for property list type in required
                                if (p.len_dtype == c_p.len_dtype):
                                    properties_found[i] = True
                                    break
                        else:
                            properties_found[i] = True
                            break
                i+=1
        i = 0
        # check all required properties were found
        for p_f in properties_found:
            if not p_f:
                print("Failed to find required property: {}".format(required_properties[i]))
                return False
            i+=1
        return True

    def check_valid_plydata(self,plydata):
        # check data is of correct format
        # check data contains correct number of elements
        correct_num_of_elements = 3
        if len(plydata.elements) != correct_num_of_elements:
            print("Invalid number of elements. MUST be {}".format(correct_num_of_elements))
            return False
        # check data elements are of the correct name
        correct_elements = ["vertex","spectrum","label"]
        for c_e, e in zip(correct_elements, plydata.elements):
            if (e.name != c_e):
                print("Invalid element name. MUST be {}".format(c_e))
                return False
        # check vertex element contains at least the properties 'x','y','z' (can contain other properties if need be)
        required_props = [PlyProperty("x","float"),PlyProperty("y","float"),PlyProperty("z","float")]
        found_element_props = self.check_element_properties(plydata.elements[0].properties,required_props)
        if (not found_element_props):
            return False
        # check spectrum element contains the correct properties
        required_props = [PlyProperty("x","float"),PlyProperty("y","float"),PlyProperty("z","float"),
                            PlyListProperty("label_indices","uchar","int"),
                            PlyListProperty("similarity","uchar","float"),
                            PlyListProperty("wavenumber","uchar","float"),
                            PlyListProperty("intensity","uchar","float")]
        found_element_props = self.check_element_properties(plydata.elements[1].properties,required_props)
        if (not found_element_props):
            return False
        # check label element contains the correct properties
        required_props = [PlyListProperty("label_text","uchar","int")]
        found_element_props = self.check_element_properties(plydata.elements[2].properties,required_props)
        if (not found_element_props):
            return False
        return True

    def addSpectro(self,plydata,spectro):
        spectroData = np.array([
                        (0, 0, 0),
                        (0, 1, 1),
                        (1, 0, 1),
                        (1, 1, 0)],
                    dtype=[ ('x', 'f4'), 
                            ('y', 'f4'),
                            ('z', 'f4')])

    def read_ply(self,filename):
        # read data from file
        plydata = PlyData.read(filename)
        isDataValid = self.check_valid_plydata(plydata)
        self.plydata = plydata
        return isDataValid, plydata

    def write_ply(self,plydata,filename,isBinary=False):
        f_plyData = PlyData(plydata.elements)
        with open(filename, mode='wb') as f:
            PlyData(f_plyData, text=True).write(f)

    def plt_matplotlib(self,plydata):
        vertex = plydata['vertex']
        fig3D = plt.figure()
        ax3D = fig3D.add_subplot(111, projection='3d')

        (x, y, z) = (vertex[t] for t in ('x', 'y', 'z'))

        required_props = [PlyProperty("red","uchar"),PlyProperty("green","uchar"),PlyProperty("blue","uchar")]
        found_element_props = self.check_element_properties(plydata.elements[0].properties,required_props)
        rgbs = 'red'
        if (found_element_props):
            rgbs = []
            for t in vertex:
                rgbs.append((t['red']/255,t['green']/255,t['blue']/255))

        ax3D.scatter(x, y, z, zdir='z', c= rgbs, s=1)

        if 'spectrum' in plydata:
            print("Spectrum included")
            (xs, ys, zs, i_s) = (plydata['spectrum'][t] for t in ('x', 'y', 'z',"label_indices"))
            ax3D.scatter(xs, ys, zs, zdir='z', c= (1,0,0), s=30, picker=30)
            for x,y,z,idx in zip(xs, ys, zs, i_s):
                most_likely_idx = idx[0]
                label_text_i = plydata["label"][most_likely_idx]["label_text"]
                label_text_s = "".join(str(chr(l)) for l in label_text_i)
                #ax3D.text(x, y, z, label_text_s, zdir='x')

            def onpick(event):
                l = plydata['spectrum'][event.ind]["label_indices"][0]
                l_ss = []
                for i in l:
                    l_i = plydata["label"][i]["label_text"]
                    l_s = "".join(str(chr(l)) for l in l_i)
                    l_ss.append(l_s)

                s = plydata['spectrum'][event.ind]["similarity"][0]

                w = plydata['spectrum'][event.ind]["wavenumber"][0]
                i = plydata['spectrum'][event.ind]["intensity"][0]

                figSpec = plt.figure(figsize=(8, 6))
                axSpec = figSpec.add_subplot(111)
                #plt.subplots_adjust(right=0.6)

                columns = ('Substance','Similarity')
                data = []
                for s, o in zip(l_ss,s):
                    data.append([str(s),str(o)])
                
                #text_ml = "ML"
                #text_ml_labels = "\n".join(str(l) for l in l_ss)
                #text_ml_similarity = "\n".join(str(l) for l in s)
                #plt.figtext(0.2, 0.85, text_ml, fontsize=10, **{'horizontalalignment': 'center'})
                #plt.figtext(0.055, 0.80, text_ml_labels, fontsize=8, **{'horizontalalignment': 'left'})
                #plt.figtext(0.05, 0.80, text_ml_similarity, fontsize=8, **{'horizontalalignment': 'right'})
                # Add a table at the bottom of the axes
                the_table = plt.table(cellText=data,
                      colLabels=columns,cellLoc='center',colWidths=[0.4 for c in columns],
                      loc='upper right')
                plt.plot(w,i,'-', c='black')
                axSpec.set_title("Spectrum")
                axSpec.set_ylim([0,200])

                plt.show()
                
            fig3D.canvas.mpl_connect("pick_event", onpick)

        plt.show()

if __name__ == "__main__":
    filename = "Data/wood_room_scan_20000_labelled.ply"
    filename_out = "Data/sample_data_out.ply"

    sp3D = Spectra3D()
    print("Reading 3D PLY data...")
    res,plydata = sp3D.read_ply(filename)

    '''
    print("Reading Spectrometer data...")
    
    print("Adding spectrometer data to 3D...")
    plydata = sp3D.addSpectro(plydata,spectro)
    '''
    
    print("Plotting data...")
    sp3D.plt_matplotlib(plydata)
    print("Data plot ready.")
