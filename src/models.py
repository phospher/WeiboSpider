class WeiboModel(object):
    def __init__(self):
        self.userName = None
        self.text = None
        self.retweetedText = None
        self.time = None
        self.id = None

class UserModel(object):
    def __init__(self):
        self.id = None
        self.name = None