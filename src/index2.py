from __future__ import absolute_import
from __future__  import division
from __future__ import print_function



import MySQLdb
#import cv2

import pandas as pd
import os
import pickle
from sklearn.model_selection import train_test_split

from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import icons
from PyQt5.uic import loadUiType

from src.main2 import Ui_Form

MainUI, _ = loadUiType('./main1.ui')
finger_print_in = ""



def progress_dialog(message):
    prgr_dialog = QProgressDialog()
    prgr_dialog.setFixedSize(300, 50)
    prgr_dialog.setAutoFillBackground(True)
    prgr_dialog.setWindowModality(Qt.WindowModal)
    prgr_dialog.setWindowTitle('Please wait')
    prgr_dialog.setLabelText(message)
    prgr_dialog.setSizeGripEnabled(False)
    prgr_dialog.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    prgr_dialog.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
    prgr_dialog.setWindowFlag(Qt.WindowCloseButtonHint, False)
    prgr_dialog.setModal(True)
    prgr_dialog.setCancelButton(None)
    prgr_dialog.setRange(0, 0)
    prgr_dialog.setMinimumDuration(0)
    prgr_dialog.setAutoClose(False)
    return prgr_dialog

def data_info(direct):
    files = [file.strip() for file in os.listdir('./data/' + direct)]
    filenames = []
    for file in files:
        add = [file[:-4], file[0]]
        filenames.append(add)
    return filenames

def pixel_info(direct, df):
    pixels = []
    for file in list(df['filename']):
        from PIL import Image
        im = Image.open('./data/' + direct + '/' + file + '.bmp')
        pix = list(im.getdata())
        pixels.append(pix)
    df_pix = pd.DataFrame(pixels, columns=list(range(144 ** 2)))
    return df_pix

def pixel_info_one(df):
    print("Att : " , finger_print_in)
    pixels = []
    from PIL import Image
    im = Image.open(finger_print_in)
    pix = list(im.getdata())
    pixels.append(pix)
    print("pixels : " )
    print("pixels : ", pixels)
    df_pix = pd.DataFrame(pixels, columns=list(range(144 ** 2)))
    print("df_prix", df_pix)
    return df_pix

#################################################################
#################################################################


class Main(QMainWindow, MainUI):


    def openWindow(self , a):
        self.widow = QtWidgets.QMainWindow()
        self.ui = Ui_Form()

        sql = ('''   SELECT * FROM persons WHERE id_person = %s''')
        self.cur.execute(sql , [(a)])

        data = self.cur.fetchone()

        print(data)

        self.ui.setupUi(self.widow, str(data[1]) , str(data[2]) ,str(data[3]) ,str(data[4]) ,str(data[5]) ,str(data[6]) ,str(data[7]) ,str(data[8]))
        self.widow.show()

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon('./icons/zaa.png'))
        self.figer_select = ""
        self.image_select = ""
        self.finger = ""
        self.setupUi(self)
        self.UI_Changes()
        self.Db_Connect()
        self.Handel_Buttons()

        self.show_all_persons()
        self.show_all_persons_table()


#################################################################
#################################################################

    def UI_Changes(self):
        #UI changes in login
        self.tabWidget.tabBar().setVisible(False)
        self.setWindowTitle('Fingerprint Recognition')
        self.setWindowIcon(QIcon('./icons/zaa.png'))

    def Db_Connect(self):
        #connection between app and DB
        self.db = MySQLdb.connect(host='localhost', user='ibrahim', password='!brahim', db='myapp')
        self.cur = self.db.cursor()
        print('Connection Accepted')

    def Handel_Buttons(self):
        #Our buttons
        self.pushButton.setToolTip('Go to the home tab')
        self.pushButton.clicked.connect(self.Open_Home_tab)

        self.pushButton_2.setToolTip('Go to the persons tab')
        self.pushButton_2.clicked.connect(self.Open_Person_tab)

        self.pushButton_3.setToolTip('Go to the information tab')
        self.pushButton_3.clicked.connect(self.Open_Info_tab)

        self.pushButton_4.setToolTip('Run the application in Real time')
        self.pushButton_4.clicked.connect(self.finger_Print_Proc)

        self.pushButton_5.setToolTip('Search about the persons')
        self.pushButton_5.clicked.connect(self.Edit_persons_search)

        self.pushButton_6.setToolTip('Save Change')
        self.pushButton_6.clicked.connect(self.Edit_persons_save)

        self.pushButton_7.setToolTip('Clicked for add new person')
        self.pushButton_7.clicked.connect(self.Add_Person)

        self.pushButton_8.setToolTip('Delete this person!!')
        self.pushButton_8.clicked.connect(self.Delete_persons)

        self.pushButton_9.clicked.connect(self.display_image_in_ADD_persons)

        self.pushButton_10.clicked.connect(self.display_image_in_edit_persons)

        self.pushButton_11.clicked.connect(self.display_finger_in_ADD_persons)


#################################################################
#################################################################

    def displayImage(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        global image_in
        image_in, _ = QFileDialog.getOpenFileName(self, "Select an image", "",
                                                         "image Files (*.jpg)", options=options)
        print("---- file selected is : ", image_in)

        self.image_select = image_in

        if image_in != "":
            QMessageBox.information(self, "[INFO]", "The image is loaded")

        else:
            QMessageBox.information(self, "[INFO]", "No Image loaded")


    def displayFinger(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        global finger_in
        finger_in, _ = QFileDialog.getOpenFileName(self, "Select an Finger", "",
                                                         "image Files (*.bmp)", options=options)
        print("---- file selected is : ", finger_in)

        self.finger = finger_in

        if finger_in != "":
            QMessageBox.information(self, "[INFO]", "The Finger is loaded")

        else:
            QMessageBox.information(self, "[INFO]", "No Finger loaded")


    def display_image_in_ADD_persons(self):

        self.displayImage()

        self.label_5.setScaledContents(True)
        pixmap = QPixmap(self.image_select)
        self.label_5.setPixmap(pixmap)
        self.label_5.repaint()
        QApplication.processEvents()


    def display_finger_in_ADD_persons(self):

        self.displayFinger()

        self.label_7.setScaledContents(True)
        pixmap = QPixmap(self.finger)
        self.label_7.setPixmap(pixmap)
        self.label_7.repaint()
        QApplication.processEvents()


    def display_image_in_edit_persons(self):

        self.displayImage()

        self.label_13.setScaledContents(True)
        pixmap = QPixmap(self.image_select)
        self.label_13.setPixmap(pixmap)
        self.label_13.repaint()
        QApplication.processEvents()

    ######################################################"

    def Add_Person(self):
        add_person_id = self.lineEdit_12.text()
        add_person_name = self.lineEdit_4.text()
        add_person_prename = self.lineEdit_8.text()
        temporaire_variable = self.dateEdit.date()
        add_person_birthday = temporaire_variable.toPyDate()
        add_person_phone = self.lineEdit_11.text()
        add_person_mail = self.lineEdit_10.text()

        add_person_image = self.image_select
        add_person_finger = self.finger
        if(add_person_id == '' or add_person_name=='' or add_person_prename =='' or add_person_finger==''):
            QMessageBox.information(self, "Error", 'Some important fields are empty')
            self.statusBar().showMessage('Be careful!! Some important fields are empty')
            return

        sql = ('''
                    INSERT INTO persons (id_person , name , lName , birthdate ,phone , mail , image , finger)
                    VALUES (%s , %s , %s , %s , %s , %s , %s , %s)    
                    ''')
        self.cur.execute(sql , (add_person_id, add_person_name, add_person_prename, add_person_birthday, add_person_phone, add_person_mail , add_person_image , add_person_finger))

        self.db.commit()
        self.show_all_persons()
        self.show_all_persons_table()
        print('Person Added')
        QMessageBox.information(self, "Success", 'Person added successfully')
        self.statusBar().showMessage('Person added successfully')

    def show_all_persons(self):             ####### for combobox in search in edit person
        self.comboBox.clear()
        self.cur.execute('''
            SELECT * FROM persons
        ''')

        person = self.cur.fetchall()

        for persons in person :
            self.comboBox.addItem(str(persons[1]))


    def show_all_persons_table(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        self.cur.execute('''
            SELECT id_person , name , lName , birthdate , phone , mail FROM persons 
        ''')
        data = self.cur.fetchall()

        for row , form in enumerate(data):
            for col , item in enumerate(form):
                self.tableWidget.setItem(row , col , QTableWidgetItem(str(item)))
                col += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)


    def Edit_persons_search(self):
        id_p = self.comboBox.currentText()

        sql = ('''   SELECT * FROM persons WHERE id_person = %s  ''')
        self.cur.execute(sql , [(id_p)])
        data = self.cur.fetchone()
        print(data)

        self.lineEdit_2.setText(str(data[2]))
        self.lineEdit_3.setText(str(data[3]))
        self.lineEdit_5.setText(str(data[4]))
        self.lineEdit_6.setText(str(data[5]))
        self.lineEdit_7.setText(str(data[6]))
        img = data[7]
        print(img)
        self.label_13.setScaledContents(True)
        pixmap = QPixmap(str(img))
        self.label_13.setPixmap(pixmap)
        self.label_13.repaint()
        QApplication.processEvents()


    def Edit_persons_save(self):
        id_person = self.comboBox.currentText()

        edit_person_name = self.lineEdit_2.text()
        edit_person_lName = self.lineEdit_3.text()
        edit_person_birthday = self.lineEdit_5.text()
        edit_person_phone = self.lineEdit_6.text()
        edit_person_mail = self.lineEdit_7.text()

        edit_person_image = self.image_select


        self.cur.execute('''
            UPDATE persons SET name = %s , lName = %s , birthdate = %s , phone = %s , mail = %s , image = %s WHERE id_person = %s
        ''',(edit_person_name,edit_person_lName,edit_person_birthday,edit_person_phone,edit_person_mail,edit_person_image,id_person))

        self.db.commit()
        self.show_all_persons_table()

        QMessageBox.information(self , "Success" ,'Information changed successfully')
        self.statusBar().showMessage('Information changed successfully')


    def Delete_persons(self):
        id_person = self.comboBox.currentText()

        result = QMessageBox.warning(self , 'Delete person' , 'Are you sure to delete this information??' , QMessageBox.Yes | QMessageBox.No )

        if (result == QMessageBox.Yes) :
            sql = ('''   DELETE FROM persons where id_person = %s   ''')
            self.cur.execute(sql , [(id_person)])
            self.db.commit()
            self.statusBar().showMessage('Person deleted successfully')
            QMessageBox.information(self, "Success", 'Person deleted successfully')
            self.show_all_persons_table()
            self.show_all_persons()
        else:
            print('nothing deleted')


########################################################
########################################################
    
    def Open_Home_tab(self):
        print("Home open")
        self.tabWidget.setCurrentIndex(0)

    def Open_Person_tab(self):
        print("Person open")
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(0)

    def Open_Info_tab(self):
        print("About open")
        self.tabWidget.setCurrentIndex(2)
        ##############################


####################################################################
####################################################################

    def finger_Print_Proc(self):
        print("part temp real is opened")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        global finger_print_in
        finger_print_in, _ = QFileDialog.getOpenFileName(self, "Select an fingerprint ", "",
                                                               "image Files (*.bmp)", options=options)
        print("---- file selected is : ", finger_print_in)

        self.figer_select = finger_print_in
        if finger_print_in != "":
            QMessageBox.information(self, "[INFO]", "the fingerprint is loaded")
            self.next_proces()

        else:
            QMessageBox.information(self, "[INFO]", "No fingerprint loaded")



    def next_proces(self):
        print ("inside the next")
        print("---- file selected is : ", self.figer_select)

        fullfile = os.path.basename(self.figer_select)
        filename = os.path.splitext(fullfile)
        print("file name : : ", filename[0])
        #df_test = data_info(direct='test')
        df_test = [[str(filename[0]), '1']]
        print("TEST  is loaded")
        df_train = data_info(direct='train')
        print("Train is loaded")

        train = pd.DataFrame(df_train, columns=['filename', 'label'])
        test = pd.DataFrame(df_test, columns=['filename', 'label'])
        print("files is good")

        train_pix = pixel_info('train', train)
        test_pix = pixel_info_one(test)


        X_train, X_val, y_train, y_val = train_test_split(train_pix.values, train['label'], test_size=0.3,
                                                          random_state=42, shuffle=True, stratify=None)
        print("end of trian")

        with open('model/model_cb.pkl', 'rb') as f:
            best = pickle.load(f)


        val_pred = best.predict(X_val)
        pred = pd.DataFrame(val_pred)
        pred = list(pred.iloc[:, 0])
        val = list(y_val)

        test_pred = best.predict(test_pix.values)
        test['label'] = test_pred
        test['filename'] = pd.to_numeric(test["filename"])

        result = test.sort_values(by=['filename'], ascending=True)

        print("fileName : ", result['filename'][0])
        print("label: ", result['label'][0])

        ###################################

        id_p = str(result['label'][0])
        self.cur.execute('''    select id_person from persons    ''')
        idd = self.cur.fetchall()
        a = 0
        for x in idd :
            if (id_p == str(x[0])) :
                QMessageBox.information(self, "[INFO]",
                                        "This finger print is already exist , ID of the persons is : " + str(result['label'][0]))
                self.openWindow(id_p)
                a = str(x[0])
                break
        if(a != str(x[0])):
            QMessageBox.information(self, "INFO", "This Person Not Exist !! \n Can't Show any Information ")


#################################################################
#################################################################

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


if  __name__ == '__main__':
    main()