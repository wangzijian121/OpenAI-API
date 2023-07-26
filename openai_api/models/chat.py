from openai_api import db


class Chat(db.Model):
    __tablename__ = "chat"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    session = db.Column(db.Text)

    def __init__(self, name, session):
        self.name = name
        self.session = session
