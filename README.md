# Exploration of Patient Data by Pathology and Age Group (2019)

This project is an interactive application developed with Dash and Plotly to explore patient data by pathology and age group, segmented by gender, for the year 2019. The application provides tools to visualize and analyze the distribution of pathologies across various French departments using a choropleth map, as well as statistical charts and data tables.

## Features

- **Intensity Map**: Visualization of French departments with color-coding based on the intensity of pathology prevalence.
- **Dynamic Graphs**: Boxplots and histograms to explore the distribution of prevalences by age group.
- **Interactive Filters**: Selection of pathologies, gender, and age ranges to filter the visualizations.
- **Key Statistics**: Display of descriptive statistics on prevalences and the affected population.

## Installation

- Clone the repository: `git clone https://github.com/StorkMiner/Pathologies-Dashboard.git`
- Install dependencies: `pip install -r requirements.txt`
- Run the application: `python pathodash.py`

## Dependencies

- Dash
- Plotly
- Pandas
- NumPy
- GeoJSON

## Authors

- Adrien Bartoletti - [GitHub](https://github.com/StorkMiner) - [LinkedIn](https://www.linkedin.com/in/adrien-bartoletti-9a57b4191/)

## Data Source

- Assurance Maladie: [Cartography of Patient Data](https://www.assurance-maladie.ameli.fr/etudes-et-donnees/cartographie-effectif-patients-par-pathologie-age-sexe)
