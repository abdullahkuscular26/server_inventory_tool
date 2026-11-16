
## 1. Three Python constructs used in my project
<br>

**If statement – `menu.py`, `delete_server()`**

```
if server_to_delete.get("environment") == "prod":
    print(f"WARNING: Server '{server_to_delete.get('name')}' is in PRODUCTION environment!")
    confirm = input("Are you sure you want to delete a PRODUCTION server? (yes/no): ").strip().lower()
```

I use an `if` statement to check whether the server belongs to the production environment.<br>
If the condition is true, the program asks the user for extra confirmation before deleting the server.<br>
This helps prevent accidental deletion of important production servers.

---
**While loop – `menu.py`, `add_server()`**

```
valid_environments = ["dev", "test", "prod"]

while True:
    environment = input(f"Enter environment ({', '.join(valid_environments)}): ").strip().lower()
    if environment in valid_environments:
       break
    print("Error: Invalid environment! Please choose dev, test, or prod.")
```

I use a `while` loop to make sure that the user enters a valid environment.<br>
As long as the value is invalid, the program asks again.<br> 
The loop stops when the user enters a valid value.

---
**Function with a parameter and return – `storage.py`, `load_servers()`**

```
def load_servers(filename=None):
    if filename is None:
        filename = get_data_filename()

    file_path = Path(filename)

    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
```

The function has a parameter called `filename`, with the default value `None`.<br>
It reads the JSON file and returns the server data as a Python list.<br>
If the file does not exist, it returns an empty list instead.

<br>
<br>

## 2. Why I use a list of dictionaries
<br>

I use a list of dictionaries to store the servers because the program needs to manage several servers.<br>
A list makes it possible to store all servers together and loop through them.

The following is an example of one server entry in the list, not the complete server list:

```
servers = [
    {
        "name": "web01",
        "address": "example.com",
        "environment": "prod",
        "role": "webserver",
        "status": "up",
        "last_checked": "2026-11-14 17:01"
    }
]
```

Each server is stored as a dictionary.<br> This is useful because every value has a key,
such as name, address, environment, role, status and last_checked.<br>
I can access each value by using its key, for example server["name"].

The values in each server dictionary are strings (str).<br> For example, the server name,
address, environment, role, status and last check time are all stored as text.<br>
This structure makes the server information easy to organize, read and update.

<br>
<br>

## 3. Why I use JSON for storing data and CSV for exporting reports
<br>
I use JSON to store the server data because this project doesn't use a database
such as MySQL.<br>
The program still needs to keep the server information when it is closed.<br>
JSON provides a simple way to save the data in a file on the disk and load it again
when the program starts.<br> JSON isn't a database,
but it works well for storing data in a small project like this.

In `storage.py`, the `load_servers()` function uses `json.load()` to read the data,
while `save_servers()` uses `json.dump()` to save the server list.

```
return json.load(file)
```

```
json.dump(servers, file, indent=2, ensure_ascii=False)
```

---

**I use CSV for exporting reports because the data is organized into rows and columns.** <br>


CSV files can easily be opened in programs such as MS Excel and Google Sheets.<br>
In the `export_to_csv()` function,
I use `csv.DictWriter()` to write the server information to the CSV file.

```
writer = csv.DictWriter(file, fieldnames=fieldnames)
writer.writeheader()

for server in servers:
    writer.writerow(server)
```

JSON is therefore used for the program's main data storage,
while CSV is used to create reports that are easy to read and share.

<br>
<br>

## 4. How my program is divided into modules and functions
<br>

I divided my program into four main Python modules to keep the code organized.<br>
Each file has its own responsibility.<br>
This makes the program easier to understand, maintain and update.

- **`main.py`:** Acts as the entry point of the program.<br>
It uses the `argparse` module to handle command-line arguments, such as `--list` and `--check-all`.<br>
It also controls the program flow and uses `sys.exit()` to return the correct exit codes.
---

- **`menu.py`:** Handles the user interface and the 8-option interactive menu.<br>
It manages user input, validation, and operations such as listing, adding and deleting servers.<br>
It also uses f-strings to display server information in a table and<br>
asks for extra confirmation before deleting production servers.

---
- **`storage.py`:** Handles data storage.<br>
It reads and saves server information in `servers.json`.<br>
It also checks the `INVENTORY_DATA_FILE` environment variable to find the data file and<br>
exports timestamped CSV reports into the `reports/` folder.

---
- **`checks.py`:** Handles server checks.<br>
It uses the `subprocess` module to run the system ping command and check whether a server is reachable.<br>
It updates the server status (`up` or `down`) and the last checked time.

For example, `main.py` also imports and calls functions from the other modules.<br>
These imports show how the modules are connected:

```
from storage import load_servers, save_servers, export_to_csv
from checks import ping_server, check_all_servers
from menu import list_servers, main_menu
```

This structure keeps different tasks separate instead of putting all the code in one large file.

<br>
<br>

## 5. Standard library modules I use and what I use them for
<br>

**In this project, I used several modules from Python's standard library.<br>
These modules are included with Python, so I did not need to install external packages.<br>
Each module has a specific purpose in my program:**

- **`datetime`:** Used in `storage.py` and `checks.py` to generate date and time information.<br>
It records when a server was last checked and adds a timestamp to exported CSV filenames.
---
- **`pathlib`:** Used in `storage.py` to handle file and folder paths.<br>
The `Path` class checks whether a file exists and creates the `reports/` folder if it does not already exist.
---
- **`json`:** Used in `storage.py` to store server data.<br>
The `json.load()` function reads the server list from `servers.json`, and `json.dump()` saves updated server<br>
data back to the file.
---
- **`csv`:** Used in `storage.py` to export server information as CSV reports.<br>
The `csv.DictWriter` class writes the server dictionaries into a CSV file inside the `reports/` folder.
---
- **`os`:** Used in `storage.py` to read the `INVENTORY_DATA_FILE` environment variable.<br>
This allows the user to choose a different data file instead of using the default `servers.json` file.
---
- **`sys`:** Used in `main.py` to control how the program exits.<br>
The `sys.exit()` function returns appropriate exit codes, for example, when a server check fails.
---
- **`argparse`:** Used in `main.py` to handle command-line arguments, such as `--list`, `--check` and `--check-all`.<br>
This allows users to run different program actions directly from the terminal.
The `argparse` module also provides the `--help` option automatically, which displays all available command-line<br>
arguments and their descriptions.
---
- **`subprocess`:** Used in `checks.py` to run the system's native `ping` command with `subprocess.run()`.<br>
This allows the program to check whether a server is reachable.





These standard library modules provide the main functions needed by my project without<br>
requiring additional third-party packages.

<br>
<br>

## 6. Three examples of good practice in my code and why they are good
<br>

**In this project, I used several good programming practices to make the code more organized, safe and reliable.**

**1. Separation of Concerns (Modularity)**

I divided the program into four separate Python modules: `main.py`, `menu.py`, `storage.py` and `checks.py`.<br>
Each file has its own responsibility.

For example, `main.py` imports functions from the other modules:

```
from storage import load_servers, save_servers, export_to_csv
from checks import ping_server, check_all_servers
from menu import list_servers, main_menu
```

This makes the code easier to read, understand and maintain.<br>
For example, if I need to change the ping functionality, I can work mainly in `checks.py` without changing<br>
the menu or storage code.
---
**2. Safety Confirmation for Production Environments**

In `menu.py`, the `delete_server()` function asks for extra confirmation before deleting a server in the production<br>
environment (`prod`).

```
if server_to_delete.get("environment") == "prod":
    confirm = input("Are you sure you want to delete a PRODUCTION server? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return servers
```

This helps prevent accidental deletion of important production servers.<br>
Such a safety check is useful because deleting a production server by mistake can cause serious problems.
---
**3. Input Validation**

In `menu.py`, the `add_server()` function checks user input before adding a new server.<br>
For example, it only accepts the environments `dev`, `test` and `prod`.

```
valid_environments = ["dev", "test", "prod"]

while True:
    environment = input(f"Enter environment ({', '.join(valid_environments)}): ").strip().lower()
    if environment in valid_environments:
        break
    print("Error: Invalid environment! Please choose dev, test, or prod.")
```

The program also checks that the server name isn't empty and that another server with<br>
the same name does not already exist.

This helps prevent invalid or duplicate data from being added to the inventory.

These practices make my program easier to maintain, safer to use and more reliable.

<br>
<br>

## 7. Sources and tools I used during the project
<br>

**During this project, I used different learning resources and tools to improve my Python knowledge,<br>
solve problems and develop the Server Inventory Tool.**

- **Online Video Courses (Udemy and YouTube):** I watched Python lessons on Udemy and YouTube to learn and<br>
review basic programming concepts such as loops, conditions, functions, lists and dictionaries.<br>
These lessons helped me understand how to write Python code and organize a small application.
---
- **LearnPython.org:** I used [learnpython.org](https://learnpython.org/) to review Python syntax and study code examples.<br>
It was useful for refreshing my knowledge and understanding basic Python concepts while working on the project.
---
- **Classmates and Peer Discussions:** I asked my classmates questions and discussed Python topics and problems with them.<br>
Sharing ideas and comparing different approaches helped me understand some concepts better and find solutions when I had difficulties.
---
- **Course Materials and Guidelines:** I used the PDFs, lessons and assignment instructions provided during the Python course.<br>
They helped me understand topics such as modules, JSON, CSV and Python's standard library.<br>
The assignment requirements also guided the structure and functionality of my program.
---
- **AI (AI Assistance):** I used AI as a learning assistant during development.<br>
I asked questions about Python syntax, functions, modules, code structure and errors.<br>
It helped me understand different solutions, review my code and work through problems step by step.<br>
I also used it to organize my ideas and improve the explanations in this report.<br>
I tested the code myself and used these explanations to understand how the program works.

By using these different resources, I was able to improve my Python knowledge while developing the project.<br>
My goal wasn't only to complete the assignment but also to understand the code and learn from the development process.