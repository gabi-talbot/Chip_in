
from backend import db

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    county = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    image_link = db.Column(db.String(), nullable=True)
    items_requested = db.relationship('Item', backref=db.backref('shows'),
                                      cascade='all, delete')


    def __repr__(self):
        return f'<Group {self.name}, {self.id}>'

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    slug = db.Column(db.String(), unique=True, nullable=False)
    image_link = db.Column(db.String(), nullable=False)
    items = db.relationship('Item', backref='category', lazy='dynamic',
                            cascade='all, delete')

    def __repr__(self):
        return f'<Category {self.name}, {self.id}>'


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f'<Item {self.name}, {self.id}>'


class ItemRequested(db.Model):
    __tablename__ = 'item_requested'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    date_requested = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"),
                               nullable=False)

    def __repr__(self):
        return f'<ItemRequested {self.date_requested}, {self.id}>'



# def format/to-json(self):
    #return {
    # "id": self.id,
    #...

