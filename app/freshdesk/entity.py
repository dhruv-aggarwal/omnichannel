from app import db


class Freshdesk(db.Model):
    __tablename__ = 'freshdesk'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('processed_text.id'))
    created_at = db.Column(db.DateTime)
    description_text_id = db.Column(
        db.Integer, db.ForeignKey('processed_text.id')
    )
    email = db.Column(db.String(255))
    sentiment = db.Column(db.String(50))
    csat_rating = db.Column(db.Float)
    country = db.Column(db.String(50))
    platform = db.Column(db.String(50))
    source = db.Column(db.String(255))
    practo_source = db.Column(db.String(255))
    practo_product = db.Column(db.String(255))
    priority = db.Column(db.String(50))
    type = db.Column(db.String(50))

    subject = db.relationship(
        'ProcessedText',
        foreign_keys=subject_id,
        back_populates="source",
        lazy='select'
    )
    description_text = db.relationship(
        'ProcessedText',
        back_populates="source",
        foreign_keys=description_text_id,
        lazy='select'
    )
