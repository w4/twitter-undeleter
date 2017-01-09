import datetime

import settings
from peewee import *


class BaseModel(Model):
    class Meta:
        database = settings.database


class Tracking(BaseModel):
    added_at = DateTimeField(null=True)
    added_by = TextField(null=True)
    id = UUIDField(primary_key=True)
    twitter = TextField(db_column='twitter_id', null=True, unique=True)

    class Meta:
        db_table = 'tracking'


class Tweet(BaseModel):
    id = TextField(primary_key=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    deleted_at = DateTimeField(null=True)
    tweet = TextField(null=True)
    twitter = TextField(db_column='twitter_id', null=True)

    class Meta:
        db_table = 'tweets'

