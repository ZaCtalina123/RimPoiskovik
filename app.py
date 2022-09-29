from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import os
import sys
import validators
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtPrintSupport
from PyQt5 import QtWidgets, uic
import json
import pickle
import datetime

class ReadHistory(QDialog): 
    def __init__(self, *args, **kwargs):
        super(ReadHistory, self).__init__(*args, **kwargs)

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()  
        layout = QVBoxLayout()
        
        object = QLabel(str('\t'))
        self.vbox.addWidget(object)
        title = QLabel("История")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)
        self.vbox.addWidget(title)
        object = QLabel(str('\n'))
        self.vbox.addWidget(object)
        user_path = os.path.expanduser('~')
        filehistory = f"{user_path}\\AppData\\Roaming\\RPoisk\\history.txt"
        
        with open(filehistory) as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]

        for i in lines:
            object = QLabel(str(i))
            object.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.vbox.addWidget(object)
            object = QLabel(str('\n'))
            self.vbox.addWidget(object)

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        layout.addWidget(self.scroll)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.jpg')))
        self.setWindowTitle('История')
        self.setLayout(layout)

class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.setStyleSheet(
            "background-color:#0088ff;color : #ffffff;")
        layout = QVBoxLayout()

        title = QLabel("Римпоисковик")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)
        self.setStyleSheet("background-color:#000000;color : #ffffff;")

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'ma-icon-128.jpg')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Рипоисковик"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)
        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.jpg')))
        self.setWindowTitle("Римпоисковик")
        self.setLayout(layout)


class Help(QDialog):
    def __init__(self, *args, **kwargs):
        super(Help, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout = QVBoxLayout()
        
        title = QLabel("Сочетания клавиш")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        layout.addWidget(QLabel(" Открыть Новаю вкладку--Ctrl+Alt+t \n Откройте HTML-файл--Ctrl+o \n Распечатать веб-страницу--Ctrl+p \n Получить информацию об используемой версии web plus--Ctrl+Alt+a \n Посетить официальный веб-сайт Web Plus--Ctrl+Alt+h \n Просмотреть исходный код страницы--Ctrl+Alt+v \n Вернуться на предыдущую страницу--Ctrl+b \n Перейти на следующую страницу - Ctrl+f \n Перезагрузить страницу -Ctrl+Alt+r \n Открыть домашнюю страницу -Ctrl+h"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)
        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.jpg')))
        self.setWindowTitle("Сочетания клавиш")
        self.setLayout(layout)



class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, parent=None):
        super(WebEnginePage, self).__init__(parent)
        self.featurePermissionRequested.connect(
            self.handleFeaturePermissionRequested)

    @QtCore.pyqtSlot(QtCore.QUrl, QtWebEngineWidgets.QWebEnginePage.Feature)
    def handleFeaturePermissionRequested(self, securityOrigin, feature):
        title = "Запрос разрешения"
        questionForFeature = {
            QtWebEngineWidgets.QWebEnginePage.Geolocation: "Разрешить {feature} доступ к информации о вашем местоположении?",
            QtWebEngineWidgets.QWebEnginePage.MediaAudioCapture: "Разрешить {feature} доступ к вашему микрофону?",
            QtWebEngineWidgets.QWebEnginePage.MediaVideoCapture: "Разрешить {feature} доступ к вашей веб-камере?",
            QtWebEngineWidgets.QWebEnginePage.MediaAudioVideoCapture: "Разрешить {feature} блокировать курсор мыши?",
            QtWebEngineWidgets.QWebEnginePage.DesktopVideoCapture: "Разрешить {feature} захватывать видео с вашего рабочего стола?",
            QtWebEngineWidgets.QWebEnginePage.DesktopAudioVideoCapture: "Разрешить {feature} захватывать аудио и видео с вашего рабочего стола?"
        }
        question = questionForFeature.get(feature)
        if question:
            question = question.format(feature=securityOrigin.host())
            if QtWidgets.QMessageBox.question(self.view().window(), title, question) == QtWidgets.QMessageBox.Yes:
                self.setFeaturePermission(
                    securityOrigin, feature, QtWebEngineWidgets.QWebEnginePage.PermissionGrantedByUser)
            else:
                self.setFeaturePermission(
                    securityOrigin, feature, QtWebEngineWidgets.QWebEnginePage.PermissionDeniedByUser)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)
        # defining shotcuts

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+Alt+t'), self)
        self.shortcut_open.activated.connect(self.add_new_tab)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+p'), self)
        self.shortcut_open.activated.connect(self.printRequested)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+o'), self)
        self.shortcut_open.activated.connect(self.open_file)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+Alt+a'), self)
        self.shortcut_open.activated.connect(self.about)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+Alt+h'), self)
        self.shortcut_open.activated.connect(self.navigate_mozarella)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+Alt+v'), self)
        self.shortcut_open.activated.connect(self.view)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+b'), self)
        self.shortcut_open.activated.connect(
            lambda: self.tabs.currentWidget().back())

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+f'), self)
        self.shortcut_open.activated.connect(
            lambda: self.tabs.currentWidget().forward())

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+Alt+r'), self)
        self.shortcut_open.activated.connect(
            lambda: self.tabs.currentWidget().reload())

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+h'), self)
        self.shortcut_open.activated.connect(self.navigate_home)

        
        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)


        self.navtb = QToolBar("Навигация")
        self.navtb.setIconSize(QSize(25, 25))
        self.navtb.setMovable(False)
        self.addToolBar(self.navtb)

        back_btn = QAction(
            QIcon(os.path.join('images', 'arrow-180.png')), "Назад", self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        self.navtb.addAction(back_btn)

        next_btn = QAction(
            QIcon(os.path.join('images', 'arrow-000.png')), "Вперед", self)
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        self.navtb.addAction(next_btn)
        

        reload_btn = QAction(
            QIcon(os.path.join('images', 'arrow-circle-315.png')), "Перезагрузить", self)
        reload_btn.triggered.connect(
            lambda: self.tabs.currentWidget().reload())
        self.navtb.addAction(reload_btn)


        self.connect_btn = QAction(QIcon(os.path.join('images', 'lock-nossl.png')), "Состояние подключения", self)
        self.navtb.addAction(self.connect_btn)

        self.urlbar = QLineEdit()
        # self.urlbar.setStyleSheet("background-color : none; border-radius : None")
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        #self.urlbar.setFixedWidth(1640)
        self.urlbar.setFixedHeight(28)
        self.navtb.addWidget(self.urlbar)

        stop_btn = QAction(
            QIcon(os.path.join('images', 'cross-circle.png')), "Стоп", self)
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        self.navtb.addAction(stop_btn)

        menu = QtWidgets.QMenu(self)
        new_tab_action = QAction(
            QIcon(os.path.join('images', 'ui-tab--plus.png')), "Новая вкладка", self)
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        menu.addAction(new_tab_action)

        print_action = QAction(
            QIcon(os.path.join('images', 'printer.png')), "Печать", self)
        print_action.triggered.connect(self.printRequested)
        menu.addAction(print_action)

        open_file_action = QAction(
            QIcon(os.path.join('images', 'disk--arrow.png')), "Открыть файл...", self)
        open_file_action.triggered.connect(self.open_file)
        menu.addAction(open_file_action)

        about_action = QAction(QIcon(os.path.join('images', 'question.png')), "О Римпоисковик", self)
        about_action.triggered.connect(self.about)
        menu.addAction(about_action)

        keyboard = QAction(
            QIcon(os.path.join('images', 'keyboard.png')), "Сочетание клавиш", self)
        keyboard.triggered.connect(self.keyboardshotcut)
        menu.addAction(keyboard)
        
        readhistory = QAction(
            QIcon(os.path.join('images', 'history.png')), "История", self)
        readhistory.triggered.connect(self.read_history)
        menu.addAction(readhistory)

        navigate_mozarella_action = QAction(QIcon(os.path.join('images', 'lifebuoy.png')),
                                            "Римпоисковик Домашняя страница", self)
        navigate_mozarella_action.triggered.connect(self.navigate_mozarella)
        menu.addAction(navigate_mozarella_action)

        view = QAction(QIcon(os.path.join('images', 'view.png')),
                       "Просмотр исходного кода страницы", self)
        view.triggered.connect(self.view)
        menu.addAction(view)

        option_btn = QAction(
            QIcon(os.path.join('images', 'options.png')), "Вариант", self)
        option_btn.setMenu(menu)
        self.navtb.addAction(option_btn) 

        self.add_new_tab(QUrl('file:///html/home.html'), 'UNTITLED')

        self.show()


        self.setWindowTitle("Римпоисковик")
        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.jpg')))


    @QtCore.pyqtSlot("QWebEngineDownloadItem*")
    def on_downloadRequested(self, download):
        old_path = download.url().path()  # download.path()
        suffix = QtCore.QFileInfo(old_path).suffix()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", old_path, "*." + suffix
        )
        if path:
            download.setPath(path)
            download.accept()

    def add_new_tab(self, qurl=None, label="UNTITLED"):

        if qurl is None:
            qurl = QUrl('file:///html/home.html')

        
        browser = QWebEngineView()
        page = WebEnginePage(browser)
        browser.setPage(page)
        browser.setUrl(qurl)
        page.printRequested.connect(self.printRequested)
        QtWebEngineWidgets.QWebEngineProfile.defaultProfile(
        ).downloadRequested.connect(self.on_downloadRequested)

        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        self.tabs.setTabIcon(i, browser.page().icon())

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

        browser.iconChanged.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabIcon(i, browser.icon()))


    def printRequested(self):
        # if you are viewing this part of my code can you please improve this as I don't think this is the best way to print a page and I can't understand how to fix this
        url = self.urlbar.text()
        if url == "":
            url = 'file:///html/home.html'
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.page = QtWebEngineWidgets.QWebEnginePage(self)
        self.view.setPage(self.page)
        self.view.load(QtCore.QUrl(url))
        defaultPrinter = QtPrintSupport.QPrinter(
            QtPrintSupport.QPrinterInfo.defaultPrinter())
        dialog = QtPrintSupport.QPrintDialog(defaultPrinter, self)
        if dialog.exec():
            # printer object has to be persistent
            self._printer = dialog.printer()
            self.page.print(self._printer, self.printResult)

    def printResult(self, success):
        if success:
            pass
        else:
            QtWidgets.QMessageBox.information(self, 'Ошибка печати',
                                              'Сбой печати!', QtWidgets.QMessageBox.Ok)
        del self._printer

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():

            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - Римпоисковик" % title)

    def navigate_mozarella(self):
        self.tabs.currentWidget().setUrl(
            QUrl("https://zactalina123.pythonanywhere.com/"))

    def view(self):
        url = self.urlbar.text()
        if url == "":
            url = "file:///html/home.html"
        url = f"view-source:{url}"
        self.add_new_tab(QUrl(url), 'UNTITLED')

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def keyboardshotcut(self):
        dlg = Help()
        dlg.exec_()
    
    def read_history(self):
        dlg = ReadHistory()
        dlg.exec_()
        
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "HTML(*.htm *.html);;")
        if filename == "":
            pass
        else:
            self.tabs.currentWidget().setUrl(QUrl(f"file:///{filename}"))

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("file:///html/home.html"))

    def navigate_to_url(self):
        inputtext = self.urlbar.text()
        if validators.url(inputtext):
            text = QUrl(inputtext)
        elif validators.url(f"https://{inputtext}"):
            text = QUrl(f"http://{inputtext}")
        elif inputtext.find("file:///") == 0 or inputtext.find("view-source:") == 0 :
            text = QUrl(inputtext)

        else:
            url = f'https://www.google.com/search?q={inputtext.replace("+","%2B").replace(" ","+")}'
            text = QUrl(url)

        if text.scheme() == "":
            text.setScheme("http")

        self.tabs.currentWidget().setUrl(text)
        

    def update_urlbar(self, q, browser=None):
        url = q.toString()
        self.history(url)
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        if q.scheme() == 'https':
            # Secure padlock icon
            self.connect_btn.setIcon(QIcon(os.path.join('images', 'ssl.png')))
            #self.connect_btn.setStatusTip("Your connection is secure")

        elif q.scheme() == 'http':
            # Insecure padlock icon
            self.connect_btn.setIcon(QIcon(os.path.join('images', 'lock-nossl.png')))
            #self.connect_btn.setStatusTip("Your connection is not secure")

        elif q.scheme() == 'file':
            if url == "file:///html/home.html":
                # search padlock icon
                self.connect_btn.setIcon(QIcon(os.path.join('images', 'search.png')))
                #self.connect_btn.setStatusTip("Search or type a url")
            else:
                # file padlock icon

                self.connect_btn.setIcon(QIcon(os.path.join('images', 'document.png')))
                #self.connect_btn.setStatusTip("You are viewing a local or shared file")

        elif q.scheme() == 'view-source':
            # source code padlock icon
            self.connect_btn.setIcon(QIcon(os.path.join('images', 'code.png')))
            #self.connect_btn.setStatusTip(f"You are viewing the source of a website")

        if url == "file:///html/home.html":
            self.urlbar.setText("")
        else:
            self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
    
    def history(self, url):
        user_path = os.path.expanduser('~')
        if not os.path.exists(f"{user_path}\\AppData\\Roaming\\RPoisk"):
            os.mkdir(f"{user_path}\\AppData\\Roaming\\RPoisk")
        dat = str(datetime.datetime.now())
        
        home_dir = os.getcwd()
        
        os.chdir(f"{user_path}\\AppData\\Roaming\\RPoisk")
    
        with open("history.txt", "a+") as f:
            f.writelines(f'{dat} {url}\n')
        
        os.chdir(home_dir)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Римпоисковик")
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
