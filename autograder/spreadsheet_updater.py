from tempfile import NamedTemporaryFile
import shutil
import csv
import sys

minimum_score = 0.5
hw_name_column = 6  # which column the HW name is in
# on the gradebook-downloaded spreadsheet

mark_file = sys.argv[1]  # path to output of mark.sh
blackboard_filepath = sys.argv[2]  # path to original CSV from Blackboard

# write to a temporary file
# tempfile = NamedTemporaryFile(mode='w', delete=False)

# read in the file of grades from the autograder
# store in dict of username : (mark, comments)
with open(mark_file, 'r') as f:
    print("reading in marks")
    marks = {}
    mark_reader = csv.DictReader(f, dialect='unix')
    for student in mark_reader:
        marks[student["Username"]] = (student["Mark"], student["Feedback"])

with open(blackboard_filepath, 'r') as blackboard_csv:
    reader = csv.DictReader(blackboard_csv, delimiter=',', dialect='unix')
    with open("temp.csv", "w") as output_file:
        # print(reader.fieldnames)
        hw_name = reader.fieldnames[hw_name_column]
        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames, dialect='unix')  # unix seems to solve the student ids with 0s at the start, but still prints a BOM in Last Name column header
        writer.writeheader()

        # go through original rows
        for row in reader:
            student_id = row["Username"]
            found = False
            # look for the matching student mark in the auto-generated file
            if student_id in marks:
                # update mark and comments
                student = marks[student_id]
                print('updating student', student_id)
                row['Feedback to Learner'] = student[1]
                row[hw_name] = student[0]
                found = True
            if not found and row[hw_name] == "Needs Grading":
                row[hw_name] = str(minimum_score)
                row["Feedback to Learner"] = "Misnamed file"
            writer.writerow(row)

    id_length = 7
    with open("temp.csv", "r") as input_file:
        with open("marks.csv", "w") as output_file:
            for i, line in enumerate(input_file.readlines()):
                if i == 0:
                    parts = line.split(",")
                    print(parts[0])
                    parts[0] = "\"Last Name\""
                    output_file.write(",".join(parts))
                else:
                    output_file.write(line)









