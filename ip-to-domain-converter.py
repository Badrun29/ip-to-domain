import socket
import concurrent.futures

def ip_to_domain(ip_address):
    try:
        hostname = socket.gethostbyaddr(ip_address)
        return hostname[0]
    except socket.herror:
        return ""

def read_ip_addresses(filename):
    try:
        with open(filename, 'r') as file:
            ip_addresses = file.read().splitlines()
        return ip_addresses
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return []

def convert_ip_to_domain(ip_address):
    domain_name = ip_to_domain(ip_address)
    if domain_name:
        result = f"{domain_name}"
    else:
        result = f"NULL"

    print(f"Konversi: {ip_address} -> {domain_name}")
    return result

def convert_ips_parallel(ip_addresses, output_filename):
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_ip = {executor.submit(convert_ip_to_domain, ip): ip for ip in ip_addresses}

        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f"Konversi alamat IP {ip} gagal: {exc}")

    try:
        with open(output_filename, 'w') as file:
            file.write('\n'.join(results))
        print(f"Hasil konversi telah disimpan dalam file {output_filename}.")
    except:
        print("Terjadi kesalahan saat menyimpan file.")

# Contoh penggunaan
input_filename = "input.txt"
output_filename = "output.txt"

ip_addresses = read_ip_addresses(input_filename)
convert_ips_parallel(ip_addresses, output_filename)
