import pandas as pd
import data_preparation
import datetime
import numpy as np

WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


def parse_date(date):
    date_components = date.replace("/", "").split(".")
    DAY = -1
    MONTH = -1
    YEAR = -1
    HOUR = -1
    MINUTES = -1
    if (len(date_components) == 5):  # has time specified
        DAY = int(date_components[0])
        MONTH = int(date_components[1])
        YEAR = int(date_components[2])
        HOUR = int(date_components[3])
        MINUTES = int(date_components[4])
    else:
        DAY = int(date_components[0])
        MONTH = int(date_components[1])
        YEAR = int(date_components[2])
    return (DAY, MONTH, YEAR, HOUR, MINUTES)


def parse_day(DAY, MONTH, YEAR):
    global WEEKDAYS
    some_day = datetime.date(YEAR, MONTH, DAY)
    day = some_day.weekday()
    day = WEEKDAYS[day]
    if (day == "Saturday" or day == "Sunday"):
        type_of_day = "weekend"
    else:
        type_of_day = "weekday"
    return (day, type_of_day)


def parse_time_of_day(HOUR):
    return (
        "morning" if 5 <= HOUR <= 11
        else
        "afternoon" if 12 <= HOUR <= 17
        else
        "evening" if 18 <= HOUR <= 22
        else
        "night"
    )


def map_values_for_CRF(df):
    mapping = {}
    mapping[1] = 'one'
    mapping[2] = 'three'
    mapping[3] = 'five'
    mapping[4] = 'two'
    mapping[5] = 'four'
    df.replace({'CRF':mapping}, inplace = True)
    s = {}
    s['one'] = 1
    s['two'] = 2
    s['three'] = 3
    s['four'] = 4
    s['five'] = 5
    df.replace({'CRF': s}, inplace = True)
    return df

def map_values_for_Rezolucija(df):
    mapping = {}
    mapping[1] = 'five'
    mapping[2] = 'six'
    mapping[3] = 'seven'
    mapping[4] = 'one'
    mapping[5] = 'two'
    mapping[6] = 'three'
    mapping[7] = 'four'
    df.replace({'Rezolucija':mapping}, inplace = True)
    s = {}
    s['one'] = 1
    s['two'] = 2
    s['three'] = 3
    s['four'] = 4
    s['five'] = 5
    s['six'] = 6
    s['seven'] = 7
    df.replace({'Rezolucija': s}, inplace = True)
    return df

def get_date_time_parsed(video_qoE, column_name):
    # video_qoE = pd.read_csv("/home/irma/Dropbox/Documents/Work/Research/Sabina_collab/Video_QoE_Modeling/Video_QoE_Modeling.csv", header=0)

    months = []
    days = []
    type_of_days = []
    years = []
    time_of_days = []

    datetimes = video_qoE[column_name]
    for t in datetimes:
        DAY, MONTH, YEAR, HOUR, MINUTES = parse_date(t)
        day, type_of_day = parse_day(DAY, MONTH, YEAR)
        days.append(DAY)
        type_of_days.append(type_of_day)
        if (HOUR != -1):  # sometimes hour is not defined!
            time_of_days.append(parse_time_of_day(HOUR))
        else:
            time_of_days.append(parse_time_of_day(HOUR))
        months.append(MONTH)
        years.append(YEAR)
    return days, months, type_of_days, years, time_of_days


if __name__ == '__main__':
    col_names = ["Broj", "Osoba", "God", "NM_Spol", "StepenObrazovanja", "PrethodnoIskustvo", "Naocale", "Sluh", "Ruka",
                 "Emocije", "Lokacija", "Guzva", "Buka", "Osvjetljeno", "Brand", "Vrijeme", "Video", "Rezolucija",
                 "CTU",
                 "CRF", "bitrate", "QP", "velicinaDatotekeMB", "P1", "P2", "P3.1", "P3.2", "P3.3", "P3.4", "P3.5",
                 "P3.6",
                 "P3.7", "P3_AVG", "P4.1", "P4.2", "P4.3", "P4.4", "P4.5", "P4.6", "P4.7", "P4_AVG"]

    categorical_variables = ['NM_Spol', 'StepenObrazovanja', 'PrethodnoIskustvo', 'Naocale', 'Sluh', 'Ruka', 'Emocije',
                             'Lokacija', 'Guzva', 'Buka', 'Osvjetljeno', 'Brand', 'Video', 'Rezolucija', 'CTU', 'CRF',
                             'Dan', 'Mjesec', 'Tip_dana', 'Dio_dana']

    numerical_variables = ['God', 'Godina', 'bitrate', 'QP', 'velicinaDatotekeMB', "P1", "P2", "P3.1", "P3.2", "P3.3", "P3.4", "P3.5",
                 "P3.6", "P3.7", "P3_AVG", "P4.1", "P4.2", "P4.3", "P4.4", "P4.5", "P4.6", "P4.7", "P4_AVG"]

    video_qoE = pd.read_csv("/home/irma/Dropbox/Documents/Work/Research/Sabina_collab/Video_QoE_Modeling/original_data/Video_QoE_Modeling.csv", header=0,names=col_names)

    # all columns are number format  - except for date, we need to parse it separately
    for col in col_names:
        if col == "Vrijeme":
            pass
        else:
            video_qoE[col] = pd.to_numeric(video_qoE[col])

    # parse date-time column
    days, months, type_of_days, years, time_of_days = get_date_time_parsed(video_qoE, 'Vrijeme')
    video_qoE['Dan'] = days
    video_qoE['Mjesec'] = months
    video_qoE['Godina'] = years
    video_qoE['Tip_dana'] = type_of_days
    video_qoE['Dio_dana'] = time_of_days
    del video_qoE['Vrijeme']
    del video_qoE['Broj']
    #del video_qoE['Osoba']

    #there was lokacija = 5 change that
    values = video_qoE["Lokacija"].to_numpy()
    inds = np.where(values == 5)
    for i in inds[0]:
        video_qoE.iloc[i, video_qoE.columns.get_loc("Lokacija")] = 4


video_qoE = data_preparation.replace_missing_values(video_qoE,'/home/irma/Dropbox/Documents/Work/Research/Sabina_collab/Video_QoE_Modeling/original_data/missingData.info', numerical_variables)

video_qoE = map_values_for_CRF(video_qoE)
video_qoE = map_values_for_Rezolucija(video_qoE)

print(video_qoE.head().CRF)

video_qoE.to_csv('/home/irma/Dropbox/Documents/Work/Research/Sabina_collab/Video_QoE_Modeling/processed_data/Processed_Video_QoE_Modeling.csv', index=False)

