from flask import Flask, render_template
import json
import pandas as pd
# from sklearn.preprocessing import PCA
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
# import random

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
plot_variables = [col for col in all_columns if col not in non_info_columns]


# Define plot variables
# plot_variables = ['Employment in agriculture (% of total employment) (modeled ILO estimate)',
#                   'Agriculture, forestry, and fishing, value added (% of GDP)',
#                   'Birth rate, crude (per 1,000 people)']



@app.route('/')
def data():
    # Select the columns to plot
    # cols_to_keep = plot_variables + ['year', 'Country Name']
    plot_df = df
    # selected_countries = random.sample(list(plot_df["Country Name"]), 40)
    selected_countries = ["Australia", "Azerbaijan", "Belarus", "Belgium", "Belize", "Benin", "Bolivia", "Botswana", "Brazil", "Bulgaria", "Burkina Faso", "Burundi", "Cameroon", "Chad", "Colombia", "Croatia", "Denmark", "Dominican Republic", "Ecuador", "Egypt", "Finland", "Gambia", "Georgia", "Ghana", "Guinea", "Haiti", "Honduras", "Indonesia", "Iraq", "Ireland", "Israel", "Jordan", "Kuwait", "Latvia", "Lebanon", "Liberia", "Libya", "Mali", "Mauritania", "Moldova", "Mongolia", "Morocco"]

    plot_df = plot_df[plot_df['Country Name'].isin(selected_countries)]
    
    grouped_df = plot_df.groupby(['Country Name', 'year']).sum().reset_index()

    # for line plots
    sel_dat_line = ['Country Name', 'year', plot_variables[0], plot_variables[1]]
    data_line = grouped_df[sel_dat_line]
    # data_line = data_line.rename(columns={plot_variables[0]: 'employed in agriculture', plot_variables[1]: 'agriculture in GDP'})

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

    pca_df = pd.DataFrame(pc, columns=['PC1', 'PC2'])
    pca_df.index = X.index
    pca_df['Country Name'] = grouped_df_for_pca['Country Name']
    # Convert to JSON
    data = pca_df.to_json(orient='records')

    return render_template("index.html", pca_df=json.loads(data), data=json.dumps(df.to_json(orient='records')), data2=json.loads(data_line.to_json(orient='records')), variables=plot_variables, selected_countries=selected_countries)

if __name__ == '__main__':
    app.run()
