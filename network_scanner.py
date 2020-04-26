#!/usr/bin/env python

# This is a script to scan the network in Kali Linux 2020. The output results MAC and IP of the clients connected to the network

import scapy.all as scapy
import argparse

# This function gets the argument and displays the function purpose

def get_argument():
    parser = argparse.ArgumentParser(description='This is a program to scan the network at subnet boundary')
    parser.add_argument("-t", "--target", dest="target", help="Subnet to scan")
    results = parser.parse_args()

    if not results.target:
        parser.error("[-] Please specify a subnet. Use --help for more details")
    return results

# This function scans the network for a given IP/subnetmask

def scan(ips):
    arp_request = scapy.ARP(pdst=ips)
    # arp_request.show()
    # scapy.ls(scapy.ARP())
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")   # sending a broadcast ethernet frame for ARP data
    arp_request_broadcast = broadcast / arp_request    # combining arp packet with ethernet frame
    answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)[0] # returns two lists (answered and unanswered)
    arp_table = []
    for answer in answered_list:
        client_dict = {"ip": answer[1].psrc,"mac": answer[1].hwsrc}
        arp_table.append(client_dict)
    return arp_table

# This function prints the result in a table

def print_arp_table(results_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    for clients in results_list:
        print(clients["ip"] + "\t\t" + clients["mac"])


options = get_argument()
scan_result = scan(options.target)
print_arp_table(scan_result)
