# This file should be run with real python, different from all the other files in this project

import os
import sys
import subprocess
import difflib
import argparse
from pathlib import Path


def find_input_files(directory):
    """Find all .in.txt files in the given directory."""
    return [f for f in os.listdir(directory) if f.endswith('.in.txt')]


def get_output_filename(input_filename):
    """Convert input filename to corresponding output filename."""
    return input_filename.replace('.in.txt', '.out.txt')


def run_test(micropython_exe, input_file, output_file, update_mode=False):
    """Run the test and compare or update the output."""
    input_path = os.path.join('interaction', input_file)
    output_path = os.path.join('interaction', output_file)
    
    # Run main.py with the given input file
    with open(input_path, 'r') as f_in:
        result = subprocess.run(
            [micropython_exe, 'main.py'],
            input=f_in.read(),
            text=True,
            capture_output=True
        )
    
    actual_output = result.stdout
    
    if update_mode:
        # Update the expected output file
        with open(output_path, 'w') as f_out:
            f_out.write(actual_output)
        print("Updated {}".format(output_path))
        return True
    else:
        # Compare with expected output
        try:
            with open(output_path, 'r') as f_out:
                expected_output = f_out.read()
            
            if expected_output == actual_output:
                print("✅ {}: Test passed".format(input_file))
                return True
            else:
                print("❌ {}: Test failed".format(input_file))
                print("Differences:")
                diff = difflib.unified_diff(
                    expected_output.splitlines(),
                    actual_output.splitlines(),
                    fromfile=output_file,
                    tofile="actual output",
                    lineterm=''
                )
                for line in diff:
                    print(line)
                return False
        except FileNotFoundError:
            print("❌ {}: Expected output file {} not found".format(input_file, output_path))
            print("Actual output:")
            print(actual_output)
            return False


def main():
    parser = argparse.ArgumentParser(description='Test interaction with input files')
    parser.add_argument('micropython_exe', help='Path to micropython executable')
    parser.add_argument('--update', '-u', action='store_true', 
                      help='Update expected output files with actual output')
    parser.add_argument('--file', '-f', help='Test a specific input file')
    args = parser.parse_args()
    
    # Create interaction directory if it doesn't exist
    Path('interaction').mkdir(exist_ok=True)
    
    if args.file:
        # Test a specific file
        if not args.file.endswith('.in.txt'):
            print("Error: Input file must end with .in.txt")
            return 1
        
        output_file = get_output_filename(args.file)
        success = run_test(args.micropython_exe, args.file, output_file, args.update)
        return 0 if success else 1
    else:
        # Test all input files in the interaction directory
        input_files = find_input_files('interaction')
        if not input_files:
            print("No input files found in the interaction directory")
            return 0
        
        print("Found {} input files".format(len(input_files)))
        failures = 0
        
        for input_file in input_files:
            output_file = get_output_filename(input_file)
            if not run_test(args.micropython_exe, input_file, output_file, args.update):
                failures += 1
        
        if failures > 0:
            print("{} test(s) failed".format(failures))
            return 1
        else:
            print("All tests passed!")
            return 0


if __name__ == '__main__':
    sys.exit(main())