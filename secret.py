import socket
import requests
import sys
import os
from datetime import datetime
from scapy.all import traceroute
from colorama import Fore, Style, init

# Inicialización
init(autoreset=True)

# --- CONFIGURACIÓN Y AUTOR ---
AUTHOR = "Thesixclown/lapsusgroup"
VERSION = "2.0.1"

def banner():
    banner_text = f"""
    {Fore.CYAN}███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    {Fore.CYAN}████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    {Fore.BLUE}██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    {Fore.BLUE}██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    {Fore.CYAN}██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    {Fore.WHITE}      [ OSINT & INFRASTRUCTURE SCANNER ]
    {Fore.YELLOW}             Author: {33g}
    """
    print(banner_text)

def save_to_file(domain, content):
    filename = f"scan_{domain.replace('.', '_')}.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(content + "\n")

def get_geo_info(ip, domain):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,as,query"
        data = requests.get(url).json()
        
        if data['status'] == 'success':
            info = (
                f"\n[+] IP INVESTIGADA: {data['query']}\n"
                f"    País: {data.get('country')}\n"
                f"    Ciudad: {data.get('city')} ({data.get('regionName')})\n"
                f"    ISP: {data.get('isp')}\n"
                f"    ASN: {data.get('as')}\n"
            )
            print(Fore.GREEN + info)
            save_to_file(domain, info)
    except Exception as e:
        print(Fore.RED + f"[!] Error obteniendo Geo-IP: {e}")

def track_http(domain):
    print(Fore.YELLOW + "\n[*] Analizando HTTP Tracking & Headers...")
    try:
        url = f"http://{domain}" if not domain.startswith("http") else domain
        r = requests.get(url, timeout=5)
        header_info = f"--- HTTP HEADERS ({domain}) ---\n"
        for k, v in r.headers.items():
            line = f"{k}: {v}"
            print(f"    {Fore.WHITE}{line}")
            header_info += line + "\n"
        save_to_file(domain, header_info)
    except:
        print(Fore.RED + "    [!] No se pudo conectar al servidor HTTP.")

def run_traceroute(domain):
    print(Fore.YELLOW + f"\n[*] Iniciando Traceroute hacia {domain}...")
    try:
        # En Windows/Termux sin root esto puede fallar, en Kali con sudo funciona perfecto
        res, unans = traceroute(domain, verbose=0, maxttl=20)
        print(Fore.WHITE + "    [Ruta completada]")
        # Guardamos el resumen
        save_to_file(domain, f"--- TRACEROUTE INFO ---\n{res.show(dump=True)}")
    except:
        print(Fore.RED + "    [!] Traceroute requiere privilegios de ROOT (Sudo).")

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    banner()
    
    target = input(f"{Fore.WHITE}Ingrese el dominio o URL: ").strip().replace("https://", "").replace("http://", "")
    
    if not target:
        print(Fore.RED + "Debes ingresar un dominio válido.")
        return

    print(f"\n{Fore.CYAN} INICIANDO ESCANEO: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    save_to_file(target, f"ESCANEO DE INFRAESTRUCTURA - {target}\nFecha: {datetime.now()}\n" + "="*40)

    try:
        # 1. Obtener todas las IPs del dominio
        print(Fore.YELLOW + "[*] Resolviendo DNS...")
        ips = list(set([info[4][0] for info in socket.getaddrinfo(target, 80)]))
        
        # 2. Procesar cada IP
        for ip in ips:
            get_geo_info(ip, target)
        
        # 3. HTTP Track
        track_http(target)
        
        # 4. Traceroute
        run_traceroute(target)
        
        print(f"\n{Fore.GREEN}[✔] Escaneo completo. Datos guardados en: scan_{target.replace('.', '_')}.txt")

    except socket.gaierror:
        print(Fore.RED + "[!] Error: No se pudo resolver el dominio.")
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Detenido por el usuario.")

if __name__ == "__main__":
    main()
