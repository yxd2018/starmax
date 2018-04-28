# -*- coding:utf-8 -*-

from amazon.api import AmazonAPI

amazon_dict = {}

amazon_dict["it"] = AmazonAPI("AKIAINRPVKEXVQ65GN6A", "qo4GbATKZqDBpsVrFM6v3p/Y0DA5D/NogrCkyRIy", "oucher3-21",
                                  region="IT", Timeout=5, MaxQPS=1)
amazon_dict["es"] = AmazonAPI("AKIAJGLFK6P37DXE4GOQ", "CKJUOQlcQ3Ar8wH9lIBKtePt5WxzWspePL3c/QsD", "oucher0e-21",
                                  region="ES", Timeout=5, MaxQPS=1)
amazon_dict["fr"] = AmazonAPI("AKIAISQ5EL7RGVOIKCPQ", "KWZaLFPu3VY6nWKKBLldEKqTQzuFT2ahdr3VHNTy", "oucher3-21",
                                region="FR", Timeout=5, MaxQPS=1)
amazon_dict["de"] = AmazonAPI("AKIAJGLFK6P37DXE4GOQ", "CKJUOQlcQ3Ar8wH9lIBKtePt5WxzWspePL3c/QsD", "oucher0e-21",
                                region="DE", Timeout=5, MaxQPS=1)
amazon_dict["jp"] = AmazonAPI("AKIAJEHY7PZI24XSZ7GA", "al5M1gd5UVbDyjihIzF6kn/47ok7M4S29546vqRu", "oucher308-22",
                               region="JP", Timeout=5, MaxQPS=1)
# print(amazon_dict)

try:
    product = amazon_dict["it"].lookup(ItemId='B00EOE0WKQ', Timeout=5)

except Exception,e:
    print(str(e))

else:
    print (product.title)
    print(product.price_and_currency)
    print(product.ean)
    print(product.large_image_url)
    print(product.get_attribute('Publisher'))
    print(product.get_attributes(['ItemDimensions.Width', 'ItemDimensions.Height']))
    print(product.)

"""
from amazon.api import AmazonAPI
import bottlenose.api
region_options = bottlenose.api.SERVICE_DOMAINS.keys()
print(region_options)

amazon_de = AmazonAPI("AKIAINRPVKEXVQ65GN6A", "qo4GbATKZqDBpsVrFM6v3p/Y0DA5D/NogrCkyRIy", "oucher3-21",region="IT")
product = amazon_de.lookup(ItemId='B0051QVF7A')
print(product.title)
print(product.price_and_currency)
"""

"""
from amazon.api import AmazonAPI

amazon = AmazonAPI("AKIAINRPVKEXVQ65GN6A", "qo4GbATKZqDBpsVrFM6v3p/Y0DA5D/NogrCkyRIy", "oucher3-21", region="IT")
try:
    products = amazon.lookup(ItemId='B00EOE0WKQ,B0051QVF7A')
except Exception,e:
    print(str(e))
else:
    print(len(products))
    print(products)
    print(products[0].asin)
"""

"""
from amazon.api import AmazonAPI
amazon = AmazonAPI("AKIAINRPVKEXVQ65GN6A", "qo4GbATKZqDBpsVrFM6v3p/Y0DA5D/NogrCkyRIy", "oucher3-21", region="IT")
try:
    products = amazon.search(Keywords='ipad', SearchIndex='All')
except Exception,e:
    print(str(e))
else:
    # print products.current_page

    for i,product in enumerate(products):
        # print product.asin,product.title
        print('%s.%s--%s'%(i, product.price_and_currency, product.title))
        # print("{0}.'{1}'".format(i, product.title))

"""

"""
from amazon.api import AmazonAPI
amazon = AmazonAPI("AKIAINRPVKEXVQ65GN6A", "qo4GbATKZqDBpsVrFM6v3p/Y0DA5D/NogrCkyRIy", "oucher3-21", region="IT")
try:
    products = amazon.search_n(2,Keywords='ipad', SearchIndex='All')
except Exception,e:
    print(str(e))
else:
    for i,product in enumerate(products):
        print('%s.%s'%(i, product.title))

"""
"""
#长度为0
from amazon.api import AmazonAPI
amazon = AmazonAPI("AKIAINRPVKEXVQ65GN6A", "qo4GbATKZqDBpsVrFM6v3p/Y0DA5D/NogrCkyRIy", "oucher3-21", region="IT")
try:
    products = amazon.similarity_lookup(ItemId='B00EOE0WKQ,B0051QVF7A')
except Exception, e:
    print(str(e))
else:
    print(products)
    print(len(products))

"""

"""
#没有该浏览节点
from amazon.api import AmazonAPI
amazon = AmazonAPI("AKIAINRPVKEXVQ65GN6A", "qo4GbATKZqDBpsVrFM6v3p/Y0DA5D/NogrCkyRIy", "oucher3-21", region="IT")
try:
    bn = amazon.browse_node_lookup(BrowseNodeId=2642129011)
except Exception,e:
    print(str(e))
else:
    print(bn.name)
"""
"""
from amazon.api import AmazonAPI
amazon = AmazonAPI("AKIAINRPVKEXVQ65GN6A", "qo4GbATKZqDBpsVrFM6v3p/Y0DA5D/NogrCkyRIy", "oucher3-21", region="IT")
try:
    product = amazon.lookup(ItemId="B0016J8AOC")
except Exception, e:
    print(str(e))
else:
    # print(product.title,product.asin)
    item = {'offer_id': product.offer_id, 'quantity': 1}
    cart = amazon.cart_create(item)
    fetched_cart = amazon.cart_get(cart.cart_id, cart.hmac)
    another_product = amazon.lookup(ItemId='0312098286')
    another_item = {'offer_id': another_product.offer_id, 'quantity': 1}
    another_cart = amazon.cart_add(another_item, cart.cart_id, cart.hmac)
    cart_item_id = None
    for item in cart:
        cart_item_id = item.cart_item_id
    modify_item = {'cart_item_id': cart_item_id, 'quantity': 3}
    try:
        modified_cart = amazon.cart_modify(modify_item, cart.cart_id, cart.hmac)
    except Exception, e:
        print str(e)
    else:
        cleared_cart = amazon.cart_clear(cart.cart_id, cart.hmac)

"""








