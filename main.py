# importing 
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox #, QApplication
#from PyQt5.QtCore import QTimer
#from datetime import date
import sqlite3
#import time
import json
import sys
import webbrowser
import urllib.request 

# for data display later
#todays = str(date.today())

# getting json CEP data from AwesomeAPI
def printResults(data):
  dadosCEP = json.loads(data)
  if "cep" in dadosCEP:
      rua = dadosCEP['address_type']
      rua2 = dadosCEP['address_name']
      bairro = dadosCEP['district']
      estado = dadosCEP['state']
      cidade = dadosCEP['city']
      
      fouWin.lineEdit_10.setText(rua+' '+rua2)
      fouWin.lineEdit_11.setText(bairro)
      fouWin.lineEdit_12.setText(cidade)
      fouWin.lineEdit_13.setText(estado)
      fouWin.label.setText(' Por favor, digite o número do endereço do cliente') 
  else:
      fouWin.label.setText("Erro, não foi possível receber os dados.")         
  
# first window - login (need debug for incorrect data)  
def home():
    global user_name
    global user_pass
    firWin.label_5.setText("")
    user_name = firWin.lineEdit.text()
    user_pass = firWin.lineEdit_2.text()

    datab = sqlite3.connect('datab.db')
    cursor = datab.cursor()
    try:
        cursor.execute("SELECT login FROM cadastro")
        user_name_db = cursor.fetchall()
        #print(user_name_db)
        cursor.execute("SELECT senha FROM cadastro WHERE login ='{}'".format(user_name))
        pass_db = cursor.fetchall()
        print(pass_db[0][0])
        datab.close()
    except:
        firWin.label_5.setText("Erro ao validar o login")
        
    if user_name and user_pass != '':
        #for i in len(user_name_db[0][i]):
        #    print(i)
        
        #if user_name in user_name_db[0][0]:
            #print("yes")
        if user_pass == pass_db[0][0]:
            firWin.close()
            secWin.show()  
            secWin.label_3.setText(str(user_name))
        if user_pass != pass_db[0][0]:
            firWin.label_5.setText("Senha incorreta!")
    elif user_name and user_pass=='':
        firWin.label_5.setText("Digite o usuário e a senha.")

# show client table 
def showClientData():
    secWin.close()
    fifWin.show()
    datab = sqlite3.connect('datab.db')
    cursor = datab.cursor()
    cursor.execute("SELECT * FROM clientes")
    readed_data = cursor.fetchall()
    fifWin.tableWidget.setRowCount(len(readed_data))
    fifWin.tableWidget.setColumnCount(14)
    
    for i in range (0, len(readed_data)):
        for j in range(0, 14):
            fifWin.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(readed_data[i][j])))
    datab.close()
 
# sign up function    
def sign_up_db():
    usrname =  thiWin.lineEdit.text()
    login = thiWin.lineEdit_5.text()
    email = thiWin.lineEdit_2.text()  
    psd = thiWin.lineEdit_3.text()
    c_psd = thiWin.lineEdit_4.text()
    
    if (psd == c_psd):
        try:
            datab = sqlite3.connect('datab.db')
            cursor = datab.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (id INTEGER PRIMARY KEY AUTOINCREMENT, nome text NOT NULL, login text NOT NULL, email text NOT NULL, senha text NOT NULL)")
            cursor.execute("INSERT INTO cadastro VALUES (NULL ,'"+usrname+"','"+login+"','"+email+"','"+psd+"')")
            datab.commit()
            datab.close()
            
            cleanText()
            
            msg = QMessageBox()
            msg.setWindowTitle("Sucesso")
            msg.setText("Usuário cadastrado com sucesso")
            cleanText()
            
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QtGui.QIcon('./img/logo.png'))
            msg.setDefaultButton(QMessageBox.Ok)
            x = msg.exec_()

            log_in()
            
        except sqlite3.Error as erro:
            print("Erro ao inserir os dados: ", erro)
    else:
        thiWin.label_7.setText("As senhas precisam ser iguais!")

def savePdf():
    nome =  fouWin.lineEdit.text()
    email = fouWin.lineEdit_7.text()
    cpf = fouWin.lineEdit_2.text()  
    rg = fouWin.lineEdit_6.text()
    celular = fouWin.lineEdit_3.text()
    telefone = fouWin.lineEdit_5.text()
    obs = fouWin.lineEdit_4.text()
    cept = fouWin.lineEdit_8.text()
    endereco = fouWin.lineEdit_10.text()
    numendereco = fouWin.lineEdit_9.text()
    bairro = fouWin.lineEdit_11.text()
    cidade = fouWin.lineEdit_12.text()
    estado = fouWin.lineEdit_13.text()
    dadosPDF = "Nome: "+nome+"\nE-mail: "+email+"\nCPF: "+cpf+"\nCelular: "+celular+"\nObservação: "+obs+"\nCEP: "+cept+"\nEndereço: "+endereco+", "+numendereco+", "+bairro+", "+cidade+", "+estado+"."
    filePDF = QtWidgets.QFileDialog.getSaveFileName()[0]
    with open (filePDF + '.txt', 'w') as file:
        file.write(dadosPDF)

    # registering client
def client_register():
 

    nome =  fouWin.lineEdit.text()
    email = fouWin.lineEdit_7.text()
    cpf = fouWin.lineEdit_2.text()  
    rg = fouWin.lineEdit_6.text()
    celular = fouWin.lineEdit_3.text()
    telefone = fouWin.lineEdit_5.text()
    obs = fouWin.lineEdit_4.text()
    cept = fouWin.lineEdit_8.text()
    endereco = fouWin.lineEdit_10.text()
    numendereco = fouWin.lineEdit_9.text()
    bairro = fouWin.lineEdit_11.text()
    cidade = fouWin.lineEdit_12.text()
    estado = fouWin.lineEdit_13.text()
    cleanText()
    
    if ( 1==1 ):
        try:
            datab = sqlite3.connect('datab.db')
            cursor = datab.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, email TEXT NOT NULL, cpf INTEGER, rg INTEGER,celular INTEGER NOT NULL, telefone INTEGER, obs TEXT, cept INTEGER, endereco TEXT, numendereco INTEGER, bairro TEXT, cidade TEXT, estado TEXT)")
            datab.commit()
            cursor.execute("INSERT INTO clientes VALUES (NULL,'"+nome+"','"+email+"','"+cpf+"','"+rg+"','"+celular+"','"+telefone+"','"+obs+"','"+cept+"','"+endereco+"','"+numendereco+"','"+bairro+"','"+cidade+"','"+estado+"')")
    
            datab.commit()
            datab.close()
            
            msg2 = QMessageBox()
            msg2.setWindowTitle("Sucesso")
            msg2.setText("Cliente cadastrado com sucesso")
            msg2.setIcon(QMessageBox.Information)
            msg2.setWindowIcon(QtGui.QIcon('./img/logo.png'))
            x = msg2.exec_()
            fouWin.label.setText("")
            fouWin.close()
            secWin.show()
    
        except sqlite3.Error as erro:
            print("Erro ao inserir os dados: ", erro)

# getting CEP from AwesomeAPI
def cep():
    cep = fouWin.lineEdit_8.text()
    urlData = 'https://cep.awesomeapi.com.br/json/'+cep
    webUrl = urllib.request.urlopen(urlData)   
    if (webUrl.getcode() == 200 ):
        data = webUrl.read()
        printResults(data)
    else:
        fouWin.label.setText("Erro, não foi possível receber os dados.")    

def deleteClient():
    datab = sqlite3.connect('datab.db')
    line = fifWin.tableWidget.currentRow()
    fifWin.tableWidget.removeRow(line)

    cursor = datab.cursor()
    cursor.execute("SELECT id FROM clientes")
    dadosClientes = cursor.fetchall()
    idValue = dadosClientes[line][0]
    cursor.execute("DELETE FROM clientes WHERE id="+ str(idValue))
    datab.commit()
    
def updateClient(): 
    fifWin.close()
    sixWin.show()
    datab = sqlite3.connect('datab.db')
    line = fifWin.tableWidget.currentRow()

    cursor = datab.cursor()
    cursor.execute("SELECT id FROM clientes")
    dadosClientes = cursor.fetchall()
    idValue = dadosClientes[line][0]
    cursor.execute("SELECT * FROM clientes WHERE id="+ str(idValue))
    clientData = cursor.fetchall()

    sixWin.lineEdit.setPlaceholderText(str(clientData[0][0]))
    sixWin.lineEdit_2.setPlaceholderText(str(clientData[0][1]))
    sixWin.lineEdit_4.setPlaceholderText(str(clientData[0][2]))
    sixWin.lineEdit_3.setPlaceholderText(str(clientData[0][3]))
    sixWin.lineEdit_5.setPlaceholderText(str(clientData[0][4]))
    sixWin.lineEdit_6.setPlaceholderText(str(clientData[0][5]))
    sixWin.lineEdit_7.setPlaceholderText(str(clientData[0][6]))
    sixWin.lineEdit_8.setPlaceholderText(str(clientData[0][7]))
    
        
# log out - need to create checkbox for saving login info
def log_out():
    user_name = firWin.lineEdit.text()
    user_pass = firWin.lineEdit_2.text() 
    
    secWin.close()
    checkbx()
    firWin.show()

# closing and opening windows~    
def sign_up():
    firWin.close()
    thiWin.show()
    
def log_in():
    thiWin.close()
    cleanText()
    firWin.show()

def create_clientWin():
    secWin.close()
    fouWin.show()
    
def create_saleWin():
    secWin.close()
    fifWin.show()

def create_client():
    secWin.close()
    fouWin.show()
 
def cancel():
    fouWin.close()
    secWin.show()    

def leave_clients():
    fifWin.close()
    secWin.show()

def checkbx():
    if (firWin.checkBox.isChecked()):
        fifWin.lineEdit.setText(user_name)
        firWin.lineEdit_2.setText(user_pass)
    else:
        cleanText()

# clean text after deploy
def cleanText():
  firWin.lineEdit.setText('')
  firWin.lineEdit_2.setText('')
  firWin.label_5.setText('')
  thiWin.lineEdit.setText("")
  thiWin.lineEdit_2.setText("")
  thiWin.lineEdit_3.setText("")
  thiWin.lineEdit_4.setText("")
  thiWin.lineEdit_5.setText("")
  fouWin.lineEdit.setText('')
  fouWin.lineEdit_2.setText('')
  fouWin.lineEdit_3.setText('')
  fouWin.lineEdit_4.setText('')
  fouWin.lineEdit_5.setText('')
  fouWin.lineEdit_6.setText('')
  fouWin.lineEdit_7.setText('')
  fouWin.lineEdit_8.setText('')
  fouWin.lineEdit_9.setText('')
  fouWin.lineEdit_10.setText('')
  fouWin.lineEdit_11.setText('')
  fouWin.lineEdit_12.setText('')
  fouWin.lineEdit_13.setText('')

def leaveUpdating():
    sixWin.close()
    fifWin.show()


def UpdateCred():
    secWin.close()
    sevWin.show()
    
def openSite():
    webbrowser.open('https://graficaaquarela2.lojavirtualnuvem.com.br', new=1, autoraise=True)
 
def openInsta():
    webbrowser.open('https://www.instagram.com/grafica.aquarela', new=1, autoraise=True)
def openFace(): 
    webbrowser.open('https://www.facebook.com/grafica.aquarela494', new=1, autoraise=True)
def openWhats():       
    webbrowser.open('https://whats.link/graficaaquarelaa', new=1, autoraise=True)    
    
def saveUpdateCred():
    sevWin.label_2.setText("")
    newpwd = sevWin.lineEdit_4.text()
    c_newPwd = sevWin.lineEdit_5.text()
    if newpwd == c_newPwd:
        print("ok")
    else:
        sevWin.label_2.setText("As senhas precisam ser iguais!")    
    
def leaveUpdateCred():
    sevWin.close()
    secWin.show()

def enter():
    zeroWin.close()
    firWin.show()

def openr():
    time.sleep(2)
    zeroWin.close()
    firWin.show()

app = QtWidgets.QApplication([])

# windows
zeroWin = uic.loadUi("./window/win0.ui") # first window
firWin = uic.loadUi("./window/win1.ui") # login
secWin = uic.loadUi("./window/win2.ui") # home 
thiWin = uic.loadUi("./window/win3.ui") # account register
fouWin = uic.loadUi("./window/win4.ui") # client register
fifWin = uic.loadUi("./window/win5.ui") # client show
sixWin = uic.loadUi("./window/win6.ui")
sevWin = uic.loadUi("./window/win7.ui")

# events
zeroWin.pushButton.clicked.connect(enter)
zeroWin.pushButton_2.clicked.connect(openSite)
zeroWin.pushButton_3.clicked.connect(openFace)
zeroWin.pushButton_4.clicked.connect(openWhats)
zeroWin.pushButton_5.clicked.connect(openInsta)

firWin.pushButton.clicked.connect(home) # login
firWin.pushButton_2.clicked.connect(sign_up) # signup
firWin.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password) # *** in password 
firWin.pushButton_3.clicked.connect(openSite)
firWin.pushButton_4.clicked.connect(openFace)
firWin.pushButton_5.clicked.connect(openWhats)
firWin.pushButton_6.clicked.connect(openInsta)

secWin.pushButton.clicked.connect(log_out) # log out
secWin.pushButton_2.clicked.connect(showClientData) # show clients
secWin.pushButton_6.clicked.connect(UpdateCred)
secWin.pushButton_11.clicked.connect(showClientData) # show clients too
# secWin.pushButton_9.clicked.connect(create_sale) - need to create this!!
secWin.pushButton_15.clicked.connect(create_client) #r egister client in database
secWin.pushButton_7.clicked.connect(openSite)
secWin.pushButton_8.clicked.connect(openFace)
secWin.pushButton_9.clicked.connect(openWhats)
secWin.pushButton_12.clicked.connect(openInsta)

thiWin.pushButton_2.clicked.connect(log_in) # log in "already have an account?"
thiWin.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password) # *** in pwd
thiWin.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)# *** in pwd
thiWin.pushButton.clicked.connect(sign_up_db)# registering in database
thiWin.pushButton_3.clicked.connect(openSite)
thiWin.pushButton_4.clicked.connect(openFace)
thiWin.pushButton_5.clicked.connect(openWhats)
thiWin.pushButton_6.clicked.connect(openInsta)


fouWin.pushButton_4.clicked.connect(cancel)# back
fouWin.pushButton_5.clicked.connect(savePdf)
fouWin.pushButton_3.clicked.connect(client_register)# register client in database
fouWin.pushButton.clicked.connect(cep)# gets CEP json data from AwesomeAPI

fifWin.pushButton_12.clicked.connect(leave_clients)# back from clients table
fifWin.pushButton_10.clicked.connect(deleteClient)
fifWin.pushButton_11.clicked.connect(updateClient)

#sixWin.pushButton_14;clicked.connect(SaveUpdateClient)
sixWin.pushButton_15.clicked.connect(leaveUpdating)

sevWin.pushButton_14.clicked.connect(saveUpdateCred)
sevWin.pushButton_15.clicked.connect(leaveUpdateCred)
sevWin.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
sevWin.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.Password)
sevWin.pushButton_2.clicked.connect(openSite)
sevWin.pushButton_5.clicked.connect(openInsta)
sevWin.pushButton_3.clicked.connect(openFace)
sevWin.pushButton_4.clicked.connect(openWhats)

#    app = QApplication(sys.argv)
#    window = uic.loadUi("./window/win0.ui")
#    window.show()
#    QTimer.singleShot (2000, window.close)
#    sys.exit(app.exec())
    
# app init
zeroWin.show()
#openr()
app.exec()