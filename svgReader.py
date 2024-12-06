import re
import xml.etree.ElementTree as ET

def get_svg_dimensions_with_units(file_path):
    try:
        # Parse the SVG file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Check if it's an SVG file
        if not root.tag.endswith("svg"):
            raise ValueError("The file is not a valid SVG.")

        # Extract width, height, and viewBox
        width_attr = root.attrib.get("width", "").strip()
        height_attr = root.attrib.get("height", "").strip()
        viewBox = root.attrib.get("viewBox")

        # Regex to separate value and unit
        def parse_dimension(value):
            match = re.match(r"([0-9.]+)([a-z%]*)", value)
            if match:
                return float(match.group(1)), match.group(2) or "px"  # Default unit is px
            return None, None

        # Parse dimensions
        width, width_unit = parse_dimension(width_attr)
        height, height_unit = parse_dimension(height_attr)

        # If dimensions are missing, infer from viewBox
        if viewBox and (not width or not height):
            vb_x, vb_y, vb_width, vb_height = map(float, viewBox.split())
            width = width or vb_width
            height = height or vb_height
            width_unit = height_unit = "user units"  # Indicate no explicit unit

        return {
            "width": width,
            "width_unit": width_unit,
            "height": height,
            "height_unit": height_unit,
            "viewBox": viewBox,
        }

    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
svg_file = "AMY.svg"
dimensions_with_units = get_svg_dimensions_with_units(svg_file)
xDimension = dimensions_with_units["width"]
yDimension = dimensions_with_units["height"]
unit = dimensions_with_units["width_unit"]
area = xDimension * yDimension

print("Width: ", xDimension)
print("Height: ", yDimension)
print("Unit: ", unit)
print("Area: ", area)