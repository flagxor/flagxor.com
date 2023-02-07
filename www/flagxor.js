'use strict';

function AddMeta(head, name, content) {
  var meta = document.createElement('meta');
  meta.name = name;
  meta.content = content;
  head.appendChild(meta)
  return meta;
}

function AddLink(head, rel, type, href) {
  var link = document.createElement('link');
  link.rel = rel;
  link.type = type;
  link.href = href;
  head.appendChild(link);
  return link;
}

function AddAnchor(e, target, href, text) {
  var anchor = document.createElement('a');
  anchor.target = target;
  anchor.href = href;
  anchor.innerText = text;
  e.appendChild(anchor);
  return anchor;
}

function AddDiv(e, id, kind) {
  var div = document.createElement('div');
  if (id) {
    div.id = id;
  }
  if (kind) {
    div.classList.add(kind);
  }
  e.appendChild(div);
  return div;
}

function AddScript(e, src) {
  var script = document.createElement('script');
  script.src = src;
  e.appendChild(script);
  return script;
}

function AddImg(e, width, height, src) {
  var img = document.createElement('img');
  img.width = width;
  img.height = height;
  img.src = src;
  e.appendChild(img);
  return img;
}

function SetupPage() {
  // Setup head.
  var head = document.getElementsByTagName('HEAD')[0];
  AddLink(head, 'stylesheet', 'text/css',
      'https://www.flagxor.com/static/flagxor.css');
  AddLink(head, 'SHORTCUT ICON', 'image/x-icon',
      'https://www.flagxor.com/favicon.ico');
  AddLink(head, 'apple-touch-icon-precomposed', 'image/png',
      'https://www.flagxor.com/favicon.png');
  AddMeta(head, 'viewport', 'width=600');
  AddMeta(head, 'viewport', 'initial-scale=1.0');
  AddMeta(head, 'apple-mobile-web-app-capable', 'yes');
  AddMeta(head, 'apple-mobile-web-app-status-bar-style', 'black-translucent');
  AddMeta(head, 'X-UA-Compatible', 'chrome=1');
  // Hide main.
  var main = document.getElementById('main');
  main.style.display = 'none';
  // Add loading.
  document.body.style.color = '#fff';
  document.body.style.backgroundColor = '#000';
  var loading = document.createTextNode('Loading...');
  document.body.appendChild(loading);
  // Build wrapped page.
  var wrapper = AddDiv(document.body, 'wrapper', null);
  window.onload = function() {
    // Setup title.
    var header = AddDiv(wrapper, 'header', null);
    var img = AddImg(header, 40, 40,
        'https://www.flagxor.com/static/4spire.png');
    img.align = 'right';
    var title = document.getElementsByTagName('h1')[0];
    document.title = title.innerText;
    title.parentElement.removeChild(title);
    header.appendChild(title);
    // Gather up article.
    var section = AddDiv(wrapper, null, 'section');
    var article = AddDiv(section, null, 'article');
    article.appendChild(main);
    main.style.display = '';
    // Add footer.
    var footer = AddDiv(wrapper, 'footer', null);
    var links = AddDiv(footer, null, 'links');
    AddAnchor(links, '_parent', '/', 'Home');
    AddAnchor(links, '_parent',
        'https://forthsalon.appspot.com/', 'Forth Haiku');
    // Drop loading.
    document.body.removeChild(loading);
  }
}

SetupPage();
