import socket
import random
import threading
import logging
from datetime import datetime

# logger
LOG_FILE = "honeypot.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(service)s - IP: %(ip)s - Port: %(port)d",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# banners
SERVICE_BANNERS = {
    "ftp": lambda: f"220 Service FTP Server {random.choice(['2.4.8', '3.0.3'])} ready.\r\n",
    "http": lambda: (
        f"HTTP/1.1 200 OK\r\n"
        f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        f"Server: Apache/{random.choice(['2.4.41 (Ubuntu)', '2.2.34 (Unix)'])}\r\n\r\n"
    ),
    "ssh": lambda: f"SSH-2.0-OpenSSH_{random.choice(['7.9p1', '8.4p1'])}\r\n",
    "smtp": lambda: f"220 smtp.example.com ESMTP Postfix\r\n",
    "mysql": lambda: f"5.7.{random.randint(10, 35)}-log MySQL Community Server (GPL)\r\n",
    "redis": lambda: f"+OK Redis {random.choice(['6.2.6', '5.0.14'])}\r\n",
}

# response handlers
def ftp_handler(conn, addr, port):
    log_connection("ftp", addr, port)
    conn.sendall(SERVICE_BANNERS["ftp"]().encode())
    conn.sendall("331 Please specify the password.\r\n".encode())
    conn.close()

def http_handler(conn, addr, port):
    log_connection("http", addr, port)
    conn.sendall(SERVICE_BANNERS["http"]().encode())
    conn.sendall("<html><body><h1>Welcome to the HTTP Server</h1></body></html>".encode())
    conn.close()

def ssh_handler(conn, addr, port):
    log_connection("ssh", addr, port)
    conn.sendall(SERVICE_BANNERS["ssh"]().encode())
    conn.close()

def smtp_handler(conn, addr, port):
    log_connection("smtp", addr, port)
    conn.sendall(SERVICE_BANNERS["smtp"]().encode())
    conn.sendall("250 OK\r\n".encode())
    conn.close()

def mysql_handler(conn, addr, port):
    log_connection("mysql", addr, port)
    conn.sendall(SERVICE_BANNERS["mysql"]().encode())
    conn.sendall("ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)\r\n".encode())
    conn.close()

def redis_handler(conn, addr, port):
    log_connection("redis", addr, port)
    conn.sendall(SERVICE_BANNERS["redis"]().encode())
    conn.sendall("-ERR unknown command 'AUTH'\r\n".encode())
    conn.close()

SERVICE_HANDLERS = {
    "ftp": ftp_handler,
    "http": http_handler,
    "ssh": ssh_handler,
    "smtp": smtp_handler,
    "mysql": mysql_handler,
    "redis": redis_handler,
}

# logging fn
def log_connection(service_name, addr, port):
    logging.info(
        "",
        extra={
            "service": service_name.upper(),
            "ip": addr[0],
            "port": port,
        },
    )
    print(f"[{service_name.upper()}] Connection from {addr[0]}:{port}")

# connection handler
def handle_service(service_name, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", port))
        s.listen(5)
        print(f"[{service_name.upper()}] Service running on port {port}")

        while True:
            conn, addr = s.accept()
            handler = SERVICE_HANDLERS.get(service_name, lambda c, a, p: c.close())
            handler(conn, addr, port)

# socker scanner
def find_free_port():
    while True:
        port = random.randint(100, 1000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("0.0.0.0", port)) != 0:
                return port

# main
def create_services(num_services=15):
    threads = []
    for _ in range(num_services):
        service_name = random.choice(list(SERVICE_BANNERS.keys()))
        port = find_free_port()
        t = threading.Thread(target=handle_service, args=(service_name, port))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    create_services(random.randint(15, 20))
