from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("carte.html")

@app.route('/donneesgeos/<path:path>')
def send_donneesgeo(path):
	return send_from_directory('static/donneesgeos', path)

if __name__ == "__main__":
  app.run(debug=True)