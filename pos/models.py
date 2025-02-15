from parrot.base import BaseModel
        
class Customer(BaseModel):
    """
    This class represents a customer. For now customers don't have access to the
    API, therefore they are not considered users. If functionalities such as 
    online orders or loyalty systems are implemented then Customers should be 
    upgraded to users
    """

    pass

class Order(BaseModel):
    """
    """

    pass

class Product(BaseModel):
    """
    """

    pass

class ProductInstance(BaseModel):
    """
    """

    pass
    