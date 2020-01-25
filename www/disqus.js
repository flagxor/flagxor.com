'use strict';

var disqus_config = function() {
  var title = document.getElementsByTagName('h1')[0];
  var parts = document.location.href.split('/');
  var ident = parts[parts.length - 2];
  this.shortname = 'flagxor';
  this.page.identifier = ident;
  this.page.title = title.innerText;
  this.page.url = 'https://www.flagxor.com/article/' + ident;
};

(function() {
  var s = document.createElement('script');
  s.type = 'text/javascript';
  s.async = true;
  s.src = 'https://flagxor.disqus.com/embed.js';
  s.setAttribute('data-timestamp', +new Date());
  (document.head || document.body).appendChild(s);
})();
