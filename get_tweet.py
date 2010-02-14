#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch
import re
import datetime

import movies
import htmlentity2unicode

query = movies.Movies.gql('ORDER BY update_date DESC,check_time ASC')
movie = query.get()

if movie:
  api_url = 'http://search.twitter.com/search.atom?q=' + movie.title.encode('utf-8') + '&locale=ja&since_id=' + movie.since_id.encode('utf-8')
  try:
    result = urlfetch.fetch(api_url)
  except:
    movie.check_time = datetime.datetime.today()
    movie.put()
  else:
    if result.status_code == 200:
      pattern = re.compile(r'<id>tag:search.twitter.com,2005:(.*?)</id>')
      tweet_ids = pattern.findall(result.content)
      if len(tweet_ids) > 1:
        movie.since_id = tweet_ids[1]
        pattern2 = re.compile(r'<title>(.*?)</title>')
        tweet_titles = pattern2.findall(result.content)
        movie.tweet_count = movie.tweet_count + len(tweet_titles) - 1
        for i in range(len(tweet_titles)):
          if i > 0:
            tweet = htmlentity2unicode.htmlentity2unicode(tweet_titles[i]).encode('utf-8')
            pattern_good = re.compile(r'よい|よかった|すごい|すごか|おもしろい|おもしろか|かっこよい|かっこよか|わら|たのしい|たのしめた|たのしか|すばらしい|すばらしか|ヨイ|ヨカッタ|スゴイ|スゴカ|オモシロイ|オモシロカ|カッコヨイ|カッコヨカ|ワラ|タノシイ|タノシメタ|タノシカ|スバラシイ|スバラシカ|グッド|ナイス|良い|良かった|凄い|凄か|面白い|面白か|格好良い|格好良か|笑|楽しい|楽しめた|楽しか|素晴らしい|素晴らしかった|good|nice')
            score_good_result = pattern_good.findall(tweet)
            score_good_point = len(score_good_result)
            pattern_bad = re.compile(r'わるい|わるかった|すごくな|おもしろくな|かっこよくな|わらえな|たのしくな|たのしめな|すばらしくな|しょうも|つまら|ひど|ワルイ|ワルカッタ|スゴクナ|オモシロクナ|カッコヨクナ|ワラエナ|タノシクナ|タノシメナ|スバラシクナ|ショウモ|ツマラ|ヒド|バッド|悪い|悪かった|凄くな|面白くな|格好良くな|笑えな|楽しくな|楽しめな|素晴らしくな|詰まら|酷|bad')
            score_bad_result = pattern_bad.findall(tweet)
            score_bad_point = len(score_bad_result)
            if score_good_point > score_bad_point:
              movie.score_good = movie.score_good + 1
            elif score_good_point < score_bad_point:
              movie.score_bad = movie.score_bad + 1
            else:
              movie.score_other = movie.score_other + 1
      movie.check_time = datetime.datetime.today()
      movie.put()