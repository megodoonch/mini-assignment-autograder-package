"""
Checks all student submissions.
If zip file is provided, extracts zipped submissions.
If spreadsheet from Blackboard is provided, adds marks and comments to the spreadsheet so it can be uploaded
"""

import csv
import importlib
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

from mini_assignment_autograder import spreadsheet_updater
from mini_assignment_autograder.checker import student_module_path


def extract_id_and_module_from_file_name(file_name):
    """
    files look like this: "Mini-Assignment 0_0512784_attempt_2022-06-13-11-46-08_my_number.py"
    Args:
        file_name: str: the name of the file as downloaded from Blackboard

    Returns: string pair: (student id, module name)
    """
    file_parts = file_name.split("_")
    student_id_number = file_parts[1]  # 0512784
    the_module = "_".join(file_parts[4:])  # my_number.py
    the_module = the_module.split(".")[0]  # my_number
    return student_id_number, the_module


class SubmissionsChecker:
    """
    Checks all submissions for a given mini-assignment
    Attributes:
        project: the name of the assignment, e.g. favourite_number
        project_path: the local path to it, currently always the same as project
        csv: the file to write the marks to as we go
        working_directory: where we'll put all the files and run the checker, currently project/marking/
        zip_path: where to find the raw assignments as downloaded from Blackboard
        spreadsheet_path: where to find the spreadsheet for the marks as downloaded from Blackboard
        extra_files: any extra files to copy into the working directory
        local_marks_path: a more permanent place to copy the spreadsheets to, so you can just delete the marking
                            subfolder when you're done

    """
    def __init__(self, project_path, spreadsheet_path=None, hw_name_column=6, zip_path=None,
                 extra_files=None, minimum_score=0, local_path_for_marks="~/Documents"):
        """
        Initialise a submission marker for an assignment
        @param project_path: local path to the specific assignment subdirectory, e.g. favourite_number
        @param spreadsheet_path: path to the spreadsheet for the marks as downloaded from Blackboard (default None)
        @param zip_path: path to the raw assignments as downloaded from Blackboard (default None)
        @param extra_files: any extra files to copy into the working directory (default None)
        """
        self.hw_name_column = int(hw_name_column)
        self.minimum_score = minimum_score
        project_parts = [s for s in project_path.split("/") if len(s) > 0]
        self.project = project_parts[-1]
        self.project_path = project_path
        self.csv = f"{self.project}.csv"
        self.submissions_directory_name = "submissions"
        self.working_directory = f"{self.project_path}/{self.submissions_directory_name}"
        self.zip_path = zip_path
        self.spreadsheet_path = spreadsheet_path
        self.extra_files = extra_files

        # update the path to where the marks will be written
        self.local_marks_path = local_path_for_marks
        self.local_marks_path += self.project
        self.local_marks_path = Path(self.local_marks_path).expanduser()

    def set_up_working_directory(self):
        """
        Unzip the submissions, rename them so Python can talk to them, copy in needed files
        """

        # make the working directory and unzip the student files
        os.makedirs(self.working_directory, exist_ok=True)
        try:
            with zipfile.ZipFile(self.zip_path) as z:
                z.extractall(self.working_directory)
                print("Extracted all submissions")

        except Exception as err:
            print(f"couldn't unzip: {err}")

        # rename the files and put them in their own folders, e.g. 1234567/my_number.py
        for file in os.listdir(self.working_directory):
            if file.endswith(".py") and file != "checker.py" and file != "hw_checker.py":
                current_id, module = extract_id_and_module_from_file_name(file)
                os.makedirs(f"{self.working_directory}/{current_id}")
                print(f"made directory {self.working_directory}/{current_id}")
                os.rename(f"{self.working_directory}/{file}",
                          f"{self.working_directory}/{student_module_path(module, current_id)}")

        self.copy_in_extra_files()

    def check_all_submissions(self):
        """
        Loops throught the submissions, builds a HWChecker for each, and runs check()
        Writes results to self.csv
        """
        # not sure if these are both needed
        # os.chdir(self.working_directory)
        sys.path.append(self.working_directory)

        # initialise the CSV file of marks
        with open(f"{self.project}/{self.csv}", 'w') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerow(
                ["Username", "Mark", "Feedback"])

        checker = importlib.import_module(f"{self.project}.hw_checker")
        # mark the assignments
        os.chdir(self.project)
        print("now in directory", os.getcwd())
        print("marking submissions in", self.submissions_directory_name)
        for student_id in os.listdir(f"{self.submissions_directory_name}"):
            if re.search(r'[a-zA-Z]', student_id): # Student folders are just their ID #s, so ignore things with letters
                continue
            print(f"student {student_id}")
            student_checker = checker.HWChecker(student_id)
            try:
                grade, comments = student_checker.check()
                with open(self.csv, 'a') as f:
                    writer = csv.writer(f, dialect='unix')
                    writer.writerow([student_id, grade, comments])
            except Exception as err:
                print("\n**FAILED**", err)
                with open(self.csv, 'a') as f:
                    writer = csv.writer(f, dialect='unix')
                    writer.writerow([student_id, student_checker.min_output_grade, # if can't mark, they get min grade
                                     f"autograding threw error: {err}"])

    def update_spreadsheet(self):
        """
        Copy the data from self.csv into a copy of the Blackboard spreadsheet
        The BB spreadsheet needs to be a very specific format, so we copy everything over and add the marks and comments
        Copy both self.csv and the copy we made, called marks.csv, to the local marks path
        """
        if self.spreadsheet_path and self.hw_name_column:
            os.makedirs(self.local_marks_path, exist_ok=True)
            print("updating spreadsheet", self.spreadsheet_path)
            spreadsheet_updater.update_spreadsheet(self.minimum_score, self.hw_name_column, f"{self.csv}", self.spreadsheet_path)
            # command = f"python spreadsheet_updater.py {self.working_directory}/{self.csv} {self.spreadsheet_path}"
            # result = subprocess.run(command.split())

            # if result.returncode == 0:
            print("copying marks to", self.local_marks_path, "/marks.csv")
            # shutil.copy(f"{self.working_directory}/{self.csv}", self.local_marks_path)
            shutil.copy("marks.csv", self.local_marks_path)

    def copy_in_extra_files(self):
        """
        used by self.set_up_working_directory
        """
        if self.extra_files is not None:
            for path in self.extra_files:
                shutil.copy(path, self.working_directory)
