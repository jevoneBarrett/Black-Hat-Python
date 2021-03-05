import socket

def show_ip(hostname):
    try:
        host_ip = socket.gethostbyname(hostname)
        print(f'Host: {hostname} IP: {host_ip}')
    except Exception as e:
        print(f'Error retrieving host: {e}')

def main():
    host = input("Please enter a host you want an IP for: ")
    show_ip(host)

if __name__=='__main__':
    main()