from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.IFSelect import IFSelect_ReturnStatus
from OCC.Core.Interface import Interface_Static
import math

def extract_dimensions(cad_file):
    """Extracts the bounding box and units of a STEP file."""
    # Create a STEP reader
    step_reader = STEPControl_Reader()
    print("Creating STEP reader")
    
    # Read the STEP file
    status = step_reader.ReadFile(cad_file)
    if status != IFSelect_ReturnStatus.IFSelect_RetDone:
        raise ValueError("Error: Failed to read the STEP file.")
    print("Step 2")
    
    # Transfer the shape from the STEP file
    step_reader.TransferRoots()
    shape = step_reader.Shape()
    print("Step 3")

    # Compute the bounding box
    bbox = Bnd_Box()
    brepbndlib.Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    print("Step 4")

    width = xmax - xmin
    height = ymax - ymin

    # Extract units and convert to mm if necessary
    """Extracts the unit system from the STEP file using Interface_Static."""
    length_unit = Interface_Static.CVal("xstep.cascade.unit")
    units = length_unit.lower()
    if "mm" in units:
        width = math.ceil(width) / 1000
        height = math.ceil(height) / 1000
    elif "cm" in units:
        width = math.ceil(width * 10) / 1000
        height = math.ceil(height * 10) / 1000
    elif "m" in units:
        width = math.ceil(width * 1000) / 1000
        height = math.ceil(height * 1000) / 1000 
    elif "in" in units:
        width = math.ceil(width * 25.4) / 1000
        height = math.ceil(height * 25.4) / 1000
    elif "ft" in units:
        width = math.ceil(width * 304.8) / 1000
        height = math.ceil(height * 304.8) / 1000
    elif "yd" in units:
        width = math.ceil(width * 914.4) / 1000
        height = math.ceil(height * 914.4) / 1000
    else:
        print("Unit not supported. Supported units are: Millimeters, Centimeters, Meters, Inches, Feet or Yards")



    area = width * height
    area = math.ceil(area * 1000) / 1000

    return {
        'width': width,
        'height': height,
        'area': area
    }