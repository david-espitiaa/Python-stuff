import pymysql
import random
import time
from PyQt5 import QtWidgets, uic, QtCore
import pyqtgraph as pg
from pushbullet import PushBullet

app = QtWidgets.QApplication([])
gui = uic.loadUi('acceso.ui')
gui2 = uic.loadUi('registro.ui')
gui3 = uic.loadUi('visualizar.ui')
gui4 = uic.loadUi('graficartablas.ui')


timer = QtCore.QTimer()
timer.setInterval(1000)

pb = PushBullet('o.c24gYX9kPZNAzV9hHe3hqcKnr3S7sgH3')
dev1 = pb.new_device('LAPTOP-R3EGDAGH')


def salir():
    gui.destroy()
   
def registro():
    gui.hide()
    gui2.show()
   
def accesoUsuario():
    try:
        #Verificamos la conexión a la DB
        db = pymysql.connect(host='localhost',user='root',password='boom99xd',database='USERS_IET701')
       
        cursor = db.cursor()
       
        user = gui.user.text()
        paswd = gui.pswrd.text()
       
        sql = "SELECT Usuario,Password FROM Users WHERE Usuario=%s and Password=%s"
       
        data = cursor.execute(sql,(user,paswd))
       
        if (len(cursor.fetchall())>0):
            gui.hide()
            gui3.show()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('ALERTA')
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setText('Datos Incorrectos de Acceso')
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
       
        db.close()
    except Exception as e:
        print(e)
 
def insertar_valores():
    db = pymysql.connect(host='localhost',user='root',password='boom99xd', database='USERS_IET701')
   
    cursor = db.cursor()
   
    user = gui2.usuario.text()
    pswd = gui2.password.text()
    cpswd = gui2.cpass.text()
   
    if pswd == cpswd:
       
               
        sql4 = "INSERT INTO Users(Usuario, Password) VALUES(%s,%s)"
        cursor.execute(sql4,(user,pswd))
        db.commit()
        sql9 = "SELECT * FROM Users"
        cursor.execute(sql9)
        datos = cursor.fetchall()
        for dato in datos:
            print(f"Valor de tabla es: {dato}")
       
        db.close()
       
    else:
        msj = QtWidgets.QMessageBox()
        msj.setWindowTitle('Error')
        msj.setText("Las contraseñas no coinciden")
        msj.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msj.exec_()
 
def visualizar_tabla():
    try:
        #Verificamos la conexión a la DB
        db = pymysql.connect(host='localhost',user='root',password='boom99xd',database='USERS_IET701')
       
        cursor = db.cursor()
       
        sql = "SELECT * FROM Sensor1"
       
        cursor.execute(sql)
       
        tabla = cursor.fetchall()
       
        gui3.tableWidget.setRowCount(0)
 
        for no_fila, dato_fila in enumerate(tabla):
            gui3.tableWidget.insertRow(no_fila)
            for no_columna, dato in enumerate(dato_fila):
                dato = QtWidgets.QTableWidgetItem(str(dato))
                gui3.tableWidget.setItem(no_fila,no_columna,dato)
       
        db.close()
    except Exception as e:
        print(e)
       
def Salir():
    gui2.destroy()
    gui.show()
 
def graftemp():
    try:
        db = pymysql.connect(host='localhost',user='root',password='boom99xd',database='USERS_IET701')
        cursor = db.cursor()
        sql = "SELECT Temperatura FROM Sensor1"
        cursor.execute(sql)
        data = cursor.fetchall()
        db.close()
        valores = [i[0] for i in data]
        return valores
    except Exception as e:
        print(e)

def grafhum():
    try:
        db = pymysql.connect(host='localhost',user='root',password='boom99xd',database='USERS_IET701')
        cursor = db.cursor()
        sql = "SELECT Humedad FROM Sensor1"
        cursor.execute(sql)
        data = cursor.fetchall()
        db.close()
        valores = [i[0] for i in data]
        return valores
    except Exception as e:
        print(e)



gui4.grafica1.setBackground('w')
gui4.grafica1.setTitle("Humedad", color="r", size="15pt")
gui4.grafica1.setLabel("left", "Valor", color="r", size=10)
gui4.grafica1.setLabel("bottom", "Dato", color="r", size=10)
gui4.grafica1.addLegend()
gui4.grafica1.showGrid(x=True, y=True)
gui4.grafica1.setYRange(0, 100, padding=0.1)
xdata = []
ydata = []
grafica1 = gui4.grafica1.plot(xdata, ydata, pen=pg.mkPen(color="g", width=2))

gui4.grafica2.setBackground('w')
gui4.grafica2.setTitle("Temperatura", color="r", size="15pt")
gui4.grafica2.setLabel("left", "Valor", color="r", size=10)
gui4.grafica2.setLabel("bottom", "Dato", color="r", size=10)
gui4.grafica2.addLegend()
gui4.grafica2.showGrid(x=True, y=True)
gui4.grafica2.setYRange(-20, 200, padding=0.1)
xdata2 = []
ydata2 = []
grafica2 = gui4.grafica2.plot(xdata2, ydata2, pen=pg.mkPen(color="g", width=2))


def update_mysql_data():
    global ydata, xdata
    global ydata2, xdata2
    gui3.hide()
    gui4.show()

    ydata = grafhum()  # Obtener los valores de la columna 'valor'
    xdata = list(range(len(ydata)))  # Crear una lista de índices para el eje X
    grafica1.setData(xdata, ydata)  # Actualizar el gráfico con los datos

    ydata2 = graftemp()  # Obtener los valores de la columna 'valor'
    xdata2 = list(range(len(ydata2)))  # Crear una lista de índices para el eje X
    grafica2.setData(xdata2, ydata2)  # Actualizar el gráfico con los datos


    tiempoReal()
    timer.timeout.connect(tiempoReal)
    timer.start()


def tiempoReal():
    try:
        # Variables globales para los datos de los gráficos
        global xdata, ydata
        global ydata2, xdata2

        # Generar valores aleatorios para "Temperatura" y "Humedad"
        nuevo_valor = random.uniform(0, 100)  # Valor aleatorio para "Temperatura"
        nuevo_valor2 = random.uniform(-20, 200)  # Valor aleatorio para "Humedad"

        # Actualizar los datos en las listas locales
        ydata.append(nuevo_valor)
        xdata = list(range(len(ydata)))

        ydata2.append(nuevo_valor2)
        xdata2 = list(range(len(ydata2)))

        # Limitar el número de puntos visibles (por ejemplo, solo mostrar los últimos 100)
        if len(xdata) > 100:
            xdata = xdata[1:]  # Eliminar el primer elemento de la lista
            ydata = ydata[1:]  # Eliminar el primer elemento de la lista

        if len(xdata2) > 100:
            xdata2 = xdata2[1:]  # Eliminar el primer elemento de la lista
            ydata2 = ydata2[1:]  # Eliminar el primer elemento de la lista

        if nuevo_valor > 180:
            pb.push_note("ALERTA","Temperatura Alta")
        else:
            pass

        if nuevo_valor2 > 90:
            pb.push_note("ALERTA","Temperatura Alta")
        else:
            pass
        

        # Conectarse a la base de datos
        db = pymysql.connect(host='localhost', user='root', password='boom99xd', database='USERS_IET701')
        cursor = db.cursor()

        # Insertar los nuevos valores directamente en la base de datos
        sql = "INSERT INTO Sensor1 (Temperatura, Humedad) VALUES (%s, %s)"
        cursor.execute(sql, (nuevo_valor, nuevo_valor2))
        db.commit()

        # Actualizar los gráficos con los nuevos datos generados
        grafica1.setData(xdata, ydata)
        grafica2.setData(xdata2, ydata2)

        # Cerrar la conexión con la base de datos
        db.close()

        timer.timeout.connect(update_mysql_data)
    except Exception as e:
        print(e)



def stopTiempo():
    timer.stop()

def regresartablas():
    gui3.show()
    gui4.hide()





gui.btnAcceso.clicked.connect(accesoUsuario)
gui.btnRegistro.clicked.connect(registro)
gui.actionSalir.triggered.connect(salir)
   
gui2.insertar_valores.clicked.connect(insertar_valores)
gui2.btnsalir.clicked.connect(Salir)
 
gui3.btnTabla.clicked.connect(visualizar_tabla)
gui3.btnGraficar.clicked.connect(update_mysql_data)

gui4.btnRegresar.clicked.connect(regresartablas)
#gui4.btnTiempo.clicked.connect(tiempoReal)
gui4.btnStopTiempo.clicked.connect(stopTiempo)
 
gui.show()
app.exec()