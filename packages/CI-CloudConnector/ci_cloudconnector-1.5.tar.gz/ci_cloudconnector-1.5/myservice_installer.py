import subprocess

def main():
    try:
        result = subprocess.run(
            ['python', 'myservice.py', 'install'],
            capture_output=True,
            text=True,
            check=True
        )
        print("Output:\n", result.stdout)
        print("Error (if any):\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print("An error occurred:\n", e.stderr)

if __name__ == '__main__':
    main()
