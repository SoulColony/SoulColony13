import socket


class IRC:
    def __init__(self, network, port, name, hostName, serverName, realName):
        self.network = network
        self.port = port
        self.hostName = hostName
        self.serverName = serverName
        self.realName = realName
        self.queue = []
        self.partial = b""

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.network, self.port))
        self.address = self.socket.getpeername()

        self.nick(name)
        self.send(
            "USER " + self.name + " " + self.serverName + " "
            + self.hostName + " :" + self.realName
        )

    def quit(self):
        try:
            self.send("QUIT")
        finally:
            self.socket.close()

    def send(self, text):
        self.socket.sendall((text + "\r\n").encode("utf-8"))

    def nick(self, name):
        self.name = name
        self.send("NICK " + self.name)

    def addressquery(self):
        print(self.address)
        return socket.gethostbyaddr(str(self.address[0]))

    def recv(self, size=2048):
        chunk = self.socket.recv(size)

        if not chunk:
            raise ConnectionError("IRC server closed the connection")

        commands = (self.partial + chunk).split(b"\r\n")
        self.partial = commands.pop()

        self.queue.extend(
            command.decode("utf-8", errors="replace")
            for command in commands
            if command
        )

    def retrieve(self):
        if self.queue:
            return self.queue.pop(0)
        return False

    def dismantle(self, command):
        if command:
            source = command.split(":")[1].split(" ")[0]
            parameters = command.split(":")[1].split(" ")[1:]

            if parameters and not parameters[-1]:
                parameters.pop()

            if command.count(":") > 1:
                start = command.find(":", command.find(":") + 1)
                parameters.append(command[start + 1:])

            return source, parameters

    def privmsg(self, destination, message):
        self.send("PRIVMSG " + destination + " :" + message)

    def handshake(self, hexstring):
        self.send("PONG :" + hexstring)

    def notice(self, destination, message):
        self.send("NOTICE " + destination + " :" + message)

    def join(self, channel):
        self.send("JOIN " + channel)

    def part(self, channel):
        self.send("PART " + channel)

    def topic(self, channel, topic=""):
        self.send("TOPIC " + channel + " " + topic)

    def names(self, channel):
        self.send("NAMES " + channel)

    def invite(self, nick, channel):
        self.send("INVITE " + nick + " " + channel)

    def mode(self, channel, mode, nick=""):
        self.send("MODE " + channel + " " + mode + " " + nick)

    def banon(self, channel, name):
        self.mode(channel, "+b", name)

    def banoff(self, channel, name):
        self.mode(channel, "-b", name)

    def kick(self, channel, nick, reason=""):
        self.send("KICK " + channel + " " + nick + " " + reason)

    def who(self, pattern):
        self.send("WHO " + pattern)

    def whois(self, nick):
        self.send("WHOIS " + nick)

    def whowas(self, nick):
        self.send("WHOWAS " + nick)