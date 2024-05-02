# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QProgressBar,
    QPushButton, QScrollArea, QSizePolicy, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1728, 463)
        self.gridLayout_6 = QGridLayout(Form)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1694, 472))
        self.gridLayout_5 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.widget = QWidget(self.scrollAreaWidgetContents)
        self.widget.setObjectName(u"widget")
        self.gridLayout_4 = QGridLayout(self.widget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.progressbar = QProgressBar(self.widget)
        self.progressbar.setObjectName(u"progressbar")
        self.progressbar.setValue(0)

        self.verticalLayout.addWidget(self.progressbar)


        self.gridLayout_4.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_open_file = QPushButton(self.widget)
        self.button_open_file.setObjectName(u"button_open_file")

        self.horizontalLayout.addWidget(self.button_open_file)

        self.button_open_directory = QPushButton(self.widget)
        self.button_open_directory.setObjectName(u"button_open_directory")

        self.horizontalLayout.addWidget(self.button_open_directory)

        self.button_usage_guide = QPushButton(self.widget)
        self.button_usage_guide.setObjectName(u"button_usage_guide")

        self.horizontalLayout.addWidget(self.button_usage_guide)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineedit_description = QLineEdit(self.groupBox)
        self.lineedit_description.setObjectName(u"lineedit_description")

        self.gridLayout.addWidget(self.lineedit_description, 7, 3, 1, 1)

        self.label_publisher = QLabel(self.groupBox)
        self.label_publisher.setObjectName(u"label_publisher")

        self.gridLayout.addWidget(self.label_publisher, 5, 2, 1, 1)

        self.lineedit_track_number = QLineEdit(self.groupBox)
        self.lineedit_track_number.setObjectName(u"lineedit_track_number")

        self.gridLayout.addWidget(self.lineedit_track_number, 7, 1, 1, 1)

        self.lineedit_title = QLineEdit(self.groupBox)
        self.lineedit_title.setObjectName(u"lineedit_title")

        self.gridLayout.addWidget(self.lineedit_title, 1, 1, 1, 1)

        self.label_composer = QLabel(self.groupBox)
        self.label_composer.setObjectName(u"label_composer")

        self.gridLayout.addWidget(self.label_composer, 1, 2, 1, 1)

        self.label_description = QLabel(self.groupBox)
        self.label_description.setObjectName(u"label_description")

        self.gridLayout.addWidget(self.label_description, 7, 2, 1, 1)

        self.lineedit_album_artist = QLineEdit(self.groupBox)
        self.lineedit_album_artist.setObjectName(u"lineedit_album_artist")

        self.gridLayout.addWidget(self.lineedit_album_artist, 4, 1, 1, 1)

        self.lineedit_composer = QLineEdit(self.groupBox)
        self.lineedit_composer.setObjectName(u"lineedit_composer")

        self.gridLayout.addWidget(self.lineedit_composer, 1, 3, 1, 1)

        self.lineedit_conductor = QLineEdit(self.groupBox)
        self.lineedit_conductor.setObjectName(u"lineedit_conductor")

        self.gridLayout.addWidget(self.lineedit_conductor, 4, 3, 1, 1)

        self.label_artist = QLabel(self.groupBox)
        self.label_artist.setObjectName(u"label_artist")

        self.gridLayout.addWidget(self.label_artist, 2, 0, 1, 1)

        self.label_title = QLabel(self.groupBox)
        self.label_title.setObjectName(u"label_title")

        self.gridLayout.addWidget(self.label_title, 1, 0, 1, 1)

        self.label_genre = QLabel(self.groupBox)
        self.label_genre.setObjectName(u"label_genre")

        self.gridLayout.addWidget(self.label_genre, 6, 0, 1, 1)

        self.label_comments = QLabel(self.groupBox)
        self.label_comments.setObjectName(u"label_comments")

        self.gridLayout.addWidget(self.label_comments, 8, 0, 1, 1)

        self.label_original_artist = QLabel(self.groupBox)
        self.label_original_artist.setObjectName(u"label_original_artist")

        self.gridLayout.addWidget(self.label_original_artist, 2, 2, 1, 1)

        self.lineedit_album = QLineEdit(self.groupBox)
        self.lineedit_album.setObjectName(u"lineedit_album")

        self.gridLayout.addWidget(self.lineedit_album, 3, 1, 1, 1)

        self.lineedit_artist = QLineEdit(self.groupBox)
        self.lineedit_artist.setObjectName(u"lineedit_artist")

        self.gridLayout.addWidget(self.lineedit_artist, 2, 1, 1, 1)

        self.label_year = QLabel(self.groupBox)
        self.label_year.setObjectName(u"label_year")

        self.gridLayout.addWidget(self.label_year, 5, 0, 1, 1)

        self.lineedit_original_artist = QLineEdit(self.groupBox)
        self.lineedit_original_artist.setObjectName(u"lineedit_original_artist")

        self.gridLayout.addWidget(self.lineedit_original_artist, 2, 3, 1, 1)

        self.label_cover_art = QLabel(self.groupBox)
        self.label_cover_art.setObjectName(u"label_cover_art")

        self.gridLayout.addWidget(self.label_cover_art, 6, 2, 1, 1)

        self.label_album = QLabel(self.groupBox)
        self.label_album.setObjectName(u"label_album")

        self.gridLayout.addWidget(self.label_album, 3, 0, 1, 1)

        self.label_lyrics = QLabel(self.groupBox)
        self.label_lyrics.setObjectName(u"label_lyrics")

        self.gridLayout.addWidget(self.label_lyrics, 3, 2, 1, 1)

        self.button_change_coverart = QPushButton(self.groupBox)
        self.button_change_coverart.setObjectName(u"button_change_coverart")

        self.gridLayout.addWidget(self.button_change_coverart, 6, 3, 1, 1)

        self.label_conductor = QLabel(self.groupBox)
        self.label_conductor.setObjectName(u"label_conductor")

        self.gridLayout.addWidget(self.label_conductor, 4, 2, 1, 1)

        self.lineedit_comments = QLineEdit(self.groupBox)
        self.lineedit_comments.setObjectName(u"lineedit_comments")

        self.gridLayout.addWidget(self.lineedit_comments, 8, 1, 1, 3)

        self.label_track_number = QLabel(self.groupBox)
        self.label_track_number.setObjectName(u"label_track_number")

        self.gridLayout.addWidget(self.label_track_number, 7, 0, 1, 1)

        self.button_apply = QPushButton(self.groupBox)
        self.button_apply.setObjectName(u"button_apply")

        self.gridLayout.addWidget(self.button_apply, 9, 0, 1, 2)

        self.button_edit_next = QPushButton(self.groupBox)
        self.button_edit_next.setObjectName(u"button_edit_next")

        self.gridLayout.addWidget(self.button_edit_next, 9, 2, 1, 2)

        self.lineedit_publisher = QLineEdit(self.groupBox)
        self.lineedit_publisher.setObjectName(u"lineedit_publisher")

        self.gridLayout.addWidget(self.lineedit_publisher, 5, 3, 1, 1)

        self.lineedit_year = QLineEdit(self.groupBox)
        self.lineedit_year.setObjectName(u"lineedit_year")

        self.gridLayout.addWidget(self.lineedit_year, 5, 1, 1, 1)

        self.lineedit_genre = QLineEdit(self.groupBox)
        self.lineedit_genre.setObjectName(u"lineedit_genre")

        self.gridLayout.addWidget(self.lineedit_genre, 6, 1, 1, 1)

        self.button_change_lyrics = QPushButton(self.groupBox)
        self.button_change_lyrics.setObjectName(u"button_change_lyrics")

        self.gridLayout.addWidget(self.button_change_lyrics, 3, 3, 1, 1)

        self.label_album_artist = QLabel(self.groupBox)
        self.label_album_artist.setObjectName(u"label_album_artist")

        self.gridLayout.addWidget(self.label_album_artist, 4, 0, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 4)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox, 1, 1, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.treeWidget = QTreeWidget(self.widget)
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout_2.addWidget(self.treeWidget)


        self.gridLayout_4.addLayout(self.verticalLayout_2, 1, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_ststus = QLabel(self.widget)
        self.label_ststus.setObjectName(u"label_ststus")

        self.horizontalLayout_3.addWidget(self.label_ststus)

        self.lineedit_status = QLineEdit(self.widget)
        self.lineedit_status.setObjectName(u"lineedit_status")
        self.lineedit_status.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.lineedit_status)

        self.label_update = QLabel(self.widget)
        self.label_update.setObjectName(u"label_update")

        self.horizontalLayout_3.addWidget(self.label_update)

        self.lineedit_update = QLineEdit(self.widget)
        self.lineedit_update.setObjectName(u"lineedit_update")
        self.lineedit_update.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.lineedit_update)


        self.gridLayout_4.addLayout(self.horizontalLayout_3, 2, 0, 1, 2)


        self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_6.addWidget(self.scrollArea, 0, 0, 1, 1)

        QWidget.setTabOrder(self.scrollArea, self.button_open_file)
        QWidget.setTabOrder(self.button_open_file, self.button_open_directory)
        QWidget.setTabOrder(self.button_open_directory, self.button_usage_guide)
        QWidget.setTabOrder(self.button_usage_guide, self.treeWidget)
        QWidget.setTabOrder(self.treeWidget, self.lineedit_title)
        QWidget.setTabOrder(self.lineedit_title, self.lineedit_composer)
        QWidget.setTabOrder(self.lineedit_composer, self.lineedit_artist)
        QWidget.setTabOrder(self.lineedit_artist, self.lineedit_original_artist)
        QWidget.setTabOrder(self.lineedit_original_artist, self.lineedit_album)
        QWidget.setTabOrder(self.lineedit_album, self.button_change_lyrics)
        QWidget.setTabOrder(self.button_change_lyrics, self.lineedit_album_artist)
        QWidget.setTabOrder(self.lineedit_album_artist, self.lineedit_conductor)
        QWidget.setTabOrder(self.lineedit_conductor, self.lineedit_year)
        QWidget.setTabOrder(self.lineedit_year, self.lineedit_publisher)
        QWidget.setTabOrder(self.lineedit_publisher, self.lineedit_genre)
        QWidget.setTabOrder(self.lineedit_genre, self.button_change_coverart)
        QWidget.setTabOrder(self.button_change_coverart, self.lineedit_track_number)
        QWidget.setTabOrder(self.lineedit_track_number, self.lineedit_description)
        QWidget.setTabOrder(self.lineedit_description, self.lineedit_comments)
        QWidget.setTabOrder(self.lineedit_comments, self.button_apply)
        QWidget.setTabOrder(self.button_apply, self.button_edit_next)
        QWidget.setTabOrder(self.button_edit_next, self.lineedit_status)
        QWidget.setTabOrder(self.lineedit_status, self.lineedit_update)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Tag Editor (C) Johannes Habel GPLv3 v1.0 -- Source Code: https://github.com/EchterAlsFake/TagEditor", None))
        self.button_open_file.setText(QCoreApplication.translate("Form", u"Open a file", None))
        self.button_open_directory.setText(QCoreApplication.translate("Form", u"Open a directory", None))
        self.button_usage_guide.setText(QCoreApplication.translate("Form", u"Usage Guide", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Editing...", None))
        self.label_publisher.setText(QCoreApplication.translate("Form", u"Publisher:", None))
        self.label_composer.setText(QCoreApplication.translate("Form", u"Composer:", None))
        self.label_description.setText(QCoreApplication.translate("Form", u"Description:", None))
        self.label_artist.setText(QCoreApplication.translate("Form", u"Artist:", None))
        self.label_title.setText(QCoreApplication.translate("Form", u"Title:", None))
        self.label_genre.setText(QCoreApplication.translate("Form", u"Genre:", None))
        self.label_comments.setText(QCoreApplication.translate("Form", u"Comments:", None))
        self.label_original_artist.setText(QCoreApplication.translate("Form", u"Original Artist:", None))
        self.label_year.setText(QCoreApplication.translate("Form", u"Year:", None))
        self.label_cover_art.setText(QCoreApplication.translate("Form", u"Cover Art:", None))
        self.label_album.setText(QCoreApplication.translate("Form", u"Album:", None))
        self.label_lyrics.setText(QCoreApplication.translate("Form", u"Lyrics:", None))
        self.button_change_coverart.setText(QCoreApplication.translate("Form", u"Select", None))
        self.label_conductor.setText(QCoreApplication.translate("Form", u"Conductor:", None))
        self.label_track_number.setText(QCoreApplication.translate("Form", u"Track Number:", None))
        self.button_apply.setText(QCoreApplication.translate("Form", u"Apply", None))
        self.button_edit_next.setText(QCoreApplication.translate("Form", u"Edit next file", None))
        self.button_change_lyrics.setText(QCoreApplication.translate("Form", u"Change", None))
        self.label_album_artist.setText(QCoreApplication.translate("Form", u"Album Artist:", None))
        self.label.setText(QCoreApplication.translate("Form", u"Important: Not all file types support every attribute. You'll be able to write them, but if they don't show up after you edited them, it means it's not supported!", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Form", u"Album", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"Artist", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Title", None));
        self.label_ststus.setText(QCoreApplication.translate("Form", u"Status:", None))
        self.label_update.setText(QCoreApplication.translate("Form", u"Update:", None))
    # retranslateUi

