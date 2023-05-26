from app import db


class Error(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    error_data = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Error %r>' % self.error_data
