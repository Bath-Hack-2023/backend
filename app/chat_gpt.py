import openai
import re

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
                                                          "content": productNames}])

        print(response)
        return response.choices[0].message.content.split("\n")

    except Exception as e:
        print(e)
        return None


# When given a product name, returns an array of the estimates of the carbon footprint in kgs(?). May
# return None.
def getCarbonInfoOne(productName):
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
                                                              "content": productName}])
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



