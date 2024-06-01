import psutil
import subprocess
import winreg
import json
import platform
from requests_html import HTMLSession
import traceback
from datetime import datetime

def log(Type, Message):
    error_time = datetime.now().isoformat()
    error_details = traceback.format_exc()
    
    log_entry = {
        "time": error_time,
        "type": Type,
        "details": Message
    }
    
    #Create or append to log.json
    with open("log.json", "a+") as log_file:
        log_file.seek(0)
        if log_file.read(1):
            log_file.write(",\n")
        else:
            log_file.write("[\n")
        json.dump(log_entry, log_file, indent=4)
        log_file.write("\n]")

def InitiateCollecection(HWDeviceID, ObserverVersion):  
   
    log("get_system_usage", "Starting")
    get_system_usage(HWDeviceID,ObserverVersion)
    log("get_system_usage", "Completed")

    log("get_installed_applications", "Starting")
    get_installed_applications(HWDeviceID)
    log("get_installed_applications", "Completed")

    collect_firewall_logs()

def collect_firewall_logs():
    #Use PowerShell to collect firewall logs
    powershell_command = """
    $events = Get-WinEvent -LogName 'Security' -MaxEvents 100
    $logs = $events | ForEach-Object { $_.Message }
    $logs
    """
    logs = subprocess.check_output(["powershell", "-Command", powershell_command], shell=True)
    return logs.decode('utf-8')
    
def get_installed_applications(HWDeviceID):
    #Example: Retrieve installed applications and their version numbers from the Windows Registry
    key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    installed_apps = []
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as reg_key:
        for i in range(winreg.QueryInfoKey(reg_key)[0]):
            try:
                app_key = winreg.EnumKey(reg_key, i)
                with winreg.OpenKey(reg_key, app_key) as app_reg_key:
                    app_name = winreg.QueryValueEx(app_reg_key, "DisplayName")[0]
                    app_version = winreg.QueryValueEx(app_reg_key, "DisplayVersion")[0]
                    app_name = str(app_name).replace("-","").replace("/","").replace("(","").replace(")","")

                    #Replace special characters in app_name
                    
                    url = f"https://api.hakware.com/HakObserver/DeviceApps/{HWDeviceID}/{app_name}/{app_version}"

                    #Make a GET request to the URL
                    session = HTMLSession()
                
                    response = session.get(url, verify=False)

                    if response.status_code == 200:
                        print("Device Data inserted successfully via API.")
                    else:
                        print(url)
                        print(app_name)
                        print(f"Failed to insert data via API. Status code: {response.status_code}")

                    installed_apps.append({"name": app_name, "version": app_version})
            except FileNotFoundError:
                pass
    return installed_apps

def get_system_usage(HWDeviceID,ObserverVersion):

    #Example: Retrieve OS version using system-specific commands
    os_version = str(subprocess.check_output("ver", shell=True)).replace('(', '').replace(')', '')

    # CPU, RAM, and disk usage
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    #disk_usage = psutil.disk_usage('C:').percent  Replace 'C:' with appropriate drive letter

    #Retrieve total memory
    total_memory = psutil.virtual_memory().total
    total_memory_gb = total_memory / (1024**3)
    #Retrieve total number of CPUs and cores
    total_cpus = psutil.cpu_count(logical=False)  #Physical CPUs
    total_cores = psutil.cpu_count(logical=True)  #Logical CPUs (cores)

  

    device_name = str(platform.node()).replace('(', '').replace(')', ''),
    processor = str(platform.processor()).replace('(', '').replace(')', ''),
    device_id = str(platform.node()).replace('(', '').replace(')', ''),  #You may replace this with an appropriate identifier for your system
    system_type = str(platform.system()).replace('(', '').replace(')', '')


    
    ObserverVersion = str(ObserverVersion).replace("(","").replace(")","").replace(",","").replace("\\r\\n","").replace("'","")
    device_id =str(device_id).replace("(","").replace(")","").replace(",","").replace("\\r\\n","").replace("'","")
    device_name = str(device_name).replace("(","").replace(")","").replace(",","").replace("\\r\\n","").replace("'","")
    processor = str(processor).replace("(","").replace(")","").replace(",","").replace("\\r\\n","").replace("'","")
    system_type = str(system_type).replace("(","").replace(")","").replace(",","").replace("\\r\\n","").replace("'","")
    os_version = str(os_version).replace("(","").replace(")","").replace(",","").replace("\\r\\n","").replace("b","").replace("'","")

    print(ObserverVersion)
    print(device_name)
    print(processor)
    print(system_type)
    print(os_version)


    from requests_html import HTMLSession

    url = f"https://api.hakware.com/HakObserver/Device/{HWDeviceID}/{ObserverVersion}/{device_name}/{processor}/{device_id}/{system_type}/{os_version}/{total_memory_gb}/{total_cpus}/{total_cores}"
    
  

    #Make a GET request to the URL
    session = HTMLSession()
   
    response = session.get(url, verify=False, timeout=10)

    print(response)

    if response.status_code == 200:
        print("Device Data inserted successfully via API.")
    else:
        print(f"Failed to insert data via API. Status code: {response.status_code}")
    return {
        "cpu_usage_percent": cpu_usage,
        "ram_usage_percent": ram_usage,
        #"disk_usage_percent": disk_usage,
        "total_memory": total_memory_gb,
        "total_cpus": total_cpus,
        "total_cores": total_cores
    }
###############################################################################################################################################################################
