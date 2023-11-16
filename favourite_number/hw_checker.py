import sys

from mini_assignment_autograder.checker import *


class HWChecker(Checker):
    """
    Instructions:
    store your favourite number in the variable my_number
    print "My favourite number is x" where x is my_number
    """

    def __init__(self, sid):
        super().__init__(sid)

        # give the list of modules to import here
        self.modules = ["my_number"]
        # the name of the directory, checker file, and csv file
        self.project = "digital_tools_1"
        # self.module_import_path = f'{self.sid}.{self.module_name(0)}'

    def script_checker(self):
        """
        should print My favourite number is <n> where <n> is a number
        """
        try:
            output_string = subprocess.check_output(["python", self.module_file_path()]).decode("utf-8")

            lines = output_string.split("\n")
            text = lines[0]
            text = text.strip("\n")
            if len(output_string) == 0:
                self.lower_score(2,
                                 "nothing printed when run as a script but should print `My favourite number is...'")
            else:
                if text.startswith("my favorite number is ") or \
                        text.startswith("My favorite number is "):
                    self.lower_score(1, f"printing should start with 'My favourite number is', but instead it prints {trunc(text)}")
                elif not text.startswith("My favourite number is ") and not text.startswith("my favourite number is "):
                    self.lower_score(2, f"printing should start with 'My favourite number is', but instead it prints {trunc(text)}")

                try:
                    float(text.split()[-1])  # try casting last word to float
                except ValueError:
                    self.lower_score(1, f"last thing printed should have been a number, but it was a {type(text.split()[-1])}")
                except Exception as e:
                    self.lower_score(3, f"running output checker failed with exception {e}")
                if len(lines) > 2:
                    self.lower_score(1, f"importing module should print one line, but it prints {len(lines) -1}")

        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)

    def module_checker(self):
        """
        my_number should contain a number
        calling hooray(n) should print hooray! on n lines
        """
        mod = importlib.import_module(self.module_import_path(0))

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
            mod = importlib.import_module(self.module_import_path(0))
            output_string = output_capture.getvalue()
            # print("output string", output_string, file=sys.stderr)
            if not output_string.lower().startswith("my favo"):
                self.lower_score(1, "my_number should print My favourite number is... on import")
            # reset stdout
            sys.stdout = sys.__stdout__

        except Exception as e:
            self.lower_score(3, f"Error importing module: {e}")


if __name__ == "__main__":
    checker = HWChecker(sys.argv[1])
    mark, comments = checker.check()
    print(mark)
    print(comments)