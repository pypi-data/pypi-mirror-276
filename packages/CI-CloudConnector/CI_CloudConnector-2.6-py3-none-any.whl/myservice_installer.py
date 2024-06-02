import os
import subprocess
import time


def main():
    try:

        # Path to the virtual environment
        venv_path = 'venv'  # Adjust the path to your virtual environment
        python_executable = os.path.join(venv_path, 'Scripts', 'python')  # On Windows
        # python_executable = os.path.join(venv_path, 'bin', 'python')  # On Unix or MacOS

        print("python_executable", python_executable)

        # Install the service
        result_install = subprocess.run([python_executable, 'myservice.py', 'install'], capture_output=True, text=True,
                                        check=True)
        print("Output (install):\n", result_install.stdout)
        print("Error (install if any):\n", result_install.stderr)
        print("Service installed.")

        # Start the service
        result_start = subprocess.run([python_executable, 'myservice.py', 'start'], capture_output=True, text=True,
                                      check=True)
        print("Output (start):\n", result_start.stdout)
        print("Error (start if any):\n", result_start.stderr)
        print("Service started.")

        time.sleep(10)

        #result = subprocess.run(
        #    ['python', 'myservice.py', 'install'],
        #    capture_output=True,
        #    text=True,
        #    check=True
        #)
        #print("Output:\n", result.stdout)
        #print("Error (if any):\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print("An error occurred:\n", e.stderr)

if __name__ == '__main__':
    main()
