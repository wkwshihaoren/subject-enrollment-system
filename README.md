# subject-enrollment-system
Fundamentals of Software Development - Autumn 2026 AssignmentsPart 2:Software Development
Group number:Jingxiang Wang, Jason Maharjan, Miki Hayashi, Aditya Maurya.


## Task Delegation

1. Student, Student Controller -> Aditya
2. Admin, Admin Controller -> Jingxiang
3. Subject (+Enrolment), Subject Controller -> Jinxiang
4. Database -> Jason 
5. Utilities (Regex Validation, Id and Mark generators, Log Formatters, Grade calculator) -> Jason
6. GUI -> Miki

## Setting up Dev Environment

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

### Installing python dependencies
```bash
pip install -r requirements.txt
```

### Formatting

```bash
ruff check . && ruff format .
```

## Coloured Printing

For colour prints, use the c_print function imported from `utility.py` along with the log level as shown in the example:
```bash
c_print("This is a success message", "SUCCESS")
```

## Coloured Input

For coloured inputs, just use the `c_input` function. This displays the input using the required colour.
```bash
c_input("This is a prompt")
```
