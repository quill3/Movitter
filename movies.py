#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Movies(db.Model):
  title = db.StringProperty()
  detail_url = db.StringProperty()
  create_date = db.DateProperty(auto_now_add=True)
  update_date = db.DateProperty()
  check_time = db.DateTimeProperty()
  tweet_count = db.IntegerProperty()
  score_good = db.IntegerProperty()
  score_bad = db.IntegerProperty()
  score_other = db.IntegerProperty()
  since_id = db.StringProperty()