#!/usr/bin/env python
# -*- coding: utf-8 -*-

import movies

query = movies.Movies.gql('ORDER BY update_date DESC,tweet_count DESC')
first_movie = query.get()
fetched_movies = query.fetch(20)

print '''<html>
<head>
<title>Movitter</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link type="text/css" rel="stylesheet" href="stylesheets/mainpage.css" />
</head>
<body>
<div style="text-align:center;">
<div class="content">

<div class="roundedcornr_box_621317">
<div class="roundedcornr_top_621317"><div></div></div>
<div class="roundedcornr_content_621317">

<p class="logo">
<img src="images/movitter_logo.png" alt="MovitterLogo" border="0">
<br>
twitterをスキャンして現在公開中の映画の評価を集計しています
</p>'''

for fetched_movie in fetched_movies:

  print '<p class="title">'
  print '<a href="http://movie.nifty.com/' + fetched_movie.detail_url.encode('utf-8')  + '" target="_blank" >' + fetched_movie.title.encode('utf-8') +'</a>'
  print '<br>'
  print '<strong>' + str(fetched_movie.tweet_count) + ' tweets</strong>'
  print '</p>'

  print '<p class="chart">'
  if fetched_movie.tweet_count > 0:
    graph_length = 300 * fetched_movie.tweet_count / first_movie.tweet_count
    graph_good = fetched_movie.score_good * 100 / fetched_movie.tweet_count
    graph_bad = fetched_movie.score_bad * 100 / fetched_movie.tweet_count
    graph_other = fetched_movie.score_other * 100 / fetched_movie.tweet_count
    print '<img src="http://chart.apis.google.com/chart?chs=' + str(graph_length) + 'x30&chd=t:' + str(graph_good) + '|' + str(graph_bad) + '|' + str(graph_other) + '&cht=bhs&chco=00FF7F,ff0000,FFD700" alt="chart" border="0">'
    print '<br>'
  print '<span class="chartgood">good:' + str(fetched_movie.score_good) + '</span>/<span class="chartbad">bad:' + str(fetched_movie.score_bad) + '</span>/<span class="chartother">other:' + str(fetched_movie.score_other) + '</span>'
  print '</p>'

  print'<p class="line"></p>'

print '''<div class="footer">
<img src="http://code.google.com/appengine/images/appengine-noborder-120x30.gif" alt="Powered by Google App Engine" />
<br>
This service is created by <a href="http://d.hatena.ne.jp/quill3/" target="_blank" >quill3</a>.
<br>
(Here is <a href="http://github.com/quill3/Movitter" target="_blank" >source code</a> & <a href="http://d.hatena.ne.jp/quill3/archive?word=%2a%5bMovitter%5d" target="_blank" >development log</a>.)
</div>

</div>
<div class="roundedcornr_bottom_621317"><div></div></div>
</div>

</div>
</div>

<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-568420-5");
pageTracker._trackPageview();
} catch(err) {}</script>

</body>
</html>'''