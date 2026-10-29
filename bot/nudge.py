import pickle
import socket
import sys

import CORE_DATA


def pack():
    if len(sys.argv) < 2:
        return

    ip = sys.argv[1]
    data = sys.argv[2:]
    dictionary = {"ip": ip, "data": data}
    pickled = pickle.dumps(dictionary)
    nudge(pickled)


def nudge(data):
    if CORE_DATA.DISABLE_ALL_NON_MANDATORY_SOCKET_CONNECTIONS:
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        connection.connect(("localhost", 45678))
        connection.sendall(data)


if __name__ == "__main__" and len(sys.argv) > 1:
    pack()