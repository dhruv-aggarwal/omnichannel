from app import db


class PlayStore(db.Model):
    __tablename__ = 'play_store'

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(20))
    title_id = db.Column(db.Integer, db.ForeignKey('processed_text.id'))
    vote_count = db.Column(db.Integer)
    rating = db.Column(db.Float)
    client_id = db.Column(db.Integer)
    review_id = db.Column(db.Integer, db.ForeignKey('processed_text.id'))
    author_url = db.Column(db.Text)
    author = db.Column(db.String(255))

    title = db.relationship(
        'ProcessedText',
        foreign_keys=client_id,
        back_populates="source",
        lazy='select'
    )
    review = db.relationship(
        'ProcessedText',
        back_populates="source",
        foreign_keys=review_id,
        lazy='select'
    )
