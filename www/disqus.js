'use strict';

var disqus_shortname = 'flagxor';
var disqus_identifier;
var disqus_title;
var disqus_url = 'https://www.flagxor.com/article/' + disqus_identifier;

(function() {
  var title = document.getElementsByTagName('h1')[0];
  var parts = document.location.href.split('/');

  disqus_identifier = parts[parts.length - 2];
  disqus_title = title.innerText;

  var dsq = document.createElement('script');
  dsq.type = 'text/javascript';
  dsq.async = true;
  dsq.src = 'https://' + disqus_shortname + '.disqus.com/embed.js';
  (document.getElementsByTagName('head')[0] ||
   document.getElementsByTagName('body')[0]).appendChild(dsq);
})();
