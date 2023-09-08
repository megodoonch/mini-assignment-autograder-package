from checker import *


class HWChecker(Checker):
    """
    Attributes (new)
        modules: list of strings; the modules the students will hand in (minus the .py)
        project: str; the hw name, shared by the directory, python file for the checker, and csv file
    """

    def __init__(self, sid):
        super().__init__(sid)

        # give the list of modules to import here
        self.modules = ["hello"]
        # the name of the directory, checker file, and csv file
        self.project = "printing"

    def script_checker(self):
        """
        default: pass
        override to run as a script and inspect output
        """
        output_string = subprocess.check_output(["python", f"{self.sid}-{self.modules[0]}.py"]).decode("utf-8").strip()
        if not output_string.lower() == "hello world":
            self.lower_score(2, f"should print 'hello world', but instead it prints {trunc(output_string)}")

    def module_output_checker(self):
        """
        override to see what it prints when imported
        default: check that nothing was printed when imported
        """

        import_output = subprocess.check_output(["python", "importer.py", f"{self.sid}-{self.modules[0]}"],
                                                timeout=10).decode("utf-8").strip()
        if not import_output.lower() == "hello world":
            self.lower_score(2, f"should print 'hello world', but instead it prints {trunc(import_output)}")

    def module_checker(self):
        """
        override to import as a module and inspect it
        default: pass
        """

        # import sid-hello.py
        hello = importlib.import_module(self.module_file_path(0))

        # check variables etc
        try:
            msg = hello.message()
            if msg != "hello world":
                self.lower_score(3, "msg should be 'hello world' but it is {}".format(trunc(msg)))

        except Exception as e:

            self.lower_score(3,
                             "message failed with exception '{}'".format(e))

        # if function prints to sout, redirect it to the output file.
        try:
            # direct stout to a file
            output = open(self.out_file, 'w')
            orig_stdout = sys.stdout
            sys.stdout = output

            # run the function that will print
            hello.greet()

            # put stout back to normal
            sys.stdout = orig_stdout
            output.close()

            # read file back in and check it's right

            with open(self.out_file, 'r') as f:
                l = f.read().strip("\n").lower()
                if l != "hello world":
                    self.lower_score(1, f"should print hello world, but printed {trunc(l)}")

        except Exception as e:
            self.lower_score(3,
                             "greet failed with exception '{}'".format(e))


if __name__ == "__main__":
    # command line arg: student id number
    checker = HWChecker(sys.argv[1])
    checker.check()
