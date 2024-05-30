from mutagen import File
from mutagen.id3 import ID3NoHeaderError, ID3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.asf import ASF
from src.backend.consts import *
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QVBoxLayout, QTextEdit, QDialogButtonBox, QDialog
from PySide6.QtGui import QTextCursor


def get_tag_mapping(file_extension):
    tag_mappings = {
        '.mp3': TAGS_MP3,
        '.flac': TAGS_FLAC,
        '.m4a': TAGS_MP4,
        '.aac': TAGS_AAC,
        '.ogg': TAGS_OGG,
        '.oga': TAGS_OGG,
        '.wma': TAGS_WMA,
        '.aiff': TAGS_AIFF,
        '.aif': TAGS_AIFF,
        '.ape': TAGS_APE,
        '.mpc': TAGS_MPC,
        '.tta': TAGS_TTA,
        '.wv': TAGS_WV,
        '.spx': TAGS_SPEEX,
        '.asf': TAGS_WMA
    }
    return tag_mappings.get(file_extension)


def get_audio_file(file_path, file_extension):
    audio_classes = {
        '.mp3': ID3,
        '.flac': MP4,
        '.m4a': MP4,
        '.mp4': MP4,
        '.aac': MP4,
        '.ogg': OggVorbis,
        '.oga': OggVorbis,
        '.wma': ASF,
        '.asf': ASF,
        '.ofr': TAGS_OPTIMFROG,
        '.aiff': File,
        '.aif': File,
        '.ape': File,
        '.mpc': File,
        '.tta': File,
        '.wv': File,
        '.spx': File
    }
    audio_class = audio_classes.get(file_extension)
    if not audio_class:
        return None

    if file_extension == '.mp3':
        try:
            return audio_class(file_path)

        except ID3NoHeaderError:
            return audio_class()

    return audio_class(file_path)


class Signals(QObject):
    signal_read_tag = Signal(dict)
    signal_progress = Signal(int, int)
    signal_get_files = Signal(list)
    signal_error = Signal(str)
    signal_start_undefined_range = Signal()
    signal_stop_undefined_range = Signal()
    signal_finished = Signal()
    signal_update_result = Signal(bool)


class LyricsInputDialog(QDialog):
    def __init__(self, parent=None):
        super(LyricsInputDialog, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Input Lyrics")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setPlaceholderText("Enter lyrics here...")
        layout.addWidget(self.textEdit)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def getText(self):
        return self.textEdit.toPlainText()

    def showEvent(self, event):
        super(LyricsInputDialog, self).showEvent(event)
        self.textEdit.setFocus()
        self.textEdit.moveCursor(QTextCursor.Start)
