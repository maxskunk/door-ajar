from db import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'users'

    go_id = db.Column(db.String(80), primary_key=True)
    nick = db.Column(db.String(80))
    email = db.Column(db.String(80))
    over_18 = db.Column(db.Integer)
    terms_accepted = db.Column(db.Integer)
    is_admin = db.Column(db.Integer)
    toybox_public = db.Column(db.Integer)
    sash_public = db.Column(db.Integer)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    pronouns = db.Column(db.String(80))
    nipple_play = db.Column(db.Integer)
    vagina_play = db.Column(db.Integer)
    penis_play = db.Column(db.Integer)
    anal_play = db.Column(db.Integer)

    def __init__(self, go_id, nick, email, over_18, terms_accepted, toybox_public, sash_public, pronouns, nipple_play, vagina_play, penis_play, anal_play):
        self.go_id = go_id
        self.nick = nick
        self.email = email
        self.over_18 = over_18
        self.terms_accepted = terms_accepted
        self.toybox_public = toybox_public
        self.sash_public = sash_public
        self.date_joined = datetime.now()
        self.pronouns = pronouns
        self.nipple_play = nipple_play
        self.vagina_play = vagina_play
        self.penis_play = penis_play
        self.anal_play = anal_play
        self.is_admin = 0

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_go_id(cls, _id):
        return cls.query.filter_by(go_id=_id).first()

    @classmethod
    def user_registered(cls, _id):
        if cls.query.filter_by(go_id=_id).first():
            return True
        else:
            return False
