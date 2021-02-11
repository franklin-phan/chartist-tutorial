"""
    Visualizing diets over the course of time
"""
import datetime
from functools import reduce

import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)
#about to graph some movie data

# Attach our dataframe to our app
app.loaded_csv = pd.read_csv("multiTimeline.csv", skiprows=1)
app.loaded_csv.columns = ["month", "diet", "gym", "finance"]

# Convert dates to datetimes
app.loaded_csv["month"] = pd.to_datetime(
    app.loaded_csv["month"], format="%Y-%d")


@app.route("/", methods=["GET"])
def get_root():
    """
    Root route that returns the index page
    """
    return render_template("index.html"), 200


@app.route("/time_series", methods=["GET"])
def get_time_series_data():
    """
    Return the necessary data to create a time series
    """
    # Grab the requested years and trends from the query arguments
    # default range is from 2004-2005 and default trends are diet and gym.
    range_of_years = [int(year) for year in request.args.getlist("years")]
    trends = request.args.getlist("trends")

    # Generate a list of all the months we need to get
    min_year = min(range_of_years)
    max_year = max(range_of_years)

    # Grab all of the data specified from start to stop range.
    selected_date_range = app.loaded_csv[
        (app.loaded_csv["month"] >= datetime.datetime(min_year, 1, 1)) &
        (app.loaded_csv["month"] <= datetime.datetime(max_year, 12, 31))
    ]

    # Slice the DF to include only the trends we want and then to sort our
    # dataframe by those trends.
    requested_trend_data = selected_date_range[["month"] + trends]
    requested_trend_data = requested_trend_data.sort_values(by=["month"])

    # Return the dataframe as json
    return requested_trend_data.to_json(), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

