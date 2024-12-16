from OCC.Core.IGESControl import IGESControl_Reader
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRep import BRep_Tool
from OCC.Core.gp import gp_Pnt

def extract_dimensions(cad_file):
    """
    Extracts the dimensions from the provided IGES file.

    Args:
        iges_file (str): The path to the IGES file.

    Returns:
        dict: A dictionary containing the width, height, and depth of the bounding box.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file cannot be parsed or contains no valid geometry.
    """

    # Initialize IGES reader
    iges_reader = IGESControl_Reader()
    status = iges_reader.ReadFile(cad_file)

    if status != 1:
        raise ValueError(f"Failed to read the IGES file: {cad_file}")

    # Transfer contents from IGES to shapes
    iges_reader.TransferRoots()
    shape = iges_reader.OneShape()

    # Compute the bounding box
    bounding_box = Bnd_Box()
    brepbndlib_Add(shape, bounding_box)

    if bounding_box.IsVoid():
        raise ValueError("No valid geometry found in the IGES file.")

    # Get the bounding box dimensions
    xmin, ymin, xmax, ymax = bounding_box.Get()
    width = xmax - xmin
    height = ymax - ymin
    area = width * height

    return {
        'width': width,
        'height': height,
        'area': area
    }