#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import NavSatFix
from transformations import *
import psycopg2

#ponto de referencia 0,0 do mundo,  lat,long PontoA
Lat_o = -22.8189685 
Lon_o = -47.0647617

# Car position - car to origin
Xcar_o = 0
Ycar_o = 0
Theta_car = 0

# Cam position - cam to car (model.sdf  <pose>1.2 0.0 1.1 0 0 0</pose>)
Xcam_car = 1.2
Ycam_car = 0.0

# obj position - obj to cam
Xr_cam = 0
Yr_cam = 0
obj_in_scene = 0

#funcao que chama vilma_compass para obter o angulo yaw do veiculo
def callbackCompass(data):
    global Theta_car
    Theta_car = data.data[2]  #yaw veiculo

#funcao que chama vilma_detection_camera_scan para obter a posicao do objeto R com respeito ao 0,0 do mundo
def callbackObjPos(data):
    global Xr_cam, Yr_cam, obj_in_scene
    Xr_cam = data.data[0] #posicao em x
    Yr_cam = data.data[1] #posicao em y
    obj_in_scene = data.data[4] #conferir se tenho um objeto na escena ou nao

#funcao que chama os dados do GPS low cost, latitude e longitude do veiculo
def callbackGPS(data):
    global Xcar_o, Ycar_o
    #fazo a transformada de lat,long a um ponto em metros x,y
    Xcar_o, Ycar_o, z = lla2flat((data.latitude,data.longitude,data.altitude),(Lat_o,Lon_o),0,0)
    
if __name__ == '__main__':
    rospy.init_node('vilma_vision_position', anonymous=True)

    #suscribers
    rospy.Subscriber("compass_yaw", Float32MultiArray, callbackCompass)
    rospy.Subscriber("position_obj_R", Float32MultiArray, callbackObjPos)
    rospy.Subscriber("lowcost_gps", NavSatFix, callbackGPS)

    pub = rospy.Publisher('vilma_vision_position', Float32MultiArray)

    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()
    r = rospy.Rate(10)
    Xcar_m = []
    Ycar_m = []
    while not rospy.is_shutdown():
        if obj_in_scene:
            #calcula a posicao do ponto R[m], matriz de transformacao, com a funcao de rotacao (transformations.py)
            Xr_o,Yr_o = rotation(Theta_car, (Xcam_car + Xr_cam, Ycam_car + Yr_cam), (Xcar_o,Ycar_o))
            #print Xr_o,Yr_o

            #converte o ponto R [m] em uma coordenada [lat,long]. funcao flat2lla (transformations.py)
            lat,lon,h = flat2lla((Xr_o,Yr_o,0),(Lat_o,Lon_o),0,0)
            #print lat,lon

            #conexao com DB, tabela info_vilma
            conexion = psycopg2.connect(dbname='gis')
            cur = conexion.cursor()

            #distacia maxima para procurar
            d_max = 1000

            #ponto R[lat,long]
            point = str(lon) + " " + str(lat)
            
            #procurar o primeiro ponto mais perto lat, long
            search = "SELECT ST_AsText(ST_Transform(position,4326)), type, info, ST_Distance(ST_Transform(ST_GeomFromText('POINT(" + point + ")',4326),900913), position) FROM info_vilma WHERE ST_Distance(ST_Transform(ST_GeomFromText('POINT(" + point + ")',4326),900913), position) < " + str(d_max) + " ORDER BY ST_Distance(ST_Transform(ST_GeomFromText('POINT(" + point + ")',4326),900913), position) LIMIT 1"
            #print search

            cur.execute(search)

            p = cur.fetchall()

            conexion.commit()
            conexion.close()
            P = p[0][0]

            P =  P.split('(')[1].split(')')[0].split()
            #ponto mais perto na DB, em lat,long
            lat_star = float(P[1])
            lon_star = float(P[0])
            #mostra o ponto
            #print lat_star, lon_star

            #converte o ponto lat,lon da DB em um ponto em metros 
            Xr_star,Yr_star,Zr_star = lla2flat((lat_star,lon_star,0),(Lat_o,Lon_o),0,0)
            #print Xr_star, Yr_star
           
            #calcula a posicao em metros do ponto da DB, encontra o ponto do veiculo medida
            Xcar_aux,Ycar_aux = rotation(Theta_car, (- Xcam_car - Xr_cam, - Ycam_car - Yr_cam), (Xr_star, Yr_star))
            if Xcar_m:
                d = sqrt((Xcar_m - Xcar_aux)*(Xcar_m - Xcar_aux) + (Ycar_m - Ycar_aux)*(Ycar_m - Ycar_aux))
                if d < 10.0:
                    Xcar_m = Xcar_aux
                    Ycar_m = Ycar_aux
                    
                    array = Float32MultiArray()
                    array.data = [Xcar_m,Ycar_m,1]
                    pub.publish(array)
                    
                    #mostra o ponto da posicao do veiculo medida (DB) e a posicao do veiculo com o GPS lowcost
                    print "[",Xcar_m,Ycar_m,"][",Xcar_o,Ycar_o,"]"
                else:
                    array = Float32MultiArray()
                    array.data = [-1,-1,0]
                    #print "Punto muy lejano"
                    pub.publish(array)
            else:
                Xcar_m = Xcar_aux
                Ycar_m = Ycar_aux
                
                array = Float32MultiArray()
                array.data = [Xcar_m,Ycar_m,1]
                pub.publish(array)
                
                #mostra o ponto da posicao do veiculo medida (DB) e a posicao do veiculo com o GPS lowcost
                print "[",Xcar_m,Ycar_m,"][",Xcar_o,Ycar_o,"]"


           
        else:
            array = Float32MultiArray()
            array.data = [-1,-1,0]
            #print "Obj doesn't appear in the scene"
            pub.publish(array)

        r.sleep()
