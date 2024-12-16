import math
import re
import xml.etree.ElementTree as ET

def extract_dimensions(cad_file):
    try:
        # Parse the SVG file
        tree = ET.parse(cad_file)
        root = tree.getroot()

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

        if "mm" in width_unit:
            width = math.ceil(width) / 1000
            height = math.ceil(height) / 1000
        elif "cm" in width_unit:
            width = math.ceil(width * 10) / 1000
            height = math.ceil(height * 10) / 1000
        elif "in" in width_unit:
            width = math.ceil(width * 25.4) / 1000
            height = math.ceil(height * 25.4) / 1000
        elif "pt" in width_unit:
            width = math.ceil(width * 0.352777778) / 1000
            height = math.ceil(height * 0.352777778) / 1000
        elif "pc" in width_unit:
            width = math.ceil(width * 4.23333333) / 1000
            height = math.ceil(height * 4.23333333) / 1000
        else:
            print("Unit not supported. Supported units are: Millimeters, Centimeters, Inches, Points or Picas")

        area = width * height
        area = math.ceil(area * 1000) / 1000

        return {
            'width': width,
            'height': height,
            'area': area
        }

    except Exception as e:
        print(f"Error: {e}")
        return None