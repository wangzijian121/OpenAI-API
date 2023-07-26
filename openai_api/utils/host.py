from netifaces import ifaddresses, AF_INET


def get_ip_in_net_segment():
    """
    Get ip in this  net segment.
    """
    local_ip = ifaddresses("eth0")[AF_INET][0]["addr"]
    base_local_ip = ".".join(local_ip.split(".")[0:3])
    local_segment_ips = [base_local_ip + "." + str(i) for i in range(1, 256)]
    return local_segment_ips
