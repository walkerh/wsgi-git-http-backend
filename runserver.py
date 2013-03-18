from app import app

# if you need to make it public (available beyond localhost), use
# host="0.0.0.0", but note that debug=True on a public is bad news
# security-wise
#app.run(host="0.0.0.0")
app.run()
