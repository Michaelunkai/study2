from twisted.internet import protocol, reactor
from twisted.protocols import basic

class ChatServerProtocol(basic.LineReceiver):
    def __init__(self):
        self.name = None
        self.state = "REGISTER"
        self.factory = None  # Initialize factory attribute

    def connectionMade(self):
        self.sendLine(b"Welcome to the chat server! What's your name?")

    def connectionLost(self, reason):
        if self.name in self.factory.clients:
            del self.factory.clients[self.name]
            self.broadcastMessage(f"{self.name} has left the chat.")

    def lineReceived(self, line):
        if self.state == "REGISTER":
            self.handle_REGISTER(line)
        else:
            self.handle_CHAT(line)

    def handle_REGISTER(self, name):
        if name in self.factory.clients:
            self.sendLine(b"Name taken, please choose another.")
            return

        self.sendLine(f"Welcome, {name}!".encode('utf-8'))
        self.broadcastMessage(f"{name} has joined the chat.")
        self.name = name
        self.factory.clients[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = f"{self.name}: {message}"
        self.broadcastMessage(message)

    def broadcastMessage(self, message):
        for name, protocol in self.factory.clients.items():
            if protocol != self:
                protocol.sendLine(message.encode('utf-8'))

class ChatServerFactory(protocol.Factory):
    def __init__(self):
        self.clients = {}

    def buildProtocol(self, addr):
        protocol = ChatServerProtocol()
        protocol.factory = self  # Set factory attribute
        return protocol

if __name__ == "__main__":
    reactor.listenTCP(8123, ChatServerFactory())
    reactor.run()
