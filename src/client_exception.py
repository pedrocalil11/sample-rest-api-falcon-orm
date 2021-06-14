import falcon

class ClientException(Exception):
    title = ''
    description = ''
    _http_status = None

    def __init__(self, title, description, http_status):
        Exception.__init__(self)
        self.title = title
        self.description = description
        self._http_status = http_status
    
    def get(self):
        my_dict = dict()
        my_dict['title'] = self.title
        my_dict['description'] = self.description
        return my_dict
    
    def http_status(self):
        return self._http_status

class NotFoundException(ClientException):
    def __init__(self, title, description):
        ClientException.__init__(self, title, description, falcon.HTTP_404)

class ConflictException(ClientException):
    def __init__(self, title, description):
        ClientException.__init__(self, title, description, falcon.HTTP_409)

class BadRequestException(ClientException):
    def __init__(self, title, description):
        ClientException.__init__(self, title, description, falcon.HTTP_400)

class NotAuthorizedException(ClientException):
    def __init__(self, title, description):
        ClientException.__init__(self, title, description, falcon.HTTP_401)

class ForbiddenException(ClientException):
    def __init__(self, title, description):
        ClientException.__init__(self, title, description, falcon.HTTP_403)

class NoContentException(ClientException):
    def __init__(self, title, description):
        ClientException.__init__(self, title, description, falcon.HTTP_204)