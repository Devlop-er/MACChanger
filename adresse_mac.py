#!/usr/bin/env python3
# coding: utf-8

# Utilisation du module subprocess pour gérer les fonctionnalités système (ifconfig)
import subprocess

# Utilisation du module optparse pour gérer l'utilisation d'arguments
import optparse

# Utilisation du module re pour spécifier un pattern (Pythex)
import re

print("""\


   ██╗  ██╗ █████╗ ████████╗ █████╗ ██╗  ██╗██████╗
   ██║  ██║██╔══██╗╚══██╔══╝██╔══██╗██║ ██╔╝██╔══██╗
   ███████║███████║   ██║   ███████║█████╔╝ ██████╔╝
   ██╔══██║██╔══██║   ██║   ██╔══██║██╔═██╗ ██╔══██╗
   ██║  ██║██║  ██║   ██║   ██║  ██║██║  ██╗██║  ██║
   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
"""

# Création d'une fonction permettant de récupérer les arguments utilisés (-i, -m, -h)
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", dest="interface",
        help="Interface sur laquelle changer l'adresse MAC")
    parser.add_option("-m", dest="adresse_mac",
        help="Adresse MAC à utiliser")

    (options, arguments) = parser.parse_args()

# Affichage des messages d'erreurs si (-i) ou (-m-) sont manquants
    if not options.interface:
        parser.error("[-] Veuillez choisir votre interface, utiliser --help pour plus d'informations.")
    elif not options.adresse_mac:
        parser.error("[-] Veuillez saisir une adresse MAC, utiliser --help pour plus d'informations.")
    return options

# Fonction permettant de modifier l'addresse MAC avec les informations données (interface + nouvelle_adresse_mac)
def change_mac(interface, nouvelle_adresse_mac):
    print("[+] L'adresse MAC utilisée sur " + interface + " est : " + nouvelle_adresse_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", nouvelle_adresse_mac])
    subprocess.call(["ifconfig", interface, "up"])

# Fonction permettant de vérifier l'output avec les informations données + le charset spécifié
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",
        ifconfig_result.decode("utf-8"))

    if mac_address_search_result:
        return mac_address_search_result.group(0)

    print("[-] Impossible de lire l'adresse MAC")

    return None

if __name__ == "__main__":
    options = get_arguments()
    current_mac = get_current_mac(options.interface)
    change_mac(options.interface, options.adresse_mac)
    nouvelle_adresse_mac = get_current_mac(options.interface)

    if current_mac == options.adresse_mac:
        print("[+] L'adresse MAC utilisée est la suivante " + current_mac)
