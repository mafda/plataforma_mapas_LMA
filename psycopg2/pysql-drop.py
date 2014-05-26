#!/usr/bin/env python
import psycopg2
conexion = psycopg2.connect(dbname='gis', user='mafda')
cur = conexion.cursor()


cur.execute("DROP TABLE IF EXISTS info_vilma")
conexion.commit()

conexion.close()