import yaml
from netmiko import ConnectHandler

# Load config
with open('autoAP.yml') as f:
    data = yaml.safe_load(f)

device = data['aironetInfo']
config = data['aironetConfig']

# Connect
conn = ConnectHandler(**device)
conn.enable()

# Configure
commands = [
    f"hostname {config['hostname']}",
    "default interface Dot11Radio0",
    "default interface GigabitEthernet0",
    "interface Dot11Radio0",
    "no shutdown",
    f"channel {config['channel']}",
    f"encryption mode ciphers {config['encr-mod']}",
    f"dot11 ssid {config['ssid']}",
    "authentication open",
    "guest-mode",
    "authentication key-management wpa",
    f"wpa-psk ascii {config['wifi-pass']}",
    "exit",
    "exit",
    "write memory"
]

output = conn.send_config_set(commands)
print(output)

# Disconnect
conn.disconnect()

# Save output
with open('show_run_output.txt', 'w') as f:
    f.write(output)

print("\n Configuration completed successfully!")
