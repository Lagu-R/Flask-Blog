import datetime
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # MongoDB connection
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")

            # append new data to MongoDB
            app.db.entries.insert_one(
                {"content": entry_content,
                 "date": formatted_date}
            )

            # Redirect to the home page to avoid form resubmission
            return redirect(url_for('home'))

        entries_with_date = [
            (entry["content"],
             entry["date"],
             datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"))
            for entry in app.db.entries.find({})
        ]

        return render_template("index.html", entries=entries_with_date)

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
