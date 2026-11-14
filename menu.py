from storage import load_servers, save_servers, export_to_csv
from checks import check_single_server, check_all_servers


def list_servers(servers):
    """
    Prints all saved servers in a clean, aligned table format.
    If the list is empty, shows a warning message.
    """
    if not servers:
        print("\nNo servers found in inventory.")
        return

    print("\n--- Server List ---")
    print(f"{'Name':<15} {'Address':<20} {'Environment':<15} {'Status':<10} {'Last Checked':<20}")
    print("-" * 80)

    for server in servers:
        print(
            f"{server.get('name', ''):<15} "
            f"{server.get('address', ''):<20} "
            f"{server.get('environment', ''):<15} "
            f"{server.get('status', 'unknown'):<10} "
            f"{server.get('last_checked', ''):<20}"
        )
    print("-" * 80)


def list_servers_by_environment(servers):
    """
    Filters and prints servers based on a specific environment chosen by the user.
    Keeps asking until a valid environment is entered.
    """
    if not servers:
        print("\nNo servers found in inventory.")
        return

    print("\n--- List Servers by Environment ---")
    valid_environments = ["dev", "test", "prod"]

    while True:
        target_env = input(f"Enter environment to filter ({', '.join(valid_environments)}): ").strip().lower()
        if target_env in valid_environments:
            break
        print("Error: Invalid environment choice! Please try again.")

    filtered_servers = []
    for server in servers:
        if server.get("environment") == target_env:
            filtered_servers.append(server)

    if not filtered_servers:
        print(f"\nNo servers found in environment '{target_env}'.")
        return

    print(f"\n--- Servers in '{target_env}' Environment ---")
    print(f"{'Name':<15} {'Address':<20} {'Environment':<15} {'Status':<10} {'Last Checked':<20}")
    print("-" * 80)

    for server in filtered_servers:
        print(
            f"{server.get('name', ''):<15} "
            f"{server.get('address', ''):<20} "
            f"{server.get('environment', ''):<15} "
            f"{server.get('status', 'unknown'):<10} "
            f"{server.get('last_checked', ''):<20}"
        )
    print("-" * 80)


def add_server(servers):
    """
    Asks the user for info to add a new server.
    Checks for empty inputs, ensures unique names, and validates environment choice.
    """
    print("\n--- Add New Server ---")
    name = input("Enter server name: ").strip()

    if not name:
        print("Error: Server name cannot be empty!")
        return servers

    for server in servers:
        if server.get("name", "").lower() == name.lower():
            print("Error: A server with this name already exists!")
            return servers

    address = input("Enter server address (IP or domain): ").strip()

    if not address:
        print("Error: Server address cannot be empty!")
        return servers

    valid_environments = ["dev", "test", "prod"]
    while True:
        environment = input(f"Enter environment ({', '.join(valid_environments)}): ").strip().lower()
        if environment in valid_environments:
            break
        print("Error: Invalid environment! Please choose dev, test, or prod.")

    role = input("Enter server role (e.g. web, database): ").strip()

    new_server = {
        "name": name,
        "address": address,
        "environment": environment,
        "role": role,
        "status": "unknown",
        "last_checked": ""
    }

    servers.append(new_server)
    save_servers(servers)
    print(f"Server '{name}' added successfully!")

    return servers


def delete_server(servers):
    """
    Deletes a server by its name.
    Asks for extra confirmation before deleting a production server
    to prevent accidental deletion of critical systems.
    """
    if not servers:
        print("\nNo servers found in inventory to delete.")
        return servers

    print("\n--- Delete Server ---")
    target_name = input("Enter the name of the server to delete: ").strip()

    server_to_delete = None
    for server in servers:
        if server.get("name", "").lower() == target_name.lower():
            server_to_delete = server
            break

    if not server_to_delete:
        print(f"Error: Server '{target_name}' not found!")
        return servers

    if server_to_delete.get("environment") == "prod":
        print(f"WARNING: Server '{server_to_delete.get('name')}' is in PRODUCTION environment!")
        confirm = input("Are you sure you want to delete a PRODUCTION server? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Deletion cancelled.")
            return servers

    servers.remove(server_to_delete)
    save_servers(servers)
    print(f"Server '{server_to_delete.get('name')}' deleted successfully!")

    return servers


def export_csv_menu(servers):
    """
    Triggers CSV export function and displays the result path to the user.
    """
    if not servers:
        print("\nNo servers found in inventory to export.")
        return

    file_path = export_to_csv(servers)
    if file_path:
        print(f"\nCSV report successfully exported to: {file_path}")
    else:
        print("\nExport failed: No server data available.")


def main_menu():
    """
    Main loop running when the program starts.
    Keeps showing the 8-option menu until the user chooses to exit.
    """
    servers = load_servers()

    while True:
        print("\n=== Server Inventory Menu ===")
        print("1. List all servers")
        print("2. Add new server")
        print("3. Delete a server")
        print("4. List servers by environment")
        print("5. Check a single server")
        print("6. Check all servers")
        print("7. Export report as CSV")
        print("8. Exit")

        choice = input("Select an option (1-8): ").strip()

        if choice == "1":
            list_servers(servers)
        elif choice == "2":
            servers = add_server(servers)
        elif choice == "3":
            servers = delete_server(servers)
        elif choice == "4":
            list_servers_by_environment(servers)
        elif choice == "5":
            servers = check_single_server(servers)
        elif choice == "6":
            servers = check_all_servers(servers)
        elif choice == "7":
            export_csv_menu(servers)
        elif choice == "8":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice, please enter a valid number between 1 and 8.")


