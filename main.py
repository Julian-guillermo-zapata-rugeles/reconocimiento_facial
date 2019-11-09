	
import os
#OpenCV module
import cv2
#OpenCV trabaja con arreglos de numpy
import numpy
#Se importa la lista de personas con acceso al laboratorio
os.system("clear")
print("iniciando reconocimiento")
# Parte 1: Creando el entrenamiento del modelo
#Directorio donde se encuentran las carpetas con las caras de entrenamiento
dir_faces = 'att_faces/orl_faces'
#Tamaño para reducir a miniaturas las fotografias
size = 4

# Crear una lista de imagenes y una lista de nombres correspondientes
(images, lables, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(dir_faces):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(dir_faces, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            lable = id
            images.append(cv2.imread(path, 0))
            lables.append(int(lable))
        id += 1
(im_width, im_height) = (112, 92)

# Crear una matriz Numpy de las dos listas anteriores
(images, lables) = [numpy.array(lis) for lis in [images, lables]]
# OpenCV entrena un modelo a partir de las imagenes
print("")
model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, lables)


# Parte 2: Utilizar el modelo entrenado en funcionamiento con la camara
face_cascade = cv2.CascadeClassifier( 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

while True:
    #leemos un frame y lo guardamos
    rval, frame = cap.read()
    frame=cv2.flip(frame,1,0)

    #convertimos la imagen a blanco y negro    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #redimensionar la imagen
    mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))

    """buscamos las coordenadas de los rostros (si los hay) y
   guardamos su posicion"""
    faces = face_cascade.detectMultiScale(mini)
    
    for i in range(len(faces)):
        face_i = faces[i]
        (x, y, w, h) = [v * size for v in face_i]
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (im_width, im_height))

        # Intentado reconocer la cara
        prediction = model.predict(face_resize)
        
         #Dibujamos un rectangulo en las coordenadas del rostro
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        
        # Escribiendo el nombre de la cara reconocida
        # La variable cara tendra el nombre de la persona reconocida
        cara = '%s' % (names[prediction[0]])

        #Si la prediccion tiene una exactitud menor a 100 se toma como prediccion valida
        if prediction[1]<100 :
          #Ponemos el nombre de la persona que se reconoció
          cv2.putText(frame,'%s - %.0f' % (cara,prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
          comando="notify-send "+"' Hola "+str(cara)+" Bienvenido!'"
          os.system(comando)
          #os.system("mpg123 pitido.mp3")
          exit()
          #En caso de que la cara sea de algun conocido se realizara determinadas accione          

        #Si la prediccion es mayor a 100 no es un reconomiento con la exactitud suficiente
        elif prediction[1]>101 and prediction[1]<500:           
            #Si la cara es desconocida, poner desconocido
            cv2.putText(frame, 'Desconocido',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
            os.system("notify-send 'Posible Error de seguridad'")
            os.system("mpg123 pitido.mp3")
            data=open("accesos","a")
            data=data.write("1")
            exit()
        #Mostramos la imagen
        cv2.imshow('OpenCV Reconocimiento facial', frame)


    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyAllWindows()
        break

