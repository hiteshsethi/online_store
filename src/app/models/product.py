from src.app import db


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.String(512), nullable=False)
    price = db.Column(db.Float(2, True))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
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
    __table_args__ = (db.UniqueConstraint('name', name='products_name_uniq'),)

    def serialize(self):
        field = ['id',
                 'name',
                 'description',
                 'price',
                 'category_id',
                 'is_active',
                 'created_at',
                 'updated_at']
        res = {}
        for each in field:
            res[each] = getattr(self, each)
        return res
