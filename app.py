from flask import Flask, render_template
import json
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Able to reload when we change the HTML / JS
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Load data
df = pd.read_csv('static/data/agriRuralDevelopment_reduced.csv', sep=",")

# Define plot variables
plot_variables = ['Employment in agriculture (% of total employment) (modeled ILO estimate)',
                  'Agriculture, forestry, and fishing, value added (% of GDP)']

@app.route('/')
def data():
    # Select the columns to plot
    cols_to_keep = plot_variables + ['year', 'Country Name']
    plot_df = df[cols_to_keep]

    selected_countries = ['Germany', 'France', 'Italy']  # Replace with your list of 40 countries
    plot_df = plot_df[plot_df['Country Name'].isin(selected_countries)]
    
    # Group the data by country and year
    grouped_df = plot_df.groupby(['Country Name', 'year']).sum().reset_index()

    # Select the most recent year
    most_recent_year = grouped_df['year'].max()
    grouped_df_for_pca = grouped_df[grouped_df['year'] == most_recent_year]

    # Standardize the data for PCA
    X = grouped_df[plot_variables]
    scaler = StandardScaler()
    X_std = scaler.fit_transform(X)

    # Perform PCA
    pca = PCA(n_components=2)
    pca.fit(X_std)
    pc = pca.transform(X_std)

    pca_df = pd.DataFrame(pc, columns=['PC1', 'PC2'])
    pca_df.index = X.index
    pca_df['Country Name'] = grouped_df['Country Name']
    print(pca_df)
    # Convert the data to JSON and pass it to the template
    data = pca_df.to_json(orient='records')

    # return the index file and the data
    return render_template("index.html", plot_df=plot_df, pca_df=json.dumps(data))

if __name__ == '__main__':
    app.run()
