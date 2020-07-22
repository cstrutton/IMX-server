import glob
import os
from time import sleep

import mysql.connector

config = {
    'database': 'prodrptdb',
    'user': 'stuser',
    'password': 'stp383',
    'host': '10.4.1.224'
}

cnx = mysql.connector.connect


def executesql(directory='/var/local/1617SQL/', config=config):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    for filepath in glob.iglob(directory+'*.sql'):
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                sql = line.strip()
                cursor.execute(sql)
                print(sql)
        cnx.commit()
        os.remove(filepath)

    cursor.close()
    cnx.close()


if __name__ == '__main__':
    while True:
        executesql()
        sleep(2)
