import json
from netmiko import ConnectHandler

with open('autoAP-jsn.json') as f:
    data = json.load(f)

conn = ConnectHandler(
    device_type=data['aironetInfo']['device_type'],
    host=data['aironetInfo']['host'],
    username=data['aironetInfo']['username'],
    password=data['aironetInfo']['password'],
    secret=data['aironetInfo']['secret']
)

conn.enable()

commands = [
    f"hostname {data['aironetConfig']['hostname']}",
    "default interface Dot11Radio0",
    "interface Dot11Radio0",
    "no shutdown",
    f"channel {data['aironetConfig']['channel']}",
    f"encryption mode ciphers {data['aironetConfig']['encr-mod']}",
    f"dot11 ssid {data['aironetConfig']['ssid']}",
    "authentication open",
    "guest-mode",
    "authentication key-management wpa",
    f"wpa-psk ascii {data['aironetConfig']['wifi-pass']}",
    "exit",
    "exit",
    "write memory"
]

output = conn.send_config_set(commands)
print(output)

conn.disconnect()

with open('show_run_output.txt', 'w') as f:
    f.write(output)
