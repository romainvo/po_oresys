from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")

def home():
  return render_template("home.html")

@app.route("/John")
def John():
  return "Hello John."

@app.route("/osm")
def test_map():
  return render_template("test_map.html")

@app.route("/mapbox")
def test_mapbox():
  return render_template("test_mapbox.html")

@app.route("/polygon")
def test_polygon():
  return render_template("test_polygon.html")

@app.route("/leaflet")
def test_leaflet():
  return render_template("test_leaflet.html")

@app.route("/about")
def about():
  return render_template("about.html")


if __name__ == "__main__":
  app.run(debug=True)