import csv
import random
import os
import pandas as pd


class SecretSantaGame:
    def __init__(self, employees_file, previous_file=None):
        """
        Initialize the game with input file paths.

        :param employees_file: Path to employee CSV/XLSX file
        :param previous_file: Path to previous year's assignment file (optional)
        """
        self.employees_file = employees_file
        self.previous_file = previous_file
        self.employees = []
        self.previous_assignments = {}

    def _read_file(self, file_path):
        """
        Reads input data from CSV or XLSX file and returns a list of dictionaries.
        :param file_path: Path to CSV or XLSX file
        :return: List of dictionaries representing rows
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            if file_path.endswith(".csv"):
                with open(file_path, newline='', encoding="utf-8") as file:
                    return list(csv.DictReader(file))

            elif file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path)
                return df.to_dict(orient="records")

            else:
                raise ValueError("Unsupported file format. Use .csv or .xlsx")

        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {e}")

    def load_employees(self):
        """
        Loads previous year's Secret Santa assignments.
        """
        self.employees = self._read_file(self.employees_file)

        if len(self.employees) < 2:
            raise ValueError("At least two employees are required.")

    def load_previous_assignments(self):
        if not self.previous_file:
            return

        rows = self._read_file(self.previous_file)

        for row in rows:
            self.previous_assignments[
                row["Employee_EmailID"]
            ] = row["Secret_Child_EmailID"]

    def generate_assignments(self):
        """
        Generates Secret Santa assignments while enforcing all constraints:
        - No self-assignment
        - No duplicate receivers
        - No same assignment as previous year
        """
        for _ in range(1000):
            shuffled = self.employees[:]
            random.shuffle(shuffled)

            assignments = {}
            valid = True

            for giver, receiver in zip(self.employees, shuffled):
                if giver["Employee_EmailID"] == receiver["Employee_EmailID"]:
                    valid = False
                    break

                if self.previous_assignments.get(
                    giver["Employee_EmailID"]
                ) == receiver["Employee_EmailID"]:
                    valid = False
                    break

                assignments[giver["Employee_EmailID"]] = receiver

            receiver_emails = {
                r["Employee_EmailID"] for r in assignments.values()
            }

            if valid and len(assignments) == len(receiver_emails):
                return assignments

        raise Exception("Unable to generate valid Secret Santa assignments.")

    def write_output(self, assignments, output_file):
        """
        Writes the final Secret Santa assignments to a CSV output file.
        :param assignments: Mapping of employee_email -> receiver record
        :param output_file: Path to output CSV file
        """
        try:
            with open(output_file, "w", newline='', encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "Employee_Name",
                        "Employee_EmailID",
                        "Secret_Child_Name",
                        "Secret_Child_EmailID",
                    ],
                )
                writer.writeheader()

                for giver in self.employees:
                    receiver = assignments[giver["Employee_EmailID"]]
                    writer.writerow({
                        "Employee_Name": giver["Employee_Name"],
                        "Employee_EmailID": giver["Employee_EmailID"],
                        "Secret_Child_Name": receiver["Employee_Name"],
                        "Secret_Child_EmailID": receiver["Employee_EmailID"],
                    })

        except Exception as e:
            raise Exception(f"Error writing output file: {e}")


if __name__ == "__main__":
    try:
        game = SecretSantaGame("Employee-List.xlsx", "previous_year.csv")
        # game = SecretSantaGame("employees.csv", "previous_year.csv")   # For CSV input
        game.load_employees()
        game.load_previous_assignments()
        assignments = game.generate_assignments()
        game.write_output(assignments, "output.csv")
        print("Secret Santa assignments generated successfully!")

    except Exception as error:
        print(f"Error: {error}")
