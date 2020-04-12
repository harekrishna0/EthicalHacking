#!/usr/bin/python

# This is a script to change the MAC address of the interface specified in Kali Linux 2020.

import subprocess
import argparse
import re


# This function gets the argument and displays the function purpose

def get_argument():
    parser = argparse.ArgumentParser(description='This is a program to change MAC address of an interface')
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change the MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac", help="Change to new MAC address")
    results = parser.parse_args()

    if not results.interface:
        parser.error("[-] Please specify an interface. Use --help for more details")
    elif not results.new_mac:
        parser.error("[-] Please specify a MAC address. Use --help for more details ")
    return results

# This function changes the mac_address of the interface

def mac_changer(interface, macaddr):
    subprocess.call(["sudo","/sbin/ifconfig",interface,"down"])
    subprocess.call(["sudo","/sbin/ifconfig",interface,"hw","ether",macaddr])
    subprocess.call(["sudo","/sbin/ifconfig",interface,"up"])
    print("[+] Changing the MAC Address of the interface {} to {}".format(interface,macaddr))


# This function uses regex to print out the final mac-address

def print_mac(interface):
    final_result = subprocess.check_output(["sudo","/sbin/ifconfig",interface])
    displayed_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",final_result)

    if displayed_mac:
        return displayed_mac.group(0)

    else:
        return None


options = get_argument()
mac_changer(options.interface,options.new_mac)
final_mac = print_mac(options.interface)

if final_mac == options.new_mac:
    print(" MAC Address Successfully Changed")
else:
    print("Error occurred somewhere, please FIX it.")