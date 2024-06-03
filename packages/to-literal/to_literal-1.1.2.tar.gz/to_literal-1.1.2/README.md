# To_literal

Is a micro librery to use it with pydantic, we can do now convert Literal[] to simple array in python, or reverse in a simple way.

Repository:
![Static Badge](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge&logo=GitHub&logoColor=%23ffffff&label=LINK&color=white&link=https%3A%2F%2Fgithub.com%2FHarryEddward%2Fto_literal%3Ftab%3Dreadme-ov-file)


## Why i do it?

I'm still doing a RestAPI with FastAPI with React Native, and when you need to obtain from your database with nosql an array, you can't convert in the simplest way array to Literal[] and you can't validate data in a flexible way. To save before data an after apply to your new values to use it, from your database to validate with Pydantic.


## How to use it

```python
from pydantic import BaseModel
from to_literal.v1 import toLiteral

hoursL = toLiteral([
    '9:00',
    '9:30',
])

class testLiteral(BaseModel):
    hours: hoursL


#   Good Example:

test = testLiteral(hours='9:30')
print(test.model_dump())

#   Result:
#   { 
#       'hours': '9:30'
#   }



#   Bad Example -> ERROR:

test = testLiteral(hours='10:30')
print(test.model_dump())

```