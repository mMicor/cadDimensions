import subprocess
import re

def build_docker_image(tag="my_image"):
    """Builds the Docker image."""
    result = subprocess.run(
        ["docker", "build", "-t", tag, "."],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Docker build failed:")
        print(result.stderr)
    return result.returncode == 0

def run_docker_container(tag="my_image", container_name="my_container"):
    """Runs the Docker container."""
    result = subprocess.run(
        ["docker", "run", "--rm", "-e", "BUCKET_PATH=`./exampleFiles/example.stp`", "--name", container_name, tag],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Container run failed:")
        print(result.stderr)
    subprocess.run(["docker", "rm", container_name], capture_output=True)  # Cleanup
    return result.stderr  # Return error logs

def detect_missing_dependency(error_log):
    """Parses error logs to find missing dependencies."""
    match = re.search(r"ImportError: ([\w.]+): cannot open shared object file: No such file or directory", error_log)
    if match:
        return match.group(1)
    return None


def update_dockerfile(dependency_path):
    """Updates the Dockerfile to copy the missing dependency."""
    dockerfile = "Dockerfile"
    copy_command = f"COPY --from=builder {dependency_path} /usr/local/lib/\n"
    with open(dockerfile, "r") as file:
        lines = file.readlines()
    
    # Insert copy command before the last line (assumes it's the CMD/ENTRYPOINT)
    lines.insert(-1, copy_command)
    
    with open(dockerfile, "w") as file:
        file.writelines(lines)

def main():
    tag = "cad"
    container_name = "my_container"
    while True:
        print("Building Docker image...")
        if not build_docker_image(tag):
            break
        print("Running Docker container...")
        error_log = run_docker_container(tag, container_name)
        missing_dependency = detect_missing_dependency(error_log)
        if missing_dependency:
            print(f"Missing dependency detected: {missing_dependency}")
            update_dockerfile(f"/opt/conda/envs/occenv311/lib/{missing_dependency}")
        else:
            print("No missing dependencies. Container ran successfully.")
            break

if __name__ == "__main__":
    main()
