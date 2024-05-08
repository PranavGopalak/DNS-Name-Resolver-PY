import sys
import socket

def resolve_domains(input_file, output_file):
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                domain = line.strip()
                try:
                    ip_address = socket.gethostbyname(domain)
                    outfile.write(f"{domain}: {ip_address}\n")
                except socket.gaierror:
                    outfile.write(f"{domain}: Error resolving domain\n")
    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python <script> <input_file> <output_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    resolve_domains(input_file_path, output_file_path)
