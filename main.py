import stepReader
import dxfReader
#import svgReader
import svgReader2
import os
import requests
import sys

def download_file(url, local_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return local_path
    else:
        raise ValueError(f"Error: Unable to download file from {url}. HTTP Status: {response.status_code}")

def step_dimensions(cad_url):
    local_file_path = "/tmp/file.stp"
    cad_file = download_file(cad_url, local_file_path)
    data = stepReader.extract_dimensions(cad_file)
    print(data['width'], data['height'], data['area'])

""" def stl_dimensions(cad_file):
    data = stlReader.extract_dimensions(cad_file)
    print(data['width'], data['height'], data['area']) """

def svg_dimensions(cad_url):
    local_file_path = "/tmp/file.svg"
    cad_file = download_file(cad_url, local_file_path)
    data = svgReader2.extract_dimensions(cad_file)
    print(data['width'], data['height'], data['area'])

def dxf_dimensions(cad_url):
    local_file_path = "/tmp/file.dxf"
    cad_file = download_file(cad_url, local_file_path)
    data = dxfReader.extract_dimensions(cad_file)
    print(data['width'], data['height'], data['area'])

file_type = {
    ".stp": step_dimensions,
    ".svg": svg_dimensions,
    ".dxf": dxf_dimensions
}

def main():
    # Ask for the cad file to use
    cad_url  = os.getenv("BUCKET_PATH")

    # Check if the file exists
    try:
        response = requests.head(cad_url)
        if response.status_code != 200:
            print(f"Error: Remote file '{cad_url}' does not exist or is inaccessible.")
            sys.exit(1)
    except requests.RequestException as e:
        print(f"Error: Failed to connect to '{cad_url}'. Exception: {e}")
        sys.exit(1)



    # Get the file extension
    _, file_extension = os.path.splitext(cad_url)

    # Find and execute the correct handler
    handler = file_type.get(file_extension.lower())
    if handler:
        handler(cad_url)
    else:
        print(f"Error: Unsupported file type '{file_extension}'.")


if __name__ == "__main__":
    main()