import csv
import io
from abc import ABC, abstractmethod
import subprocess
import importlib
import sys


def student_module_path(module, sid):
    return f"{sid}/{module}.py"


class Checker(ABC):
    """
    Abstract Class for marking mini-assignment
    Implement this for each assignment
    A new Checker instance is created for each student's assignment

    internal vs output grades: all the assignments I made are built assuming a total of 10, but you might want to
        report a grade out of a different amount, e.g. 100 or 1. internal grades are out of 10, unless you change that,
        and external grades are calculated at the end

    Attributes:
        sid : (str) student ID number
        grade : (float) tracks the student's grade
        comments : (str) gathers the comments into a string

        show_subtractions : (bool) if false, comments don't include specific point losses
        full_points_if_runs : (bool) if true, students get 100% as long as running/importing doesn't throw errors

        max_internal_grade : what counts as 100% within the autograder (see comment about internal and output grades)
        min_internal_grade : the lowest grade possible within the autograder
        max_output_grade : (int or float) what counts as 100% in the final score
        min_output_grade : (int or float) the lowest grade possible in the final score (calculated from the above)

        unusable : (bool) true if importer and/or script checker threw error

    """

    project: str
    modules: [str]

    def __init__(self,
                 sid,
                 submissions_folder_name="submissions",
                 show_subtractions=True,
                 full_points_if_runs=False,
                 max_output_grade=1,
                 max_internal_grade=10,
                 min_internal_grade=5
                 ):
        """
        :param sid: student id number
        """
        # self.csv = f"{self.project}.csv"
        self.sid = sid
        self.comments = ""
        self.show_subtractions = show_subtractions  # if True, prints the subtracted marks for each infraction
        self.full_points_if_runs = full_points_if_runs  # if True, students lose points only for code that throws errors
        self.max_output_grade = max_output_grade  # report mark out of 1 since it's worth only 1%
        self.max_internal_grade = max_internal_grade  # max score for the grader, traditionally 10
        self.min_internal_grade = min_internal_grade # this'll replace their mark if it goes below it
        self.grade = self.max_internal_grade  # initialise to 100%
        self.min_output_grade = self.min_internal_grade * (self.max_output_grade / self.max_internal_grade)
        self.unusable = False
        self.parent_folder_name = submissions_folder_name

    def module_name(self, n=0):
        """
        makes the module name for the nth module of self.modules
        Args:
            n: int: which module

        Returns:
            str: {self.modules[n]}
        """
        return f"{self.modules[n]}"

    def module_file_path(self, n=0):
        """
        Makes the file name for the nth module of self.modules
        Args:
            n: int: which module

        Returns:
            str: f"{self.id}/{self.modules[n]}.py"
        """
        return f"{self.parent_folder_name}/{self.sid}/{self.modules[n]}.py"

    def script_checker(self):
        """
        Runs submitted file as a script and checks the output
        :return:
        """
        pass

    def module_import_path(self, n=0):
        return f'{self.parent_folder_name}.{self.sid}.{self.module_name(n)}'

    def module_checker(self):
        """
        imports all modules and updates grades and comments
        Note we check in check() whether the modules are importable,
        and remove them from self.modules if not.
        :return:
        """
        pass

    def module_output_checker(self):
        """
        checks what is printed when imported as a module
        Default behaviour: checks that nothing was printed on import.
        Override it if you want a different behaviour, e.g. pass
        """

        for i in range(len(self.modules)):
            try:
                output_capture = io.StringIO()
                sys.stdout = output_capture
                output_string = output_capture.getvalue()
                # put stout back to normal
                sys.stdout = sys.__stdout__
                if len(output_string) > 0:
                    self.lower_score(
                        2,
                        f"{self.modules[i]} shouldn't print when called as a module, but it prints {trunc(output_string)}"
                    )
            except subprocess.CalledProcessError as e:
                self.lower_score(10, f"importing {self.modules[i]} raised error: {e.output}")

    def add_comment(self, c):
        """
        makes a comment appropriate for the csv out of a string
        removes any commas, adds a space and a semicolon at the end
        :param c: string
        :return: string
        """
        c = c.replace('\n', ' ')
        self.comments += f"{c}; "

    def lower_score(self, points, comment=None):
        print_points = points * (self.max_output_grade / self.max_internal_grade)
        if comment is None:
            comment = ""
        if self.show_subtractions:
            self.add_comment("(-{}) {}".format(print_points, comment))
        else:
            self.add_comment(comment)
        self.grade -= points

    def check(self):
        """
        checks the homework, calling script_checker, module_output_checker, and module_checker
        """

        self.script_checker()
        self.module_output_checker()
        self.module_checker()

        # adjust mark according to rules about minimum and maximum scores
        if self.grade < self.min_internal_grade:
            self.grade = self.min_internal_grade

        if self.grade >= self.max_internal_grade:
            self.add_comment("Excellent!")

        if self.full_points_if_runs and self.grade < self.max_internal_grade:
            self.grade = self.max_internal_grade

        if self.unusable:
            self.grade = self.min_internal_grade

        self.grade = self.grade * (self.max_output_grade / self.max_internal_grade)
        self.grade = round(self.grade, 3)
        self.comments = f"Score {self.grade}/{self.max_output_grade}; Comments: {self.comments}"

        # write to csv
        # with open(self.csv, 'a') as f:
        #     writer = csv.writer(f, dialect='unix')
        #     writer.writerow([self.sid, self.grade, self.comments])
        return self.grade, self.comments


def trunc(text, length=100):
    """
    truncates `text` to `length`
    Args:
        text: string
        length: int (default 30)

    Returns:
        string of length `length` plus "..."
    """
    if len(text) > length:
        return text[:30] + "..."
    else:
        return text
