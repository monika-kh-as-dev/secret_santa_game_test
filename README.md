# secret_santa_game

## Overview

This project automates the Secret Santa assignment process for employees while enforcing all business rules.
It supports CSV and Excel (.xlsx) inputs, avoids self-assignment, prevents repeating last year’s assignments, and ensures a one-to-one mapping between employees and secret children.
The solution is intentionally kept simple, modular, testable, and extensible, following OOP best practices with proper error handling. 

## Features & Rules Enforced

- No employee can be assigned to themselves
- No employee receives the same secret child as the previous year
- Each employee has exactly one secret child
- Each secret child is assigned only once
- Automatic retries to ensure valid assignments
- Supports .csv and .xlsx input formats
- Robust error handling and validation

## Requirements
- Python 3.8+
- pandas
- openpyxl
- pytest

## Install dependencies:
```
pip install -r requirements.txt
```

## How to Run the code

```
python secret_santa.py
```

## Running Tests

```
pytest test_secret_santa.py
```

It validate:
- No self-assignment
- No duplicate receivers
- No repeated previous-year assignments