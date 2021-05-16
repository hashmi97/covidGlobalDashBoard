import numpy as np
import pandas as pd

RECOVERED = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/" \
            "master/csse_covid_19_data/csse_covid_19_time_series/" \
            "time_series_covid19_recovered_global.csv"
CONFIRMED = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/" \
            "master/csse_covid_19_data/csse_covid_19_time_series/" \
            "time_series_covid19_confirmed_global.csv"
DEATHS = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/" \
         "master/csse_covid_19_data/csse_covid_19_time_series/" \
         "time_series_covid19_deaths_global.csv"


class Dataset:
    def __init__(self, URL):
        self.df = pd.read_csv(URL, error_bad_lines=False, header=0,
                              index_col=1)
        self.countries = self.df.index.to_numpy()
        self.dates = self.df.columns.to_numpy()[3:]
        self.type = URL[130:-11].capitalize()

    def createCountry(self, country):
        return Dataset.Country(self, country)

    class Country:
        def __init__(self, dataset_self, country):
            self.name = country
            self.dataset = dataset_self
            self.record = np.diff(self.get_record())

        def get_record(self):
            df = self.dataset.df
            try:
                data_points = df.loc[self.name]
                data_points = data_points.values.tolist()
                if isinstance(data_points[0], list):
                    cumulative = np.zeros(len(data_points[0]) - 3)
                    for value in data_points:
                        cumulative += np.array(value[3:])
                    return cumulative
                else:
                    return np.array(data_points[3:])
            except KeyError:
                print("This country does not exist in the data set")

        def get_seven_day_average_df(self):
            x = self.record
            n = x.shape[0]
            averaging_mat = np.identity(n)
            for i in range(n):
                averaging_mat[i:i + 7, i] = 1 / 7
            averaged = (x.T @ averaging_mat)[:-6].astype(int)
            averageDF = pd.DataFrame(data=np.vstack((self.dataset.dates[7:],
                                                     averaged)).T,
                                     columns=["Date", "{} cases".format(
                                         self.dataset.type)])
            return averageDF

        def get_record_df(self):
            recordDF = pd.DataFrame(data=np.vstack((self.dataset.dates[:-1],
                                                    self.record)).T,
                                    columns=["Date", "{} cases".format(
                                        self.dataset.type)])
            return recordDF
