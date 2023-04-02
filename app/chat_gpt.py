import openai
import re
import config

# Put key in env file.
openai.api_key = config.open_ai_creds


# When given a product title, returns the product name and manufacturer. May return None.
def extractInfoOne(productTitle):
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=[{"role": "system",
                                                           "content": "From now on, I will give you a product title. "
                                                                      "Return the product name and then the manufacturer, "
                                                                      "split by a comma."},
                                                          {
                                                              "role": "user",
                                                              "content": productTitle}],
                                                temperature = 0.1
                                                              )

        return response.choices[0].message.content.split(",")

    except Exception as e:
        return None


# When given an array of product names, returns the product names and manufacturers as an array. May return None.
def extractInfoMultiple(productNames):
    productNames = str(productNames)
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=[{"role": "system",
                                                           "content": "From now on, I will give you a list of product titles. "
                                                                      "For each, return the product name and the manufacturer, "
                                                                      "split by a comma."},
                                                          {"role": "user",
                                                          "content": productNames}],
                                                          temperature = 0.2)
                                                

        #print(response)
        return response.choices[0].message.content.split("\n")

    except Exception as e:
        print(e)
        return None


# When given a product name and product manufacturer, returns an array of the estimates of the carbon footprint in kgs(?). May
# return None.
def getCarbonInfoOne(productName, productManu):
    product = f'{productManu} {productName}'
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                temperature=0.1,
                                                messages=[{"role": "system",
                                                           "content": "From now on, I will give you a product "
                                                                      "title."
                                                                      "Return the carbon emissions "
                                                                      "of its life cycle in kg CO2e, and no other words."},
                                                          {
                                                              "role": "user",
                                                              "content": product}])
        return response.choices[0].message.content
    except Exception as e:
        return None


# When given a product name, returns an array of the estimates of the carbon footprint in kgs(?). May
# return None.
def getCarbonInfoMultiple(productNames):
    productNames = str(productNames)
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                temperature=0.1,
                                                messages=[{"role": "system",
                                                           "content": "From now on, I will give you a list of product "
                                                                      "titles."
                                                                      "Return the carbon emissions "
                                                                      "of its life cycle in kg CO2e for each, split "
                                                                      "by commas, and no other words. "},
                                                          {
                                                              "role": "user",
                                                              "content": productNames}])

        response = response.choices[0].message.content
        response = re.split(': |,', response)

        i = 1
        result = []
        while(i<len(response)):
            result.append(response[1])
            i+=2
        return result
    except Exception as e:
        return None


def getCarbonInfoManuGPT(manu):
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                temperature=0.4,
                                                messages=[{"role": "system",
                                                           "content": "From now on, I will give you a manufacturer. "
                                                                      "Return its total carbon emissions over all "
                                                                      "time in kilograms CO2e and no other words. "},
                                                          {
                                                              "role": "user",
                                                              "content": manu}])

        return response.choices[0].message.content

    except Exception as e:
        return None
