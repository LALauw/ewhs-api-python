import pytest
from ewhs.exceptions import BadRequest


ORDER_ID = "94dbdb91-87ac-4634-b77d-e126a6206b15"


def test_get_order(authenticated_client, response):
    """Retrieve a single order by order ID."""
    response.get(f"https://eu.middleware.ewarehousing-solutions.com/wms/orders/{ORDER_ID}/", "order_single")

    order = authenticated_client.order.get(ORDER_ID)
    assert isinstance(order, dict)

    assert order['id'] == ORDER_ID
    assert order['external_reference'] == 'ORD001'
    assert order['address'] == {
        'street': 'Nijverheidsweg'
    }


def test_list_orders(authenticated_client, response):
    """Retrieve a list of orders"""
    response.get(f"https://eu.middleware.ewarehousing-solutions.com/wms/orders/", "order_list")

    orders = authenticated_client.order.list()
    assert isinstance(orders, list)

    assert len(orders) == 2

    assert orders[0]['id'] == ORDER_ID
    assert orders[0]['external_reference'] == 'ORD001'
    assert orders[0]['address'] == {
        'street': 'Nijverheidsweg'
    }

    assert orders[1]['external_reference'] == 'ORD002'
    assert orders[1]['address'] == {
        'street': 'Nijverheidsweg'
    }


def test_filer_orders(authenticated_client, response):
    """Retrieve a list of orders"""
    response.get(f"https://eu.middleware.ewarehousing-solutions.com/wms/orders/?status=created", "order_list")

    orders = authenticated_client.order.list(
        params={'status': 'created'}
    )

    assert isinstance(orders, list)


def test_create_order(authenticated_client, response):
    """Create an order."""
    response.post(f"https://eu.middleware.ewarehousing-solutions.com/wms/orders/", "order_single")

    data = {
        "note": "Testorder",
        "customer": "53b5a543-129a-403c-9a6e-3d9c525ffa5b",
        "order_lines": [
            {
                "quantity": 7,
                "description": "Voorbeeldproduct-B",
                "variant": "default_variant_b_id"
            },
            {
                "quantity": 15,
                "description": "Voorbeeldproduct-A",
                "variant": "default_variant_a_id"
            }
        ],
        "shipping_email": "test@ewarehousing.nl",
        "shipping_method": None,
        "shipping_address": {
            "city": "Heinenoord",
            "state": "ZH",
            "street": "Nijverheidsweg",
            "country": "NL",
            "street2": None,
            "zipcode": "3274 KJ",
            "fax_number": None,
            "addressed_to": None,
            "phone_number": "0186 612 267",
            "mobile_number": "",
            "street_number": 27,
            "street_number_addition": ""
        },
        "external_reference": "ORD001",
        "requested_delivery_date": "2018-11-19"
    }
    order = authenticated_client.order.create(data)
    assert isinstance(order, dict)
    assert order['id'] == ORDER_ID


def test_update_order(authenticated_client, response):
    """Update an order."""
    response.patch("https://eu.middleware.ewarehousing-solutions.com/wms/orders/94dbdb91-87ac-4634-b77d-e126a6206b15/", "order_single")

    data = {
        "note": "Testorder",
        "customer": "53b5a543-129a-403c-9a6e-3d9c525ffa5b",
        "order_lines": [
            {
                "quantity": 7,
                "description": "Voorbeeldproduct-B",
                "variant": "default_variant_b_id"
            },
            {
                "quantity": 15,
                "description": "Voorbeeldproduct-A",
                "variant": "default_variant_a_id"
            }
        ],
        "shipping_email": "test@ewarehousing.nl",
        "shipping_method": None,
        "shipping_address": {
            "city": "Heinenoord",
            "state": "ZH",
            "street": "Nijverheidsweg",
            "country": "NL",
            "street2": None,
            "zipcode": "3274 KJ",
            "fax_number": None,
            "addressed_to": None,
            "phone_number": "0186 612 267",
            "mobile_number": "",
            "street_number": 27,
            "street_number_addition": ""
        },
        "external_reference": "ORD001",
        "requested_delivery_date": "2018-11-19"
    }
    order = authenticated_client.order.update(ORDER_ID, data)
    assert isinstance(order, dict)
    assert order['id'] == ORDER_ID


def test_bad_request(authenticated_client, response):
    """Test a bad request."""
    response.patch("https://eu.middleware.ewarehousing-solutions.com/wms/orders/94dbdb91-87ac-4634-b77d-e126a6206b15/",
                   "bad_request",
                   status=400
                   )

    data = {
        "note": "Testorder",
        "customer": "53b5a543-129a-403c-9a6e-3d9c525ffa5b",
        "order_lines": [
            {
                "quantity": 7,
                "description": "Voorbeeldproduct-B",
                "variant": "default_variant_b_id"
            },
            {
                "quantity": 15,
                "description": "Voorbeeldproduct-A",
                "variant": "default_variant_a_id"
            }
        ],
        "shipping_email": "test@ewarehousing.nl",
        "shipping_method": None,
        "shipping_address": {
            "city": "Heinenoord",
            "state": "ZH",
            "street": "Nijverheidsweg",
            "country": "NL",
            "street2": None,
            "zipcode": "3274 KJ",
            "fax_number": None,
            "addressed_to": None,
            "phone_number": "0186 612 267",
            "mobile_number": "",
            "street_number": 27,
            "street_number_addition": ""
        },
        "external_reference": "ORD001",
        "requested_delivery_date": "2018-11-19"
    }

    with pytest.raises(BadRequest):
        try:
            authenticated_client.order.update(ORDER_ID, data)
        except BadRequest as e:
            assert e.errors == {
                  "errors": {
                    "0": "Reference is not unique",
                    "externalReference": [
                      "Reference is not unique"
                    ]
                  }
                }
            raise e
