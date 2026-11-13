import subprocess
from datetime import datetime
from storage import save_servers


def ping_server(server):
    """
     Checks if a server responds to ping and updates its status and check time.
    """
    address = server.get("address")

    # If address is empty, mark as down immediately
    if not address:
        server["status"] = "down"
        server["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        return server

    # Create the ping command for Linux
    command = ["ping", "-c", "1", address]

    try:
        # Run the ping command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            server["status"] = "up"
        else:
            server["status"] = "down"
    except Exception:
        server["status"] = "down"

    # Update the last checked time
    server["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return server


def check_single_server(servers):
    """
    Asks the user for a server name and checks its status.
    """
    if not servers:
        print("\nNo servers found in inventory to check.")
        return servers

    print("\n--- Check Single Server ---")
    target_name = input("Enter the name of the server to check: ").strip()

    # Find the server in the list
    target_server = None
    for server in servers:
        if server.get("name", "").lower() == target_name.lower():
            target_server = server
            break

    if not target_server:
        print(f"Error: Server '{target_name}' not found!")
        return servers

    print(f"Pinging {target_server.get('name')} ({target_server.get('address')})...", end=" ")
    ping_server(target_server)
    save_servers(servers)
    print(f"[{target_server.get('status').upper()}]")

    return servers


def check_all_servers(servers):
    """
    Pings all servers in the list, updates their status and timestamp, and saves changes.
    """
    if not servers:
        print("\nNo servers found to check.")
        return servers

    print("\nChecking all servers...")
    for server in servers:
        name = server.get("name")
        print(f"Pinging {name} ({server.get('address')})...", end=" ")
        ping_server(server)
        print(f"[{server.get('status').upper()}]")

    save_servers(servers)
    print("All server checks completed and saved!")
    return servers