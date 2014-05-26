#!/usr/bin/env python
import psycopg2
conexion = psycopg2.connect(dbname='gis', user='mafda')
cur = conexion.cursor()


#cur.execute("SELECT osm_id, name, way FROM planet_osm_point")
cur.execute("SELECT * FROM info_vilma")
rows = cur.fetchall()
for row in rows:
	print row

conexion.close()