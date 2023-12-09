def authorize_user(USER_DB, username,password)->bool:

    for record in USER_DB:
        if record['username'] == username.lower() and record['password'] == password :
            return True
    return False


def remove_auction_item_by_id(AUCTION_ITEMS, id):

    for item in AUCTION_ITEMS:
        if item['id'] == int(id):
            AUCTION_ITEMS.remove(item)
            break


def add_item_to_auction_list(AUCTION_ITEMS,item):

    id = len(AUCTION_ITEMS) +1
    item['id'] = id
    AUCTION_ITEMS.append(item)

def find_auction_item(AUCTION_ITEMS,id):
    for idx,item in enumerate(AUCTION_ITEMS):
        if item['id'] == int(id):
            return idx