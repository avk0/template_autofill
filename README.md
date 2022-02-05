# template_autofill
This is a [web service](http://129.151.204.37:5000/) that fills PPTX template with Excel data. \
Output is filled separate presentations and one filled joint presentation. \
Written on Flask, python-pptx.

---

Run instructions: \
`export FLASK_APP="template_autofill:create_app()"`  # Windows = set \
`export FLASK_ENV='developement'` \
`python -m flask run` or \
`gunicorn -w 4 -b 127.0.0.1:5000 "template_autofill:create_app()"`  ## only on Linux
