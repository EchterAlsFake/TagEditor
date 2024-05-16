"""
This file contains the tags and attributes for every audio file.

This is needed to make the app compatible with all formats and tags, because the 'easy' mode on mutagen is as it says
an easy mode which doesn't support the whole range of files.

I know that this looks and sounds complicated, but trust me, it's easier than it looks like :)
"""
from mutagen.id3 import TIT2, TPE1, TALB, TPE2, TCON, TRCK, TPUB, TCOM, TOPE, USLT, TPE3, COMM, TDRC


TAGS_MP3 = {
    "title": "TIT2",
    "artist": "TPE1",
    "album": "TALB",
    "albumartist": "TPE2",
    "date": "TYER",  # or TDRC
    "genre": "TCON",
    "tracknumber": "TRCK",
    "publisher": "TPUB",
    "composer": "TCOM",
    "originalartist": "TOPE",
    "lyrics": "USLT",
    "conductor": "TPE3",
    "comments": "COMM"
}

TAGS_MP3_WRITE = {
    "title": TIT2,
    "artist": TPE1,
    "album": TALB,
    "albumartist": TPE2,
    "date": TDRC,
    "genre": TCON,
    "tracknumber": TRCK,
    "publisher": TPUB,
    "composer": TCOM,
    "originalartist": TOPE,
    "lyrics": USLT,
    "conductor": TPE3,
    "comments": COMM
}

TAGS_FLAC = {
    "title": "TITLE",
    "artist": "ARTIST",
    "album": "ALBUM",
    "albumartist": "ALBUMARTIST",
    "date": "DATE",
    "genre": "GENRE",
    "tracknumber": "TRACKNUMBER",
    "publisher": "PUBLISHER",
    "composer": "COMPOSER",
    "originalartist": "ORIGINALARTIST",
    "lyrics": "LYRICS",
    "conductor": "CONDUCTOR",
    "comments": "COMMENT"
}

TAGS_MP4 = {
    "title": "\xa9nam",
    "artist": "\xa9ART",
    "album": "\xa9alb",
    "albumartist": "aART",
    "date": "\xa9day",
    "genre": "\xa9gen",
    "tracknumber": "trkn",
    "publisher": "\xa9pub",
    "composer": "\xa9wrt",
    "originalartist": "\xa9ope",
    "lyrics": "\xa9lyr",
    "conductor": "\xa9con",
    "comments": "\xa9cmt"
}

TAGS_OGG = {
    "title": "TITLE",
    "artist": "ARTIST",
    "album": "ALBUM",
    "albumartist": "ALBUMARTIST",
    "date": "DATE",
    "genre": "GENRE",
    "tracknumber": "TRACKNUMBER",
    "publisher": "PUBLISHER",
    "composer": "COMPOSER",
    "originalartist": "ORIGINALARTIST",
    "lyrics": "LYRICS",
    "conductor": "CONDUCTOR",
    "comments": "COMMENT"
}

TAGS_WMA = {
    "title": "Title",
    "artist": "Author",
    "album": "WM/AlbumTitle",
    "albumartist": "WM/AlbumArtist",
    "date": "WM/Year",
    "genre": "WM/Genre",
    "tracknumber": "WM/TrackNumber",
    "publisher": "WM/Publisher",
    "composer": "WM/Composer",
    "originalartist": "WM/OriginalArtist",
    "lyrics": "WM/Lyrics",
    "conductor": "WM/Conductor",
    "comments": "Description"
}

TAGS_AIFF = {
    "title": "\xa9nam",
    "artist": "\xa9ART",
    "album": "\xa9alb",
    "albumartist": "aART",
    "date": "\xa9day",
    "genre": "\xa9gen",
    "tracknumber": "trkn",
    "publisher": "\xa9pub",
    "composer": "\xa9wrt",
    "originalartist": "\xa9ope",
    "lyrics": "\xa9lyr",
    "conductor": "\xa9con",
    "comments": "\xa9cmt"
}

TAGS_APE = {
    "title": "Title",
    "artist": "Artist",
    "album": "Album",
    "albumartist": "Album Artist",
    "date": "Year",
    "genre": "Genre",
    "tracknumber": "Track",
    "publisher": "Publisher",
    "composer": "Composer",
    "originalartist": "Original Artist",
    "lyrics": "Lyrics",
    "conductor": "Conductor",
    "comments": "Comment"
}

TAGS_MPC = {
    "title": "TITLE",
    "artist": "ARTIST",
    "album": "ALBUM",
    "albumartist": "ALBUMARTIST",
    "date": "DATE",
    "genre": "GENRE",
    "tracknumber": "TRACKNUMBER",
    "publisher": "PUBLISHER",
    "composer": "COMPOSER",
    "originalartist": "ORIGINALARTIST",
    "lyrics": "LYRICS",
    "conductor": "CONDUCTOR",
    "comments": "COMMENT"
}

TAGS_TTA = {
    "title": "TITLE",
    "artist": "ARTIST",
    "album": "ALBUM",
    "albumartist": "ALBUMARTIST",
    "date": "DATE",
    "genre": "GENRE",
    "tracknumber": "TRACKNUMBER",
    "publisher": "PUBLISHER",
    "composer": "COMPOSER",
    "originalartist": "ORIGINALARTIST",
    "lyrics": "LYRICS",
    "conductor": "CONDUCTOR",
    "comments": "COMMENT"
}

TAGS_WV = {
    "title": "TITLE",
    "artist": "ARTIST",
    "album": "ALBUM",
    "albumartist": "ALBUMARTIST",
    "date": "DATE",
    "genre": "GENRE",
    "tracknumber": "TRACKNUMBER",
    "publisher": "PUBLISHER",
    "composer": "COMPOSER",
    "originalartist": "ORIGINALARTIST",
    "lyrics": "LYRICS",
    "conductor": "CONDUCTOR",
    "comments": "COMMENT"
}

TAGS_SPEEX = {
    "title": "TITLE",
    "artist": "ARTIST",
    "album": "ALBUM",
    "albumartist": "ALBUMARTIST",
    "date": "DATE",
    "genre": "GENRE",
    "tracknumber": "TRACKNUMBER",
    "publisher": "PUBLISHER",
    "composer": "COMPOSER",
    "originalartist": "ORIGINALARTIST",
    "lyrics": "LYRICS",
    "conductor": "CONDUCTOR",
    "comments": "COMMENT"
}

TAGS_AAC = {
    "title": "\xa9nam",
    "artist": "\xa9ART",
    "album": "\xa9alb",
    "albumartist": "aART",
    "date": "\xa9day",
    "genre": "\xa9gen",
    "tracknumber": "trkn",
    "publisher": "\xa9pub",
    "composer": "\xa9wrt",
    "originalartist": "\xa9ope",
    "lyrics": "\xa9lyr",
    "conductor": "\xa9con",
    "comments": "\xa9cmt"
}

