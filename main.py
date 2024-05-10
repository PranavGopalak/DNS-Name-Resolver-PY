import sys
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def resolve_domain_name(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return (domain, ip_address)
    except socket.gaierror:
        return (domain, "Error resolving domain")

def resolve_domains_concurrently(input_file, output_file):
    domains = []
    try:
        with open(input_file, 'r') as infile:
            domains = [line.strip() for line in infile]
    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    # Resolve domains concurrently
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_domain = {executor.submit(resolve_domain_name, domain): domain for domain in domains}
        for future in as_completed(future_to_domain):
            results.append(future.result())

    # Write results to the output file
    try:
        with open(output_file, 'w') as outfile:
            for domain, ip in results:
                outfile.write(f"{domain}: {ip}\n")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python <script> <input_file> <output_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    resolve_domains_concurrently(input_file_path, output_file_path)
