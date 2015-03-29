package flagxor

import (
	"html/template"
	"net/http"

	"appengine"
)

func init() {
	http.HandleFunc("/", handleMainPage)
}

var mainPage = template.Must(template.New("guestbook").Parse(
	`<html>
<body>
Testing.
</body>
</html>
`))

func handleMainPage(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" || r.URL.Path != "/" {
		http.NotFound(w, r)
		return
	}
	c := appengine.NewContext(r)
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	if err := mainPage.Execute(w, nil); err != nil {
		c.Errorf("%v", err)
	}
}
