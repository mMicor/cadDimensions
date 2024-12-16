import logging
import os
import subprocess
import azure.functions as func

def main(blob: func.InputStream, name: str):
    logging.info(f"Processing file: {name} ({blob.length} bytes)")

    # Save the uploaded file temporarily
    temp_file = f"/tmp/{name}"
    with open(temp_file, "wb") as f:
        f.write(blob.read())

    # Determine the appropriate script to run based on file type or name
    if name.endswith('.dwg'):
        script = "extract_dwg.py"
    elif name.endswith('.dxf'):
        script = "extract_dxf.py"
    else:
        logging.error("Unsupported file type")
        return

    # Run the script with the file as an argument
    try:
        result = subprocess.run(
            ["python", script, temp_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            logging.info(f"Script output: {result.stdout}")
        else:
            logging.error(f"Script error: {result.stderr}")
    except Exception as e:
        logging.error(f"Error running script: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
