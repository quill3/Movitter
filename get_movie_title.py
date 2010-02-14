#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db
from google.appengine.api import urlfetch
import re
import datetime

import movies

result = urlfetch.fetch('http://movie.nifty.com/cs/movie/list/1.htm')
if result.status_code == 200:
  pattern = re.compile(r'<span class="item"><a href="(.*?)">(.*?)</a>')
  movie_titles = pattern.findall(result.content)
  for movie_title in movie_titles:
    movie_title_u = unicode(movie_title[1],'Shift_JIS')
    query = movies.Movies.gql('WHERE title = :title',title=movie_title_u)
    movie = query.get()
    if movie:
      movie.update_date = datetime.date.today()
    else:
      movie = movies.Movies()
      movie.title = movie_title_u
      movie.detail_url = movie_title[0]
      movie.update_date = datetime.date.today()
      movie.check_time = datetime.datetime.today()
      movie.tweet_count = 0
      movie.score_good = 0
      movie.score_bad = 0
      movie.score_other = 0
      movie.since_id = '0'
    movie.put()