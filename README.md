# project-parks-pulse

# Description
The project aims to analyze the U.S. National Parks System data to construct a composite measure of individual parks’ health status, which we will henceforth call the Park Health Index (PHI). To compute this index, we will examine and assign appropriate weight to various aspects of a park’s current state, including park usage, climate data, park management, and hazards. With this index, we will also look at NPS’s financial data to see if any interesting correlation can be observed. From individual time series data by parks unit, we are also interested in exploring trends in visitation and impact of climate change among parks over the last 13 years. The goal of this project is threefold: (1) spreading awareness of national parks’ health (snapshot and overtime), (2) uncovering patterns that might reveal useful information for assessment and evaluation of parks management, and (3) providing a benchmark to highlight risk areas to better inform policy-makers on parks conservation and resources allocation.


# Built with
- Python
- matplotlib/Seaborn
- Statsmodels
- Pandas
- Numpy
- BeautifulSoup4
- geopandas
- lxml
- cssselect
- fastkml

# Data Sources
1.	DMR: https://www.pewtrusts.org/
2.	NPS Spending Data: https://www.nps.gov/aboutus/budget.htm
3.	Weather data: https://www.visualcrossing.com/ 
4.	NP Basic Info(name/location/size) Data: https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States
5.	NP Visitation Data: https://irma.nps.gov/Stats/SSRSReports/National%20Reports/Annual%20Visitation%20and%20Record%20Year%20by%20Park%20(1904%20-%20Last%20Calendar%20Year)


# Getting Started
To get started with the Dashboard, follow these steps:
1.	Clone the repository: "git clone https://github.com/SeongyeonYang/30122-project-parks-pulse.git"
2.	Run "poetry install" to install the necessary packages
3.	Run "poetry shell" to activate the virtual environment
4.	Run "python -m ppp" to open the visualization and analysis

# Project Directory Structure
- ppp
  - analysis
    - visualizations
    - app.py
    - .py files about analysis (total 5)
  - cleaning
    - cleaned_data
      - cleaned_time_series_all.csv (all merged files based on time series)
      - cleaned_nps_info.csv (all merged files based on information)
      - .py files about cleaned data before merge into 2 files above (total 14)
    - raw_data
      - climate
      - nps_spending
      - dmr-2015-2019.csv
      - dmr-2023.csv
      - npca-orphaned-wells.csv
      - nps-boundary.geojson

# Data Visualization Demo
- Correlation Matrix of Visitation, Spending, and Climate Variables (2011-2019
![Correlation Matrix of Visitation, Spending, and Climate Variables (2011-2022)](ppp/analysis/visualizations/Correlation%20Matrix%20of%20Visitation%2C%20Spending%2C%20and%20Climate%20Variables%20%282011-2022%29.png)

- Partial Regression Plot: DMR, Visitation, and Spending at NPs (2015-2019)
![Regression Plot](ppp/analysis/visualizations/regression_plot.png)


# Authors
- Minh Nghiem 
- Seongyeon Yang 
- Yi-Huai Chang 
- Diyanet Nijiati 

