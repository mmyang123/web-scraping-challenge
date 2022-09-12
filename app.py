#import necessary libraries
from flask import Flask, render_template, make_response, request

# Create instance of Flask app
app = Flask(__name__)

# Create route that renders index.html templates
from cgitb import text


@app.route("/")
def echo():
    return render_template("index.html", text="Serving")

if __name__=="__main__":
    app.run(debug=True)
