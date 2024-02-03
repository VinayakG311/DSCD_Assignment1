class Video:
    name: str
    def __init__(self,name):
        self.name=name

class Youtuber:
    name: str
    Videos: [Video]
    def __init__(self):
        self.Videos=[]
    def Req_Subscribe(self):
        pass

    def Req_Unsubscribe(self):
        pass




class User:
    name: str
    subscription: [Youtuber]
    Notifications: [Video,Youtuber,int]
    def __init__(self):
        self.subscription=[]
        self.Notifications=[]
    def Req_PublishVideos(self,name):
        video = Video(name)
        pass



class Server:
    Users: [User]
    Youtubers : [Youtuber]
    Notifiers: [User,[Video,Youtuber,int]]

    def __init__(self):
        self.Youtubers=[]
        self.Users=[]
        self.Notifiers=[]
    def NotifiyUsers(self):
        pass

    def Res_Sub(self):
        pass

    def Res_unsub(self):
        pass

    def Res_publish(self):
        pass


