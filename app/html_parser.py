from bs4 import BeautifulSoup
from typing import List
import requests
from config import vendor_title_ids

def getRawHtml(url: str) -> str:
    headers={"User-Agent":"Defined"}
    response = requests.get(url, headers=headers)
    status_code = response.status_code

    if status_code != 200:
        return [None, f"Status code: {status_code}. Resp: {response.text}"]
    
    html = response.content.decode("utf-8")

    
    return html
    

def extractProductTitle(html: str, vendor: str) -> str:
    vendor_id = vendor_title_ids[vendor]

    soup = BeautifulSoup(html, "html.parser")
    element_by_id=soup.select(vendor_id)
    title = element_by_id[0].text.strip()
    
    return  title

    
def getVendor(url: str) -> str:
    url = url.replace("//", "/")
    domain = url.split("/")[1]

    if "amazon" in domain:
        return "amazon"
    else:
        return None


def getProductTitle(url) -> List[str]:
    try:
        raw_html = getRawHtml(url)
        vendor = getVendor(url)
        
        if vendor == None:
            return [None, f"Not a supported site"]

        product_title = extractProductTitle(raw_html, vendor)

        return [product_title, None]
    
    except Exception as e:
        return [None, f"Error while getting product title: {e}"]
