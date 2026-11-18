#socket is for the ip validation
import socket

#file name
INVENTORY_FILE = "network_inventory.txt"
#device optionas
DEVICE_TYPES = ["Router", "Switch", "Server", "Firewall", "Access Point"]
#status options
STATUSES = ["Online", "Offline"]

#dict where all infor on devices will be held when registered
devices = {}


# ip validation heere -----------------------------------------------------------

def is_valid_ip(addr):
    #teturn true only for IPv4 addresses from 192.168.1.1 to 192.168.1.254.
    # exactly four numeric octets separated by dots each 0-255
    octets = addr.split(".")
    #dots seperating
    if len(octets) != 4:
        return False
    for octet in octets:
        #keeps it within range of 0-255
        if not (octet.isdigit() and octet.isascii()):
            return False
        #cant be from 1
        if len(octet) > 1 and octet.startswith("0"):
            return False
        #catn be over 225
        if int(octet) > 255:
            return False

    # got this from stack overflow, checks if address is legal/valid using a sockert
    try:
        socket.inet_aton(addr)
        # legal address
    except socket.error:
        # illegal address
        return False
    
    #RANGE OF IP=============================================================================
    #  only 192.168.1.1 to 192.168.1.254 are accepted
    if octets[:3] != ["192", "168", "1"]:
        return False
    return 1 <= int(octets[3]) <= 254


def normalise_option(value, options):
    #Match user input to a valid option ignoring case. Return None if no match.
    for option in options:
        if value.lower() == option.lower():
            return option
    return None


def ip_in_use(ip):
    #Look for ip already in dict
    for info in devices.values():
        if info["ip"] == ip:
            return True
    return False


# MENU SECTION---------------------------------------------------------------------------

def register_device():
    print("\n--- Register New Device ---(˶ˆᗜˆ˵)")
    
    
    name = input("Enter device name: ")
    if name == "":
        print("Error: device name cannot be empty.₍^. .^₎⟆")
        return
    if name in devices:
        print(f"Error: device name '{name}' is already registered.(つ╥﹏╥)つ")
        return

    ip = input("Enter IP address: ")
    if not is_valid_ip(ip):
        print("Error: Invalid IP address or address outside the allowed range.¯\_(ツ)_/¯")
        return
    if ip_in_use(ip):
        print(f"Error: IP address {ip} is already assigned.")
        return

    device_type = normalise_option(
        input("Enter device type (Router/Switch/Server/Firewall/Access Point): "),
        DEVICE_TYPES)
    if device_type is None:
        print("Error: Invalid device type.Someone call Shepard this one can't follow instructions.")
        return

    status = normalise_option(input("Enter status (Online/Offline): "), STATUSES)
    if status is None:
        print("Error: Invalid status. Use Online or Offline.")
        return

    devices[name] = {"ip": ip, "type": device_type, "status": status}
    print(f"Success: {name} has been registered.")


def search_device():
    print("\n--- Search for Device ---")
    name = input("Enter device name: ").strip()

    info = devices.get(name)
    if info is None:
        print(f"Error: no device named '{name}' was found.")
        return

    print(f"Name: {name}")
    print(f"IP Address: {info['ip']}")
    print(f"Type: {info['type']}")
    print(f"Status: {info['status']}")


def update_status():
    print("\n--- Update Device Status ---")
    name = input("Enter device name: ")

    if name not in devices:
        print(f"Error: no device named '{name}' was found.(╥‸╥)")
        return

    new_status = normalise_option(input("Enter new status (Online/Offline): "), STATUSES)
    if new_status is None:
        print("Error: Invalid status. Use Online or Offline.")
        return

    devices[name]["status"] = new_status
    print(f"Success: {name} status updated to {new_status}.ദ്ദി˙∇˙)ว")


def remove_device():
    print("\n--- Remove Device ---")
    name = input("Enter device name: ")

    if name not in devices:
        print(f"Error: no device named '{name}' was found.")
        return

    confirm = input(f"Are you sure you want to remove {name}? (yes/no): ").lower()
    if confirm == "yes":
        devices.pop(name)   # frees the name and IP address for reuse
        print(f"Success: {name} has been removed.")
    else:
        print("Removal cancelled.")


def display_inventory():
    print("\n========== NETWORK INVENTORY ==========")
    if len(devices) == 0:
        print("No devices are registered.")
        return

    print(f"{'Name':<12}{'IP Address':<17}{'Type':<14}{'Status'}")
    print("-" * 52)
    for name, info in devices.items():
        print(f"{name:<12}{info['ip']:<17}{info['type']:<14}{info['status']}")


def summary_report():
    print("\n========== NETWORK SUMMARY ==========")
    total = len(devices)

    online = 0
    for info in devices.values():
        if info["status"] == "Online":
            online += 1
    offline = total - online

    percent_online = (online / total * 100) if total > 0 else 0.0

    print(f"Total devices: {total}")
    print(f"Online devices: {online}")
    print(f"Offline devices: {offline}")
    print(f"Network availability: {percent_online:.1f}%")

    # Set of unique device types
    unique_types = set()
    for info in devices.values():
        unique_types.add(info["type"])

    # Count each type that is in use, in the order of DEVICE_TYPES
    type_counts = {}
    for device_type in DEVICE_TYPES:
        count = 0
        for info in devices.values():
            if info["type"] == device_type:
                count += 1
        if device_type in unique_types:
            type_counts[device_type] = count

    summary_parts = [f"{t}: {c}" for t, c in type_counts.items()]
    print("Devices by type: " + (", ".join(summary_parts) if summary_parts else "None"))
    print(f"Unique device types: {len(unique_types)}")


# FILE HANDLING SECTION ----------------------------------------------------------------------

def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as file:
            count = 0
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                parts = [part.strip() for part in line.split(",")]
                if len(parts) != 4:
                    continue   # skip malformed lines
                name, ip, device_type, status = parts
                devices[name] = {"ip": ip, "type": device_type, "status": status}
                count += 1
        print(f"Loaded {count} device(s) from {INVENTORY_FILE}.")
    except FileNotFoundError:
        print("No saved inventory found. Starting with an empty inventory.")

#save the dang info
def save_inventory():
    with open(INVENTORY_FILE, "w") as file:
        for name, info in devices.items():
            file.write(f"{name},{info['ip']},{info['type']},{info['status']}\n")
    print(f"Inventory saved to {INVENTORY_FILE}")


#MAIN MENUUU_-----------------------------------------------------------------------

def show_menu():
    print("\n========== NETWORK DEVICE MANAGER ==========")
    print("1. Register New Device")
    print("2. Search for Device")
    print("3. Update Device Status")
    print("4. Remove Device")
    print("5. Display Network Inventory")
    print("6. Network Summary Report")
    print("7. Exit")

#options to chood=sde from
def main():
    load_inventory()

    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            register_device()
        elif choice == "2":
            search_device()
        elif choice == "3":
            update_status()
        elif choice == "4":
            remove_device()
        elif choice == "5":
            display_inventory()
        elif choice == "6":
            summary_report()
        elif choice == "7":
            print("\nSaving network inventory...beep beep boop...")
            save_inventory()
            print("Goodbye!")
            break
        else:
            print("JUST PICK A NUMBER FROM 1-7 HOW HARD CAN IT BE.")


if __name__ == "__main__":
    main()
