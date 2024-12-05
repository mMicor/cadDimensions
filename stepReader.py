from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.TopoDS import TopoDS_Shape

def extract_bounding_box(step_file_path):
    """Extracts the bounding box of a STEP file."""
    # Create a STEP reader
    step_reader = STEPControl_Reader()
    
    # Read the STEP file
    status = step_reader.ReadFile(step_file_path)
    if status != 1:  # 1 = IFSelect_RetDone
        raise ValueError("Error: Failed to read the STEP file.")
    
    # Transfer the shape from the STEP file
    step_reader.TransferRoots()
    shape = step_reader.Shape()
    
    # Compute the bounding box
    bbox = Bnd_Box()
    brepbndlib_Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    
    return {
        "xmin": xmin,
        "ymin": ymin,
        "zmin": zmin,
        "xmax": xmax,
        "ymax": ymax,
        "zmax": zmax
    }

# Example usage
if __name__ == "__main__":
    step_file = "test.stp"  # Replace with your STEP file path
    try:
        bounding_box = extract_bounding_box(step_file)
        print("Bounding Box:")
        print(f"Xmin: {bounding_box['xmin']}, Xmax: {bounding_box['xmax']}")
        print(f"Ymin: {bounding_box['ymin']}, Ymax: {bounding_box['ymax']}")
        print(f"Zmin: {bounding_box['zmin']}, Zmax: {bounding_box['zmax']}")
    except Exception as e:
        print(str(e))
