class BaseResponse(object):

    def __init__(self,status=True,data=None,error=None):
        self.status = status
        self.data = data
        self.error = error

    @property
    def dict(self):
        return self.__dict__