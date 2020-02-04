# coding: utf-8

from __future__ import absolute_import

import hashlib
import flask
import flask_restful

from api import helpers
import model
import task

from main import api_v2


@api_v2.resource('/post/', endpoint='api.data.create')
class DrawingCreateAPI(flask_restful.Resource):
  def post(self):
    data = flask.request.get_data()
    m = hashlib.md5()
    m.update(data)
    drawing_hash = m.hexdigest()
    drawing_db = model.Drawing.get_by('hash', drawing_hash)
    if not drawing_db:
      drawing_db = model.Drawing(hash=drawing_hash, data=data)
    drawing_db.put()
    task.task_calculate_stats(drawing_db.created)

    return flask.jsonify(
      id=drawing_db.key.id(),
      data=flask.url_for('api.data.id', drawing_id=drawing_db.key.id(), _external=True),
    )


@api_v2.resource('/<int:drawing_id>', endpoint='api.data.id')
class DrawingHashAPI(flask_restful.Resource):
  def get(self, drawing_id):
    drawing_db = model.Drawing.get_by_id(drawing_id)
    if not drawing_db:
      helpers.make_not_found_exception('Drawing %s not found' % drawing_id)

    response = flask.make_response(drawing_db.data)
    response.headers.set('Content-Type', 'application/octet-stream')
    return response
