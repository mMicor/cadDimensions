import os
import xml.etree.ElementTree as ET

def extract_dimensions(x3d_file):
    """
    Extracts the dimensions from the provided X3D file.

    Args:
        x3d_file (str): The path to the X3D file.

    Returns:
        dict: A dictionary containing the width, height, and depth of the bounding box.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file cannot be parsed or contains no valid geometry.
    """

    # Parse the X3D file
    try:
        tree = ET.parse(x3d_file)
        root = tree.getroot()
    except ET.ParseError as e:
        raise ValueError(f"Failed to parse the X3D file: {e}")

    # Look for bounding box information in the X3D file
    bbox_elements = root.findall(".//*[@bboxCenter][@bboxSize]")

    if not bbox_elements:
        raise ValueError("No bounding box information found in the X3D file.")

    # Initialize bounding box dimensions
    xmin, ymin, zmin = float('inf'), float('inf'), float('inf')
    xmax, ymax, zmax = float('-inf'), float('-inf'), float('-inf')

    for element in bbox_elements:
        bbox_center = element.attrib.get("bboxCenter", "0 0 0").split()
        bbox_size = element.attrib.get("bboxSize", "0 0 0").split()

        if len(bbox_center) != 3 or len(bbox_size) != 3:
            continue

        cx, cy, cz = map(float, bbox_center)
        sx, sy, sz = map(float, bbox_size)

        xmin = min(xmin, cx - sx / 2)
        ymin = min(ymin, cy - sy / 2)

        xmax = max(xmax, cx + sx / 2)
        ymax = max(ymax, cy + sy / 2)

    if xmin == float('inf') or xmax == float('-inf'):
        raise ValueError("No valid bounding box dimensions found in the X3D file.")

    # Calculate dimensions
    width = xmax - xmin
    height = ymax - ymin
    area = width * height

    return {
        'width': width,
        'height': height,
        'area': area
    }