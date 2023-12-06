from typing import List

from pydantic import BaseModel
import xml.etree.ElementTree as et


class Product(BaseModel):
    id: int
    shop_id: int
    price: int
    quantity: int
    name: str
    city_code: int


class Offers(BaseModel):
    offers: List[Product]
    partner_id: int


async def generate_xml(product_data: Offers):

    root = et.Element('kaspi_catalog', date='string', xmlns='kaspiShopping',)
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.set('xsi:schemaLocation', 'kaspiShopping http://kaspi.kz/kaspishopping.xsd')
    company = et.SubElement(root, 'company')
    merchantid = et.SubElement(company, 'merchantid')
    merchantid.text = 'merchantid'

    offers = et.SubElement(company, 'offers')

    for product in product_data.offers:
        offer = et.SubElement(offers, 'offer', sku=str(product.id))
        model = et.SubElement(offer, 'model')
        model.text = product.name
        availabilities = et.SubElement(offer, 'availabilities')
        availability = et.SubElement(availabilities, 'availability', available='yes', storeID=str(product.shop_id))
        cityprices = et.SubElement(offer, 'cityprices')
        cityprice = et.SubElement(cityprices, 'cityprice', cityID='id')
        cityprice.text = product.price

    xml_data = et.tostring(root, encoding='utf-8').decode()
    return xml_data
