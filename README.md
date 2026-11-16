
# Server Inventory Tool

**A Python application for managing, monitoring, and reporting server inventory**

<br>
<br>

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [What the Program Does](#2-what-the-program-does)
3. [Requirements](#3-requirements)
4. [Installation and Setup](#4-installation-and-setup)
5. [How to Run the Program](#5-how-to-run-the-program)
6. [Command-Line Arguments](#6-command-line-arguments)
7. [Environment Variable (`INVENTORY_DATA_FILE`)](#7-environment-variable-inventory_data_file)
8. [Project Structure](#8-project-structure)
9. [Data Format (`servers.json`)](#9-data-format-serversjson)
10. [CSV Export](#10-csv-export)
11. [Testing and Platform Notes](#11-testing-and-platform-notes)


<br>
<br>

---

## 1. Project Overview
The Server Inventory Tool is a Python application that allows users to manage and monitor a list of servers<br>
through an interactive menu or command-line arguments.<br>
It provides basic server management, production safety checks, network connectivity checks, and CSV report exporting.

<br>
<br>


---

## 2. What the Program Does

- **Manage Servers:** Add new servers, view the inventory list, filter servers by environment, and delete servers.

- **Production Safety Check:** If you try to delete a server in the prod (production) environment,<br>
the program asks for extra confirmation. The user must type "yes" to continue with the deletion.

- **Server Checking Functionality:** The program uses the system ping command to check whether servers are<br>
reachable (up or down) and updates the last checked timestamp.

- **CSV Reporting:** You can export the current server inventory into a CSV file, which can easily be opened<br>
in Microsoft Excel or Google Sheets.

<br>
<br>


---
## 3. Requirements

- **Python Version:** Python 3.8 or newer.

- **External Packages:** No external packages are required. The project uses only Python's standard library,<br>
including json, csv, os, sys, subprocess, pathlib, datetime, and argparse.<br>
You do not need to install anything using pip.

- **Ping Utility:** The system ping command must be available to use the server checking functionality.<br>
The current implementation uses the Linux ping option -c.


<br>
<br>

---

## 4. Installation and Setup

**You can download the project in two ways:**

- **Option 1: Clone using Git**

1. Clone the project from GitHub:

   ```
   git clone https://github.com/abdullahkuscular26/server_inventory_tool.git
   ```

2. Open the project directory:

   ```
   cd server_inventory_tool
   ```

- **Option 2: Download as a ZIP file**

1. Open the [GitHub repository](https://github.com/abdullahkuscular26/server_inventory_tool).
2. Click the **Code** button and select **Download ZIP**.
3. Extract the ZIP file to a folder on your computer.

After downloading, make sure you are in the project root directory, where `main.py`, the other Python modules,<br>
and `servers.json` are located.

No additional packages need to be installed.


<br>
<br>

---

## 5. How to Run the Program

**You can run the program in two different ways:**

- **Interactive Menu Mode (Default)**

If you run the script without any arguments, it opens an interactive menu with 8 options:

```
python main.py
```

You can use the menu numbers to navigate, list servers, add new ones, delete servers, check statuses,or export reports.

- **Command-Line Interface (CLI) Mode**

You can also run specific commands directly from your terminal using command-line arguments.

<br>
<br>

---


## 6. Command-Line Arguments

**The program supports the following command-line options:**

- **Show available options:**

  ```
  python main.py --help
  ```

- **List all servers:**

  ```
  python main.py --list
  ```

- **List servers filtered by environment (e.g., `prod`):**

  ```
  python main.py --list --environment prod
  ```

- **Check a specific server by name:**

  ```
  python main.py --check web01
  ```

- **Check all servers using ping:**

  ```
  python main.py --check-all
  ```

- **Export the server inventory to CSV:**

  ```
  python main.py --export
  ```
  
<br>
<br>

---


## 7. Environment Variable (`INVENTORY_DATA_FILE`)

By default, the program saves and reads data from `servers.json`.<br>
If you want to use a different JSON file without changing the source code,<br>
you can use the `INVENTORY_DATA_FILE` environment variable.

- **On Linux / macOS / Git Bash:**

  ```
  export INVENTORY_DATA_FILE="my_custom_servers.json"
  python main.py
  ```

- **On Windows (CMD):**

  ```
  set INVENTORY_DATA_FILE=my_custom_servers.json
  python main.py
  ```

- **On Windows (PowerShell):**

  ```
  $env:INVENTORY_DATA_FILE="my_custom_servers.json"
  python main.py
  ```
  
<br>
<br>

---

## 8. Project Structure

**To keep the code organized, I divided the project into four main Python files:**

1. **`main.py`:** The entry point of the program. It handles command-line arguments using `argparse` and<br>
controls program exit codes with `sys.exit()`.

2. **`menu.py`:** Handles the user interface, the interactive menu loop, input validation, table formatting,<br>
and production deletion confirmation.

3. **`storage.py`:** Handles saving and loading data in `servers.json`, reading the environment variable,<br>
and exporting timestamped CSV reports into the `reports/` folder.

4. **`checks.py`:** Handles server checking by running the system ping command using `subprocess` to check<br>
whether a server is up or down.

<br>
<br>

---

## 9. Data Format (`servers.json`)

Servers are stored as a list of dictionaries. Each server record contains the following fields:

- `name`: The unique name of the server (string).
- `address`: The IP address or hostname (string).
- `environment`: The deployment environment (`dev`, `test`, or `prod`) (string).
- `role`: The server's function, such as webserver or database (string).
- `status`: The server status, such as `unknown`, `up`, or `down` (string).
- `last_checked`: The timestamp of the last connectivity check (string).

**Example structure:**

```
[
  {
    "name": "web01",
    "address": "example.com",
    "environment": "prod",
    "role": "webserver",
    "status": "up",
    "last_checked": "2026-11-16 20:30"
  }
]
```

<br>
<br>


---

## 10. CSV Export

When exporting reports, the application automatically creates a `reports/` directory if it doesn't exist<br>
and generates a timestamped CSV file (for example: `reports/inventory_2026-11-16_203000.csv`).

This allows users to open and inspect inventory records easily in Microsoft Excel or Google Sheets.

<br>
<br>

---

## 11. Testing and Platform Notes

- **Tested Environments:** The program has been tested in three environments: Windows, a local Ubuntu virtual<br>
machine running in VMware, and the teacher's cloud container environment.


- **Ping Limitation:** The current implementation uses the Linux ping option `-c`. On Windows,<br>
the ping command uses `-n` instead. Therefore, the server checking functionality is currently designed<br>
for Linux environments. The ping command would need a platform-specific adjustment to work correctly on Windows. Other program features were tested on Windows.
