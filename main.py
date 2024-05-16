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
import argparse

from sys import argv
from src.frontend.ui_form import Ui_Form
from src.backend.consts import *
from src.backend.shared_functions import *

from PySide6.QtCore import (QCoreApplication, QTranslator, QRunnable, QThreadPool, QFile, QTextStream, Qt, QLocale)
from PySide6.QtWidgets import (QApplication, QWidget, QMessageBox, QFileDialog, QTreeWidgetItem, QDialog)


from requests import get
from mutagen.id3 import APIC, Encoding
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, USLT
from mutagen.flac import FLAC, Picture, FLACNoHeaderError, error as flac_error
from mutagen.mp4 import MP4, MP4Cover
from mutagen.oggvorbis import OggVorbis

__author__ = "Johannes Habel"
__version__ = "1.0"
__next_release__ = "1.1"
__license__ = "GPLv3"

errors = []  # This dictionary saves all files with the error that happened


class Setup(QRunnable):
    """
    Checks for an update and notifies the user if an update was found.
    """

    def __init__(self):
        super(Setup, self).__init__()
        self.signals = Signals()

    def run(self):
        try:
            _ = get(f"https://github.com/EchterAlsFake/TagEditor/releases/{__next_release__}")

            if _.status_code == 200:
                self.signals.signal_update_result.emit(True)

            elif _.status_code == 404:
                self.signals.signal_update_result.emit(False)

            else:
                print("Error checking for an update...")

        except Exception as e:
            print(f"Error checking for an update... {e}")


class LoadFiles(QRunnable):
    def __init__(self, directory):
        super(LoadFiles, self).__init__()
        self.directory = directory
        self.signals = Signals()

    def run(self):
        files_ = []
        invalid_extensions = [".jpg", ".jpeg", ".png", ".cue", ".mov", ".log", ".m3u", ".txt", ".mp4", ".JPG", ".mkv"
                              ".nfo", ".CUE", ".LOG", ".M3U", ".gif", ".pdf", ".clpi", ".mpls", ".m2ts", ".bdmv", ".iso",
                              ".xml", ".sqlite", "nfo", ".sfv"]

        self.signals.signal_start_undefined_range.emit()
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if not file.endswith(tuple(invalid_extensions)):
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
        files = [self.file] if not self.is_directory else self.file
        total_length = len(files)

        for idx, file in enumerate(files):
            try:
                file_extension = os.path.splitext(file)[1].lower()
                tag_mapping = get_tag_mapping(file_extension)
                if not tag_mapping:
                    _ = {"path": file, "error": "Not supported"}
                    errors.append(_)
                    continue

                audio = get_audio_file(file, file_extension)
                if audio:
                    tags = {}
                    for tag in self.tags_to_extract:
                        tag_name = tag_mapping.get(tag)
                        if tag_name:
                            tags[tag] = audio.get(tag_name, [''])[0]

                    title = tags['title'] if tags['title'] else os.path.splitext(os.path.basename(file))[0]
                    tags.update({'title': title, 'idx': idx, "file_path": file})
                    self.signals.signal_progress.emit(idx, total_length)
                    self.signals.signal_read_tag.emit(tags)

                else:
                    print(f"The file: {file} couldn't be loaded, because it's not supported or contains invalid headers.")

            except FLACNoHeaderError:
                _ = {"path": file, "error": "FLAC Header is invalid!"}
                errors.append(_)

            except flac_error:
                _ = {"path": file, "error": "FLAC file is corrupted!"}

        self.signals.signal_finished.emit()


class TagEditor(QWidget):
    def __init__(self):
        super(TagEditor, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.load_style()
        self.button_connectors()

        self.threadpool = QThreadPool()
        self.last_index = 0
        self.current_item = None
        self.setup()

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
        self.ui.stackedWidget.setCurrentIndex(0)

        self.header = self.ui.treeWidget.header()
        self.header.resizeSection(0, 300)
        self.header.resizeSection(1, 200)
        self.header.resizeSection(2, 100)
        self.header.resizeSection(3, 100)

        self.header_2 = self.ui.treeWidget_2.header()
        self.header_2.resizeSection(0, 300)
        self.header_2.resizeSection(1, 200)

    def button_connectors(self):
        self.ui.button_open_file.clicked.connect(self.load_tags_file)
        self.ui.button_open_directory.clicked.connect(self.load_tags_directory)
        self.ui.treeWidget.itemClicked.connect(self.edit_tags)
        self.ui.button_edit_next.clicked.connect(self.edit_next)
        self.ui.button_change_coverart.clicked.connect(self.select_cover_art)
        self.ui.button_change_lyrics.clicked.connect(self.add_lyrics)
        self.ui.button_apply.clicked.connect(self.apply_tags)
        self.ui.button_usage_guide.clicked.connect(self.usage_guide)
        self.ui.button_error_log.clicked.connect(self.switch_errors)

    def setup(self):
        self.update_check = Setup()
        self.update_check.signals.signal_update_result.connect(self.update_result)
        self.threadpool.start(self.update_check)

    def update_result(self, value):
        found = QCoreApplication.tr( f"Version: {__next_release__} is out!", None)
        not_found = QCoreApplication.tr( f"No update was found...", None)

        if value:
            self.ui.lineedit_update.setText(found)

        else:
            self.ui.lineedit_update.setText(not_found)

    def start_undefined_range(self):
        self.ui.progressbar.setRange(0, 0)

    def stop_undefined_range(self):
        self.ui.progressbar.setRange(0, 1)

    def update_progressbar(self, pos, total):
        self.ui.progressbar.setValue(pos)
        self.ui.progressbar.setMaximum(total)

    def on_error(self, e):
        self.ui_popup(e)

    def edit_next(self):
        self.last_index += 1
        self.edit_tags(item=self.ui.treeWidget.topLevelItem(self.last_index))

    def finished(self):
        self.ui.progressbar.setValue(0)
        self.ui.progressbar.setMaximum(100)
        self.edit_tags(item=self.ui.treeWidget.topLevelItem(0))
        self.ui.lineedit_status.clear()

    def load_tags_file(self):
        file, type = QFileDialog().getOpenFileName(None, QCoreApplication.tr("Select a music file", None),
                                                   "", "Audio Files (*.mp3 *.flac *.m4a *.ogg *.oga"
                                                       " *.wma *.aiff *.aif *.ape *.mpc *.tta *.ofr *.ofs *.spx *.asf "
                                                       "*.wv *.aac)")

        if file is None or file == "":
            self.ui_popup(QCoreApplication.tr("No file was selected...", None))
            return

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
        title = data.get("title")
        artist = data.get("artist")
        album = data.get("album")
        albumartist = data.get("albumartist")
        date = data.get("date")
        genre = data.get("genre")
        tracknumber = data.get("tracknumber")
        publisher = data.get("publisher")
        composer = data.get("composer")
        originalartist = data.get("originalartist")
        lyrics = data.get("lyrics")
        conductor = data.get("conductor")
        comments = data.get("comments")
        idx = data.get("idx")
        path = data.get("file_path")

        item = QTreeWidgetItem(self.ui.treeWidget)
        item.setText(0, f"{idx}) {title}")
        item.setText(1, artist)
        item.setText(2, album)
        item.setText(3, "No")

        item.setData(0, Qt.UserRole, str(title))
        item.setData(1, Qt.UserRole, str(artist))
        item.setData(2, Qt.UserRole, str(album))
        item.setData(3, Qt.UserRole, str(albumartist))
        item.setData(4, Qt.UserRole, str(date))
        item.setData(5, Qt.UserRole, str(genre))
        item.setData(6, Qt.UserRole, str(tracknumber))
        item.setData(7, Qt.UserRole, str(publisher))
        item.setData(8, Qt.UserRole, str(composer))
        item.setData(9, Qt.UserRole, str(originalartist))
        item.setData(10, Qt.UserRole, str(lyrics))
        item.setData(11, Qt.UserRole, str(conductor))
        item.setData(12, Qt.UserRole, str(comments))
        item.setData(13, Qt.UserRole, str(path))

    def edit_tags(self, item):
        self.current_item = item
        self.last_index = self.ui.treeWidget.indexOfTopLevelItem(item)
        self.ui.lineedit_title.setText(item.data(0, Qt.UserRole))
        self.ui.lineedit_artist.setText(item.data(1, Qt.UserRole))
        self.ui.lineedit_album.setText(item.data(2, Qt.UserRole))
        self.ui.lineedit_album_artist.setText(item.data(3, Qt.UserRole))
        self.ui.lineedit_year.setText(item.data(4, Qt.UserRole))
        self.ui.lineedit_genre.setText(item.data(5, Qt.UserRole))
        self.ui.lineedit_track_number.setText(item.data(6, Qt.UserRole))
        self.ui.lineedit_publisher.setText(item.data(7, Qt.UserRole))
        self.ui.lineedit_composer.setText(item.data(8, Qt.UserRole))
        self.ui.lineedit_original_artist.setText(item.data(9, Qt.UserRole))
        self.ui.lineedit_conductor.setText(item.data(11, Qt.UserRole))
        self.ui.lineedit_comments.setText(item.data(12, Qt.UserRole))

    def apply_tags(self):
        TagEditor.tags_to_be_written = {
            "title": self.ui.lineedit_title.text(),
            "artist": self.ui.lineedit_artist.text(),
            "album": self.ui.lineedit_album.text(),
            "albumartist": self.ui.lineedit_album_artist.text(),
            "date": self.ui.lineedit_year.text(),
            "genre": self.ui.lineedit_genre.text(),
            "tracknumber": self.ui.lineedit_track_number.text(),
            "comments": self.ui.lineedit_comments.text(),
            "composer": self.ui.lineedit_composer.text(),
            "originalartist": self.ui.lineedit_original_artist.text(),
            "conductor": self.ui.lineedit_conductor.text(),
            "publisher": self.ui.lineedit_publisher.text(),
        }

        file_path = self.current_item.data(13, Qt.UserRole)
        file_extension = os.path.splitext(file_path)[1].lower()

        tag_mapping = get_tag_mapping(file_extension)
        if not tag_mapping:
            self.ui.lineedit_status.setText(QCoreApplication.tr("Unsupported file format.", ""))
            return

        audio = get_audio_file(file_path, file_extension)
        if not audio:
            self.ui.lineedit_status.setText(QCoreApplication.tr("Error loading file.", ""))
            return

        # Apply tags
        for tag, frame in tag_mapping.items():
            value = TagEditor.tags_to_be_written.get(tag)
            if value:
                if file_extension == '.mp3':
                    audio.add(frame(encoding=Encoding.UTF8, text=value))
                else:
                    audio[frame] = value

        if file_extension == '.mp3':
            audio.save(v2_version=3)  # Save as ID3v2.3
        else:
            audio.save()
        self.ui.lineedit_status.setText(QCoreApplication.tr("Tags have been written: ✔", ""))

    def select_cover_art(self):
        art_path, _ = QFileDialog.getOpenFileName(None, QCoreApplication.tr("Select Cover Art",
                                                                              None), "",
                                                  "Image Files (*.png *.jpg *.jpeg)")
        if not art_path:
            return

        if self.current_item is None:
            self.ui_popup(QCoreApplication.tr("No file was selected...", None))
            return

        file_path = self.current_item.data(13, Qt.UserRole)
        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.mp3':
            self.add_cover_art_mp3(file_path, art_path)
        elif ext == '.flac':
            self.add_cover_art_flac(file_path, art_path)
        elif ext in ['.m4a']:
            self.add_cover_art_m4a(file_path, art_path)
        else:
            self.ui_popup(QCoreApplication.tr("""
Unsupported file format!, only mp3, flac and m4a support" "cover images!""", None))

    @classmethod
    def add_cover_art_mp3(cls, file_path, art_path):
        audio = MP3(file_path, ID3=ID3)
        try:
            audio.add_tags()
        except Exception:
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

    @classmethod
    def add_cover_art_flac(cls, file_path, art_path):
        audio = FLAC(file_path)
        pic = Picture()
        pic.type = 3
        pic.mime = 'image/jpeg'
        pic.desc = 'Cover'
        with open(art_path, "rb") as img_file:
            pic.data = img_file.read()
        audio.add_picture(pic)
        audio.save()

    @classmethod
    def add_cover_art_m4a(cls, file_path, art_path):
        audio = MP4(file_path)
        with open(art_path, "rb") as img_file:
            cover_data = img_file.read()
        audio["covr"] = [MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_JPEG)]
        audio.save()

    def add_lyrics(self):
        item = self.current_item
        path = item.data(13, Qt.UserRole)
        file_extension = os.path.splitext(path)[1].lower()

        dialog = LyricsInputDialog()
        if dialog.exec() == QDialog.Accepted:
            lyrics = dialog.getText()

            if file_extension == '.flac':
                file = FLAC(path)
                file["LYRICS"] = lyrics

            elif file_extension == '.mp3':
                file = ID3(path)
                file.add(USLT(encoding=Encoding.UTF8, text=lyrics))

            elif file_extension in ['.m4a', '.mp4', '.aac']:
                file = MP4(path)
                file["\xa9lyr"] = lyrics

            elif file_extension == '.ogg':
                file = OggVorbis(path)
                file["LYRICS"] = lyrics

            else:
                self.ui_popup(QCoreApplication.tr("Unsupported file format.", ""))
                return

            file.save()
            self.ui_popup(QCoreApplication.tr("Lyrics have been updated. Please note, that not all audio "
                                              "codecs support embedded lyrics.", ""))

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
Note: The Lyrics and the Cover Art will be immediately applied, when you select them.

Tag Editor supports the following file formats:

MP3,FLAC,M4A,OGG,WMA,AIFF,APE,MPC,TrueAudio (TTA), OptimFROG, Speex, ASF, WV, AAC

(and even more...)


If you experience any issues, please let me know :)

! Note:

Some files may be corrupted in their headers. For example some of my own .flac files won't work with this tool, because
they've been poorly ripped or people manually changed them.

If this occurs, I recommend you to use a tool called ffmpeg, to re-encode the file. This gives you the same quality, but
ensures that the file headers are correct.


e.g,  ffmpeg -i your_file.flac -o fixed_file.flac

(Pretty simple)
""", None))

    def switch_errors(self):
        if self.ui.stackedWidget.currentIndex() == 0:
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.button_error_log.setText(QCoreApplication.tr("Switch Back", None))

        else:
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.button_error_log.setText(QCoreApplication.tr("Error Log", None))

        print(errors)
        for error in errors:
            file = error.get("path")
            reason = error.get("error")
            print(file)
            print(reason)
            item = QTreeWidgetItem(self.ui.treeWidget_2)
            item.setText(0, str(file))
            item.setText(1, str(reason))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-fe", "--force_english", action="store_true", help="Forces the application to load in english language")
    app = QApplication(argv)
    app.setStyle("Fusion")
    args = parser.parse_args()

    if args.force_english:
        language_code = "en"

    else:
        locale = QLocale.system()
        language_code = locale.name()

    path = f":/translations/translations/{language_code}.qm"
    translator = QTranslator(app)
    if translator.load(path):
        print(f"Loaded: {language_code} translation")

    else:
        # Try loading a more general translation if specific one fails
        general_language_code = language_code.split('_')[0]
        path = f":/translations/translations/{general_language_code}.qm"
        if translator.load(path):
            print(f"{general_language_code} translation loaded as fallback")
        else:
            print(f"Failed to load {language_code} translation")

    app.installTranslator(translator)

    file = QFile(":/style/stylesheets/stylesheet.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    w = TagEditor()
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
