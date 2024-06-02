#!/usr/bin/python3

import sys
import argparse
import os
import subprocess
from tqdm import tqdm

# Testing suite names
TESTING_SUITES = ['ENT', 'PractRand', 'SmallCrush', 'Dieharder', 'NIST']

# Testing setting options
TESTING_SETTING_OPTIONS = {
    'Light': {TESTING_SUITES[0], TESTING_SUITES[1], TESTING_SUITES[2]},  # ENT, PractRand, TestU01 SmallCrush
    'Recommended': set(),  # Add actual recommended settings here
    'All': set(TESTING_SUITES),
    'Custom': set()
}

def print_testing_settings():
    """Prints the available testing settings."""
    print("Testing settings:")
    for num, setting in enumerate(TESTING_SETTING_OPTIONS.keys(), start=1):
        print(f"    ({num}): {setting}")

def handle_setting_input():
    """Handles user input for selecting a testing setting."""
    print_testing_settings()
    while True:
        # Get the selected setting from the user
        setting = input("Please select testing setting (number): ")
        try:
            setting = int(setting) - 1
            if setting not in range(len(TESTING_SETTING_OPTIONS)):
                raise ValueError
            return setting
        except ValueError:
            print(f"Invalid setting number. Please choose a number between 1 and {len(TESTING_SETTING_OPTIONS)} inclusive.")

def handle_custom_setting_input():
    """Handles user input for custom setting binary representation."""
    # Print the available testing suites
    for num, suite in enumerate(TESTING_SUITES, start=1):
        print(f"    {num}. {suite}")
    while True:
        # Get the binary input from the user
        setting_input = input("Please input binary representation of the tests to run: ")

        # Check if the input is a binary number with the correct number of digits
        if not all(char in '01' for char in setting_input) or len(setting_input) != len(TESTING_SUITES):
            print(f"Error: Please enter a binary number with exactly {len(TESTING_SUITES)} digits (0 or 1).")
        else:
            return setting_input

def handle_selected_setting(setting_index, binary_setting=None):
    """Handles the selected testing setting and returns the binary representation of the tests to run."""
    setting_name = list(TESTING_SETTING_OPTIONS.keys())[setting_index]

    # If the setting is Custom, handle the custom setting input
    if setting_name == 'Custom':
        return binary_setting if binary_setting else handle_custom_setting_input()
    
    # Else return the binary representation of the selected setting
    else:
        return ''.join('1' if suite in TESTING_SETTING_OPTIONS[setting_name] else '0' for suite in TESTING_SUITES)

def handle_directory_input():
    """Handles user input for specifying the directory to store the results in."""
    while True:
        result_dir = input("Please specify directory name to store results in (ENTER for pwd): ")
        if not result_dir:
            return os.getcwd()
        if not os.path.exists(result_dir):
            try:
                os.makedirs(result_dir)
                return result_dir
            except OSError:
                print(f"Error: Could not create directory '{result_dir}'. Please try again.")
        else:
            return result_dir

def run_testing_suites(binary_file_path, setting, result_dir):
    """Runs the testing suites with the specified binary file and setting."""
    try:
        # Count the total number of tests to run and create a progress bar
        total_tests = setting.count('1')
        with tqdm(total=total_tests, desc="Running tests", unit="test", bar_format='{l_bar}{bar:12}{r_bar}{bar:-12b}') as pbar:
            
            # Iterate over the testing suites and run the selected ones
            for suite_index, suite in enumerate(TESTING_SUITES):
                if setting[suite_index] == '1':
                    # Get the directory of the currently executing script
                    script_dir = os.path.dirname(os.path.realpath(__file__))
                    testing_suites_scripts_path = os.path.join(script_dir, f"testing_suites_scripts/run_{suite.lower()}.sh")
                    args = [testing_suites_scripts_path, binary_file_path, result_dir]

                    # Run the testing suite script
                    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    # Read the output of the process line by line and update the progress bar accordingly
                    for line in process.stdout:
                        if any(suite in line for suite in TESTING_SUITES):
                            pbar.update(1)

                    # Wait for the process to finish and get the exit code
                    process.wait()
                    exit_code = process.returncode

                    # Check if the process exited with an error
                    if exit_code != 0:
                        print(f"An error occurred while running the {suite} script.")
                        print("Error output:", process.stderr.read())

    # Handle any exceptions that occur while running the script
    except subprocess.CalledProcessError as e:
        print("An error occurred while running the script:", e)
        print("Error output:", e.stderr)

def handle_parsed_args(parser, parsed_args):
    """Handles the parsed command-line arguments."""

    # Check if the binary file is provided
    if parsed_args.binary_file:

        # Handle the testing setting input
        setting_index = handle_setting_input() if parsed_args.setting is None else parsed_args.setting - 1

        # Check if the binary input flag is used with the Custom setting
        if parsed_args.binary_setting and setting_index != list(TESTING_SETTING_OPTIONS.keys()).index('Custom'):
            print("Error: The --binary-setting (-i) flag can only be used with the Custom setting.")
            sys.exit(1)

        # Handle the selected setting
        binary_setting = parsed_args.binary_setting if setting_index == list(TESTING_SETTING_OPTIONS.keys()).index('Custom') else None
        handled_setting = handle_selected_setting(setting_index, binary_setting)

        # Handle the result directory input
        result_dir = handle_directory_input() if parsed_args.directory is None else parsed_args.directory
        os.makedirs(result_dir, exist_ok=True)

        # Run the testing suites
        run_testing_suites(parsed_args.binary_file.name, handled_setting, result_dir)
    else:
        parser.print_help()

def main(args=None):
    """Main function to parse command-line arguments and execute the script."""
    parser = argparse.ArgumentParser(description="cryptoguard is a Python package designed for conducting comprehensive testing of random number generators. It provides a collection of testing suites that evaluate the statistical properties and reliability of random number sequences.")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-b', '--binary-file', type=argparse.FileType('rb'), help="Binary file to test")
    parser.add_argument('-s', '--setting', type=int, choices=range(1, len(TESTING_SETTING_OPTIONS) + 1), help="Testing setting number (" + ", ".join(f"{idx}: {key}" for idx, key in enumerate(TESTING_SETTING_OPTIONS.keys(), start=1)) + ")")
    parser.add_argument('-i', '--binary-setting', type=str, help="Binary representation of the tests to run (only for Custom setting)")
    parser.add_argument('-d', '--directory', type=str, help="Directory to store the results (will be created if it doesn't exist)")

    # Parse the command-line arguments
    if args is None:
        args = sys.argv[1:]

    # Handle the parsed arguments
    parsed_args = parser.parse_args(args)
    handle_parsed_args(parser, parsed_args)

if __name__ == "__main__":
    main()
