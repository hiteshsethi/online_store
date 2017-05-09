from src.app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp(),
        server_onupdate=db.func.current_timestamp()
    )
    __table_args__ = (db.UniqueConstraint('user_name', name='users_user_name_uniq'),)
