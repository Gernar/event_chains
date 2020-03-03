from app import db
from datetime import datetime


class Vector(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    vector = db.Column(db.Text)
    new_id = db.Column(db.Integer, db.ForeignKey('new.id'), nullable=False)


class New(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    edition = db.Column(db.String(64), index=True)
    topics = db.Column(db.String(120), index=True)
    subtopics = db.Column(db.String(120), index=True)
    title = db.Column(db.Text, index=True)
    subtitle = db.Column(db.Text, index=True)
    text = db.Column(db.Text)
    tags = db.Column(db.Text)
    author = db.Column(db.String(120))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    vector = db.relationship('Vector', backref=db.backref('new'), lazy=True)

    def __repr__(self):
        return '<New id: {}, edition: {}>'.format(self.id, self.edition)