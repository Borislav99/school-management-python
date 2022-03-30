#  ---------- IMPORTI ----------
from codecs import register
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# unesi datumsku datoteku
from datetime import date
# sistemska biblioteka
import sys
# biblioteka za povezivanje korisnickog interfejsa sa python fajlom
from PyQt5.uic import loadUiType
# varijabla konekcije
import mysql.connector as con
from mysql.connector.errors import Error
ui, _ = loadUiType("school.ui")
#  ---------- IMPORTI ----------


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.menubar.setVisible(False)
        # Kada pritisne prijavu pokreni metodu login
        self.b01.clicked.connect(self.login)
        # Kada pritisne add new student, da prikaze tu stranicu
        self.menu11.triggered.connect(self.show_add_new_student_tab)
        # Kada pritisne dugme dodaj ucenika, ucenik se doda u bazu podataka
        self.b12.clicked.connect(self.save_student_details)
        # Kada pritisne Uredi ili obrisi studenta da mu se to prikaze
        self.menu12.triggered.connect(self.show_edit_delete_student_tab)
        # Prilikom izbora registracionog broja ispuni detalje
        self.cb21.currentIndexChanged.connect(
            self.fill_details_when_combobox_selected)
        # Azuriraj podatke korisnika kada se pritisne dugme Uredi
        self.b21.clicked.connect(self.edit_student_details)
        # Obrisi podatke ucenika kada se pritisne dugme "Obrisi studenta"
        self.b22.clicked.connect(self.delete_student_details)
        # Otvori tab za ocjene klikom na meni
        self.menu21.triggered.connect(self.show_mark_tab)
        # Kada administrator pritisne dugme "Sacuvaj ocjenu" ocjena se salje na bazu
        self.b31.clicked.connect(self.save_mark_details)
        # Ispuni testove na osnovu registracionog broja
        self.cb32.currentIndexChanged.connect(self.fill_exam_names_in_combobox_for_registration_number_selected)
        # Kada pritisne dugme "Ocjene" izvrsi se ispis ocjena
        self.b32.clicked.connect(self.fill_exam_details_in_textbox_for_exam_name_selected)
        # Kada pritisne uredi ocjenu izvrsi se uredjivanje ocjene
        self.b33.clicked.connect(self.update_mark_details)
        # Obrisi ocjene nakon sto pritisne "Obrisi ocjene" dugme
        self.b34.clicked.connect(self.remove_mark_details)
        # Kada otvori prisustvo preko menu-bar zelimo mu prikazati to
        self.menu31.triggered.connect(self.show_attendance)
        # Kada pritisne na sacuvaj prisustvo pokrese se metoda
        self.b41.clicked.connect(self.save_attendance_details)
        # Kada administrator promjeni indeks registracionog broja u prisustvo zelimo da se pokrene event izmjene datuma
        self.cb42.currentIndexChanged.connect(self.fill_dates_in_combobox_for_registration_number_selected)
        # Kada administrator pritisne dugme "Datum" ispunjavaju se polja
        self.b42.clicked.connect(self.fill_attendance_status_on_button_click)
        # Kada administrator pritisne "Uredi prisustvo"
        self.b43.clicked.connect(self.update_attendance_details)
        # Kada administrator pritisne dugme "Obrisi prisustvo"
        self.b44.clicked.connect(self.delete_attendance_details)
        # Prikaz uplatnica kad klikne na meni
        self.menu41.triggered.connect(self.show_fees_tab)
        # Kada pritisne sacuvaj placanje
        self.b51.clicked.connect(self.save_fees_details)
        # Kada se izmjeni broj indeksa pokreni metodu za ispunjavanje podataka
        self.cb52.currentIndexChanged.connect(self.fill_receipt_details_in_textboxes_for_receipt_combo_selected)
        # Kada pritisne "Uredi placanje" pokrece se metoda update_fees_details
        self.b52.clicked.connect(self.update_fees_details)
        # Kada korisnik pritisne dugme "Orisi placanje", placanje se brise
        self.b53.clicked.connect(self.delete_fees_details)
        # Otvori tab kada pritisne na tab-bar
        self.menu51.triggered.connect(self.show_report)
        self.menu52.triggered.connect(self.show_report)
        self.menu53.triggered.connect(self.show_report)
        self.menu54.triggered.connect(self.show_report)

# --- Metoda za prikaz taba ---
    def show_report(self):
        # ime menija
        table_name = self.sender()
        # prikazi izvjestaj tab
        self.tabWidget.setCurrentIndex(7)
        # ...
        try:
            # postavi broj redova na 0
            self.tableReport.setRowCount(0)
            # provjeri koji je meni selektovan
            if table_name.text() == "Izvjestaji za ucenike":
                self.l61.setText(table_name.text())
                mydb = con.connect(
                    host="localhost",
                    user="root",
                    password="",
                    db="school")
                cursor = mydb.cursor()
                query = "SELECT registration_number, full_name, gender, date_of_birth, age, adress, phone, email, standard FROM student"
                cursor.execute(query)
                result = cursor.fetchall()
                redovi = 0
                kolone = 0
                # ... kada bi isprintao r_number to ti je indeks od svakog od elemenata, znaci imas 3 ucenika indeksi su 0,1,2. r_data su ti podaci koji dolaze u tuple-u. Njihov id broj, registracioni, itd...
                # ... Za svaku iteraciju povecavas broj redova, znaci 3 iteracije, 3 reda
                # ... Nakon toga prolazis kroz r_data, r_data ti je tuple sa podacima svakog ucenika pojedinacno, za svaku iteraciju povecavas broj kolona. Nakon toga postavljas broj kolona
                # ... upjesno si napravio tabelu sa 10 kolona
                for r_number, r_data in enumerate(result):
                    redovi += 1
                    kolone = 0
                    for r_number, data in enumerate(r_data):
                        kolone +=1
                self.tableReport.clear()
                self.tableReport.setColumnCount(kolone)
                # ... ponovo prolazis kroz rezultate i za svaku iteraciju, imas ih 3 ubacujes red. Odnosno podatke iz row_number (tuple)
                # ... medjutim redovi su prazni potrebno je ubaciti podatke, to radis tako sto prolazis kroz row data i ubacujes iteme u tabelu
                for row_number, row_data in enumerate(result):
                    self.tableReport.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableReport.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                self.tableReport.setHorizontalHeaderLabels(['Registracijski broj', 'Ime', 'Pol', 'Datum rodjenja', 'Godine', 'Adresa', 'Broj telefona', 'Email', 'Predmet'])
            elif table_name.text() == "Izvjestaji za ocjene":
                self.l61.setText(table_name.text())
                mydb = con.connect(
                    host="localhost",
                    user="root",
                    password="",
                    db="school")
                cursor = mydb.cursor()
                query = "SELECT registration_number, exam_name, language, english, maths, science, social FROM mark"
                cursor.execute(query)
                result = cursor.fetchall()
                redovi = 0
                kolone = 0
                for r_number, r_data in enumerate(result):
                    redovi += 1
                    kolone = 0
                    for r_number, data in enumerate(r_data):
                        kolone +=1
                self.tableReport.clear()
                self.tableReport.setColumnCount(kolone)
                for row_number, row_data in enumerate(result):
                    self.tableReport.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableReport.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                self.tableReport.setHorizontalHeaderLabels(['Registracijski broj', 'Naziv testa', 'Srpski', 'Engleski', 'Matematika', 'Priroda', 'Drustvo'])
            elif table_name.text() == "Izvjestaji za prisustvo":
                self.l61.setText(table_name.text())
                mydb = con.connect(
                    host="localhost",
                    user="root",
                    password="",
                    db="school")
                cursor = mydb.cursor()
                query = "SELECT registration_number, attendance_date, morning, evening FROM attendance"
                cursor.execute(query)
                result = cursor.fetchall()
                redovi = 0
                kolone = 0
                for r_number, r_data in enumerate(result):
                    redovi += 1
                    kolone = 0
                    for r_number, data in enumerate(r_data):
                        kolone +=1
                self.tableReport.clear()
                self.tableReport.setColumnCount(kolone)
                for row_number, row_data in enumerate(result):
                    self.tableReport.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableReport.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                self.tableReport.setHorizontalHeaderLabels(['Registracijski broj', 'Datum', 'Prva smjena', 'Druga smjena'])
            elif table_name.text() == "Izvjestaji placanja":
                self.l61.setText(table_name.text())
                mydb = con.connect(
                    host="localhost",
                    user="root",
                    password="",
                    db="school")
                cursor = mydb.cursor()
                query = "SELECT receipt_number, registration_number, reason, amount, fees_date FROM fees"
                cursor.execute(query)
                result = cursor.fetchall()
                redovi = 0
                kolone = 0
                for r_number, r_data in enumerate(result):
                    redovi += 1
                    kolone = 0
                    for r_number, data in enumerate(r_data):
                        kolone +=1
                self.tableReport.clear()
                self.tableReport.setColumnCount(kolone)
                for row_number, row_data in enumerate(result):
                    self.tableReport.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableReport.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                self.tableReport.setHorizontalHeaderLabels(['Broj uplatnice', 'Registracioni broj', 'Razlog', 'Suma', 'Datum'])
        except con.Error as e:
            print("There was an error")
# --- Metoda za prikaz taba ---

# --- Metoda za brisanje placanja ---
    def delete_fees_details(self):
        try:
            # postavljanje baze
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            # registracioni broj
            registration_number = self.tb55.text()
            # datum
            date = self.tb58.text()
            # broj uplatnice
            receipt_number = self.cb52.currentText()
            m = QMessageBox.question(self, "Obrisi placanje", "Molim, potvrdite brisanje placanja? ", QMessageBox.Yes|QMessageBox.No)
            if m == QMessageBox.Yes:
                # upit za unos podataka u bazu
                query = f"DELETE FROM fees WHERE registration_number = '{registration_number}' and fees_date = '{date}' and receipt_number = '{receipt_number}'"
                cursor.execute(query)
                mydb.commit()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Placenje uspjesno obrisano")
                msg.setWindowTitle("Brisanje placanja")
                msg.exec_()
                self.tabWidget.setCurrentIndex(1)
        except con.Error as e:
            print("Upit brisanja placanja u bazu neuspjesan!" + e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Error)
            msg.setText("Greska prilikom brisanja placanja")
            msg.setWindowTitle("Brisanje placanja")
            msg.exec_()
# --- Metoda za brisanje placanja ---

# --- Azuriraj placanje ---
    def update_fees_details(self):
        try:
            # postavljanje baze
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            # registracioni broj
            registration_number = self.tb55.text()
            # broj uplatnice
            receipt_number = str(self.cb52.currentText())
            # razlog uplate
            reason = self.tb56.text()
            # kolicina novca
            amount = self.tb57.text()
            # datum uplate
            date = self.tb58.text()
            # upit za unos podataka u bazu
            query = f"UPDATE fees SET registration_number = '{registration_number}', reason = '{reason}', amount = '{amount}', fees_date = '{date}' WHERE receipt_number = '{receipt_number}'"
            cursor.execute(query)
            mydb.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Uplata uspjesno uredjena")
            msg.setWindowTitle("Uredjivanje uplata")
            msg.exec_()
            self.tabWidget.setCurrentIndex(6)
        except con.Error as e:
            print("Upit uredjivanja uplata u bazu neuspjesan!" + e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Error)
            msg.setText("Greska prilikom uredjivanja uplata")
            msg.setWindowTitle("Uredjivanje uplata")
            msg.exec_()
# --- Azuriraj placanje ---

# --- Metoda za ispunjavanje detalja na osnovu izmjene indeksa comboboxa ---
    def fill_receipt_details_in_textboxes_for_receipt_combo_selected(self):
        try:
            # povezivanje sa bazon
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            cursor.execute(f"select * from fees where receipt_number = '{self.cb52.currentText()}'")
            result = cursor.fetchall()
            if result:
                # ispisi  detalje na osnovu broja uplatnice
                for stud_reg_number in result:
                    self.tb55.setText(str(stud_reg_number[2]))
                    self.tb56.setText(str(stud_reg_number[3]))
                    self.tb57.setText(str(stud_reg_number[4]))
                    self.tb58.setText(str(stud_reg_number[5]))
        except con.Error as e:
            print("Greska prilikom izbora registracionog broja u combo boxu" + e)
# --- Metoda za ispunjavanje detalja na osnovu izmjene indeksa comboboxa ---

# --- Metoda za uredjivanje uplatnica ---
    def fill_receipt_number_in_combobox_for_edit_fees_tab(self):
        try:
            self.cb52.clear()
            # povezivanje sa bazon
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from fees")
            result = cursor.fetchall()
            if result:
                # ubaci registracioni broj svakog studenta u combo box
                for stud_reg_number in result:
                    self.cb52.addItem(str(stud_reg_number[1]))
        except con.Error as e:
            print("Greska prilikom izbora registracionog broja u combo boxu" + e)
# --- Metoda za uredjivanje uplatnica ---

# --- Metoda za cuvanje uplatnica ---
    def save_fees_details(self):
        try:
            # postavljanje baze
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            # registracioni broj uzima preko polja registracionog broja
            registration_number = str(self.cb51.currentText())
            # datum 
            fees_date = self.tb54.text()
            # broj uplatnice
            receipt_number = self.tb51.text()
            # razlog
            reason = self.tb52.text()
            # price
            amount = self.tb53.text()
            # upit za unos podataka u bazu
            query = f"INSERT INTO fees (receipt_number, registration_number, reason, amount, fees_date) VALUES ('{receipt_number}', '{registration_number}', '{reason}', '{amount}', '{fees_date}')"
            cursor.execute(query)
            mydb.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Uplatnica uspjesno ubacena u bazu podataka")
            msg.setWindowTitle("Ubacivanje uplatnice")
            msg.exec_()
            # ocisti polja
            self.tb51.setText("")
            self.tb52.setText("")
            self.tb53.setText("")
            self.fill_next_receipt_number()
            self.fill_receipt_number_in_combobox_for_edit_fees_tab()
        except con.Error as e:
            print("Upit upisa uplatnice u bazu neuspjesan!" + e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Error)
            msg.setText("Greska prilikom upisa uplatnice")
            msg.setWindowTitle("Upis uplatnice")
            msg.exec_()
# --- Metoda za cuvanje uplatnica ---

# --- Metoda za ispis broja uplatnice ---
    def fill_next_receipt_number(self):
        try:
            rn = 0
            # povezivanje sa bazon
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from fees")
            result = cursor.fetchall()
            if result:
                # ubaci registracioni broj svakog studenta u combo box
                for stud_reg_number in result:
                    rn += 1
            self.tb51.setText(str(rn + 1))
        except con.Error as e:
            print("Greska prilikom izbora registracionog broja u combo boxu" + e)
# --- Metoda za ispis broja uplatnice ---

# --- Metoda za ispis registracionog broja u uplatnicama ---
    def fill_registration_number_in_combobox_for_fees_tab(self):
        try:
            self.cb51.clear()
            # povezivanje sa bazon
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from student")
            result = cursor.fetchall()
            if result:
                # ubaci registracioni broj svakog studenta u combo box
                for stud_reg_number in result:
                    self.cb51.addItem(str(stud_reg_number[1]))
        except con.Error as e:
            print("Greska prilikom izbora registracionog broja u combo boxu" + e)
# --- Metoda za ispis registracionog broja u uplatnicama ---

# --- Metoda za prikaz uplanica ---
    def show_fees_tab(self):
        self.tabWidget.setCurrentIndex(6)
        self.fill_registration_number_in_combobox_for_fees_tab()
        self.fill_next_receipt_number()
        self.tb54.setText(str(date.today()))
        self.fill_receipt_number_in_combobox_for_edit_fees_tab()
        # self.tb41.setText(str(date.today()))
# --- Metoda za prikaz uplanica ---

# --- Metoda za brisanje prisustva ucenika ---
    def delete_attendance_details(self):
        try:
            # postavljanje baze
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            # registracioni broj
            registration_number = str(self.cb42.currentText())
            # datum
            attendance_date = str(self.cb43.currentText())
            m = QMessageBox.question(self, "Obrisi prisustvo", "Molim, potvrdite brisanje prisustva? ", QMessageBox.Yes|QMessageBox.No)
            if m == QMessageBox.Yes:
                # upit za unos podataka u bazu
                query = f"DELETE FROM attendance WHERE registration_number = '{registration_number}' and attendance_date = '{attendance_date}'"
                cursor.execute(query)
                mydb.commit()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Prisustvo uspjesno obrisano")
                msg.setWindowTitle("Brisanje prisustva")
                msg.exec_()
                self.tabWidget.setCurrentIndex(1)
        except con.Error as e:
            print("Upit uredjivanja prisustva u bazu neuspjesan!" + e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Error)
            msg.setText("Greska prilikom uredjivanja prisustva")
            msg.setWindowTitle("Uredjivanje prisustva")
            msg.exec_()
# --- Metoda za brisanje prisustva ucenika ---
# --- Metoda za azuriranje prisustva ucenika ---
    def update_attendance_details(self):
        try:
            # postavljanje baze
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            # registracioni broj
            registration_number = str(self.cb42.currentText())
            # datum
            attendance_date = str(self.cb43.currentText())
            # prva smjena
            morning = self.tb44.text()
            # druga smjena
            evening = self.tb45.text()
            # upit za unos podataka u bazu
            query = f"UPDATE attendance SET morning = '{morning}', evening = '{evening}' WHERE registration_number = '{registration_number}' and attendance_date = '{attendance_date}'"
            cursor.execute(query)
            mydb.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Prisustvo uspjesno uredjeno")
            msg.setWindowTitle("Uredjivanje prisustva")
            msg.exec_()
            self.tb44.setText("")
            self.tb45.setText("")
        except con.Error as e:
            print("Upit uredjivanja prisustva u bazu neuspjesan!" + e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Error)
            msg.setText("Greska prilikom uredjivanja prisustva")
            msg.setWindowTitle("Uredjivanje prisustva")
            msg.exec_()
# --- Metoda za azuriranje prisustva ucenika ---

# --- Metoda za prikaz detalja kada je bio prisutan a kada nije ---
    def fill_attendance_status_on_button_click(self):
        try:
            # povezivanje sa bazon
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            cursor.execute(f"select * from attendance where registration_number = '{self.cb42.currentText()}' and attendance_date = '{self.cb43.currentText()}'")
            result = cursor.fetchall()
            if result:
                # ubaci registracioni broj svakog studenta u combo box
                for stud_reg_number in result:
                    self.tb44.setText(str(stud_reg_number[3]))
                    self.tb45.setText(str(stud_reg_number[4]))
        except con.Error as e:
            print("Greska prilikom izbora datuma u combo boxu" + e)
# --- Metoda za prikaz detalja kada je bio prisutan a kada nije ---

# --- Metoda za generisanje datuma na osnovu registracionog broja - prisustvo ---
    def fill_dates_in_combobox_for_registration_number_selected(self):
        try:
            self.cb43.clear()
            # povezivanje sa bazon
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            cursor.execute(f"select * from attendance where registration_number = '{self.cb42.currentText()}'")
            result = cursor.fetchall()
            if result:
                # ubaci registracioni broj svakog studenta u combo box
                for stud_reg_number in result:
                    self.cb43.addItem(str(stud_reg_number[2]))
        except con.Error as e:
            print("Greska prilikom izbora datuma u combo boxu" + e)
# --- Metoda za generisanje datuma na osnovu registracionog broja - prisustvo ---

# --- Sacuvaj prisustvo ---
    def save_attendance_details(self):
        try:
            # postavljanje baze
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            # registracioni broj uzima preko polja registracionog broja
            registration_number = str(self.cb41.currentText())
            # datum prisustva
            attendance_date = self.tb41.text()
            # prva smjena
            morning = self.tb42.text()
            # druga smjena
            evening = self.tb43.text()
            print(registration_number, attendance_date, morning, evening)
            # upit za unos podataka u bazu
            query = f"INSERT INTO attendance (registration_number, attendance_date, morning, evening) VALUES ('{registration_number}', '{attendance_date}', '{morning}', '{evening}')"
            cursor.execute(query)
            mydb.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Prisustvo uspjesno ubaceno u bazu podataka")
            msg.setWindowTitle("Ubacivanje prisustva")
            msg.exec_()
            # ocisti polja
            self.tb42.setText("")
            self.tb43.setText("")
        except con.Error as e:
            print("Upit upisa prisustva u bazu neuspjesan!" + e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Error)
            msg.setText("Greska prilikom upisa prisustva")
            msg.setWindowTitle("Upis prisustva")
            msg.exec_()
# --- Sacuvaj prisustvo ---

# --- Prikazi prisustvo --- 
    def show_attendance(self):
        self.tabWidget.setCurrentIndex(5)
        self.fill_registration_number_in_combobox_for_attendance_tab()
        self.tb41.setText(str(date.today()))
# --- Prikazi prisustvo --- 
# --- Popuni registracione brojeve kod prisustva --- 
    def fill_registration_number_in_combobox_for_attendance_tab(self):
        try:
            self.cb41.clear()
            self.cb42.clear()
            # povezivanje sa bazon
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from student")
            result = cursor.fetchall()
            if result:
                # ubaci registracioni broj svakog studenta u combo box
                for stud_reg_number in result:
                    self.cb41.addItem(str(stud_reg_number[1]))
                    self.cb42.addItem(str(stud_reg_number[1]))
        except con.Error as e:
            print("Greska prilikom izbora registracionog broja u combo boxu" + e)
# --- Popuni registracione brojeve kod prisustva --- 

# --- Obrisi ocjene ---
    def remove_mark_details(self):
        registration_number = str(self.cb32.currentText())
        exam_name = self.cb33.currentText()
        m = QMessageBox.question(self, "Obrisi ocjene", "Molim, potvrdite brisanje ocjena? ", QMessageBox.Yes|QMessageBox.No)
        if m == QMessageBox.Yes:
            try:
                # postavljanje baze
                mydb = con.connect(
                    host="localhost",
                    user="root",
                    password="",
                    db="school")
                cursor = mydb.cursor()
                # registracioni broj uzima preko polja registracionog broja
                query = f"DELETE FROM mark WHERE registration_number = '{registration_number}' and exam_name = '{exam_name}'"
                cursor.execute(query)
                mydb.commit()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Ocjene uspjesno obrisane")
                msg.setWindowTitle("Brisanje ocjena")
                msg.exec_()
                self.tabWidget.setCurrentIndex(1)
            except con.Error as e:
                print("Upit brisanja ocjena u bazu neuspjesan!" + e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Error)
                msg.setText("Greska prilikom brisanja ocjena")
                msg.setWindowTitle("Brisanje ocjena")
                msg.exec_()
# --- Obrisi ocjene ---

# --- Uredi ocjene ---
    def update_mark_details(self):
        try:
            # postavljanje baze
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            # registracioni broj
            registration_number = str(self.cb32.currentText())
            # naziv testa
            test_name = str(self.cb33.currentText())
            # srpski jezik
            language = self.tb37.text()
            # engleski jezik
            english_language = self.tb38.text()
            # matematika
            maths = self.tb39.text()
            # priroda
            science = self.tb310.text()
            # drustvo
            social = self.tb311.text()
            # upit za unos podataka u bazu
            query = f"UPDATE mark SET language = {language}, english = {english_language}, maths = {maths}, science = {science}, social = {social} WHERE registration_number = '{registration_number}' and exam_name = '{test_name}'"
            cursor.execute(query)
            mydb.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Ocjene uspjesno uredjene")
            msg.setWindowTitle("Uredjivanje ocjena")
            msg.exec_()
        except con.Error as e:
            print("Upit upisa ocjena u bazu neuspjesan!" + e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Error)
            msg.setText("Greska prilikom uredjivanja ocjena")
            msg.setWindowTitle("Uredjivanje ocjena")
            msg.exec_()
# --- Uredi ocjene ---

# --- Na osnovu registracionog broja i naziva testa dobij ocjene studenta ---
    def fill_exam_details_in_textbox_for_exam_name_selected(self):
        try:
            registration_number = str(self.cb32.currentText())
            test_name = str(self.cb33.currentText())
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            cursor.execute(f"select * from mark where registration_number = '{registration_number}' and exam_name = '{test_name}'")
            result = cursor.fetchall()
            if result:
                # ispuni polja
                for stud_reg_number in result:
                    self.tb37.setText(str(stud_reg_number[3]))
                    self.tb38.setText(str(stud_reg_number[4]))
                    self.tb39.setText(str(stud_reg_number[5]))
                    self.tb310.setText(str(stud_reg_number[6]))
                    self.tb311.setText(str(stud_reg_number[7]))
        except con.Error as e:
            print("Greska prilikom ispisa ocjena" + e)
# --- Na osnovu registracionog broja i naziva testa dobij ocjene studenta ---
# --- Ispuni imena testova ---
    def fill_exam_names_in_combobox_for_registration_number_selected(self):
        try:
            self.cb33.clear()
            registration_number = str(self.cb32.currentText())
            # povezivanje sa bazon
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            cursor.execute(f"select * from mark where registration_number = '{registration_number}'")
            result = cursor.fetchall()
            if result:
                # ubaci registracioni broj svakog studenta u combo box
                for stud_reg_number in result:
                    self.cb33.addItem(str(stud_reg_number[2]))
        except con.Error as e:
            print("Greska prilikom izbora test u combo boxu" + e)
# --- Ispuni imena testova ---

# --- Dodaj novu ocjenu na bazu ---
    def save_mark_details(self):
        try:
            # postavljanje baze
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            # registracioni broj uzima preko polja registracionog broja
            registration_number = str(self.cb31.currentText())
            # naziv testa
            test_name = self.tb31.text()
            # srpski jezik
            language = self.tb32.text()
            # engleski jezik
            english_language = self.tb33.text()
            # matematika
            maths = self.tb34.text()
            # priroda
            science = self.tb35.text()
            # drustvo
            social = self.tb36.text()
            # upit za unos podataka u bazu
            query = f"INSERT INTO mark (registration_number, exam_name, language, english, maths, science, social) VALUES ('{registration_number}', '{test_name}', {language}, {english_language}, {maths}, {science}, {social})"
            cursor.execute(query)
            mydb.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Ocjene uspjesno ubacene u bazu podataka")
            msg.setWindowTitle("Ubacivanje ocjena")
            msg.exec_()
        except con.Error as e:
            print("Upit upisa ocjena u bazu neuspjesan!" + e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Error)
            msg.setText("Greska prilikom upisa ocjena")
            msg.setWindowTitle("Upis ocjena")
            msg.exec_()
# --- Dodaj novu ocjenu na bazu ---

# --- Otvori meni za ocjene ---
    def show_mark_tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.fill_registration_number_in_combobox_for_mark_tab()
# --- Otvori meni za ocjene ---
# --- Ispuni podatke za registracioni broj ocjena ---
    def fill_registration_number_in_combobox_for_mark_tab(self):
        try:
            self.cb31.clear()
            self.cb32.clear()
            # povezivanje sa bazon
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from student")
            result = cursor.fetchall()
            if result:
                # ubaci registracioni broj svakog studenta u combo box
                for stud_reg_number in result:
                    self.cb31.addItem(str(stud_reg_number[1]))
                    self.cb32.addItem(str(stud_reg_number[1]))
        except con.Error as e:
            print("Greska prilikom izbora registracionog broja u combo boxu" + e)
# --- Ispuni podatke za registracioni broj ocjena ---




# --- Obrisi podatke korisnika ---
    def delete_student_details(self):
        m = QMessageBox.question(self, "Obrisi ucenika", "Molim, potvrdite brisanje ucenika? ", QMessageBox.Yes|QMessageBox.No)
        if m == QMessageBox.Yes:
            try:
                # postavljanje baze
                mydb = con.connect(
                    host="localhost",
                    user="root",
                    password="",
                    db="school")
                cursor = mydb.cursor()
                # registracioni broj uzima preko polja registracionog broja
                registration_number = self.cb21.currentText()
                query = f"DELETE FROM student WHERE registration_number = '{registration_number}'"
                cursor.execute(query)
                mydb.commit()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Ucenik uspjesno obrisan")
                msg.setWindowTitle("Brisanje ucenika")
                msg.exec_()
                self.tabWidget.setCurrentIndex(1)
            except con.Error as e:
                print("Upit upisa ucenika u bazu neuspjesan!" + e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Error)
                msg.setText("Greska prilikom uredjivanja ucenika")
                msg.setWindowTitle("Uredjivanje ucenika")
                msg.exec_()
# --- Obrisi podatke korisnika ---


# --- Azuriraj podatke korisnika ---
    def edit_student_details(self):
        try:
            # postavljanje baze
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            # registracioni broj uzima preko polja registracionog broja
            registration_number = self.cb21.currentText()
            # ime ucenika
            full_name = self.tb21.text()
            # pol ucenika
            gender = self.cb22.currentText()
            # datum rodjenja
            date_of_birth = self.tb23.text()
            # godine
            age = self.tb24.text()
            # adresa
            adress = self.mtb21.toPlainText()
            # phone
            phone = self.tb25.text()
            # email
            email = self.tb26.text()
            # predmet
            standard = self.tb27.text()
            # upit za unos podataka u bazu
            # query = f"INSERT INTO student (registration_number, full_name, gender, date_of_birth, age, adress, phone, email, standard) VALUES ({registration_number}, '{full_name}', '{gender}', '{date_of_birth}', {age}, '{adress}', '{phone}', '{email}', '{standard}')"
            query = f"UPDATE student SET full_name = '{full_name}', gender = '{gender}', date_of_birth = '{date_of_birth}', age = {age}, adress = '{adress}', phone = '{phone}', email = '{email}', standard = '{standard}' WHERE registration_number = '{registration_number}'"
            cursor.execute(query)
            mydb.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Ucenik uspjesno uredjen")
            msg.setWindowTitle("Uredjivanje ucenika")
            msg.exec_()
        except con.Error as e:
            print("Upit upisa ucenika u bazu neuspjesan!" + e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Error)
            msg.setText("Greska prilikom uredjivanja ucenika")
            msg.setWindowTitle("Uredjivanje ucenika")
            msg.exec_()
# --- Azuriraj podatke korisnika ---


# --- UREDI/OBRISI STUDENTA METODA  ---


    def show_edit_delete_student_tab(self):
        self.tabWidget.setCurrentIndex(3)
        self.fill_registration_number_in_combobox()
# --- UREDI/OBRISI STUDENTA METODA ---

# --- REGISTRACIONI BROJ ISPIS METODA ---
    def fill_registration_number_in_combobox(self):
        try:
            self.cb21.clear()
            # povezivanje sa bazon
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from student")
            result = cursor.fetchall()
            if result:
                # ubaci registracioni broj svakog studenta u combo box
                for stud_reg_number in result:
                    self.cb21.addItem(str(stud_reg_number[1]))
        except con.Error as e:
            print("Greska prilikom izbora registracionog broja u combo boxu" + e)
# --- REGISTRACIONI BROJ ISPIS METODA ---


# --- NAKON IZBORA REGISTRACIONOG BROJA ISPUNI DETALJE  ---


    def fill_details_when_combobox_selected(self):
        try:
            # povezivanje sa bazon
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            cursor.execute(
                f"select * from student where registration_number = '{self.cb21.currentText()}'")
            result = cursor.fetchall()
            if result:
                for stud_reg_number in result:
                    # postavi ime ucenika
                    self.tb21.setText(str(stud_reg_number[2]))
                    current_gender = stud_reg_number[3]
                    # postavi pol ucenika
                    if current_gender == "Musko":
                        self.cb22.setCurrentIndex(0)
                    else:
                        self.cb22.setCurrentIndex(1)
                    # datum rodjenja
                    self.tb23.setText(str(stud_reg_number[4]))
                    # godine
                    self.tb24.setText(str(stud_reg_number[5]))
                    # adresa
                    self.mtb21.setText(str(stud_reg_number[6]))
                    # broj telefona
                    self.tb25.setText(str(stud_reg_number[7]))
                    # email
                    self.tb26.setText(str(stud_reg_number[8]))
                    # predmet
                    self.tb27.setText(str(stud_reg_number[9]))

        except con.Error as e:
            print("Greska prilikom ispisa detalja pomocu registracionog broja" + e)
# --- NAKON IZBORA REGISTRACIONOG BROJA ISPUNI DETALJE  ---


# --- SACUVAJ NOVOG UCENIKA -----


    def save_student_details(self):
        try:
            # postavljanje baze
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            # registracioni broj uzima preko polja registracionog broja
            registration_number = self.tb11.text()
            # ime ucenika
            full_name = self.tb12.text()
            # pol ucenika
            gender = self.cb11.currentText()
            # datum rodjenja
            date_of_birth = self.tb13.text()
            # godine
            age = self.tb14.text()
            # adresa
            adress = self.mtb11.toPlainText()
            # phone
            phone = self.tb15.text()
            # email
            email = self.tb16.text()
            # predmet
            standard = self.cb12.currentText()
            # upit za unos podataka u bazu
            query = f"INSERT INTO student (registration_number, full_name, gender, date_of_birth, age, adress, phone, email, standard) VALUES ({registration_number}, '{full_name}', '{gender}', '{date_of_birth}', {age}, '{adress}', '{phone}', '{email}', '{standard}')"
            cursor.execute(query)
            mydb.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Ucenik uspjesno ubacen u bazu podataka")
            msg.setWindowTitle("Ubacivanje ucenika")
            msg.exec_()
        except con.Error as e:
            print("Upit upisa ucenika u bazu neuspjesan!" + e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Error)
            msg.setText("Greska prilikom upisa ucenika")
            msg.setWindowTitle("Ubacivanje ucenika")
            msg.exec_()
# --- SACUVAJ NOVOG UCENIKA -----


# --- DODAJ NOVOG STUDENTA METODA  ---

    def show_add_new_student_tab(self):
        self.tabWidget.setCurrentIndex(2)
        self.fill_next_registration_number()
# --- DODAJ NOVOG STUDENTA METODA ---

# --- REGISTRACIONI BROJ METODA ---
    def fill_next_registration_number(self):
        try:
            # pocetni registracioni broj
            rn = 0
            # povezivanje sa bazon
            mydb = con.connect(
                host="localhost",
                user="root",
                password="",
                db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from student")
            result = cursor.fetchall()
            if result:
                for stud in result:
                    rn += 1
            self.tb11.setText(str(rn + 1))
        except con.Error as e:
            print("Greska prilikom izbora registracionog broja studenta" + e)
# --- REGISTRACIONI BROJ METODA ---

# --- PRIJAVLJIVANJE METODA ---
    def login(self):
        # korisnicko ime
        un = self.tb01.text()
        # lozinka
        pw = self.tb02.text()
        # VALIDACIJA
        if un == "borislav" and pw == "borislav":
            self.tabWidget.setCurrentIndex(1)
            self.menubar.setVisible(True)
        else:
            # prikaz greske
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Molim unesite validne podatke")
            msg.setWindowTitle("Greska")
            msg.exec_()
# --- PRIJAVLJIVANJE METODA ---


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
