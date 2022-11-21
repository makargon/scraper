from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QThread
import sys
import csv
import Scrap_copy as Scrap

scrapper = Scrap.Scrap()
class Scrapper(QThread):# Класс второго потока, чтобы не вис интерфейс, QThread
    command="openBrowser"
    def __init__(self, parent=None):
        super(Scrapper, self).__init__(parent)
        self.value = 0
    def run(self): # Стандартная функция потока
        if self.command=="openBrowser": scrapper.openBrowser()
        elif self.command=="scraping": scrapper.adds_analyze()
        elif self.command=="call_analyze": scrapper.call_analyze()
        elif self.command=="stop": scrapper.stop()
        elif self.command=="closeBrowser": scrapper.closeBrowser()
        elif self.command=="clear": scrapper.clear_the_table()
        else: print("Неверная команда")


class Ui_ModeWindow(object): #Окно выбора режима работы
    def setupUi(self, ModeWindow):
        ModeWindow.setObjectName("ModeWindow")
        ModeWindow.resize(290, 299)
        self.centralwidget = QtWidgets.QWidget(ModeWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.radioCall = QtWidgets.QRadioButton(self.centralwidget)
        self.radioCall.setGeometry(QtCore.QRect(20, 70, 191, 20))
        self.radioCall.setObjectName("radioCall")

        self.radioAds = QtWidgets.QRadioButton(self.centralwidget)
        self.radioAds.setGeometry(QtCore.QRect(20, 100, 191, 20))
        self.radioAds.setObjectName("radioAds")

        self.radioAds.toggled.connect(self.adsSelect)
        self.radioCall.toggled.connect(self.callSelect)

        self.nextBtn = QtWidgets.QPushButton(self.centralwidget)
        self.nextBtn.setGeometry(QtCore.QRect(190, 210, 93, 28))
        self.nextBtn.setObjectName("nextBtn")
        ModeWindow.setCentralWidget(self.centralwidget)

        self.nextBtn.clicked.connect(self.next_click)# Подключение события нажатия кнопки

        self.retranslateUi(ModeWindow)
        QtCore.QMetaObject.connectSlotsByName(ModeWindow)

    mode=True
    def callSelect(self, selected): # Радио перетыкатели
        if selected:
            self.mode=True
    def adsSelect(self, selected):
        if selected:
            self.mode=False

    def next_click(self, selected): #Переключение окон
        if self.mode:
            CallWindow.show()
            ModeWindow.close()
        else:
            AdsWindow.show()
            ModeWindow.close()

    def retranslateUi(self, ModeWindow):
        _translate = QtCore.QCoreApplication.translate
        ModeWindow.setWindowTitle(_translate("ModeWindow", "Парсер Авито"))
        self.radioCall.setText(_translate("ModeWindow", "Сбор базы для холодных звонков"))
        self.radioAds.setText(_translate("ModeWindow", "Анализ объявлений"))
        self.nextBtn.setText(_translate("ModeWindow", "Далее"))


class Ui_CallWindow(object): #Окно холодных звонков
    def setupUi(self, CallWindow):
        CallWindow.setObjectName("CallWindow")
        CallWindow.resize(393, 300)
        self.widget = QtWidgets.QWidget(CallWindow)
        self.widget.setGeometry(QtCore.QRect(12, 52, 364, 41))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.checPhone = QtWidgets.QCheckBox(self.widget)
        self.checPhone.setObjectName("checPhone")
        self.gridLayout.addWidget(self.checPhone, 0, 0, 1, 1)
        self.checkServices = QtWidgets.QCheckBox(self.widget)
        self.checkServices.setObjectName("checkServices")
        self.gridLayout.addWidget(self.checkServices, 0, 1, 1, 1)
        self.checkViewsAll = QtWidgets.QCheckBox(self.widget)
        self.checkViewsAll.setObjectName("checkViewsAll")
        self.gridLayout.addWidget(self.checkViewsAll, 1, 0, 1, 1)
        self.checkViewsDay = QtWidgets.QCheckBox(self.widget)
        self.checkViewsDay.setObjectName("checkViewsDay")
        self.gridLayout.addWidget(self.checkViewsDay, 1, 1, 1, 1)
        self.widget1 = QtWidgets.QWidget(CallWindow)
        self.widget1.setGeometry(QtCore.QRect(13, 120, 181, 41))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.labelCategory = QtWidgets.QLabel(self.widget1)
        self.labelCategory.setObjectName("labelCategory")
        self.verticalLayout_3.addWidget(self.labelCategory)
        self.comboCaterory = QtWidgets.QComboBox(self.widget1)
        self.comboCaterory.setObjectName("comboCaterory")
        with open('Categoryy.csv', 'r', newline='', encoding='cp866') as self.csvfile:
            self.reader=csv.reader(self.csvfile, delimiter=';', )
            self.dictionary=dict()
            for x in self.reader:
                self.comboCaterory.addItem(x[0])

        self.verticalLayout_3.addWidget(self.comboCaterory)
        self.widget2 = QtWidgets.QWidget(CallWindow)
        self.widget2.setGeometry(QtCore.QRect(220, 120, 161, 68))
        self.widget2.setObjectName("widget2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.labelLocation = QtWidgets.QLabel(self.widget2)
        self.labelLocation.setObjectName("labelLocation")
        self.verticalLayout_4.addWidget(self.labelLocation)
        self.comboLocation = QtWidgets.QComboBox(self.widget2)
        self.comboLocation.setObjectName("comboLocation")
        self.comboLocation.addItem("")
        self.comboLocation.addItem("")
        self.comboLocation.addItem("")
        self.comboLocation.addItem("")
        self.comboLocation.addItem("")
        self.comboLocation.addItem("")
        self.verticalLayout_4.addWidget(self.comboLocation)
        self.lineLocate = QtWidgets.QLineEdit(self.widget2)
        self.lineLocate.setObjectName("lineLocate")
        self.verticalLayout_4.addWidget(self.lineLocate)
        self.nextBtn_2 = QtWidgets.QPushButton(CallWindow)
        self.nextBtn_2.setGeometry(QtCore.QRect(290, 250, 93, 28))
        self.nextBtn_2.setObjectName("nextBtn_2")
        self.backBtn_1 = QtWidgets.QPushButton(CallWindow)
        self.backBtn_1.setGeometry(QtCore.QRect(20, 250, 93, 28))
        self.backBtn_1.setObjectName("backBtn_1")

        # Подключение события нажатия кнопки
        self.backBtn_1.clicked.connect(self.back_click)
        self.nextBtn_2.clicked.connect(self.call_analyze)
        self.comboLocation.currentTextChanged.connect(self.locationEdit)
        self.comboCaterory.currentTextChanged.connect(self.categoryEdit)

        self.retranslateUi(CallWindow)
        QtCore.QMetaObject.connectSlotsByName(CallWindow)

    def retranslateUi(self, CallWindow):
        _translate = QtCore.QCoreApplication.translate
        CallWindow.setWindowTitle(_translate("CallWindow", "Парсер Авито"))
        self.checPhone.setText(_translate("CallWindow", "Номер телефона"))
        self.checkServices.setText(_translate("CallWindow", "Платные услуги продвижения"))
        self.checkViewsAll.setText(_translate("CallWindow", "Кол-во просмотров за все время"))
        self.checkViewsDay.setText(_translate("CallWindow", "Кол-во просмотров за сутки"))
        self.labelCategory.setText(_translate("CallWindow", "Категория услуг или товаров"))
        self.labelLocation.setText(_translate("CallWindow", "Город или регион"))
        self.comboLocation.setItemText(0, _translate("CallWindow", "Москва"))
        self.comboLocation.setItemText(1, _translate("CallWindow", "Санкт-Петербург"))
        self.comboLocation.setItemText(2, _translate("CallWindow", "Казань"))
        self.comboLocation.setItemText(3, _translate("CallWindow", "Уфа"))
        self.comboLocation.setItemText(4, _translate("CallWindow", "Ижевск"))
        self.comboLocation.setItemText(5, _translate("CallWindow", "Иркутск"))
        self.nextBtn_2.setText(_translate("CallWindow", "Далее"))
        self.backBtn_1.setText(_translate("CallWindow", "Назад"))

    def back_click(self, selected): #Переключение окон
        CallWindow.close()
        ModeWindow.show()

    def locationEdit(self, selected):
        self.lineLocate.setText(self.comboLocation.currentText())

    def categoryEdit(self, selected):
        scrapper.category = selected
    
    def call_analyze(self, selected):
        Scrapper_insance.command = "call_analyze"
        # if self.Search.text() != "":
        #     scrapper.searchText=self.Search.text()
        #     scrapper.searchMode=True
        # else:
        #     scrapper.searchMode=False
        if self.checPhone.checkState()=="CheckState.Checked": 
            scrapper.checkPhone=True
            print(1)
        else: print(2)

        # print(self.checPhone.checkState())
        # print(self.checkServices.checkState())
        scrapper.city = self.lineLocate.text()
        Scrapper_insance.start()



class Ui_AdsWindow(object): #Окно объявлений
    def setupUi(self, AdsWindow):
        AdsWindow.setObjectName("AdsWindow")
        AdsWindow.resize(400, 300)
        self.backBtn = QtWidgets.QPushButton(AdsWindow)
        self.backBtn.setGeometry(QtCore.QRect(20, 260, 93, 28))
        self.backBtn.setObjectName("backBtn")
        self.clearBtn = QtWidgets.QPushButton(AdsWindow)
        self.clearBtn.setGeometry(QtCore.QRect(10, 10, 93, 28))
        self.clearBtn.setObjectName("clearBtn")
        self.layoutWidget = QtWidgets.QWidget(AdsWindow)
        self.layoutWidget.setGeometry(QtCore.QRect(230, 70, 161, 68))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.labelLocation_2 = QtWidgets.QLabel(self.layoutWidget)
        self.labelLocation_2.setObjectName("labelLocation_2")
        self.verticalLayout_5.addWidget(self.labelLocation_2)
        self.comboLocation_2 = QtWidgets.QComboBox(self.layoutWidget)
        self.comboLocation_2.setObjectName("comboLocation_2")
        self.comboLocation_2.addItem("")
        self.comboLocation_2.addItem("")
        self.comboLocation_2.addItem("")
        self.comboLocation_2.addItem("")
        self.comboLocation_2.addItem("")
        self.comboLocation_2.addItem("")
        self.verticalLayout_5.addWidget(self.comboLocation_2)
        self.lineLocate_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineLocate_2.setObjectName("lineLocate_2")
        self.verticalLayout_5.addWidget(self.lineLocate_2)
        self.widget = QtWidgets.QWidget(AdsWindow)
        self.widget.setGeometry(QtCore.QRect(200, 260, 195, 30))
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.stopBtn = QtWidgets.QPushButton(self.widget)
        self.stopBtn.setObjectName("stopBtn")
        self.horizontalLayout_3.addWidget(self.stopBtn)
        self.startBtn = QtWidgets.QPushButton(self.widget)
        self.startBtn.setObjectName("startBtn")
        self.horizontalLayout_3.addWidget(self.startBtn)
        self.widget1 = QtWidgets.QWidget(AdsWindow)
        self.widget1.setGeometry(QtCore.QRect(10, 140, 381, 22))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget1)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.Search = QtWidgets.QLineEdit(self.widget1)
        self.Search.setText("")
        self.Search.setClearButtonEnabled(False)
        self.Search.setObjectName("Search")
        self.horizontalLayout.addWidget(self.Search)
        self.widget2 = QtWidgets.QWidget(AdsWindow)
        self.widget2.setGeometry(QtCore.QRect(60, 180, 120, 22))
        self.widget2.setObjectName("widget2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spinPage = QtWidgets.QSpinBox(self.widget2)
        self.spinPage.setObjectName("spinPage")
        self.horizontalLayout_2.addWidget(self.spinPage)
        self.widget3 = QtWidgets.QWidget(AdsWindow)
        self.widget3.setGeometry(QtCore.QRect(20, 70, 191, 41))
        self.widget3.setObjectName("widget3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.widget3)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.comboCategory = QtWidgets.QComboBox(self.widget3)
        self.comboCategory.setObjectName("comboCategory")
        self.spinPage.setMinimum(1)
        with open('Categoryy.csv', 'r', newline='', encoding='cp866') as self.csvfile:
            self.reader=csv.reader(self.csvfile, delimiter=';', )
            self.dictionary=dict()
            for x in self.reader:
                self.comboCategory.addItem(x[0])

        self.verticalLayout.addWidget(self.comboCategory)

        # Подключение события нажатия кнопки
        self.backBtn.clicked.connect(self.back_click)
        self.startBtn.clicked.connect(self.start)
        self.stopBtn.clicked.connect(self.stop)
        self.clearBtn.clicked.connect(self.clearing)

        self.comboLocation_2.currentTextChanged.connect(self.locationEdit)
        self.comboCategory.currentTextChanged.connect(self.categoryEdit)

        self.retranslateUi(AdsWindow)
        QtCore.QMetaObject.connectSlotsByName(AdsWindow)

    def retranslateUi(self, AdsWindow):
        _translate = QtCore.QCoreApplication.translate
        AdsWindow.setWindowTitle(_translate("AdsWindow", "Парсер Авито"))
        self.backBtn.setText(_translate("AdsWindow", "Назад"))
        self.clearBtn.setText(_translate("AdsWindow", "Очистить"))
        self.labelLocation_2.setText(_translate("AdsWindow", "Город или регион"))
        self.comboLocation_2.setItemText(0, _translate("AdsWindow", "Москва"))
        self.comboLocation_2.setItemText(1, _translate("AdsWindow", "Санкт-Петербург"))
        self.comboLocation_2.setItemText(2, _translate("AdsWindow", "Казань"))
        self.comboLocation_2.setItemText(3, _translate("AdsWindow", "Уфа"))
        self.comboLocation_2.setItemText(4, _translate("AdsWindow", "Ижевск"))
        self.comboLocation_2.setItemText(5, _translate("AdsWindow", "Иркутск"))
        self.stopBtn.setText(_translate("AdsWindow", "Стоп"))
        self.startBtn.setText(_translate("AdsWindow", "Старт"))
        self.label.setText(_translate("AdsWindow", "Точный поисковой запрос"))
        self.label_2.setText(_translate("AdsWindow", "Кол-во страниц"))
        self.label_3.setText(_translate("AdsWindow", "Категория услуг или товаров"))

    # def locationEdit(self, selected):
    #     scrapper.city = selected

    def categoryEdit(self, selected):
        scrapper.category = selected
    
    def locationEdit(self, selected):
        self.lineLocate_2.setText(self.comboLocation_2.currentText())


    def clearing(self, selected):
        Scrapper_insance.command = "clear"
        Scrapper_insance.start()

    def back_click(self, selected): #Переключение окон
        AdsWindow.close()
        ModeWindow.show()

    def start(self, selected):
        scrapper.city = self.lineLocate_2.text()
        scrapper.pages = self.spinPage.text()
        if self.Search.text() != "":
            scrapper.searchText=self.Search.text()
            scrapper.searchMode=True
        else:
            scrapper.searchMode=False
        Scrapper_insance.command = "scraping"
        Scrapper_insance.start()

    def stop(self, selected):
        Scrapper_insance.command = "stop"
        Scrapper_insance.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    ModeWindow = QtWidgets.QMainWindow()    # Окно режимов
    ui = Ui_ModeWindow()
    ui.setupUi(ModeWindow)

    AdsWindow = QtWidgets.QDialog()         # Окно объявлений
    ui2 = Ui_AdsWindow()
    ui2.setupUi(AdsWindow)

    CallWindow = QtWidgets.QDialog()        # Окно прозвонов
    ui3 = Ui_CallWindow()
    ui3.setupUi(CallWindow)

    ModeWindow.show()
    Scrapper_insance = Scrapper()           # Первичное открытие браузера
    Scrapper_insance.command = "openBrowser"
    Scrapper_insance.start()

    sys.exit(app.exec())