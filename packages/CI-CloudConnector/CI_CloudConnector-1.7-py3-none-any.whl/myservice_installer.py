import subprocess

def main():
    try:

        # Install the service
        result = subprocess.run(['python', 'myservice.py', 'install'], check=True)

        print("Output:\n", result.stdout)
        print("Error (if any):\n", result.stderr)
        print("Service installed.")

        # Start the service
        result = subprocess.run(['python', 'myservice.py', 'start'], check=True)
        print("Output:\n", result.stdout)
        print("Error (if any):\n", result.stderr)
        print("Service started.")




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
