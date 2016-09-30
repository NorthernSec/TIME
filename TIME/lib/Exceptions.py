class WebException(Exception):
  def __init__(self, message, json=False, status_code=None, payload=None):
    Exception.__init__(self)
    self.message     = message
    self.json        = json
    self.status_code = status_code if status_code else 400
    self.payload     = payload
    self.error_type  = str(type(self)).split("'")[1]

  def to_dict(self):
    rv = dict(self.payload or ())
    rv['message'] = self.message
    return rv


class InvalidCase(WebException):
  def __init__(self, *args, **kwargs):
    WebException.__init__(self, *args, **kwargs)

