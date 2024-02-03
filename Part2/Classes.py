class Message:
    content: str
    timestamp: str


class User:
    address: str
    uuid: str
    def __init__(self,uuid,address):
        self.address=address
        self.uuid=uuid

    def Req_Get_Group_List(self):
        # Req server to get all available group lists
        pass
    def Req_Join_Group(self):
        # Req group to join it
        pass
    def Req_Leave_Group(self):
        # Req group to leave it
        pass
    def Req_Get_Messages(self):
        # Req group for all messages
        pass
    def Req_Send_Messages(self):
        # Req group to send messages
        pass



class Group:
    uuid: str
    address: str
    Users: [User]
    Messages: [Message]

    def __init__(self, uuid, address):
        self.uuid = uuid
        self.address = address
        self.Users = []
        self.Messages = []

    def Req_Register(self):
        # Send a req to register to server

        pass



class Server:
    Groups: [Group]
