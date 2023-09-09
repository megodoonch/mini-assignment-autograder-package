from setuptools import setup, find_packages

packages = find_packages(include=['mini_assigment_autograder', 'mini_assignment_autograder.*'])

setup(name='mini_assignment_autograder',
      version='0.0.1',
      description='autogrades tiny python assignments',
      # url='http://github.com/storborg/funniest',
      author='Meaghan',
      # author_email='flyingcircus@example.com',
      # license='MIT',
      # packages=['lunch_options',
      #           'lunch_options.fast_food'],
      packages=packages,
      # zip_safe=False
)

