import openai

# Put key in env file.
openai.api_key = "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"


# When given a product title, returns the product name and manufacturer. May return None.
def extractInfoOne(productTitle):
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=[{"role": "system",
                                                           "content": "From now on, I will give you a product title. "
                                                                      "Return the product name and the manufacturer, "
                                                                      "split by a comma."},
                                                          {
                                                              "role": "user",
                                                              "content": productTitle}])

        return response.choices[0].message.content.split(",")

    except Exception as e:
        return None


# When given an array of product titles, returns the product names and manufacturers as an array. May return None.
def extractInfoMultiple(productTitles):
    pass


# When given a product title, returns an array of the estimates of the carbon footprint in kgs(?). May
# return None.
def getCarbonInfo(productTitle):
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=[{"role": "system",
                                                           "content": "From now on, I will give you a product title. "
                                                                      "Return the carbon footprint in kgs and nothing else."},
                                                          {
                                                              "role": "user",
                                                              "content": productTitle}])
        return response
    except Exception as e:
        return None


print(extractInfoOne("Apple iPhone 13 (128GB) - Midnight"))
