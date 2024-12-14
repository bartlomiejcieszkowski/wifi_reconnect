import argparse
import sys
from subprocess import TimeoutExpired
from time import sleep

import winwifi

def wifi_is_connected(ssid):
    while True:
        try:
            for conn in winwifi.WinWiFi.get_connected_interfaces():
                if conn.ssid == ssid:
                    return True
        except TimeoutExpired:
            continue
        break
    return False

def wifi_reconnect():
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--ssid", default=None, type=str, help="wifi name")

    args = ap.parse_args()
    if args.ssid is None:
        return -1

    while True:
        if not wifi_is_connected(args.ssid):
            print(f"[{args.ssid}] Reconnecting..")
            try:
                winwifi.WinWiFi.connect(args.ssid)
            except RuntimeError:
                pass
            sleep(5)
            print(f"[{args.ssid}] Connected? {wifi_is_connected(args.ssid)}")
        sleep(5 * 60)

if __name__ == '__main__':
    ec = wifi_reconnect()
    sys.exit(ec)
