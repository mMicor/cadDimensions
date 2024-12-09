#Requires pip install ezdxf

import sys
import ezdxf
import math

try:
    doc = ezdxf.readfile("example.dxf")
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

xDimension = extMax[0] - extMin[0]
yDimension = extMax[1] - extMin[1]
print("X-Dimension: ", xDimension)
print("Y-Dimension: ", yDimension)

xDimRounded = math.ceil(xDimension * 1000) / 1000
yDimRounded = math.ceil(yDimension * 1000) / 1000
print("X-Dimension rounded: ", xDimRounded)
print("Y-Dimension rounded: ", yDimRounded)

units = doc.header["$INSUNITS"]
#0 = Unitless; 1 = Inches; 2 = Feet; 3 = Miles; 4 = Millimeters; 5 = Centimeters; 6 = Meters; 7 = Kilometers; 8 = Microinches; 9 = Mils; 10 = Yards; 11 = Angstroms; 12 = Nanometers; 13 = Microns; 14 = Decimeters; 15 = Decameters; 16 = Hectometers; 17 = Gigameters; 18 = Astronomical units; 19 = Light years; 20 = Parsecs
if units == 1:
    print("Inches")
elif units == 2:
    print("Feet")
elif units == 4:
    print("Millimeters")
elif units == 5:
    print("Centimeters")
elif units == 6:
    print("Meters")
else:
    print("Unit not supported. Make sure the units of the file is either Inches, Feet, Millimeters, Centimeters or Meters.")

#measurment = doc.header["$MEASUREMENT"]
#if measurment == 0:
#    print("Imperial")
#elif measurment == 1:
#    print("Metric")

area = xDimension * yDimension
print("Area: ", area)
areaRounded = math.ceil(area * 1000) / 1000
print("Rounded area: ", areaRounded)