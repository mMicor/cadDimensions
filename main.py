import stepReader
import dxfReader
#import svgReader
import svgReader2
import os
import sys

def step_dimensions(cad_file):
    data = stepReader.extract_dimensions(cad_file)
    print(data['width'], data['height'], data['area'])

""" def stl_dimensions(cad_file):
    data = stlReader.extract_dimensions(cad_file)
    print(data['width'], data['height'], data['area']) """

def svg_dimensions(cad_file):
    data = svgReader2.extract_dimensions(cad_file)
    print(data['width'], data['height'], data['area'])

def dxf_dimensions(cad_file):
    data = dxfReader.extract_dimensions(cad_file)
    print(data['width'], data['height'], data['area'])

file_type = {
    ".stp": step_dimensions,
    ".svg": svg_dimensions,
    ".dxf": dxf_dimensions
}

def main():
    # Ask for the cad file to use
    cad_file  = input("Please enter the file path: ")

    # Check if the file exists
    if not os.path.isfile(cad_file):
        print(f"Error: File '{cad_file}' does not exist.")
        sys.exit(1)

    # Get the file extension
    _, file_extension = os.path.splitext(cad_file)

    # Find and execute the correct handler
    handler = file_type.get(file_extension.lower())
    if handler:
        handler(cad_file)
    else:
        print(f"Error: Unsupported file type '{file_extension}'.")


if __name__ == "__main__":
    main()