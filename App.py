from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# Scrape Data and pull into Mongo DB
client = pymongo.MongoClient()
db = client.Mars_db
collection = db.Facts

@app.route("/")
def home():
    mars = list(db.collection.find())
    print(mars)
    return render_template("index.html", mars = mars)

@app.route('/scrape')
def scrape():
    db.collection.remove({})
    Mars_Data = scrape_mars.scrape()
    db.collection.insert_one(Mars_Data)
    return render_template("index.html", Mars_Data = Mars_Data)

if __name__ == "__main__":
    app.run(debug=True)