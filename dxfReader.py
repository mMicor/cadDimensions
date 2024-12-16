#Requires pip install ezdxf


import ezdxf
import math

def extract_dimensions(cad_file):
    # Open the DXF file
    try:
        doc = ezdxf.readfile(cad_file)
    except IOError:
        raise FileNotFoundError(f"File '{cad_file}' could not be read.")
    except ezdxf.DXFStructureError as e:
        raise ValueError(f"Invalid DXF file: {e}")

    ext_max = doc.header["$EXTMAX"]
    ext_min = doc.header["$EXTMIN"]
    limMax = doc.header["$LIMMAX"]
    limMin = doc.header["$LIMMIN"]

    #print("extMax: ", ext_max)
    #print("extMin: ", ext_min)
    #print("limMin: ", limMin)
    #print("limMin: ", limMin)

    width = ext_max[0] - ext_min[0]
    height = ext_max[1] - ext_min[1]

    units = doc.header["$INSUNITS"]
    #0 = Unitless; 1 = Inches; 2 = Feet; 3 = Miles; 4 = Millimeters; 5 = Centimeters; 6 = Meters; 7 = Kilometers; 8 = Microinches; 9 = Mils; 10 = Yards; 11 = Angstroms; 12 = Nanometers; 13 = Microns; 14 = Decimeters; 15 = Decameters; 16 = Hectometers; 17 = Gigameters; 18 = Astronomical units; 19 = Light years; 20 = Parsecs
    if units == 1:
        width = math.ceil(width * 25.4)
        height = math.ceil(height * 25.4)
    elif units == 2:
        width = math.ceil(width * 304.8)
        height = math.ceil(height * 304.8)
    elif units == 4:
        width = math.ceil(width)
        height = math.ceil(height)
    elif units == 5:
        width = math.ceil(width * 10)
        height = math.ceil(height * 10)
    elif units == 6:
        width = math.ceil(width * 1000)
        height = math.ceil(height * 1000)
    else:
        print("Unit not supported. Supported units are: Millimeters, Centimeters, Meters, Inches or Feet.")

    area = width * height

    return {
        'width': width,
        'height': height,
        'area': area
    }