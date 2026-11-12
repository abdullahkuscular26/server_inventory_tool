from storage import load_servers, save_servers


def list_servers(servers):
    """
    Prints all saved servers in a simple list.
    If the list is empty, shows a warning message.
    """
    if not servers:
        print("\nNo servers found in inventory.")
        return

    print("\n--- Server List ---")
    for server in servers:
        print(
            f"Name: {server.get('name')} | Address: {server.get('address')} | Env: {server.get('environment')} | Status: {server.get('status', 'unknown')}")
    print("-" * 25)


def list_servers_by_environment(servers):
    """
    Filters and prints servers based on a specific environment chosen by the user.
    """
    if not servers:
        print("\nNo servers found in inventory.")
        return

    print("\n--- List Servers by Environment ---")
    valid_environments = ["dev", "test", "prod"]
    target_env = input(f"Enter environment to filter ({', '.join(valid_environments)}): ").strip().lower()

    if target_env not in valid_environments:
        print("Error: Invalid environment choice!")
        return

    # Collect servers matching the target environment
    filtered_servers = []
    for server in servers:
        if server.get("environment") == target_env:
            filtered_servers.append(server)

    if not filtered_servers:
        print(f"\nNo servers found in environment '{target_env}'.")
        return

    print(f"\n--- Servers in '{target_env}' Environment ---")
    for server in filtered_servers:
        print(
            f"Name: {server.get('name')} | Address: {server.get('address')} | Status: {server.get('status', 'unknown')}")
    print("-" * 25)


def add_server(servers):
    """
    Asks the user for info to add a new server.
    Checks for empty inputs and makes sure the name is unique.
    """
    print("\n--- Add New Server ---")
    name = input("Enter server name: ").strip()

    # If user presses enter with no input, show error and return
    if not name:
        print("Error: Server name cannot be empty!")
        return servers

    # Check if a server with the same name already exists
    for server in servers:
        if server.get("name", "").lower() == name.lower():
            print("Error: A server with this name already exists!")
            return servers

    address = input("Enter server address (IP or domain): ").strip()

    # A server without an address can never be checked, so reject it early.
    if not address:
        print("Error: Server address cannot be empty!")
        return servers

    # Only accept allowed environments
    valid_environments = ["dev", "test", "prod"]
    environment = input(f"Enter environment ({', '.join(valid_environments)}): ").strip().lower()

    if environment not in valid_environments:
        print("Error: Invalid environment! Choose dev, test, or prod.")
        return servers

    role = input("Enter server role (e.g. web, database): ").strip()

    # Create new server dictionary with consistent empty string for last_checked
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
    Asks for extra confirmation before deleting a production server,
    to prevent accidental deletion of critical systems.
    """
    if not servers:
        print("\nNo servers found in inventory to delete.")
        return servers

    print("\n--- Delete Server ---")
    target_name = input("Enter the name of the server to delete: ").strip()

    # Find the server in the list
    server_to_delete = None
    for server in servers:
        if server.get("name", "").lower() == target_name.lower():
            server_to_delete = server
            break

    if not server_to_delete:
        print(f"Error: Server '{target_name}' not found!")
        return servers

    # Extra safety check if server belongs to 'prod' environment
    if server_to_delete.get("environment") == "prod":
        print(f"WARNING: Server '{server_to_delete.get('name')}' is in PRODUCTION environment!")
        confirm = input("Are you sure you want to delete a PRODUCTION server? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Deletion cancelled.")
            return servers

    # Remove server from list and save changes
    servers.remove(server_to_delete)
    save_servers(servers)
    print(f"Server '{server_to_delete.get('name')}' deleted successfully!")

    return servers


def main_menu():
    """
    Main loop running when the program starts.
    Keeps showing the menu until the user chooses to exit.
    """
    servers = load_servers()

    while True:
        print("\n=== Server Inventory Menu ===")
        print("1. List all servers")
        print("2. Add new server")
        print("3. Delete a server")
        print("4. List servers by environment")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            list_servers(servers)
        elif choice == "2":
            servers = add_server(servers)
        elif choice == "3":
            servers = delete_server(servers)
        elif choice == "4":
            list_servers_by_environment(servers)
        elif choice == "5":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice, please enter a valid number between 1 and 5.")


if __name__ == "__main__":
    main_menu()