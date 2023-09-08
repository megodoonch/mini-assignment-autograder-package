import io
import sys

from bases.checker import *


class HWChecker(Checker):

    def __init__(self, sid):
        super().__init__(sid)

        # give the list of modules to import here
        self.modules = ["my_number"]
        # the name of the directory, checker file, and csv file
        self.project = "favourite_number"
        self.module_import_path = f'{self.project}.marking.{self.sid}.{self.module_name(0)}'

    def script_checker(self):
        """
        should print My favourite number is <n> where <n> is a number
        """
        try:
            output_string = subprocess.check_output(["python", self.module_file_path()]).decode("utf-8")
        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)


        lines = output_string.split("\n")
        text = lines[0]
        text = text.strip("\n")
        if len(output_string) == 0:
            self.lower_score(2,
                             "nothing printed when run as a script but should print `My favourite number is...'")
        else:
            if text.startswith("my favourite number is ") or text.startswith("my favorite number is ") or \
                    text.startswith("My favorite number is "):
                self.lower_score(1, f"printing should start with 'My favourite number is', but instead it prints {trunc(text)}")
            elif not text.startswith("My favourite number is "):
                self.lower_score(2, f"printing should start with 'My favourite number is', but instead it prints {trunc(text)}")

            try:
                float(text.split()[-1])  # try casting last word to float
            except ValueError:
                self.lower_score(1, f"last thing printed should have been a number, but it was a {type(text.split()[-1])}")
            except Exception as e:
                self.lower_score(3, f"running output checker failed with exception {e}")
            if len(lines) > 2:
                self.lower_score(1, f"importing module should print one line, but it prints {len(lines) -1}")

    def module_checker(self):
        """
        my_number should contain a number
        calling hooray(n) should print hooray! on n lines
        """

        mod = importlib.import_module(f'{self.project}.marking.{self.sid}.{self.module_name(0)}')

        try:
            n = mod.my_number
            if type(n) != int and type(n) != float:
                self.lower_score(1, f"my_number should be a number but it's of type {type(n)}")
        except Exception as e:
            self.lower_score(2, f"my_number failed with exception {e}")

    def module_output_checker(self):
        """
        By default, wants nothing printed on import, so we override that
        """

        try:
            output_capture = io.StringIO()
            sys.stdout = output_capture
            mod = importlib.import_module(f'{self.project}.marking.{self.sid}.{self.module_name(0)}')
            output_string = output_capture.getvalue()
            print(type(output_string))
            if not output_string.lower().startswith("my favo"):
                self.lower_score(1, "my_number should print my favourite number is... on import")

            # run the function that will print
            output_capture = io.StringIO()
            sys.stdout = output_capture
            mod.hooray(5)
            output_string = output_capture.getvalue()

            # put stout back to normal
            sys.stdout = sys.__stdout__

            output_lines = output_string.split("\n")
            if len(output_lines) == 1 and output_lines[0].lower() == "hooray! hooray! hooray! hooray! hooray!":
                self.lower_score(2,
                                 "Should print hooray! on separate lines")
            else:
                i = 0
                while i < 5:
                    line = output_lines[i]
                    if line == "Hooray!" or line == "hooray" or line == "Hooray":
                        self.lower_score(0.25, f"line {i} is {trunc(line)} but should be hooray!")

                    elif line != "hooray!":
                        self.lower_score(0.5, f"line {i} is {trunc(line)} but should be hooray!")
                    i += 1
                if len(output_lines) > 5 and not (output_lines[i] is None or output_lines[i].strip() == ""):
                    self.add_comment("extra line of print")

        except Exception as e:
            self.lower_score(3, "hooray failed with exception '{}'".format(e))


if __name__ == "__main__":
    student_id = sys.argv[1]
    checker = HWChecker(student_id)
    checker.check()

