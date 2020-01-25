'use strict';

var disqus_shortname = 'flagxor';
var disqus_config = {};

(function() {
  var title = document.getElementsByTagName('h1')[0];
  var parts = document.location.href.split('/');
  var ident = parts[parts.length - 2];

  disqus_config.page = {};
  disqus_config.page.identifier = ident;
  disqus_config.page.title = title.innerText;
  disqus_config.page.url = 'https://www.flagxor.com/article/' + ident;

  var s = document.createElement('script');
  s.type = 'text/javascript';
  s.async = true;
  s.src = 'https://' + disqus_shortname + '.disqus.com/embed.js';
  s.setAttribute('data-timestamp', +new Date());
  (document.head || document.body).appendChild(dsq);
})();