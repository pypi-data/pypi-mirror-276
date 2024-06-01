from pydantic import BaseModel


class City(BaseModel):
    city_id: int
    name: str
    population: int


input = """
{
"city_id": 777,
"name": "New York",
"population": 8000000
}
"""

city = City.model_validate_json(input)

