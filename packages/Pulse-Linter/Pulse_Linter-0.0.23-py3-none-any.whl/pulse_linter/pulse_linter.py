import subprocess
import sys

def run_flake(directory):
    try:
        result = subprocess.run(['flake8', directory], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if result.stderr:
            return f"Error running flake8: {result.stderr}"
        return result.stdout
    except Exception as e:
        return f'An error occurred while processing: {e}'

def main():
    default_path = r'C:\Users\bornd\Desktop\Reflections\vuln_code'  # windows
    # default_path = r'/home/sooraj/Downloads/Lern-main'  # linux

    if len(sys.argv) > 1:
        dir_path = sys.argv[1]
    else:
        dir_path = input(f"Path to scan, default = '{default_path}': ") or default_path

    out = run_flake(dir_path)
    print(out)

if __name__ == "__main__":
    main()
