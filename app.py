from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/web_scrape_data"
mongo = PyMongo(app)


@app.route("/")
def home():
    scrape_data = mongo.db.scrapeData.find_one()
    return render_template("index.html", listings=scrape_data, redplatnetlen=len(scrape_data['redplanet_info']),hemilen=len(scrape_data['hemispheres']))
    # return "Hello World"

@app.route("/scrape")
def scraper():
    scrape_table = mongo.db.scrapeData
    mongo.db.scrapeData.drop()
    listings_data = scrape_mars.scrape()
    scrape_table.update_one({}, {"$set": listings_data}, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)