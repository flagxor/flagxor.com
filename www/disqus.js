'use strict';

(function() {
  var title = document.getElementsByTagName('h1')[0];
  var parts = document.location.href.split('/');

  var disqus_shortname = 'flagxor';
  var disqus_identifier = parts[parts.length - 2];
  var disqus_title = title.innerText;
  var disqus_url = 'http://flagxor.com/' + disqus_identifier;
  var dsq = document.createElement('script');
  dsq.type = 'text/javascript';
  dsq.async = true;
  dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
  (document.getElementsByTagName('head')[0] ||
   document.getElementsByTagName('body')[0]).appendChild(dsq);
})();
