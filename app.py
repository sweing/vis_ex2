from flask import Flask, render_template
import json
import pandas as pd
# from sklearn.preprocessing import PCA
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
# import random
import numpy as np

app = Flask(__name__)

# Able to reload when we change the HTML / JS
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Load data
df = pd.read_csv('static/data/agriRuralDevelopment_reduced.csv', sep=",")


# Get the list of all column names
all_columns = df.columns.tolist()

# Filter out the columns you don't want based on their names
non_info_columns = ['Country Name', 'year', 'Country Code', 'Unnamed: 0']

# plot_variables = [col for col in all_columns if col not in non_info_columns]
# plot_variables.remove('Agricultural irrigated land (% of total agricultural land)')
# plot_variables.remove('Agricultural machinery, tractors')
# plot_variables.remove('Agricultural machinery, tractors per 100 sq. km of arable land')
# plot_variables.remove('CPIA gender equality rating (1=low to 6=high)')
# plot_variables.remove('Fertilizer consumption (% of fertilizer production)')
# plot_variables.remove('Fertilizer consumption (kilograms per hectare of arable land)')
# plot_variables.remove('Literacy rate, adult total (% of people ages 15 and above)')

# Define plot variables
plot_variables = ['Access to electricity (% of population)',
                'Agricultural irrigated land (% of total agricultural land)',
                'Average precipitation in depth (mm per year)',
                'Employment in agriculture (% of total employment) (modeled ILO estimate)',
                'GDP per capita (current US$)',
                'Land area (sq. km)',
                'Mortality rate, infant (per 1,000 live births)',
                'Population, total']

selected_countries = ["Australia", "Azerbaijan", "Belarus", "Belgium", "Belize", "Benin", "Bolivia", "Botswana", "Brazil", "Bulgaria", "Burkina Faso", "Burundi", "Cameroon", "Chad", "Colombia", "Croatia", "Denmark", "Dominican Republic", "Ecuador", "Finland", "Georgia", "Ghana", "Guinea", "Haiti", "Honduras", "Indonesia", "Iraq", "Ireland", "Jordan", "Kuwait", "Latvia", "Lebanon", "Liberia", "Libya", "Mali", "Mauritania", "Moldova", "Mongolia", "Morocco", "Turkey", "Tunisia", "Tanzania", "Thailand"]

@app.route('/')
def data():
    plot_df = df[df['Country Name'].isin(selected_countries)]
    plot_df = plot_df.groupby(["Country Code"])

    # fill up NAs
    plot_df = plot_df.bfill()

    grouped_df = plot_df.groupby(['Country Name', 'year']).sum().reset_index()

    most_recent_year = grouped_df['year'].max()
    grouped_df_for_pca = grouped_df[grouped_df['year'] == most_recent_year]

    # Standardize for PCA
    X = grouped_df_for_pca[plot_variables]
    scaler = StandardScaler()
    X_std = scaler.fit_transform(X)

    #  PCA
    pca = PCA(n_components=2)
    pca.fit(X_std)
    pc = pca.transform(X_std)

    inf = pca.components_  # has shape (n_components, n_features)

    pca_df = pd.DataFrame(pc, columns=['PC1', 'PC2'])
    pca_df.index = X.index
    pca_df['Country Name'] = grouped_df_for_pca['Country Name']

    return render_template("index.html", pca_df=json.loads(pca_df.to_json(orient='records')), data=json.dumps(plot_df.to_json(orient='records')), variables=plot_variables, selected_countries=selected_countries)

if __name__ == '__main__':
    app.run()
