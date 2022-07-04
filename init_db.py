import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="dbProject",
    user='postgres',
    password='120616')

# Open a cursor to perform database operations
cur = conn.cursor()

# Insert data into the table

cur.execute('INSERT INTO usuario (username, documento, nacionalidade, nome, email, datadenascimento)'
            'VALUES (%s, %s, %s, %s, %s, %s)',
            ('isadora_siebert',
             '48551556596',
             'brasileiro',
             'Isadora Siebert',
             'isaahsc@gmail.com',
             '28/09/2000')
            )

conn.commit()

cur.close()
conn.close()
