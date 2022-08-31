from ..models.product import Product
from ..models.store_stock_change import StoreStockChange

PROPS = ['1', '2', '3', '4']


def is_value_valid(key, value):
    if key == '1':
        if value is True or value is False:
            return True
    else:
        if value is not None and value != float(0.0):
            return True


def create_stock_product_change_log(request, store, old_items, new_items):
    

    old_items_ids = [item.product_id for item in old_items]
    new_items_ids = [item.product_id for item in new_items]

    #
    added = list(set(new_items_ids) - set(old_items_ids))
    deleted = list(set(old_items_ids) - set(new_items_ids))
    updated = list(set(new_items_ids).intersection(old_items_ids))

    # deleted
    for item in deleted:#O(n)<-n is deleted
        p = Product.objects.get(id=item)
        StoreStockChange.objects.create(user_id=request.user.id,
                                        store=store,
                                        product=p,
                                        prop='-',
                                        old_value='-',
                                        new_value='-',
                                        action_type="deleted")
        
    # added
    for item in added:#O(n)<-n is added
        p = Product.objects.get(id=item)
        new_item = next(i for i in new_items if i.product_id == item).as_dict()
        #
        for prop in PROPS:#O(1) <-m is props 4
            if prop in new_item:
                if is_value_valid(prop, new_item[prop]):
                    StoreStockChange.objects.create(user_id=request.user.id,
                                                    store=store,
                                                    product=p,
                                                    prop=prop,
                                                    old_value='-',
                                                    new_value=new_item[prop],
                                                    action_type="added")

    # updated
    for item in updated:#O(n)<-n is updated
        p = Product.objects.get(id=item)
        old_item = next(i for i in old_items if i.product_id == item).as_dict()
        new_item = next(i for i in new_items if i.product_id == item).as_dict()
        #
        for prop in PROPS:#O(1)<-m is props
            if prop in new_item and prop in old_item:
                if old_item[prop] != new_item[prop]:
                    StoreStockChange.objects.create(user_id=request.user.id,
                                                    store=store,
                                                    product=p,
                                                    prop=prop,
                                                    old_value=old_item[prop],
                                                    new_value=new_item[prop],
                                                    action_type="updated")

            elif prop not in old_item:
                if prop in new_item:
                    StoreStockChange.objects.create(
                        user_id=request.user.id,
                        store=store,
                        product=p,
                        prop=prop,
                        old_value='-',
                        new_value=new_item[prop],
                        action_type="updated")
