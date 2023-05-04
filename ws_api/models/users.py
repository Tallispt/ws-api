import datetime as dt

class User():
  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = password
    self.created_at = dt.datetime.now()
    
