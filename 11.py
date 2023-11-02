import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QTabWidget, QPushButton, QMainWindow, QLabel, \
    QPlainTextEdit, QComboBox, QTableWidgetItem, QMessageBox, QTableWidget


class AddFilmWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(300, 300, 400, 400)

        self.title_lbl = QLabel('Название', self)
        self.title_lbl.move(10, 10)

        self.title = QPlainTextEdit(self)
        self.title.move(150, 10)
        self.title.resize(200, 30)

        self.year_lbl = QLabel('Год выпуска', self)
        self.year_lbl.move(10, 60)

        self.year = QPlainTextEdit(self)
        self.year.move(150, 60)
        self.year.resize(200, 30)

        self.genre_lbl = QLabel('Жанр', self)
        self.genre_lbl.move(10, 110)

        self.comboBox = QComboBox(self)
        self.comboBox.move(150, 110)
        self.comboBox.resize(200, 30)

        self.duration_lbl = QLabel('Длина', self)
        self.duration_lbl.move(10, 160)

        self.duration = QPlainTextEdit(self)
        self.duration.move(150, 160)
        self.duration.resize(200, 30)

        self.con = sqlite3.connect("films_db.sqlite")
        self.cur = self.con.cursor()
        self.genres = self.cur.execute("SELECT * from genres").fetchall()

        self.params = {}
        for key, value in self.genres:
            self.params[value] = key

        self.comboBox.addItems(self.params.keys())

        self.pushButton = QPushButton('Сохранить', self)
        self.pushButton.move(150, 200)
        self.pushButton.resize(150, 30)

        self.statusbar = self.statusBar()

    def try_to_add(self):
        if self.get_adding_verdict():
            self.con.commit()
            self.parent().update_films()
            self.close()

    def try_to_edit(self):
        if self.get_editing_verdict():
            self.con.commit()
            self.parent().update_films()
            self.close()

    def get_adding_verdict(self):
        try:
            title = self.title.toPlainText()
            year = int(self.year.toPlainText())
            genre = int(self.params[self.comboBox.currentText()])
            duration = int(self.duration.toPlainText())

            if not title or year > 2023 or duration < 0:
                raise NameError

            self.cur.execute(f'''INSERT INTO films(title, year, genre, duration)
             VALUES("{title}", {year}, {genre}, {duration})''')
            self.con.commit()
            return True

        except Exception:
            self.statusbar.showMessage('Неверно заполнена форма')
            return False

    def get_editing_verdict(self):
        try:
            title = self.title.toPlainText()
            year = int(self.year.toPlainText())
            genre = int(self.params[self.comboBox.currentText()])
            duration = int(self.duration.toPlainText())
            row = self.parent().filmsTable.currentRow()

            if not title or year > 2023 or duration < 0:
                raise ValueError

            ID = self.parent().filmsTable.item(row, 0).text()
            self.cur.execute(f'''UPDATE films SET title = '{title}', year = {year},
             genre = {genre}, duration = {duration} where id == {ID}''')
            self.con.commit()
            return True

        except Exception as ex:
            if ex.__class__.__name__ == 'ValueError':
                self.statusbar.showMessage('Неверно заполнена форма')
            else:
                print('error')
            return False


class AddGenreWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(300, 300, 400, 400)

        self.title_lbl = QLabel('Название', self)
        self.title_lbl.move(10, 10)

        self.title = QPlainTextEdit(self)
        self.title.move(150, 10)
        self.title.resize(200, 30)

        self.con = sqlite3.connect("films_db.sqlite")
        self.cur = self.con.cursor()

        self.pushButton = QPushButton('Сохранить', self)
        self.pushButton.move(150, 200)
        self.pushButton.resize(150, 30)

        self.statusbar = self.statusBar()

    def try_to_add(self):
        if self.get_adding_verdict():
            self.con.commit()
            self.parent().update_genres()
            self.close()

    def try_to_edit(self):
        if self.get_editing_verdict():
            self.con.commit()
            self.parent().update_genres()
            self.close()

    def get_adding_verdict(self):
        try:
            title = self.title.toPlainText()
            if not title:
                raise NameError

            self.cur.execute(f'''INSERT INTO genres (title) VALUES("{title}")''')
            self.con.commit()
            return True

        except Exception:
            self.statusbar.showMessage('Неверно заполнена форма')
            return False

    def get_editing_verdict(self):
        try:
            title = self.title.toPlainText()
            row = self.parent().genresTable.currentRow()

            if not title:
                raise ValueError

            ID = self.parent().genresTable.item(row, 0).text()
            self.cur.execute(f'''UPDATE genres SET title = '{title}' where id == {ID}''')
            self.con.commit()
            return True

        except Exception as ex:
            if ex.__class__.__name__ == 'ValueError':
                self.statusbar.showMessage('Неверно заполнена форма')
            else:
                print('error')
            return False


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 650, 600)
        self.status = self.statusBar()

        main_layout = QGridLayout(self)
        self.setLayout(main_layout)
        self.tabWidget = QTabWidget(self)

        # создание страниц
        self.filmsTab = QWidget(self)
        first_layout = QGridLayout()
        self.filmsTab.setLayout(first_layout)

        self.genresTab = QWidget(self)
        second_layout = QGridLayout()
        self.genresTab.setLayout(second_layout)

        # интерфейс первой страницы
        self.addFilmButton = QPushButton('Добавить фильм', self)
        self.addFilmButton.clicked.connect(self.add_film)
        first_layout.addWidget(self.addFilmButton, 0, 0, 1, 1)

        self.editFilmButton = QPushButton('Изменить фильм', self)
        self.editFilmButton.clicked.connect(self.edit_film)
        first_layout.addWidget(self.editFilmButton, 0, 2, 1, 1)

        self.deleteFilmButton = QPushButton('Удалить фильм', self)
        self.deleteFilmButton.clicked.connect(self.delete_film)
        first_layout.addWidget(self.deleteFilmButton, 0, 4, 1, 1)

        self.filmsTable = QTableWidget(self)
        first_layout.addWidget(self.filmsTable, 1, 0, 8, 8)

        # интерфейс второй страницы
        self.addGenreButton = QPushButton('Добавить жанр', self)
        self.addGenreButton.clicked.connect(self.add_genre)
        second_layout.addWidget(self.addGenreButton, 0, 0, 1, 1)

        self.editGenreButton = QPushButton('Изменить жанр', self)
        self.editGenreButton.clicked.connect(self.edit_genre)
        second_layout.addWidget(self.editGenreButton, 0, 2, 1, 1)

        self.deleteGenreButton = QPushButton('Удалить жанр', self)
        self.deleteGenreButton.clicked.connect(self.delete_genre)
        second_layout.addWidget(self.deleteGenreButton, 0, 4, 1, 1)

        self.genresTable = QTableWidget(self)
        second_layout.addWidget(self.genresTable, 1, 0, 8, 8)

        self.tabWidget.addTab(self.filmsTab, 'Фильмы')
        self.tabWidget.addTab(self.genresTab, 'Жанры')

        # отбражение страниц
        main_layout.addWidget(self.tabWidget, 0, 0, 2, 1)
        self.container = QWidget(self)
        self.container.setLayout(main_layout)
        self.setCentralWidget(self.container)

        # работа с БД
        self.con = sqlite3.connect("films_db.sqlite")
        self.cur = self.con.cursor()

        # отображение данных в таблицы
        self.update_films()
        self.update_genres()

        self.tabWidget.currentChanged.connect(self.tab_changed)

    # методы для кнопок
    def add_film(self):
        self.add_film_widget = AddFilmWidget(self)
        self.add_film_widget.pushButton.disconnect()
        self.add_film_widget.pushButton.clicked.connect(self.add_film_widget.try_to_add)
        self.add_film_widget.show()

    def edit_film(self):
        self.status.showMessage('')
        self.edit_film_widget = AddFilmWidget(self)
        self.edit_film_widget.pushButton.disconnect()
        row = self.filmsTable.currentRow()
        if row == -1:
            self.status.showMessage('Элемент не выбран')
        else:
            self.edit_film_widget.pushButton.clicked.connect(self.edit_film_widget.try_to_edit)
            self.edit_film_widget.show()
            self.edit_film_widget.title.setPlainText(self.filmsTable.item(row, 1).text())
            self.edit_film_widget.year.setPlainText(self.filmsTable.item(row, 2).text())
            self.edit_film_widget.comboBox.setCurrentText(self.filmsTable.item(row, 3).text())
            self.edit_film_widget.duration.setPlainText(self.filmsTable.item(row, 4).text())

    def delete_film(self):
        row = self.filmsTable.currentRow()
        if row == -1:
            self.status.showMessage('Элемент не выбран')
        else:
            ID = self.filmsTable.item(row, 0).text()
            userResponse = QMessageBox.question(self, 'Are you sure?',
                                                f'Вы уверены, что хотите удалить фильм с id = {ID}',
                                                QMessageBox.Yes | QMessageBox.No)

            if userResponse == QMessageBox.Yes:
                self.cur.execute(f'DELETE from films where id == {ID}')
                self.con.commit()
                self.update_films()

    def add_genre(self):
        self.add_genre_widget = AddGenreWidget(self)
        self.add_genre_widget.pushButton.disconnect()
        self.add_genre_widget.pushButton.clicked.connect(self.add_genre_widget.try_to_add)
        self.add_genre_widget.show()

    def edit_genre(self):
        self.status.showMessage('')
        self.edit_genre_widget = AddGenreWidget(self)
        self.edit_genre_widget.pushButton.disconnect()
        row = self.genresTable.currentRow()
        if row == -1:
            self.status.showMessage('Элемент не выбран')
        else:
            self.edit_genre_widget.pushButton.clicked.connect(self.edit_genre_widget.try_to_edit)
            self.edit_genre_widget.show()
            self.edit_genre_widget.title.setPlainText(self.genresTable.item(row, 1).text())

    def delete_genre(self):
        row = self.genresTable.currentRow()
        if row == -1:
            self.status.showMessage('Элемент не выбран')
        else:
            ID = self.genresTable.item(row, 0).text()
            userResponse = QMessageBox.question(self, 'Are you sure?',
                                                f'Вы уверены, что хотите удалить жанр с id = {ID}',
                                                QMessageBox.Yes | QMessageBox.No)

            if userResponse == QMessageBox.Yes:
                self.cur.execute(f'DELETE from genres where id == {ID}')
                self.con.commit()
                self.update_genres()
                self.update_films()

    # методы для отбражени данных
    def update_films(self):
        self.genres = self.cur.execute("SELECT * from genres").fetchall()
        self.result = self.cur.execute("SELECT * from films").fetchall()

        self.id_gen = {}
        for key, value in self.genres:
            self.id_gen[key] = value

        self.filmsTable.setRowCount(len(self.result))
        self.filmsTable.setColumnCount(len(self.result[0]))

        title = ['ИД', 'Название фильма', 'Год выпуска', 'Жанр', 'Продолжительность']
        self.filmsTable.setHorizontalHeaderLabels(title)

        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                if j == 3:
                    if val not in self.id_gen:
                        self.filmsTable.setItem(i, j, QTableWidgetItem(str(val)))
                    else:
                        self.filmsTable.setItem(i, 3, QTableWidgetItem(self.id_gen[val]))
                else:
                    self.filmsTable.setItem(i, j, QTableWidgetItem(str(val)))

    def update_genres(self):
        self.genres = self.cur.execute("SELECT * from genres").fetchall()

        self.genresTable.setRowCount(len(self.genres))
        self.genresTable.setColumnCount(len(self.genres[0]))

        title = ['ИД', 'Название жанра']
        self.genresTable.setHorizontalHeaderLabels(title)

        for i, elem in enumerate(self.genres):
            for j, val in enumerate(elem):
                self.genresTable.setItem(i, j, QTableWidgetItem(str(val)))

    def tab_changed(self, index):
        if index == 0:
            self.update_films()
        else:
            self.update_genres()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())