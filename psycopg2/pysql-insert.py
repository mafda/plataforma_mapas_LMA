#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix
import psycopg2
import sys

vel = 0

def callback(data):
	conexion = psycopg2.connect(dbname='gis')
	cur = conexion.cursor()
	#print "Content-type:text/html\r\n\r\n"
	#print data.header.stamp, data.latitude, data.longitude, data.altitude
	#cur.execute("INSERT INTO info_vilma VALUES(data.longitude data.latitude,'Velocidade','Vel Max 20Km/h')")
	#cur.execute("INSERT INTO info_vilma VALUES(data.longitude data.latitude,'Faixa','Faixa de Pedestre')")

	point = "ST_Transform(ST_GeomFromText('POINT(" + str(data.longitude) + str(data.latitude) + ")',4326),900913)"

	insert = "INSERT INTO info_vilma (position, type, info) VALUES(" + point + ",'Velocidade','Vel Max " + str(vel) + "Km/h')"
	#print insert
	cur.execute(insert)

	conexion.commit()
	conexion.close()

	rospy.signal_shutdown('End of process!')

def getGPS():
	rospy.init_node('getGPS', anonymous=True)
	rospy.Subscriber("sensor_gps", NavSatFix, callback)
	rospy.spin()


if __name__ == '__main__':
	if len(sys.argv)!=2:
		vel = 20
	else:
		vel = int(sys.argv[1])

	getGPS()