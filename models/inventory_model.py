inventory = []

def get_all():
    return inventory

def get_one(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)

def add_item(item):
    inventory.append(item)

def update_item(item_id, data):
    item = get_one(item_id)
    if item:
        item.update(data)
    return item

def delete_item(item_id):
    global inventory
    inventory = [item for item in inventory if item["id"] != item_id]