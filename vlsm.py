import math
import json

def parse_network_ID(id: str) -> tuple:
    """
    Accept a string with the base network and return the integer values
    of both the network id and the subnet mask.

    Param:
    - id: Network ID with the subnet mask with the following format
        A.B.C.D/X

    Return:
    - decimal_network_ID: Integer value of the four octets of the network
    - decimalMask: Integer value of the four octets of the subnet mask
    """
    if 2 == len(id.split('/')):
        networkID, mask = id.split('/')
        mask = 32 - int(mask)
    else:
        print("Error: Network ID and Subnet mask are required")
        exit(-1)

    decimalMask = (2**32 - 1) & ~(2**mask - 1)

    networkID = networkID.split('.')
    if 4 == len(networkID):
        decimal_network_ID = 0
        for element in range(len(networkID)):
            decimal_network_ID += int(networkID[element])<<(32 - 8*(element + 1))

    else:
        print("Error: Invalid network ID")
        exit(-1)

    return decimal_network_ID, decimalMask

def get_network_and_mask(decimal_network_ID: int, decimal_network_mask: int) -> tuple:
    """
    Accept the integer values for the network ID and subnet mask;
    return a formatted string for the network ID and integer value
    for the subnet mask from 1 to 32.

    Param:
    - decimal_network_ID: Integer value of the four octets of the network
    - decimal_network_mask: Integer value of the four octets of the
        subnet mask

    Return:
    - network: Formated string of the network ID separated in octets
        for a better visualization
    - mask: Integer value for the subnet mask, commonly written after
        the network ID with a forward slash
    """
    network = "{}.{}.{}.{}".format((decimal_network_ID>>24) & 0xFF, \
        (decimal_network_ID>>16) & 0xFF, (decimal_network_ID>>8) & 0xFF, \
        decimal_network_ID & 0xFF)

    mask = 0
    for _ in range(32):
        mask += 1 if 1 & decimal_network_mask else 0
        decimal_network_mask>>=1

    return network, mask

def get_decimal_mask(rawMask: int) -> str:
    """
    Returns a formated string for network subnet mask in octets
    """
    mask = "{}.{}.{}.{}".format(rawMask>>24, \
        (rawMask>>16) & 0xFF, (rawMask>>8) & 0xFF, \
        rawMask & 0xFF)

    return mask

def add_hosts_to_network(decimal_network_ID: int, decimal_network_mask: int,
                         requiredHosts: int) -> tuple:
    """
    Accept the network ID and a number of hosts; returns found number
    of hosts and last usable IP.

    Params:
    - decimal_network_ID: Integer value of the four octets of the network
    - decimal_network_mask: Integer value of the four octets of the
        subnet mask
    - requiredHosts: Number of hosts required for the requested network

    Return:
    - N: The power of 2 used to calculate the foundHosts var
    - foundHosts: The value of the next power of 2 of the requiredHosts
    - decimal_network_ID + foundHosts: The last usable IP of the subnet
    """
    N = math.ceil(math.log2(requiredHosts))
    _, mask = get_network_and_mask(decimal_network_ID, decimal_network_mask)
    if 2 >= N:
        foundHosts = 2
        N = 2

    elif N > mask:
        foundHosts = 0

    else:
        foundHosts = 2**N - 2

    return N, foundHosts, decimal_network_ID + foundHosts

if "__main__" == __name__:
    try:
        with open("networks.json", "r") as networks_file:
            input_networks = json.load(networks_file)
            net_ID = input_networks["net_id"]
            networks = input_networks["networks"]
    except FileNotFoundError:
        print("File called 'networks.json' must be\
               placed in the same directory.")
        exit(-1)

    output_table = []
    table_header = [
        "Redes",
        "Hosts solicitados",
        "N",
        "Hosts encontrados",
        "Direccion de red",
        "Mascara",
        "Mascara decimal punteada",
        "Primera IP utilizable",
        "Ultima IP utilizable",
        "Broadcast"
    ]
    output_table.append(table_header)

    for network in networks:
        decimal_network_ID, decimal_network_mask = parse_network_ID(net_ID)

        row = []
        row.append(network)
        row.append(networks[network])

        print("Network: {}".format(network))
        print("Hosts: {}\n".format(networks[network]))

        N, found_hosts, new_network_ID = add_hosts_to_network(
            decimal_network_ID, decimal_network_mask, networks[network])

        row.append(N)
        row.append(found_hosts)

        network_id, network_mask = get_network_and_mask(decimal_network_ID,
                                                        decimal_network_mask)

        row.append(network_id)
        row.append("/{}".format(32 - N))

        decimal_network_ID += found_hosts + 2

        row.append(network_mask)

        output_table.append(row)

    for row in output_table:
        print(row)