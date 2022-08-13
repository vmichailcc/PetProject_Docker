import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet.settings')
django.setup()

import requests
import json
from store.models import Product, Pictures
from pet.hidden_data import auth_data
from celery import shared_task


@shared_task
def data_input():
    response = {}
    auth_url = "https://office.hubber.pro/api/v1/auth"
    url_response = requests.get(url=auth_url, auth=auth_data).json()
    token = url_response['token']
    headers = {
        'Authorization': f"Bearer {token}",
        "accept-language": "uk-UA",
    }
    product_url = "http://office.hubber.pro/ru/api/v1/product/index?page=1&limit=100"
    product_response = requests.get(url=product_url, headers=headers)
    pagination_page_number = int(product_response.headers['x-pagination-page-count'])

    count = 0
    page_number = 1
    if page_number <= pagination_page_number:
        try:
            product_url = f"http://office.hubber.pro/ru/api/v1/product/index?page={page_number}&limit=100"
            page_number += 1
            product_response = requests.get(url=product_url, headers=headers)
            products_response = product_response.json()
            upload_data_str = json.dumps(products_response)
            upload_data = json.loads(upload_data_str)
            for data in upload_data:
                if data.get("name") is not None:
                    product = Product(
                        id=data.get("id"),
                        name=data.get("name"),
                        category=data.get("category_name"),
                        vendor_code=data.get("vendor_code"),
                        price=data.get("price"),
                        old_price=data.get("old_price"),
                        availability=data.get("availability"),
                        main_picture_url=data.get("main_picture"),
                        description=data.get("description"),
                        brand=data.get("brand"),
                        options=data.get("options"),
                        attributes=data.get("attributes"),
                    )
                    product.save()
                    count += 1
                for input_image in data.get("pictures"):
                    image = Pictures(
                        pictures_point=product,
                        pictures=input_image,
                    )
                    image.save()
            # else:
            #     continue
        except ValueError:
            raise "Data input error!"
        response['status'] = product_response.status_code
        response['message'] = 'error'
        response['count'] = count
    else:
        response['status'] = product_response.status_code
        response['message'] = 'success'
        response['count'] = count
    print(response)


@shared_task
def delete_data():
    data = Product.objects.filter(availability=0).delete()
    print(data)
