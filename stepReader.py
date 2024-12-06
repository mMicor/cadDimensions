from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.IFSelect import IFSelect_ReturnStatus
from OCC.Core.Interface import Interface_Static
import math

def extract_units():
    """Extracts the unit system from the STEP file using Interface_Static."""
    length_unit = Interface_Static.CVal("xstep.cascade.unit")
    if "mm" in length_unit.lower():
        return "Millimeters"
    elif "m" in length_unit.lower():
        return "Meters"
    elif "in" in length_unit.lower():
        return "Inches"
    else:
        return "Unknown"

def extract_bounding_box_and_units(step_file_path):
    """Extracts the bounding box and units of a STEP file."""
    # Create a STEP reader
    step_reader = STEPControl_Reader()
    
    # Read the STEP file
    status = step_reader.ReadFile(step_file_path)
    if status != IFSelect_ReturnStatus.IFSelect_RetDone:
        raise ValueError("Error: Failed to read the STEP file.")
    
    # Transfer the shape from the STEP file
    step_reader.TransferRoots()
    shape = step_reader.Shape()
    
    # Compute the bounding box
    bbox = Bnd_Box()
    brepbndlib.Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    
    # Extract units
    units = extract_units()
    
    return {
        "bounding_box": {
            "xmin": xmin,
            "ymin": ymin,
            "zmin": zmin,
            "xmax": xmax,
            "ymax": ymax,
            "zmax": zmax
        },
        "units": units
    }

# Example usage
if __name__ == "__main__":
    step_file = "example.stp"  # Replace with your STEP file path
    try:
        result = extract_bounding_box_and_units(step_file)
        bbox = result["bounding_box"]
        units = result["units"]
        
        print("Bounding Box:")
        print(f"Xmin: {bbox['xmin']}, Xmax: {bbox['xmax']}")
        print(f"Ymin: {bbox['ymin']}, Ymax: {bbox['ymax']}")
        #print(f"Zmin: {bbox['zmin']}, Zmax: {bbox['zmax']}")
        print(f"Units: {units}")

        xDimension = bbox['xmax'] - bbox['xmin']
        yDimension = bbox['ymax'] - bbox['ymin']
        xDimRounded = math.ceil(xDimension * 1000) / 1000
        yDimRounded = math.ceil(yDimension * 1000) / 1000
        area = xDimension * yDimension
        areaRounded = math.ceil(area * 1000) / 1000
        print("Xtotal: ", xDimension)
        print("Ytotal: ", yDimension)
        print("Xrounded: ", xDimRounded)
        print("Yrounded: ", yDimRounded)
        print("Area: ", area)
        print("Area rounded: ", areaRounded)

    except Exception as e:
        print(str(e))
