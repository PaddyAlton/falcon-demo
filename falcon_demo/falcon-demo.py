# falcon-demo.py
# testing out what we can do with the Falcon API framework

import falcon

from dotenv import load_dotenv

from falcon_autocrud.middleware import Middleware
from falcon_autocrud.resource import CollectionResource, SingleResource

from os import getenv

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from waitress import serve


### Database Stuff
Base = automap_base()

load_dotenv(".env")
db_path = getenv("DB_PATH")

engine = create_engine(f"sqlite:///{db_path}")

Base.prepare(engine, reflect=True)
tables = Base.classes.keys()
Employee = Base.classes.Employee


### falcon-autocrud stuff
class EmployeeCollectionResource(CollectionResource):
    model = Employee


class EmployeeResource(SingleResource):
    model = Employee


### falcon stuff
app = falcon.API(middleware=[Middleware()])

app.add_route("/employees", EmployeeCollectionResource(engine))
app.add_route("/employees/{id}", EmployeeResource(engine))


if __name__ == "__main__":

    # start the server
    serve(app, port=5000)
