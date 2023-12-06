from typing import List

from pydantic import BaseModel
import xml.etree.ElementTree as ET


class Product(BaseModel):
    id: int
    shop_id: int
    price: int
    quantity: int
    name: str
    city_code: int


class Offers(BaseModel):
    offers: List[Product]


class PartnerId(BaseModel):
    partner_id: int


async def generate_xml(product_data: Offers):
    root = ET.Element('kaspi_catalog', date='string', xmlns='kaspiShopping')
    company = ET.SubElement(root, 'company')
    merchantid = ET.SubElement(company, 'merchantid')

    offers = ET.SubElement(company, 'offers')
    for product in product_data.offers:
        offer = ET.SubElement(offers, 'offer', sku=str(product.id))

        model = ET.SubElement(offer, 'model')
        model.text = product.name

    xml_data = ET.tostring(root, encoding='utf-8').decode()
    return xml_data
