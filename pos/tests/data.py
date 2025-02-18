USER_PAYLOAD={
    "username": "gus",
    "first_name": "Gustavo",
    "last_name": "Delgado",
    "email": "gustavo@parrot.com",
    "password": "Password1",
}

USER_RESPONSE = {
    "username": "gus",
    "first_name": "Gustavo",
    "last_name": "Delgado",
    "email": "gustavo@parrot.com",
}

USERLIST_RESPONSE = [{
    "username": "user1",
    "first_name": "",
    "last_name": "",
    "email": "",

},
{
    "username": "gus",
    "first_name": "Gustavo",
    "last_name": "Delgado",
    "email": "gustavo@parrot.com",
}]

ORDER_PAYLOADS=[
    {
    "customer_name": "Uri",
    "products": [
        {
        "name": "Fanta",
        "details":[{
            "price": "1500.83",
            "quantity": "90"
        }]
        },
        {
        "name": "Papas",
        "details":[{
            "price": "1200.40",
            "quantity": "22"
        }]
        },
        {
        "name": "Limonada",
        "details":[{
            "price": "45.12",
            "quantity": "9"
    }]
        }
    ]
    },
    {
    "customer_name": "Georgina",
    "products": [
        {
        "name": "Hamburguesa",
        "details":[{
            "price": "243.83",
            "quantity": "3"
        }]
        },
        {
        "name": "Papas",
        "details":[{
            "price": "1200.40",
            "quantity": "22"
        }]
        },
        {
        "name": "Fanta",
        "details":[{
            "price": "40",
            "quantity": "5"
    }]
        }
    ]
    },
    {
    "customer_name": "Carlos",
    "products": [
        {
        "name": "Fanta",
        "details":[{
            "price": "1500.83",
            "quantity": "90"
        }]
        },
        {
        "name": "Papas",
        "details":[{
            "price": "1200.40",
            "quantity": "22"
        }]
        },
        {
        "name": "Limonada",
        "details":[{
            "price": "45.12",
            "quantity": "9"
    }]
        }
    ]
    },
]

ORDER_RESPONSES = [
    {
    "customer_name": "Uri",
    "total": 161889.58,
    "products": [
        {
        "name": "Fanta",
        "details":[{
            "price": "1500.83",
            "quantity": "90"
        }]
        },
        {
        "name": "Papas",
        "details":[{
            "price": "1200.40",
            "quantity": "22"
        }]
        },
        {
        "name": "Limonada",
        "details":[{
            "price": "45.12",
            "quantity": "9"
    }]
        }
    ]
    },
    {
    "customer_name": "Georgina",
    "total": 27340.29,
    "products": [
        {
        "name": "Hamburguesa",
        "details":[{
            "price": "243.83",
            "quantity": "3"
        }]
        },
        {
        "name": "Papas",
        "details":[{
            "price": "1200.40",
            "quantity": "22"
        }]
        },
        {
        "name": "Fanta",
        "details":[{
            "price": "40",
            "quantity": "5"
    }]
        }
    ]
    },
    {
    "customer_name": "Carlos",
    "total": 161889.58,
    "products": [
        {
        "name": "Fanta",
        "details":[{
            "price": "1500.83",
            "quantity": "90"
        }]
        },
        {
        "name": "Papas",
        "details":[{
            "price": "1200.40",
            "quantity": "22"
        }]
        },
        {
        "name": "Limonada",
        "details":[{
            "price": "45.12",
            "quantity": "9"
    }]
        }
    ]
    },
]

ORDER_ERROR_PAYLOADS=[
    {
    "customer_name": "Uri",
    "products": [
        {
        "name": "Fanta",
        "details":[{
            "price": "****",
            "quantity": "90"
        }]
        },
        {
        "name": "Papas",
        "details":[{
            "price": "1200.40",
            "quantity": "22"
        }]
        },
        {
        "name": "Limonada",
        "details":[{
            "price": "45.12",
            "quantity": "9"
    }]
        }
    ]
    },
    {
    "customer_name": "Georgina",
    "products": [
        {
        "name": "Hamburguesa",
        "details":[{
            "price": "243.83",
            "quantity": "3.23"
        }]
        },
        {
        "name": "Papas",
        "details":[{
            "price": "1200.40",
            "quantity": "22"
        }]
        },
        {
        "name": "Fanta",
        "details":[{
            "price": "40",
            "quantity": "5"
    }]
        }
    ]
    },
    {
    "customer_name": "Carlos",
    "products": [
        {
        "name": "Fanta",
        "details":[{
            "price": "1500.83",
            "quantity": "90"
        }]
        },
        {
        "name": "////",
        "details":[{
            "price": "1200.40",
            "quantity": "22"
        }]
        },
        {
        "name": "Limonada",
        "details":[{
            "price": "a45.12",
            "quantity": "9"
    }]
        }
    ]
    },
]

REPORT_RESPONSE = [
    {
        "product_name": "Fanta",
        "quantity_sold": 185,
        "total_price": "270349.40"
    },
    {
        "product_name": "Papas",
        "quantity_sold": 66,
        "total_price": "79226.40"
    },
    {
        "product_name": "Limonada",
        "quantity_sold": 18,
        "total_price": "812.16"
    },
    {
        "product_name": "Hamburguesa",
        "quantity_sold": 3,
        "total_price": "731.49"
    }
]