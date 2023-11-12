from asyncmy import connect
from config import db_data

class Maria:
    def __init__(self):
        self.user = db_data[0]
        self.password = db_data[1]
        self.db = db_data[2]
        