import socket
import requests
import time
import sys
from scapy.all import traceroute
from colorama import Fore, Style, init

# Inicialización de colores
init(autoreset=True)

# Configuración de Autor
AUTHOR = "lapsusgroup/thesixclown"
VERSION = "1.0.2"

def banner():
    ascii_art = f""
    {Fore.CYAN}       ________  __    __   ______  
/        |/  |  /  | /      \ 
$$$$$$$$/ $$ |  $$ |/$$$$$$  |
   $$ |   $$ |__$$ |$$ |  $$/ 
   $$ |   $$    $$ |$$ |      
   $$ |   $$$$$$$$ |$$ |   __ 
   $$ |   $$ |  $$ |$$ \__/  |
   $$ |   $$ |  $$ |$$    $$/ 
   $$/    $$/   $$/  $$$$$$/  
                              
                              
                                      
    {Fore.CYAN}
    {Fore.BLUE}
    {Fore.BLUE}
    {Fore.CYAN}
    {Fore.CYAN}
    {Fore.WHITE}       [ LEAKS/DOXING WEBSITE ]
    {Fore.YELLOW}             Creator: {33G}
    """
    print(ascii_art)

def get_geo_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,as,query").json()
        if response['status'] == 'success':
            print(f"\n{Fore.GREEN}[+] Información para IP: {ip}")
            print(f"    {Fore.WHITE}País: {response.get('country')}")
            print(f"    {Fore.WHITE}Ciudad: {response.get('city')} ({response.get('regionName')})")
            print(f"    {Fore.WHITE}ISP: {response.get('isp')}")
            print(f"    {Fore.WHITE}ASN: {response.get('as')}")
            print(f"    {Fore.WHITE}Coordenadas: {response.get('lat')}, {response.get('lon')}")
        else:
            print(f"{Fore.RED}[!] No se pudo obtener geo-data de {ip}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error en API: {e}")

def get_http_headers(domain):
    print(f"\n{Fore.YELLOW}[*] Analizando Headers HTTP...")
    try:
        target = f"http://{domain}" if not domain.startswith("http") else domain
        res = requests.get(target, timeout=5)
        for key, value in res.headers.items():
            print(f"    {Fore.WHITE}{key}: {value}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error al conectar vía HTTP.")

def run_traceroute(domain):
    print(f"\n{Fore.YELLOW}[*] Iniciando Traceroute (Rastreo de ruta)...")
    try:
        # Ejecuta un traceroute simplificado
        ans, unans = traceroute(domain, verbose=0, maxttl=20)
        ans.show()
    except Exception:
        print(f"{Fore.RED}[!] Permisos insuficientes para Traceroute (usa sudo en Kali).")

def scan_domain(domain):
    try:
        print(f"{Fore.YELLOW}[*] Resolviendo DNS y Servidores de Nombres...")
        # Obtener IP principal
        primary_ip = socket.gethostbyname(domain)
        
        # Obtener todas las IPs asociadas (Round Robin / Balanceadores)
        addr_info = socket.getaddrinfo(domain, 80)
        ips = list(set([info[4][0] for info in addr_info]))

        print(f"{Fore.CYAN}[i] Dominio: {domain}")
        print(f"{Fore.CYAN}[i] IPs detectadas: {', '.join(ips)}")

        # Geolocation y datos de cada IP
        for ip in ips:
            get_geo_info(ip)

        # HTTP Tracking
        get_http_headers(domain)

        # Traceroute
        run_traceroute(domain)

    except socket.gaierror:
        print(f"{Fore.RED}[!] Error: El dominio no pudo ser resuelto.")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Escaneo cancelado por el usuario.")

if __name__ == "__main__":
    banner()
    if len(sys.argv) > 1:
        target_domain = sys.argv[1]
    else:
        target_domain = input(f"{Fore.WHITE}Introduce el dominio (ej: google.com): ")
    
    scan_domain(target_domain)
