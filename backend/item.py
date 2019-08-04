class item():
    def __init__(self,item_id,name,price,description,total_amount):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.description = description
        self.total_amount = total_amount
        self.quantity = 1;

    def serialize(self):
        return dict({
        'item_id': self.item_id,
        'name': self.name,
        'price': str(self.price),
        'description': self.description,
        'total_amount': self.total_amount,
        'quantity': self.quantity
        })
