# coding: utf-8

from __future__ import absolute_import

import json
import hashlib
import flask
import flask_restful
from flask_restful import reqparse

from api import helpers
import model

from main import api_v1

parser = reqparse.RequestParser()
parser.add_argument('json')


@api_v1.resource('/<string:drawing_hash>/', endpoint='api.create')
class DrawingCreateAPI(flask_restful.Resource):
  def post(self, drawing_hash):
    drawing_db = model.Drawing.get_by('hash', drawing_hash)
    if drawing_db:
      return flask.jsonify(drawing_db.json)
    try:
      drawing_json = json.loads(flask.request.data)
      import logging
      logging.info('########################## %r' % flask.request.data)
      m = hashlib.md5()
      m.update(str(drawing_json))
      if m.hexdigest() != drawing_hash:
        helpers.make_not_found_exception('Not a valid hash for that JSON (%s)' % m.hexdigest())
      else:
        drawing_db = model.Drawing(hash=drawing_hash, json=drawing_json)
        drawing_db.put()
    except (ValueError, AssertionError):
      helpers.make_not_found_exception('Not valid JSON')

    return flask.jsonify(drawing_db.json)



@api_v1.resource('/<string:drawing_hash>.json', endpoint='api.hash')
class DrawingHashAPI(flask_restful.Resource):
  def get(self, drawing_hash):
    drawing_db = model.Drawing.get_by('hash', drawing_hash)
    if not drawing_db:
      helpers.make_not_found_exception('Drawing %s not found' % drawing_hash)
    return flask.jsonify(drawing_db.json)
