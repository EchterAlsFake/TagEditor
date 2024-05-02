"""
Copyright (C) 2024 Johannes Habel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import src.frontend.ressources
import os

from sys import argv
from src.frontend.ui_form import Ui_Form

from PySide6.QtCore import QCoreApplication, QTranslator, QRunnable, QThreadPool, QSemaphore, QFile, QTextStream, QObject, Signal, Qt
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QFileDialog, QTreeWidgetItem, QInputDialog
from PySide6.QtGui import QIcon

from mutagen import File
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
from mutagen.flac import FLAC, Picture, FLACNoHeaderError, error as flac_error
from mutagen.mp4 import MP4, MP4Cover


"""
Global variables
"""
__author__ = "Johannes Habel"
__version__ = "1.0"
__license__ = "GPLv3"

tags_to_be_written = ['title', 'artist', 'album', 'albumartist',
        'date', 'genre', 'tracknumber', 'publisher'
        'composer', 'originalartist', 'conductor', 'comments']


class Signals(QObject):
    signal_read_tag = Signal(dict)
    signal_progress = Signal(int, int)
    signal_get_files = Signal(list)
    signal_error = Signal(str)
    signal_start_undefined_range = Signal()
    signal_stop_undefined_range = Signal()
    signal_finished = Signal()


class LoadFiles(QRunnable):
    def __init__(self, directory):
        super(LoadFiles, self).__init__()
        self.directory = directory
        self.signals = Signals()

    def run(self):
        files_ = []

        self.signals.signal_start_undefined_range.emit()
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                full_path = os.path.join(root, file)
                files_.append(full_path)

        self.signals.signal_get_files.emit(files_)
        self.signals.signal_stop_undefined_range.emit()


class ReadTags(QRunnable):
    def __init__(self, file, is_directory=False):
        super(ReadTags, self).__init__()

        self.signals = Signals()
        self.file = file
        self.is_directory = is_directory
        self.tags_to_extract = [
            'title', 'artist', 'album', 'albumartist', 'date', 'genre', 'tracknumber', 'publisher', 'composer',
            'originalartist', 'lyrics', 'conductor', 'comments']

    def run(self):
        if not self.is_directory:
            files = [self.file]

        else:
            files = self.file

        total_length = len(files)

        for idx, file in enumerate(files):
            try:
                audio = File(file, easy=True)

                if audio is None:
                    self.signals.signal_error.emit(f"Error: File ({file}) is unsupported or not found")

                else:
                    tags = {tag: audio.get(tag, [''])[0] for tag in self.tags_to_extract}
                    tags['idx'] = idx
                    title = audio.get('title', [''])[0]

                    if not title:
                        title = os.path.splitext(os.path.basename(file))[0]

                    tags['title'] = title
                    tags["file_path"] = file
                    self.signals.signal_progress.emit(idx, total_length)
                    self.signals.signal_read_tag.emit(tags)

            except (FLACNoHeaderError, flac_error):
                self.signals.signal_error.emit(f"Error: File: {file} is broken!")

        self.signals.signal_finished.emit()


class TagEditor(QWidget):
    def __init__(self):
        super(TagEditor, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.load_style()
        self.button_connectors()

        self.threadpool = QThreadPool()
        self.semaphore = QSemaphore(5)

        self.last_index = 0
        self.current_item = None

    @classmethod
    def load_stylesheet(cls, path):
        """Load stylesheet from a given path with explicit open and close."""
        file = QFile(path)
        if not file.open(QFile.ReadOnly | QFile.Text):
            return ""
        stylesheet = QTextStream(file).readAll()
        file.close()
        return stylesheet

    def load_style(self):
        """Refactored function to load icons and stylesheets."""
        # Stylesheets
        stylesheet_paths = {
            "progressbar": ":/style/stylesheets/progressbar.qss",
            "button_orange": ":/style/stylesheets/button_orange.qss",
            "button_purple": ":/style/stylesheets/button_purple.qss",
            "button_green": ":/style/stylesheets/button_green.qss",
            "button_blue": ":/style/stylesheets/button_blue.qss"
        }

        stylesheets = {key: self.load_stylesheet(path) for key, path in stylesheet_paths.items()}

        # Applying stylesheets to specific buttons
        # Simplify this part based on actual UI structure and naming
        self.ui.button_apply.setStyleSheet(stylesheets["button_green"])
        self.ui.button_edit_next.setStyleSheet(stylesheets["button_orange"])
        self.ui.button_open_file.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_usage_guide.setStyleSheet(stylesheets["button_green"])
        self.ui.button_change_lyrics.setStyleSheet(stylesheets["button_blue"])
        self.ui.button_change_coverart.setStyleSheet(stylesheets["button_blue"])
        self.ui.button_open_directory.setStyleSheet(stylesheets["button_purple"])
        self.ui.progressbar.setStyleSheet(stylesheets["progressbar"])

        self.header = self.ui.treeWidget.header()
        self.header.resizeSection(0, 300)
        self.header.resizeSection(1, 200)
        self.header.resizeSection(2, 100)
        self.header.resizeSection(3, 100)

    def button_connectors(self):
        self.ui.button_usage_guide.clicked.connect(self.usage_guide)
        self.ui.button_change_coverart.clicked.connect(self.select_cover_art)
        self.ui.button_open_file.clicked.connect(self.load_tags_file)
        self.ui.button_open_directory.clicked.connect(self.load_tags_directory)
        self.ui.treeWidget.itemClicked.connect(self.edit_tags)
        self.ui.button_edit_next.clicked.connect(self.edit_next)
        self.ui.button_change_lyrics.clicked.connect(self.add_lyrics)

    def start_undefined_range(self):
        self.ui.progressbar.setRange(0, 0)

    def stop_undefined_range(self):
        self.ui.progressbar.setRange(0, 1)

    def load_tags_file(self):
        file, type = QFileDialog().getOpenFileName()
        self.load_tags(path=file, is_directory=False)

    def load_tags_directory(self):
        directory = QFileDialog().getExistingDirectory()
        self.ui.lineedit_status.setText("Loading Files...")
        self.load_files_thread = LoadFiles(directory)
        self.load_files_thread.signals.signal_start_undefined_range.connect(self.start_undefined_range)
        self.load_files_thread.signals.signal_stop_undefined_range.connect(self.stop_undefined_range)
        self.load_files_thread.signals.signal_get_files.connect(self.receive_files)
        self.threadpool.start(self.load_files_thread)

    def receive_files(self, files):
        self.load_tags(path=files, is_directory=True)
        self.ui.lineedit_status.setText("Finished Loading files, loading Tags...")

    def load_tags(self, path, is_directory):
        self.read_tags_thread = ReadTags(file=path, is_directory=is_directory)
        self.read_tags_thread.signals.signal_read_tag.connect(self.read_tags_signal)
        self.read_tags_thread.signals.signal_progress.connect(self.update_progressbar)
        self.read_tags_thread.signals.signal_finished.connect(self.finished)
        self.threadpool.start(self.read_tags_thread)

    def read_tags_signal(self, data):
        # Collect tags from data dictionary and store in the global dictionary
        TagEditor.tags_to_be_written = {key: data.get(key, '') for key in data.keys() if key != 'file_path'}

        # Create and update tree widget item with tag data
        item = QTreeWidgetItem(self.ui.treeWidget)
        for idx, (tag, value) in enumerate(TagEditor.tags_to_be_written.items(), start=0):
            item.setText(idx, f"{idx}) {value}")
            item.setData(idx, Qt.UserRole, str(value))
        item.setData(13, Qt.UserRole, data.get("file_path"))  # Set the file path separately

    def edit_tags(self, item, column):
        self.current_item = item
        self.last_index = self.ui.treeWidget.indexOfTopLevelItem(item)

        # Collect tags from item data and store in the global dictionary
        TagEditor.tags_to_be_written = {
            "title": item.data(0, Qt.UserRole),
            "artist": item.data(1, Qt.UserRole),
            "album": item.data(2, Qt.UserRole),
            "albumartist": item.data(3, Qt.UserRole),
            "year": item.data(4, Qt.UserRole),
            "genre": item.data(5, Qt.UserRole),
            "tracknumber": item.data(6, Qt.UserRole),
            "publisher": item.data(7, Qt.UserRole),
            "composer": item.data(8, Qt.UserRole),
            "originalartist": item.data(9, Qt.UserRole),
            "conductor": item.data(11, Qt.UserRole),
            "comments": item.data(12, Qt.UserRole)
        }

        # Set the line edits to the values from the global dictionary
        for tag, line_edit in zip(TagEditor.tags_to_be_written.keys(),
                                  [self.ui.lineedit_title, self.ui.lineedit_artist, self.ui.lineedit_album,
                                   self.ui.lineedit_album_artist, self.ui.lineedit_year, self.ui.lineedit_genre,
                                   self.ui.lineedit_track_number, self.ui.lineedit_publisher, self.ui.lineedit_composer,
                                   self.ui.lineedit_original_artist, self.ui.lineedit_conductor,
                                   self.ui.lineedit_comments]):
            line_edit.setText(TagEditor.tags_to_be_written[tag])

    def edit_next(self):
        self.last_index += 1
        self.edit_tags(item=self.ui.treeWidget.topLevelItem(self.last_index), column=0)

    def finished(self):
        self.ui.progressbar.setValue(0)
        self.ui.progressbar.setMaximum(100)
        self.edit_tags(item=self.ui.treeWidget.topLevelItem(0), column=0)
        self.ui.lineedit_status.clear()

    def update_progressbar(self, pos, total):
        self.ui.progressbar.setValue(pos)
        self.ui.progressbar.setMaximum(total)

    def on_error(self, e):
        self.ui_popup(e)

    def select_cover_art(self):
        art_path, _ = QFileDialog.getOpenFileName(None, "Select Cover Art", "", "Image Files (*.png *.jpg *.jpeg)")
        if not art_path:
            return

        if self.current_item is None:
            print("No file selected")
            return

        file_path = self.current_item.data(13, Qt.UserRole)  # Annahme, dass dies der Pfad zur Datei ist

        # Bestimme den Dateityp basierend auf der Dateierweiterung
        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.mp3':
            self.add_cover_art_mp3(file_path, art_path)
        elif ext == '.flac':
            self.add_cover_art_flac(file_path, art_path)
        elif ext in ['.m4a', '.mp4']:
            self.add_cover_art_m4a(file_path, art_path)
        else:
            print("Unsupported file format")

    def add_cover_art_mp3(self, file_path, art_path):
        audio = MP3(file_path, ID3=ID3)
        try:
            audio.add_tags()
        except Exception as e:
            pass

        with open(art_path, "rb") as img_file:
            img_data = img_file.read()
            audio.tags.add(APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,  # Cover front
                desc='Cover',
                data=img_data
            ))
        audio.save()

    def add_cover_art_flac(self, file_path, art_path):
        audio = FLAC(file_path)
        pic = Picture()
        pic.type = 3
        pic.mime = 'image/jpeg'
        pic.desc = 'Cover'
        with open(art_path, "rb") as img_file:
            pic.data = img_file.read()
        audio.add_picture(pic)
        audio.save()

    def add_cover_art_m4a(self, file_path, art_path):
        audio = MP4(file_path)
        with open(art_path, "rb") as img_file:
            cover_data = img_file.read()
        audio["covr"] = [MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_JPEG)]
        audio.save()

    def apply_tags(self):
        # Collect tags from UI inputs and store in the global dictionary
        TagEditor.tags_to_be_written = {
            "title": self.ui.lineedit_title.text(),
            "artist": self.ui.lineedit_artist.text(),
            "album": self.ui.lineedit_album.text(),
            "albumartist": self.ui.lineedit_album_artist.text(),
            "year": self.ui.lineedit_year.text(),
            "genre": self.ui.lineedit_genre.text(),
            "tracknumber": self.ui.lineedit_track_number.text(),
            "comments": self.ui.lineedit_comments.text(),
            "composer": self.ui.lineedit_composer.text(),
            "originalartist": self.ui.lineedit_original_artist.text(),
            "conductor": self.ui.lineedit_conductor.text(),
            "publisher": self.ui.lineedit_publisher.text(),
            "description": self.ui.lineedit_description.text(),
        }

        # Use the Mutagen library to write the tags
        file = self.current_item.data[14]
        audio = File(file, easy=True)
        for tag, value in TagEditor.tags_to_be_written.items():
            if value:  # Only update tags that have been provided
                audio[tag] = value
        audio.save()

    @classmethod
    def ui_popup(cls, text):
        message_box = QMessageBox()
        message_box.setText(text)
        message_box.exec()

    def usage_guide(self):
        self.ui_popup(QCoreApplication.tr(
"""
Click on 'Open File' to open a music file or 'Open Directory' to open a directory (and their subdirectories).
All files found will be listed in the tree widget (the thing in the left).

You can click on a song their and edit the metadata on the right. After you are done, click on 'Apply' to apply the tags.
Note: The Lyrics and the Cover Art will be immeditately applied, when you select them.

Tag Editor supports the following file formats:

MP3,FLAC,M4A,OGG,WAV,WMA,AIFF,APE,MPC,TrueAudio (TTA), OptimFROG, Speex, ASF, WV, MP4, AAC

(and even more...)


If you experience any issues, please let me know :)
""", None))

    def add_lyrics(self):
        input_dialog, ok = QInputDialog().getText(self, "Add Lyrics", "Add lyrics")
        print(input_dialog)



def main():
    app = QApplication(argv)

    file = QFile(":/style/stylesheets/stylesheet.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    w = TagEditor()
    w.show()
    app.exec()

if __name__ == "__main__":
    main()