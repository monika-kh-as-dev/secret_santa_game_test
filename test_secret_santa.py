import pytest
from secret_santa import SecretSantaGame


def test_valid_secret_santa_assignment(tmp_path):
    employees_file = tmp_path / "employees.csv"
    previous_file = tmp_path / "previous.csv"

    employees_file.write_text(
        "Employee_Name,Employee_EmailID\n"
        "TEST,test@mail.com\n"
        "DEMO,demo@mail.com\n"
        "EXAMPLE,example@mail.com\n"
    )

    previous_file.write_text(
        "Employee_Name,Employee_EmailID,Secret_Child_Name,Secret_Child_EmailID\n"
        "TEST,test@mail.com,DEMO,demo@mail.com\n"
    )

    game = SecretSantaGame(str(employees_file), str(previous_file))
    game.load_employees()
    game.load_previous_assignments()

    assignments = game.generate_assignments()

    for giver_email, receiver in assignments.items():
        assert giver_email != receiver["Employee_EmailID"]
        assert game.previous_assignments.get(giver_email) != receiver["Employee_EmailID"]
