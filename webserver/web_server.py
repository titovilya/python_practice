import socket
from datetime import datetime
import _thread

def start_server(port, max_len):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", int(port)))
        server.listen(4)
        while True:
            print("Working")
            cl_socket, address = server.accept()
            # print(f"CLIENT {address[1]}")
            data = cl_socket.recv(int(max_len)).decode("utf-8")
            print(data)
            ip = address[1]
            content = page_from_get(data, ip)
            # _thread.start_new_thread(cl_socket.send(content, (cl_socket, )))
            cl_socket.send(content)
            cl_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
        print("Im over =)")

def page_from_get(request, ip):
    path = request.split(" ")[1]
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.now()}:{ip}:{path} \n ")
    print(path)
    response = ""
    HDRS = "HTTP/1.1 200 OK\r\nDate: {today}\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
    HDRS_404  = "HTTP/1.1 404 OK\r\nDate: {today}\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
    try:
        with open("views" + path, "rb") as f:
            response = f.read()
        return HDRS.encode("utf-8") + response
    except FileNotFoundError:
        return (HDRS_404 + "Sorry no page yet!").encode("utf-8")
    except IndexError:
        return (HDRS_404 + "Sorry no page yet!").encode("utf-8")


if __name__ == "__main__":
    with open("settings.txt", "r") as f:
        tmp = []
        for i in f:
            tmp.append(i.split("=")[1])
    port = tmp[0]
    max_len = tmp[2]
    start_server(port, max_len)

