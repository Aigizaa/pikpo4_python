from typing import List

from .connector import StoreConnector
from pandas import DataFrame, Series
from datetime import datetime

"""
    В данном модуле реализуется API (Application Programming Interface)
    для взаимодействия с БД с помощью объектов-коннекторов.
    
    ВАЖНО! Методы должны быть названы таким образом, чтобы по названию
    можно было понять выполняемые действия.
"""


def select_all_from_source_files(connector: StoreConnector) -> List[tuple]:
    """ Вывод списка обработанных файлов с сортировкой по дате в порядке убывания (DESCENDING) """
    query = f'SELECT * FROM source_files ORDER BY processed DESC'
    result = connector.execute(query).fetchall()
    return result


def insert_into_source_files(connector: StoreConnector, filename: str):
    """ Вставка в таблицу обработанных файлов """
    now = datetime.now()        # текущая дата и время
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")   # преобразуем дату в формат SQL, например, '2022-11-15 22:03:16'
    query = f'INSERT INTO source_files (filename, processed) VALUES (\'{filename}\', \'{date_time}\')'
    result = connector.execute(query)
    return result


def insert_rows_into_processed_data(connector: StoreConnector, dataframe: DataFrame):
    """ Вставка строк из DataFrame в БД с привязкой данных к последнему обработанному файлу (по дате) """
    rows = dataframe.to_dict('records')
    files_list = select_all_from_source_files(connector)    # получаем список обработанных файлов
    # т.к. строка БД после выполнения SELECT возвращается в виде объекта tuple, например:
    # row = (1, 'seeds_dataset.csv', '2022-11-15 22:03:16'),
    # то значение соответствующей колонки можно получить по индексу, например id = row[0]
    last_file_id = files_list[0][0]  # получаем индекс последней записи из таблицы с файлами
    if len(files_list) > 0:
        for row in rows:
            connector.execute(f'INSERT INTO processed_data ('f' country, "2000", "2001", "2002", "2003", "2004", "2005",'
                              f' "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015"'
                              f', "2016", "2017", "2018", "2019", source_file) '
                              f'VALUES (\'{row["country"]}\', \'{row["2000"]}\',\'{row["2001"]}\', \'{row["2002"]}\','
                              f'\'{row["2003"]}\', \'{row["2004"]}\',\'{row["2005"]}\', \'{row["2006"]}\','
                              f'\'{row["2007"]}\', \'{row["2008"]}\',\'{row["2009"]}\', \'{row["2010"]}\','
                              f'\'{row["2011"]}\', \'{row["2012"]}\',\'{row["2013"]}\', \'{row["2014"]}\','
                              f'\'{row["2015"]}\', \'{row["2016"]}\',\'{row["2017"]}\','
                              f'\'{row["2018"]}\', \'{row["2019"]}\', {last_file_id})')
        print('Data was inserted successfully')
    else:
        print('File records not found. Data inserting was canceled.')
