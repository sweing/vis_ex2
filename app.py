from flask import Flask, render_template
import json
import pandas as pd

app = Flask(__name__)

# ensure that we can reload when we change the HTML / JS for debugging
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True



@app.route('/')
def data():
     # Load the data
    df = pd.read_csv('static/data/agriRuralDevelopment_reduced.csv', sep=",")

    # Select the columns to plot
    plot_variables = ['Employment in agriculture (% of total employment) (modeled ILO estimate)',
                      'Agriculture, forestry, and fishing, value added (% of GDP)']
    cols_to_keep = plot_variables + ['year', 'Country Name']
    plot_df = df[cols_to_keep]

    # Group the data by country and year
    grouped_df = plot_df.groupby(['Country Name', 'year']).sum().reset_index()
    print(grouped_df)
    # Convert the data to JSON and pass it to the template
    data = grouped_df.to_json(orient='records')

    # return the index file and the data
    return render_template("index.html", data=json.dumps(data))


if __name__ == '__main__':
    app.run()
