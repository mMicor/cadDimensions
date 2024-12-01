import sys
import ezdxf
import csv

try:
    doc = ezdxf.readfile("Alec_Paras_laser_cut.dxf")
    print("Success")
except IOError:
    print(f"Not a DXF file or a generic I/O error.")
    sys.exit(1)
except ezdxf.DXFStructureError:
    print(f"Invalid or corrupted DXF file.")
    sys.exit(2)
    
print ("EXTMAX ", doc.header["$EXTMAX"])
print ("EXTMIN ", doc.header["$EXTMIN"])
print ("LIMMAX ", doc.header["$LIMMAX"])
print ("LIMMIN ", doc.header["$LIMMIN"])

with open('data.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(doc.header["$EXTMAX"])
    spamwriter.writerow(doc.header["$EXTMIN"])