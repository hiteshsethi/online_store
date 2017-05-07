from src.app import db


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    is_active = db.Column(db.Boolean)
    created_at = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime, nullable=False,
        server_default=db.func.current_timestamp(),
        server_onupdate=db.func.current_timestamp()
    )
    __table_args__ = (db.UniqueConstraint('name', name='categories_name_uniq'),)

    def serialize(self):
        field = ['id',
                 'name',
                 'is_active',
                 'created_at',
                 'updated_at']
        res = {}
        for each in field:
            res[each] = getattr(self, each)
        return res
