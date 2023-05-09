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

plot_variables = [col for col in all_columns if col not in non_info_columns]
plot_variables.remove('Agricultural irrigated land (% of total agricultural land)')
plot_variables.remove('Agricultural machinery, tractors')
plot_variables.remove('Agricultural machinery, tractors per 100 sq. km of arable land')
plot_variables.remove('CPIA gender equality rating (1=low to 6=high)')
plot_variables.remove('Fertilizer consumption (% of fertilizer production)')
plot_variables.remove('Fertilizer consumption (kilograms per hectare of arable land)')
plot_variables.remove('Literacy rate, adult total (% of people ages 15 and above)')

# Define plot variables
# plot_variables = ['Employment in agriculture (% of total employment) (modeled ILO estimate)',
#                   'Agriculture, forestry, and fishing, value added (% of GDP)',
#                   'Birth rate, crude (per 1,000 people)']



@app.route('/')
def data():
    # Select the columns to plot
    # cols_to_keep = plot_variables + ['year', 'Country Name']

    # selected_countries = random.sample(list(plot_df["Country Name"]), 40)
    selected_countries = ["Australia", "Azerbaijan", "Belarus", "Belgium", "Belize", "Benin", "Bolivia", "Botswana", "Brazil", "Bulgaria", "Burkina Faso", "Burundi", "Cameroon", "Chad", "Colombia", "Croatia", "Denmark", "Dominican Republic", "Ecuador", "Finland", "Georgia", "Ghana", "Guinea", "Haiti", "Honduras", "Indonesia", "Iraq", "Ireland", "Jordan", "Kuwait", "Latvia", "Lebanon", "Liberia", "Libya", "Mali", "Mauritania", "Moldova", "Mongolia", "Morocco", "Turkey", "Tunisia", "Tanzania", "Thailand"]

    #df = df[df['Country Name'].isin(selected_countries)]
    plot_df = df
    plot_df = plot_df[plot_df['Country Name'].isin(selected_countries)]
    
    grouped_df = plot_df.groupby(['Country Name', 'year']).sum().reset_index()

    # for line plots
    filled_df = grouped_df
    cols_to_fill = plot_variables
    for nam in selected_countries:
        testsmall = filled_df[filled_df['Country Name'] == nam]
        for col in cols_to_fill:
        # Create a boolean mask for the rows where the value is zero
            mask = (testsmall[col] == 0)
            #print(col)
            #print(nam)
            first_non_zero_index = testsmall[col].index[np.argmax(testsmall[col].values != 0)]
            first_non_zero_entry = testsmall.loc[first_non_zero_index , col]
            # testsmall[col].replace(0, first_non_zero_entry, inplace = True)
        # Fill the zeros with the first non-zero value using boolean indexing and fillna
            testsmall.loc[mask, col] = first_non_zero_entry
            filled_df[filled_df['Country Name'] == nam] = testsmall
    print('finished filling')
    #mask = (filled_df == 0)
    #zero_cols = filled_df.columns[mask.any()]



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
        # represents the directions of maximum variance in the data, which reflects the magnitude of the corresponding values in the eigenvectors (higher magnitude - higher importance)
    #max_row1 = np.max(inf[0, :])
    #max_pos_row1 = np.argmax(inf[0])
    #max_row2 = np.max(inf[1, :])
    #max_pos_row2 = np.argmax(inf[1])
    #plot_variables[max_pos_row1]
    #plot_variables[max_pos_row2]

    pca_df = pd.DataFrame(pc, columns=['PC1', 'PC2'])
    pca_df.index = X.index
    pca_df['Country Name'] = grouped_df_for_pca['Country Name']
    #import matplotlib.pyplot as plt
    #ax = pca_df.plot.scatter(x='PC1', y='PC2')
    #plt.show()

    # Convert to JSON
    data = pca_df.to_json(orient='records')

    return render_template("index.html", pca_df=json.loads(data), data=json.dumps(df.to_json(orient='records')), data2=json.loads(filled_df.to_json(orient='records')), variables=plot_variables, selected_countries=selected_countries)
                                            # PCA results           # all all                                       # only selected without 0
if __name__ == '__main__':
    app.run()
