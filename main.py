import subprocess
import os
from pathlib import Path
import streamlit as st

def get_wifi_profiles():
    """Retrieves saved WiFi profile names using nmcli (Linux)."""
    try:
        # Run nmcli connection show to get all saved network connections
        result = subprocess.check_output(
            ["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show"],
            shell=False,
            text=True
        )
        
        names = []
        for line in result.splitlines():
            if not line.strip():
                continue
            # nmcli outputs as 'Name:Type'. We check if the type is wireless (802-11-wireless)
            parts = line.split(":")
            if len(parts) >= 2 and "802-11-wireless" in parts[1]:
                names.append(parts[0])
        return names
    except Exception:
        return []

def get_wifi_password(name):
    """Retrieves the password for a specific WiFi profile using nmcli."""
    try:
        # nmcli requires root/sudo privileges to view saved security passwords
        result = subprocess.check_output(
            ["nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", name],
            shell=False,
            text=True
        )
        password = result.strip()
        return password if password else "Open Network / No Password"
    except Exception:
        return "Requires Root Access / Not Found"

def main():
    st.set_page_config(page_title="Mahigo PassView", layout="wide")
    st.title("📶 Mahigo PassView")
    st.write("View all saved WiFi profiles & passwords stored on your Linux system.")

    names = get_wifi_profiles()
    if names:
        for name in names:
            password = get_wifi_password(name)
            st.write(f"**{name}** | `{password}`")
    else:
        st.warning("No WiFi profiles found! Ensure NetworkManager (nmcli) is running.")

if __name__ == "__main__":
    main()
