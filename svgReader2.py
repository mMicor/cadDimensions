import xml.etree.ElementTree as ET
import math
import re

def extract_dimensions(cad_file):
    """
    Extract the dimensions (width and height) of a shape from the path data in an SVG file.
    
    Args:
        file_path (str): Path to the SVG file.

    Returns:
        tuple: Width and height of the shape.
    
    Raises:
        ValueError: If no valid path data or coordinates are found in the SVG file.
    """
    # Parse the SVG file
    tree = ET.parse(cad_file)
    root = tree.getroot()

    # Look for the <path> element and extract the 'd' attribute
    namespace = {'svg': 'http://www.w3.org/2000/svg'}
    path_element = root.find('.//svg:path', namespace)
    
    if path_element is None or 'd' not in path_element.attrib:
        raise ValueError("No <path> element with a valid 'd' attribute found in the SVG file.")
    
    path_data = path_element.attrib['d']

    # Split the path data into commands and coordinates
    commands_and_coords = path_data.split()
    
    # List to store the parsed coordinates
    coordinates = []
    
    # Process each item in the list
    for i, item in enumerate(commands_and_coords):
        # Check if the item is a valid command (e.g., M, L, Z)
        if item in {'M', 'L', 'Z'}:
            continue  # Skip commands, process only coordinates
        
        # Try to parse the item as a float (it should be a coordinate)
        try:
            # Parse x and y coordinates (pairs of floats)
            x = float(commands_and_coords[i])
            y = float(commands_and_coords[i + 1])
            coordinates.append((x, y))
        except (ValueError, IndexError):
            # Skip invalid or incomplete coordinate pairs
            continue
    
    if not coordinates:
        raise ValueError("No valid coordinates found in the path data.")

    # Determine the bounding box
    min_x = min(coord[0] for coord in coordinates)
    max_x = max(coord[0] for coord in coordinates)
    min_y = min(coord[1] for coord in coordinates)
    max_y = max(coord[1] for coord in coordinates)

    # Calculate dimensions
    width = max_x - min_x
    height = max_y - min_y

    width_attr = root.attrib.get("width", "").strip()
    height_attr = root.attrib.get("height", "").strip()

    def parse_dimension(value):
        match = re.match(r"([0-9.]+)([a-z%]*)", value)
        if match:
            return match.group(2) or "px"  # Default unit is px
        return None, None
    
    wunit = parse_dimension(width_attr)
    hunit = parse_dimension(height_attr)

    if wunit == hunit:
        if "mm" in wunit:
            width = math.ceil(width) / 1000
            height = math.ceil(height) / 1000
        elif "cm" in wunit:
            width = math.ceil(width * 10) / 1000
            height = math.ceil(height * 10) / 1000
        elif "in" in wunit:
            width = math.ceil(width * 25.4) / 1000
            height = math.ceil(height * 25.4) / 1000
        elif "pt" in wunit:
            width = math.ceil(width * 0.352777778) / 1000
            height = math.ceil(height * 0.352777778) / 1000
        elif "pc" in wunit:
            width = math.ceil(width * 4.23333333) / 1000
            height = math.ceil(height * 4.23333333) / 1000
        else:
            print("Unit not supported. Supported units are: Millimeters, Centimeters, Inches, Points or Picas")
    else:
        print("Unit mismatch between height and width.")

    area = width * height
    area = math.ceil(area * 1000) / 1000

    return {
        'width': width,
        'height': height,
        'area': area
    }
