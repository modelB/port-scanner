import socket
import re
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose = False):
    ip = None
    host = None
    ip_regex = pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
  
    try:
      if ip_regex.match(target) and socket.inet_aton(target):
        ip = target
        if verbose:
          try:
            host = socket.gethostbyaddr(ip)[0]
          except:
            host = None
    except:
      return "Error: Invalid IP address"
      
    if not(ip):
      try:
        host = target
        ip = socket.gethostbyname(target)
      except:
        return "Error: Invalid hostname"
    open_ports = []
    for port in range(port_range[0], port_range[1]+1):
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.settimeout(1)
      conn = s.connect_ex((ip, port))
      if conn == 0:
        open_ports.append(port)
      s.close()
    if verbose:
      stringified_host_and_ip = ''
      if host:
        stringified_host_and_ip = f"{host} ({ip})"
      else:
        stringified_host_and_ip = ip
        
      output_str = f"Open ports for {stringified_host_and_ip}\nPORT     SERVICE"
      for port in open_ports:
        output_str+='\n'
        stringified_port = str(port)
        output_str+=(stringified_port + (9-len(stringified_port))*" "+ ports_and_services[port])
      return(output_str)
    return(open_ports)