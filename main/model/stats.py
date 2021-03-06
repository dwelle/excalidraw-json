# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model


class Stats(model.Base):
  timestamp = ndb.DateProperty(required=True)
  duration = ndb.StringProperty(default='day', required=True, choices=['day', 'week', 'month', 'year'])
  drawings = ndb.IntegerProperty(default=0)
  status = ndb.StringProperty(default='dirty', required=True, choices=['dirty', 'synced', 'syncing'])

  FIELDS = {
    'timestamp': fields.DateTime,
    'duration': fields.String,
    'drawings': fields.Integer,
    'status': fields.String,
  }

  FIELDS.update(model.Base.FIELDS)
