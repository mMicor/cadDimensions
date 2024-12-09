import re
import xml.etree.ElementTree as ET

def extract_dimensions_from_path(path_data):
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

    return width, height

def get_path_data_from_file(file_path):
    # Parse the SVG file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Look for the <path> element and extract the 'd' attribute
    namespace = {'svg': 'http://www.w3.org/2000/svg'}
    path_element = root.find('.//svg:path', namespace)
    
    if path_element is None or 'd' not in path_element.attrib:
        raise ValueError("No <path> element with a valid 'd' attribute found in the SVG file.")
    
    return path_element.attrib['d']

# Main execution
if __name__ == "__main__":
    file_path = "AMY.svg"  # Replace with your SVG file path
    try:
        path_data = get_path_data_from_file(file_path)
        width, height = extract_dimensions_from_path(path_data)
        print(f"Width: {width} mm")
        print(f"Height: {height} mm")
    except Exception as e:
        print(f"Error: {e}")
