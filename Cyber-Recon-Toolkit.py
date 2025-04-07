# Cyber Recon Toolkit - Complete Version
# Author: YourName | Version: 2.0

import os
import platform
import socket
import requests
import uuid
import psutil
import subprocess
import getpass
import wmi
from colorama import Fore, Style, init

init(autoreset=True)
w = wmi.WMI()

def print_section(title):
    print(Fore.CYAN + "\n========== " + title.upper() + " ==========" + Style.RESET_ALL)

def check_internet():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        return False

def get_system_info():
    print_section("System Info")
    print(f"{Fore.GREEN}System:{Style.RESET_ALL} {platform.system()}")
    print(f"{Fore.GREEN}Node Name:{Style.RESET_ALL} {platform.node()}")
    print(f"{Fore.GREEN}Release:{Style.RESET_ALL} {platform.release()}")
    print(f"{Fore.GREEN}Version:{Style.RESET_ALL} {platform.version()}")
    print(f"{Fore.GREEN}Machine:{Style.RESET_ALL} {platform.machine()}")
    print(f"{Fore.GREEN}Processor:{Style.RESET_ALL} {platform.processor()}")

def get_private_ip():
    print_section("Private IP")
    hostname = socket.gethostname()
    private_ip = socket.gethostbyname(hostname)
    print(f"{Fore.YELLOW}Private IP:{Style.RESET_ALL} {private_ip}")

def get_public_ip():
    print_section("Public IP")
    if check_internet():
        try:
            public_ip = requests.get('https://api.ipify.org').text
            print(f"{Fore.YELLOW}Public IP:{Style.RESET_ALL} {public_ip}")
        except:
            print("Unable to fetch public IP")
    else:
        print("No Internet Connection")

def get_mac_address():
    print_section("MAC Address")
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                   for ele in range(0, 8*6, 8)][::-1])
    print(f"{Fore.MAGENTA}MAC Address:{Style.RESET_ALL} {mac}")

def get_memory_info():
    print_section("RAM Info")
    mem = psutil.virtual_memory()
    print(f"{Fore.GREEN}Total RAM:{Style.RESET_ALL} {mem.total // (1024**3)} GB")
    print(f"{Fore.GREEN}Available:{Style.RESET_ALL} {mem.available // (1024**3)} GB")
    print(f"{Fore.GREEN}Used:{Style.RESET_ALL} {mem.used // (1024**3)} GB")
    print(f"{Fore.GREEN}Usage:{Style.RESET_ALL} {mem.percent}%")

def get_disk_info():
    print_section("Disk Info")
    disk = psutil.disk_usage('/')
    print(f"{Fore.BLUE}Total Space:{Style.RESET_ALL} {disk.total // (1024**3)} GB")
    print(f"{Fore.BLUE}Used Space:{Style.RESET_ALL} {disk.used // (1024**3)} GB")
    print(f"{Fore.BLUE}Free Space:{Style.RESET_ALL} {disk.free // (1024**3)} GB")
    print(f"{Fore.BLUE}Usage Percent:{Style.RESET_ALL} {disk.percent}%")

def get_battery_info():
    print_section("Battery Info")
    battery = psutil.sensors_battery()
    if battery:
        print(f"{Fore.GREEN}Battery:{Style.RESET_ALL} {battery.percent}%")
        print(f"{Fore.GREEN}Charging:{Style.RESET_ALL} {'Yes' if battery.power_plugged else 'No'}")
    else:
        print("No battery detected")

def get_wifi_info():
    print_section("Wi-Fi Info")
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True)
        print(Fore.GREEN + result.decode() + Style.RESET_ALL)
    except:
        print("Wi-Fi info not available")

def get_saved_wifi_passwords():
    print_section("Saved Wi-Fi Passwords")
    output = subprocess.check_output("netsh wlan show profiles", shell=True).decode()
    profiles = [line.split(":")[1].strip() for line in output.split("\n") if "All User Profile" in line]
    for profile in profiles:
        try:
            result = subprocess.check_output(f"netsh wlan show profile name=\"{profile}\" key=clear", shell=True).decode()
            for line in result.split("\n"):
                if "Key Content" in line:
                    password = line.split(":")[1].strip()
                    print(f"{Fore.CYAN}SSID: {profile} | Password: {password}")
        except:
            print(f"SSID: {profile} | Password: Access Denied")

def check_vm():
    print_section("VM Detection")
    vm_detected = False
    for item in w.Win32_ComputerSystem():
        manufacturer = item.Manufacturer.lower()
        model = item.Model.lower()
        if any(vm in manufacturer + model for vm in ["vmware", "virtualbox", "kvm", "xen"]):
            vm_detected = True
    print(f"{Fore.CYAN}Running inside VM: {vm_detected}")

def check_rdp_status():
    print_section("RDP Status")
    try:
        result = subprocess.check_output("reg query \"HKLM\\System\\CurrentControlSet\\Control\\Terminal Server\" /v fDenyTSConnections", shell=True).decode()
        if "0x0" in result:
            print(f"{Fore.CYAN}RDP Enabled: Yes")
        else:
            print(f"{Fore.CYAN}RDP Enabled: No")
    except:
        print("Could not detect RDP status")

def list_open_ports():
    print_section("Open Ports")
    result = subprocess.check_output("netstat -ano", shell=True).decode()
    print(Fore.GREEN + result[:500] + "..." + Style.RESET_ALL)

def firewall_rules():
    print_section("Firewall Rules")
    rules = subprocess.check_output("netsh advfirewall firewall show rule name=all", shell=True).decode(errors='ignore')
    print(Fore.GREEN + rules[:500] + "..." + Style.RESET_ALL)

def get_antivirus_status():
    print_section("Antivirus Status")
    try:
        result = subprocess.check_output('wmic /namespace:\\root\\SecurityCenter2 path AntiVirusProduct get displayName', shell=True)
        print(Fore.GREEN + result.decode() + Style.RESET_ALL)
    except:
        print("Could not retrieve antivirus info")

def get_bios_info():
    print_section("BIOS Info")
    bios = w.Win32_BIOS()[0]
    print(f"{Fore.CYAN}Version: {bios.SMBIOSBIOSVersion} | Manufacturer: {bios.Manufacturer}")

def get_motherboard_info():
    print_section("Motherboard Info")
    try:
        result = subprocess.check_output("wmic baseboard get product,Manufacturer,version,serialnumber", shell=True)
        print(result.decode())
    except:
        print("Could not get motherboard info")

def get_gpu_info():
    print_section("GPU Info")
    for gpu in w.Win32_VideoController():
        print(f"{Fore.CYAN}{gpu.Name} | Driver: {gpu.DriverVersion}")

def ping_test():
    print_section("Ping Test")
    for host in ["8.8.8.8", "1.1.1.1"]:
        response = os.system(f"ping -n 1 {host} > nul")
        status = "Reachable" if response == 0 else "Unreachable"
        print(f"{Fore.CYAN}{host}: {status}")

def arp_table():
    print_section("ARP Table")
    result = subprocess.check_output("arp -a", shell=True).decode()
    print(Fore.CYAN + result.strip())

def traceroute():
    print_section("Traceroute")
    result = subprocess.check_output("tracert 8.8.8.8", shell=True).decode(errors='ignore')
    print(Fore.CYAN + result[:500] + "..." + Style.RESET_ALL)

def get_installed_programs():
    print_section("Installed Programs")
    try:
        result = subprocess.check_output("wmic product get name,version", shell=True)
        print(Fore.GREEN + result.decode() + Style.RESET_ALL)
    except:
        print("Unable to fetch installed programs")

def get_services():
    print_section("Running Services")
    try:
        result = subprocess.check_output("net start", shell=True)
        print(Fore.GREEN + result.decode() + Style.RESET_ALL)
    except:
        print("Could not fetch services")

def get_all_users():
    print_section("User Accounts")
    try:
        result = subprocess.check_output("net user", shell=True)
        print(result.decode())
    except:
        print("Could not fetch users")

def main():
    print(Fore.LIGHTWHITE_EX + f"Running as: {getpass.getuser()}\n")
    get_system_info()
    get_private_ip()
    get_public_ip()
    get_mac_address()
    get_memory_info()
    get_disk_info()
    get_battery_info()
    get_motherboard_info()
    get_all_users()
    get_wifi_info()
    get_saved_wifi_passwords()
    check_vm()
    check_rdp_status()
    list_open_ports()
    firewall_rules()
    get_antivirus_status()
    get_bios_info()
    get_gpu_info()
    ping_test()
    arp_table()
    traceroute()
    get_installed_programs()
    get_services()

if __name__ == "__main__":
    main()
