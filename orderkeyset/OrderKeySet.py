from pydantic.main import BaseModel


class OrderKeySet(BaseModel):
    order_id: int
    dispatcher_key: str
    driver_key: str
    customer_key: str
