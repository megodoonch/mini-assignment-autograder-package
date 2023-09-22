""""
Wrapper script for checking a mini assignment

author:  Meaghan Fowlie
contact: m.fowlie@uu.nl

Given a path to a spreadsheet and to a zip file of assignments, both as downloaded from Blackboard,
    and the path to the folder of the assignment,
    runs <assignment>.hw_checker.py

For me, if student with id 0512784 hands in Mini-Assignment 0 by submitting a file called my_number.py
    at 11:46:08 on 2022-06-13, Blackboard renames the file
    Mini-Assignment 0_0512784_attempt_2022-06-13-11-46-08_my_number.py

    If Blackboard does something different for you, update function extract_id_and_module_from_file_name

You'll also need to update local_marks_path
"""

from mini_assignment_autograder.all_submissions_checker import SubmissionsChecker
import argparse

# This is the parent directory where the output will be saved to. Update it for your system.
local_marks_path = "results/digital_tools/2023/"


# get the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--spreadsheet", help="path to downloaded BB spreadsheet for marks")
parser.add_argument("-z", "--zip", help="path to zip file of submissions")
parser.add_argument('-p', '--project', required=True,
                    help="path to assignment folder (e.g. favourite_number)")
parser.add_argument("-e", "--extra-file", dest='extra_files', action='append',
                    help="path to extra file to copy into the working directory (use more than once if needed)")

args = parser.parse_args()

# extract the name of the project from the path to the project file
project_path = args.project
# project_parts = [s for s in project_path.split("/") if len(s) > 0]
# project_name = project_parts[-1]

checker = SubmissionsChecker(args.project, args.spreadsheet, args.zip, args.extra_files)
# whether we need to unzip (this can be false if it's not your first pass)
unzip = args.zip is not None
if unzip:
    checker.set_up_working_directory()
checker.copy_in_extra_files()

checker.check_all_submissions()

if args.spreadsheet is not None:
    checker.update_spreadsheet()

