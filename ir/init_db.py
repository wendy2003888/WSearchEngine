# -*- coding:utf-8 -*-

from store import BaseModel, engine
from store.model import *


def init_db():
    BaseModel.metadata.create_all(engine)

def drop_db():
    BaseModel.metadata.drop_all(engine)


drop_db()
init_db()