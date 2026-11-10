"""Parse similar-track names without Rhythmbox or a Last.fm request."""

from xml.dom import minidom


def parse_similar_tracks(data):
    """Return track nodes in document order for the plugin to shuffle."""
    return minidom.parseString(data).getElementsByTagName('track')


def track_artist_title(track):
    """Decode one track after the queue has decided to inspect it."""
    names = track.getElementsByTagName('name')
    title = names[0].firstChild.data.encode('utf-8')
    artist = names[1].firstChild.data.encode('utf-8')
    return artist, title
