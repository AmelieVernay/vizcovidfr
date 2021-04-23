import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
model = LinearRegression()
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from sklearn.metrics import r2_score
from vizcovidfr.loads import load_datasets
from vizcovidfr.preprocesses import preprocess_classe_age as pca
from vizcovidfr.regression import regression as rg
import datetime
from matplotlib.backends.backend_pdf import PdfPages

T = load_datasets.Load_classe_age().save_as_df()


def predict_curve(num_var, num_reg, date = 'date', save = False):
    """
    Display the scatter plot of the given variable in the given region with predicted curve until the given date. Each variable and region have a special code that you can see in function parameters for details.

    Parameters
    ----------

    :param num_var: code of the variable you want to display. 
        Codes are in the following dictionnary.
    :type num_var: int
    :param num_reg: code of the region you want to display. 
        Codes are the official INSAA code region and are given in the dictionnary below.
    :type num_reg: int
    :param date: date where regression line will stop.
        Must be on YYYY/MM/DD format.
        Must be a future date, not a date from the past.
    :type date: str
    :param save: True if you want to save the graph in pdf file, False otherwise.
    :type save: bool, optionnal, default = False
    
    Variable dictionnary :

        1 : Hospitalization

        2 : Reanimation

        3 : Conventional hospitalization
    
        4 : SSR and USLD

        5 : Others

        6 : Come back home

        7 : Deaths

    - Hospitalization :
        number of hospitalized patients.

    - Reanimation :
        number of people currently in intensive care or intensive care.

    - Conventional hospitalization :
        number of people currently in conventional hospitalization.

    - SSR and USLD :
        number of people currently in Aftercare and Rehabilitation (SSR in french) or Long-Term Care Units (USLD in french).
    
    - Others :
        number of people currently hospitalized in another type of service.
    
    - Come back home :
        cumulative number of people who returned home.
    
    - Deaths :
        cumulative number of deceased persons.


    Region dictionnary :

        1 : Guadeloupe

        2 : Martinique

        3 : Guyane

        4 : La Reunion

        6 : Mayotte

        11 : Île-de-France

        24 : Centre-Val de Loire
    
        27 : Bourgogne-Franche-Comte

        28 : Normmandie

        32 : Hauts-de-France

        44 : Grand Est

        52 : Pays de la Loire

        53 : Bretagne

        75 : Nouvelle-Aquitaine

        76 : Occitanie

        84 : Auvergne-Rhône-Alpes

        93 : Provence-Alpes Côte d'Azur

        94 : Corse

    Returns
    ----------

    :return: Prediction graph of one of the Covid variable in a specific region of France.
    :rtype: Figure

    """
    #Choose region
    R = pca.reg(num_reg, T)
    #Convert to datetime format
    R = pca.date_time(R)
    #Columns dictionnary
    dico_col = pca.dico_column(R)
    #Grouping by day
    covid_day = pca.covid_day_fct(R)
    #Choose variable to explain
    x = np.arange(0, covid_day.shape[0])
    y = covid_day[dico_col[1]]
    x = x[:, np.newaxis]
    y = y[:, np.newaxis]
    #Dictionnaries
    dico_days = pca.dico_day(covid_day)
    dico_file = pca.dico_file()
    dico_var = pca.dico_var()
    dico_reg = pca.dico_reg()
    covid_day = covid_day.reset_index(drop=True)
    #Mean squared error and prediction of y
    rmselist, x_p_list, y_poly_pred_P_list = pca.rmse_list(x, y)
    deg = list(rmselist).index(rmselist.min())
    #Coefficients of the regression polynom
    coefs = np.polyfit(np.arange(0, covid_day.shape[0]), y_poly_pred_P_list[deg], deg+1)
    #Date format
    delta = datetime.timedelta(days=1)
    date2 = pd.to_datetime(date)
    #Listing dico_days keys
    keys = list(dico_days.keys())
    #Dictionnary dico_days with date until 'date'
    period = date2 - dico_days[keys[-1]]
    num_date = keys[-1] + period.days
    dico_days2 = dico_days.copy()
    for i in np.arange(keys[-1]+1,num_date+1):
        dico_days2[i] = dico_days2[i-1] + delta
    #Scatter plot with the predicted regression line
    fig = plt.scatter(dico_days.values(), y)
    plt.plot(dico_days2.values(), np.polyval(coefs, np.arange(num_date+1)), color="black")
    plt.title("Prediction curve of" + " " + dico_var[dico_col[num_var]] + " in " + dico_reg[num_reg] + "\n until " + date)
    #Saving pdf file
    if save == True:
        plt.savefig(f"predict_" + dico_file[num_var] + "_" + dico_reg[num_reg] + "_" + date + ".pdf", dpi=1200)
    plt.show()


def predict_value(num_var, num_reg, date = 'date'):
    """
    Display the predicted value of the given variable in the given region on the given date. Each variable and region have a special code that you can see in function parameters for details.

    Parameters
    ----------

    :param num_var: code of the variable you want to display. 
        Codes are in the following dictionnary.
    :type num_var: int
    :param num_reg: code of the region you want to display. 
        Codes are the official INSAA code region and are given in the dictionnary below.
    :type num_reg: int
    :param date: date when you want to predict the variable.
        Must be on YYYY/MM/DD format.
        Must be a future date, not a date from the past.
    :type date: str
    
    Variable dictionnary :

        1 : Hospitalization

        2 : Reanimation

        3 : Conventional hospitalization
    
        4 : SSR and USLD

        5 : Others

        6 : Come back home

        7 : Deaths

    - Hospitalization :
        number of hospitalized patients.

    - Reanimation :
        number of people currently in intensive care or intensive care.

    - Conventional hospitalization :
        number of people currently in conventional hospitalization.

    - SSR and USLD :
        number of people currently in Aftercare and Rehabilitation (SSR in french) or Long-Term Care Units (USLD in french).
    
    - Others :
        number of people currently hospitalized in another type of service.
    
    - Come back home :
        cumulative number of people who returned home.
    
    - Deaths :
        cumulative number of deceased persons.


    Region dictionnary :

        1 : Guadeloupe

        2 : Martinique

        3 : Guyane

        4 : La Reunion

        6 : Mayotte

        11 : Île-de-France

        24 : Centre-Val de Loire
    
        27 : Bourgogne-Franche-Comte

        28 : Normmandie

        32 : Hauts-de-France

        44 : Grand Est

        52 : Pays de la Loire

        53 : Bretagne

        75 : Nouvelle-Aquitaine

        76 : Occitanie

        84 : Auvergne-Rhône-Alpes

        93 : Provence-Alpes Côte d'Azur

        94 : Corse

    Returns
    ----------

    :return: Prediction of one of the Covid variable in a specific region of France on the given date.
    :rtype: str

    """
    #Choose region
    R = pca.reg(num_reg, T)
    #Convert to datetime format
    R = pca.date_time(R)
    #Columns dictionnary
    dico_col = pca.dico_column(R)
    #Grouping by day
    covid_day = pca.covid_day_fct(R)
    #Choose variable to explain
    x = np.arange(0, covid_day.shape[0])
    y = covid_day[dico_col[1]]
    x = x[:, np.newaxis]
    y = y[:, np.newaxis]
    #Dictionnaries
    dico_days = pca.dico_day(covid_day)
    dico_var = pca.dico_var()
    dico_reg = pca.dico_reg()
    covid_day = covid_day.reset_index(drop=True)
    #Mean squared error and prediction of y
    rmselist, x_p_list, y_poly_pred_P_list = pca.rmse_list(x, y)
    deg = list(rmselist).index(rmselist.min())
    #Coefficients of the regression polynom
    coefs = np.polyfit(np.arange(0, covid_day.shape[0]), y_poly_pred_P_list[deg], deg+1)
    #Date format
    delta = datetime.timedelta(days=1)
    date2 = pd.to_datetime(date)
    #Listing dico_days keys
    keys = list(dico_days.keys())
    #Dictionnary dico_days with date until 'date'
    period = date2 - dico_days[keys[-1]]
    num_date = keys[-1] + period.days
    dico_days2 = dico_days.copy()
    for i in np.arange(keys[-1]+1,num_date+1):
        dico_days2[i] = dico_days2[i-1] + delta
    #Predicted value
    pred = np.polyval(coefs, num_date+1)[0]
    if num_var == 6 or num_var == 7:
        res = 'The cumulative number of ' + dico_var[dico_col[num_var]] + " in " + dico_reg[num_reg] + " on " + date + f' will be {round(pred)}.' 
    else:
        res = 'The number of ' + dico_var[dico_col[num_var]] + " in " + dico_reg[num_reg] + " on " + date + f' will be {round(pred)}.'
    return res
