# REST-API-Practice
Brushing up skills in REST APIs and HATEOAS

Will use FastAPI for backend endpoints and Postgres for DB, SQLAlchemy for ORM

To install - `poetry install`, assuming you have poetry installed

---
Writeup:

Progress:

- First I poetry install the required packages of `fastapi`, `alembic` , `sqlalchemy`
- Then I run `alembic init` to generate the alembic directory
- After that I create the necessary files
- This is the resulting direcotry structure:

```jsx
venvfss@Fatehs-MacBook-Air REST-API-Practice % tree -L 2 -I venv   
.
├── README.md
├── alembic
│   ├── README
│   ├── __pycache__
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── alembic.ini
├── app
│   ├── __init__.py
│   ├── __pycache__
│   ├── crud.py 
│   ├── database.py # define the db connection string and SQLalchemy Base that Alembic uses and models.py inherit from
│   ├── models.py # deine the models (tables in our db) in sqlalchemy fashion
│   ├── routes
│   ├── schemas.py
│   └── server.py
├── db.sqlite
├── main.py
├── poetry.lock
└── pyproject.toml
```

- Now I fill in the database and models files, creating my tables for the db and the db connection string and getter functions
- Then I go to the `alembic/env.py` file to import the `Base` from `app/database.py` and set that as the `target_metadata`, also import the `SQLALCHEMY_DATABASE_URL` value from `app/database.py` and set the sqlalchemy url to it in the config
- After this I run `alembic revision --autogenerate -m "Initial migration”` to migrate the tables into my db
    - for some reason it didn’t work after I connected to the `db.sqlite` file that it made - the tables didn’t show up. This worked though: `alembic upgrade head`
- Now I fill in the [`schemas.py`](http://schemas.py) file, where I note that this file is to define Pydantic models for our API routes and is not related to SQLAlchemy in any way
- I also note that password hashing must be done in the endpoint by some hashing algorithm before it’s stored in the database. It shouldn’t be done in the frontend or the database. There’s no SecureString class in SQLAlchemy for our db models, it’s just stored as a string which should be hashed before insertion.
    - Confusion arises in [schemas.py](http://schemas.py) because I’m not sure whether I’m supposed to maintain one pydantic model for the **request** and **response** models simulataneously. For instance, if one were to do GET /user/id then the input model should just have an ID, whereas the response model should have name, email, and id. Therefore I see that there should be separate models for a request and a response. In fact for GET /user/{id} there doesn’t even need to be a pydantic model for request validation because the only piece of data the request needs in the id which is already in the endpoint.
- I realize here that since I’m defining API routes which was the point of this exercise I should fully sketch out my REST API before writing any more code.
    - I now note that it’s confusing to create a route that gets all the orders for a user.
        - Will it be `/user/{id}/orders` or `/orders?user_id={id}` ?
        - The answer is that many APIs support both and these endpoints are for different purposes - the first would be for one specific user while the second would allow for greater control such as ordering, filtering, and so on.
    - One realization is that base endpoint should be **plural** not singluar - /users instead of /user
    - As I do this exercise it becomes apparent that adding HATEOAS-style links for each endpoint is cumbersome and time-consuming
        - I read this off-topic article discussing hateoas happening organically with htmx: https://medium.com/@strasbourgwebsolutions/fastapi-as-a-hypermedia-driven-application-w-htmx-jinja2templates-644c3bfa51d1
        - I think that I can get around this by a clever solution of adding tags to urls and resources and descriptions of query params. but this can wait for now.
        - in fact even defining query params can wait until after I define all routes first. responses should only go one level deep - users/{id}/orders should return only orders and not all the products under orders; there will be a query param for that later if needed. I can generalize this to all similar endpoints for now

Created first draft of API routes, excluding HATEOAS links and query params for now:


![image](https://github.com/user-attachments/assets/967e9120-af9f-4da9-8e54-ca3c4bd87d59)


_____

March 9 2025

- picking up where I left off yesteday, I will implement each endpoint now
- I quickly implement the /users api
    - now want to test it out so I will import the collection into postman
        - I do this by `curl http://localhost:8000/openapi.json -o openapi.json` into import in postman
    - looks good for user crud
    - I now realize that I need to validate username, password, and email to prevent bullshit values
    - I implement this using simple validator functions in the endpoints (pydantic validation was too awkward to work with when using SQLAlchemy syntax - first validate in pydantic and then cast into sqlalchemy model??)
- will do the same for others
- was thinking about my return classes and whether I should just return the db value or a custom class. I decided that a custom class is better since then I can add links and other hateoas things in a customizable way. maybe I’ll add query params to the get response classes too and then in the `__init__(self)` method do something to create lists? idk
- got sidetracked for 45 minutes trying to make a pre commit hook that would update the openapi.json automatically upon commit… what a waste of time

While creating the implementation for POST /order I had a question:

- if Order class has total_price and order_items need an order ID to be inserted except Order also needs a total price how do I do this?
    - The solution is to use `db.add(new_order)` followed by `db.flush()` so that the database assigns an order_id but doesn’t commit it just yet
    - Without `db.flush()` there is no order id for the order items
    - Here is the elegant solution by Cursor:
    
    ```jsx
    @router.post("/orders")
    async def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
        # Start a transaction
        try:
            # Calculate total price from items first
            total_price = sum(item.price * item.quantity for item in order_data.items)
            
            # Create order with correct total price
            new_order = Order(
                user_id=order_data.user_id,
                total_price=total_price,
                status="pending"
            )
            db.add(new_order)
            db.flush()  # This assigns an ID without committing
            
            # Create order items
            for item in order_data.items:
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_at_purchase=item.price
                )
                db.add(order_item)
            
            # Commit everything at once
            db.commit()
            return new_order
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    ```
