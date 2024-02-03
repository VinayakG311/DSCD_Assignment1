import time


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
    Status: int

    def __init__(self, uuid, address):
        self.uuid = uuid
        self.address = address
        self.Users = []
        self.Messages = []
        self.Status=0

    def Req_Register(self,socket):
        # Send a req to register to server
        socket.send_pyobj(self)
        rep = socket.recv_string()

        if rep=='SUCCESS':
            self.Status=1



class Server:
    Groups: [Group]
    def __init__(self):
        self.Groups=[]
    def res_group_reg(self,socket):

        message=socket.recv_pyobj()

        print(message)
        print("JOIN REQUEST FROM: %s" % message.address)
        if self.Groups == []:
            print('SUCCESS')
            self.Groups.append(message)
            socket.send_string("SUCCESS")
        else:
            f = 0
            for i in self.Groups:
                if i.uuid == message.uuid:
                    f = 1
                    break
            if f == 0:
                print('SUCCESS')
                self.Groups.append(message)
                time.sleep(1)
                socket.send_string('SUCCESS')
            else:
                print('ERROR: Group already exists')
                time.sleep(1)
                socket.send_string('FAILURE')
