#!/usr/bin/env python
import psycopg2

conexion = psycopg2.connect(dbname='gis')
cur = conexion.cursor()

cur.execute("CREATE TABLE info_vilma(id SERIAL PRIMARY KEY, position GEOMETRY, type TEXT, info TEXT);")
cur.execute("GRANT ALL ON info_vilma TO \"www-data\";")
conexion.commit()

conexion.close()
