from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/test_db")
def test_db():
  from database import Airbnb
  first_airbnb = Airbnb.query.get(1)
  #print(first_airbnb.longitude)
  return str(first_airbnb.longitude)

@app.route('/donneesgeos/<path:path>')
def send_donneesgeo(path):
	return send_from_directory('static/donneesgeos', path)

@app.route("/mapbox")
def test_mapbox():
  return render_template("test_mapbox.html")

@app.route("/polygon")
def test_polygon():
  return render_template("test_polygon.html")

@app.route("/about")
def about():
  return render_template("about.html")

if __name__ == "__main__":
  app.run(debug=True)