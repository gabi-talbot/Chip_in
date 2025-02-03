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
    items_requested = db.relationship('ItemRequested', backref='group', lazy='joined',
                                      cascade='all, delete')
    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):

        items_requested = []

        for item in self.items_requested:
            item_dict = {}
            item_dict['item_id'] = item.item_id
            item_dict['date_requested'] = item.date_requested
            items_requested.append(item_dict)

        return {
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city': self.city,
            'county': self.county,
            'email': self.email,
            'image_link': self.image_link,
            'items_requested': items_requested
        }


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
    def format(self):
        return {
            'name': self.name,
            'slug': self.slug,
            'image_link': self.image_link,
            'items': self.items
        }
    def __repr__(self):
        return f'<Category {self.name}, {self.id}>'


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    groups_requesting = db.relationship('ItemRequested', backref=db.backref('item'), lazy='joined',)

    def format(self):
        return {
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id,
            'groups_requesting': self.groups_requesting,
        }
    def __repr__(self):
        return f'<Item {self.name}, {self.id}>'

# joining table for many-to-many relationship between group and item
# requested
class ItemRequested(db.Model):
    __tablename__ = 'item_requested'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    date_requested = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'group_id': self.group_id,
            'item_id': self.item_id,
            'date_requested': self.date_requested,
        }

    def __repr__(self):
        return f'<ItemRequested {self.date_requested}, {self.id}>'



