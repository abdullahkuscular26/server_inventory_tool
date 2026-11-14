
import argparse
import sys
from storage import load_servers, save_servers, export_to_csv
from checks import ping_server, check_all_servers
from menu import list_servers, main_menu


def parse_arguments():
    """
    Sets up command-line arguments using argparse.
    Allows users to run the tool interactively or via CLI flags.
    """
    parser = argparse.ArgumentParser(description="Server Inventory Management Tool")

    parser.add_argument(
        "--list",
        action="store_true",
        help="List all servers in the inventory"
    )
    parser.add_argument(
        "--environment",
        type=str,
        help="Filter servers by environment (dev, test, prod)"
    )
    parser.add_argument(
        "--check-all",
        action="store_true",
        help="Check the status of all servers in the inventory"
    )
    parser.add_argument(
        "--check",
        type=str,
        metavar="SERVER_NAME",
        help="Check the status of a specific server by name"
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export inventory report as CSV"
    )

    return parser.parse_args()


def main():
    """
    Main entry point for the application.
    Handles command-line arguments or defaults to the interactive menu.
    Exits with appropriate status codes (0 for success, 1 for failure).
    """
    args = parse_arguments()
    servers = load_servers()

    # If no arguments are provided, launch the interactive menu
    if not any(vars(args).values()):
        try:
            main_menu()
            sys.exit(0)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)

    # Handle --list argument (with optional --environment filtering)
    if args.list:
        if not servers:
            print("Error: No servers found in inventory.")
            sys.exit(1)

        target_env = args.environment.strip().lower() if args.environment else None

        if target_env:
            valid_environments = ["dev", "test", "prod"]
            if target_env not in valid_environments:
                print(f"Error: Invalid environment '{target_env}'. Choose dev, test, or prod.")
                sys.exit(1)

            filtered_servers = []
            for server in servers:
                if server.get("environment") == target_env:
                    filtered_servers.append(server)

            if not filtered_servers:
                print(f"No servers found in environment '{target_env}'.")
                sys.exit(0)

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
        else:
            list_servers(servers)

        sys.exit(0)

    # Handle --environment alone without --list (edge case protection)
    if args.environment and not args.list:
        print("Error: --environment must be used together with --list flag.")
        sys.exit(1)

    # Handle --check-all argument
    if args.check_all:
        if not servers:
            print("Error: No servers found to check.")
            sys.exit(1)

        try:
            check_all_servers(servers)

            # If any server is down, return exit code 1
            has_down_server = any(server.get("status") == "down" for server in servers)
            if has_down_server:
                print("Warning: One or more servers are down.")
                sys.exit(1)

            sys.exit(0)
        except Exception as e:
            print(f"Error during server check: {e}")
            sys.exit(1)

    # Handle --check <name> argument
    if args.check:
        if not servers:
            print("Error: No servers found in inventory.")
            sys.exit(1)

        target_name = args.check.strip()
        target_server = None
        for server in servers:
            if server.get("name", "").lower() == target_name.lower():
                target_server = server
                break

        if not target_server:
            print(f"Error: Server '{target_name}' not found!")
            sys.exit(1)

        print(f"Pinging {target_server.get('name')} ({target_server.get('address')})...", end=" ")
        ping_server(target_server)
        save_servers(servers)
        print(f"[{target_server.get('status').upper()}]")

        if target_server.get("status") == "down":
            sys.exit(1)

        sys.exit(0)

    # Handle --export argument
    if args.export:
        if not servers:
            print("Error: No servers found to export.")
            sys.exit(1)

        file_path = export_to_csv(servers)
        if file_path:
            print(f"CSV report successfully exported to: {file_path}")
            sys.exit(0)
        else:
            print("Error: Export failed.")
            sys.exit(1)


if __name__ == "__main__":
    main()