import socket

target_host = input("Please enter a host to connect to: ")
short_host = target_host[4:]
target_port = int(input("Please enter a port to connect to: "))
target_port = 9991
d = f"GET / HTTP/1.1\r\nHost: {short_host}\r\n\r\n"
data = d.encode("utf-8")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
print("Connection to host successful")
client.send(data)
resp = client.recv(4096)
response = resp.decode("utf-8")
print(response)