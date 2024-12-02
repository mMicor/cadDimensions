import sys
import ezdxf
import csv
import math

try:
    doc = ezdxf.readfile("Alec_Paras_laser_cut.dxf")
    #print("Success")
except IOError:
    print(f"Not a DXF file or a generic I/O error.")
    sys.exit(1)
except ezdxf.DXFStructureError:
    print(f"Invalid or corrupted DXF file.")
    sys.exit(2)

extMax = doc.header["$EXTMAX"]
extMin = doc.header["$EXTMIN"]
limMax = doc.header["$LIMMAX"]
limMin = doc.header["$LIMMIN"]

print("extMax: ", extMax)    
print("extMin: ", extMin)
#print("limMin: ", limMin)
#print("limMin: ", limMin)

#with open('data.csv', 'w', newline='') as csvfile:
#    csvWriter = csv.writer(csvfile, delimiter=' ',
#                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    csvWriter.writerow(extMax)
#   csvWriter.writerow(doc.header["$EXTMIN"])

xDimension = extMax[0] - extMin[0]
yDimension = extMax[1] - extMin[1]
print("X-Dimension: ", xDimension)
print("Y-Dimension: ", yDimension)

units = doc.header["$INSUNITS"]
measurment = doc.header["$MEASUREMENT"]
print(units) #0 = Unitless; 1 = Inches; 2 = Feet; 3 = Miles; 4 = Millimeters; 5 = Centimeters; 6 = Meters; 7 = Kilometers; 8 = Microinches; 9 = Mils; 10 = Yards; 11 = Angstroms; 12 = Nanometers; 13 = Microns; 14 = Decimeters; 15 = Decameters; 16 = Hectometers; 17 = Gigameters; 18 = Astronomical units; 19 = Light years; 20 = Parsecs 
print(measurment) #0=Impersial, 1=Metric

print(math.ceil(xDimension))
xDimRounded = math.ceil(xDimension * 1000) / 1000
print(xDimRounded)