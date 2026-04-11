from config import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    price = db.Column(db.Float, default=0.0)
    quantity = db.Column(db.Integer, default=0)
    barcode = db.Column(db.String(50), unique=True)
    brand = db.Column(db.String(100))
    ingredients = db.Column(db.Text)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'quantity': self.quantity,
            'barcode': self.barcode,
            'brand': self.brand,
            'ingredients': self.ingredients,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def validate(data, partial=False):
        errors = []
        if not partial:
            if not data.get('name'):
                errors.append('Name is required')
        if 'price' in data and data['price'] is not None:
            try:
                price = float(data['price'])
                if price < 0:
                    errors.append('Price must be non-negative')
            except (ValueError, TypeError):
                errors.append('Invalid price format')
        if 'quantity' in data and data['quantity'] is not None:
            try:
                qty = int(data['quantity'])
                if qty < 0:
                    errors.append('Quantity must be non-negative')
            except (ValueError, TypeError):
                errors.append('Invalid quantity format')
        return errors
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def search_by_name(cls, name):
        return cls.query.filter(cls.name.ilike(f"%{name}%")).all()
    
    @classmethod
    def filter_by_category(cls, category):
        return cls.query.filter_by(category=category).all()
    
    @classmethod
    def get_stats(cls):
        total_products = cls.query.count()
        total_quantity = db.session.query(db.func.sum(cls.quantity)).scalar() or 0
        total_value = db.session.query(db.func.sum(cls.price * cls.quantity)).scalar() or 0
        
        return {
            'total_products': total_products,
            'total_quantity': total_quantity,
            'total_value': total_value
        }