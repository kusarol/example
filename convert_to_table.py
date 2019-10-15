import xlrd
import csv
import pandas
import sqlite3
import os


con = sqlite3.connect('tables.db')


def table(path, filename):
    wb = xlrd.open_workbook(path)
    sh = wb.sheet_by_index(0)
    name_csv_file = filename.replace('.xls', '') + '.csv'
    my_csv_file = open(name_csv_file, 'w')
    wr = csv.writer(my_csv_file, quoting=csv.QUOTE_ALL)
    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    my_csv_file.close()

    con = sqlite3.connect('tables.db')
    df = pandas.read_csv(name_csv_file, encoding='latin-1')
    df.to_sql(filename.replace('.xls', ''), con,
              if_exists='append', index=False)
    con.close()
    os.remove(name_csv_file)
    return get_table(filename.replace('.xls', ''))


def get_table(filename):
    os.chdir("C:\\Users\\Anastasiia.Varinova\\Documents\\GitHub\\example")
    con = sqlite3.connect('tables.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM " + filename)
        rows = cur.fetchall()
    return rows
