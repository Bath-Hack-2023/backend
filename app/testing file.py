from backend.app.chat_gpt import extractInfoMultiple
from backend.app.ditch_carbon import getCarbonDataMultiple
from backend.app.rainforest import getRecommendations

productID = "B0B6G1W3LK"  # Get this from the product URL!
similar_products = getRecommendations(productID)
print(similar_products)
if isinstance(similar_products[0], int):  # check the rating is in the array
    rating = similar_products[0]
if similar_products[1] != False:
    # We know recommendations[1] is the array
    del similar_products[0]
    similar_products_extract = extractInfoMultiple([i[0] for i in similar_products])
    similar_products_carbon = getCarbonDataMultiple(similar_products_extract)
    print(similar_products_carbon)
