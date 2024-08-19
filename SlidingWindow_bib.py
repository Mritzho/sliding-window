# -*- coding: iso-8859-1 -*-

import numpy as np
import pandas as pd



def sliding_Window(data, window_size, step_size):
    
    SN_vector = data[:,0]
    data_vector = data[:,1]    

    new_array = []  
    first_column_values = []  # Liste für die Werte der ersten Spalte

    for i in range(0, len(data_vector) - window_size + 1, step_size):
        window_data = data_vector[i:i+window_size]

        # Extrahiere die Werte der ersten Spalte und füge sie zur Liste hinzu
        first_column_values.append(SN_vector[i])

        window_sum = np.sum(window_data)  # Summiere die Werte in window_data
        average = window_sum / window_size * 100  # in Prozent
        new_array.append(average)

    return np.array(new_array), np.array(first_column_values)


def df_to_np(df: pd.DataFrame):
    # Convert dataframe with only int values to numpy array
    
    data_array = df.to_numpy().astype(np.uint) 

    return(data_array)
    
def invert_Data(array):
    splitted = np.hsplit(array, 2)
    firstpart = splitted[0]
    secondpart = splitted[1].astype(bool)
    secondpart_inverted = np.invert(secondpart)
    
    return np.concatenate((firstpart.astype(np.uint), secondpart_inverted.astype(np.uint)), axis=1)

def fill_array_with_zero(data_array):
    new_rows = []

    # Iteriere durch das NumPy-Array
    for i in range(len(data_array) - 1):
        current_value = data_array[i, 0]
        next_value = data_array[i + 1, 0]
        current_label = data_array[i, 1]

        new_rows.append([current_value, current_label])

        # Füge fehlende Zahlen mit Nullen ein
        if next_value - current_value > 1:
            for j in range(current_value + 1, next_value):
                new_rows.append([j, 0])

    # Füge die letzte Zeile hinzu
    new_rows.append([data_array[-1, 0], data_array[-1, 1]])

    return np.array(new_rows)

def find_column(wert, start_row, df: pd.DataFrame): #Ueberarbeitet
    for spalte in df.columns:
        if df.loc[start_row - 1, spalte] == wert:
            return spalte
    return ""

def column_letter(column_number): #Ueberarbeitet
    if column_number > 0:
        column_letter = ""
        while column_number > 0:
            dividend, modulo = divmod(column_number - 1, 26)
            column_letter = chr(65 + modulo) + column_letter
            column_number = dividend
        return column_letter
    else:
        return "Ungueltige Spaltennummer"
        

def find_start_row(df: pd.DataFrame):
    for index, row in df.iterrows():
        cell_value = row.iloc[0]  # Zugriff auf den Wert in Spalte 0
        if pd.notna(cell_value):
            return index
    return -1


def find_last_row(df: pd.DataFrame):
    last_Row = df.shape
    return last_Row[0]

def find_coordinates(gesuchter_string, start_Row, df: pd.DataFrame):
    coordinates = []

    # Suche nur in der angegebenen Zeile (start_Row)
    row = df.loc[start_Row]

    for column, cell_value in row.items():
        if pd.notna(cell_value) and gesuchter_string in str(cell_value):
            coordinates.append(column)

    return coordinates[0]

def convert_to_numeric(data: pd.DataFrame, column="Serialnummer"):
    data[column] = pd.to_numeric(data[column], errors='coerce')
    return data