# covidGlobalDashboard


### Description 
Use this plolty dashboard to visualize Covid-19 trends around the world. You 
can choose a country out of 192 on the list. There are three different options 
for every country (Confirmed,Deaths and Recovered) cases. There is also an 
option to select the specific date range in interest and enable 7 day averaging
. The data is retrieved from the [COVID-19 Data Repository by the Center for 
Systems Science and Engineering (CSSE) at Johns Hopkins University.](https://github.com/CSSEGISandData/COVID-19)

The dashboard is hosted on Heroku, you can find the app [here.](https://my-covid-dashboard.herokuapp.com/ "Heroku App Dashboard")
### Python packages to install
`pip install dash`

You can find the full list of requirements [here.](../main/requirements.txt)


## Usage 
#### Date range :
- Select the date range you are interested in.
- The earliest possible date is Jan 29th 2020.
- There must be a 14-day gap between the start and end dates
- If the calendar stops you from selecting a date, that your selection is invalid.
 #### 7-day averaging:
- If you enable 7 day averaging, then the value on the y-axis becomes the average for the preceding 7 days instead of single day.
 #### Country:
- Select your country of interest using the drop down list. 
 #### Dataset:
- You can choose one of the three possible datasets (Confirmed, Deaths, Recovered).
- Note that since some countries do not track recoveries the plot my not be accurate.
