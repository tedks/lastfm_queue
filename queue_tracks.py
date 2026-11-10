"""Parse similar-track names without Rhythmbox or a Last.fm request."""

from xml.dom import minidom


def parse_similar_tracks(data):
    """Return (artist, title) byte pairs in document order.

    The Rhythmbox plugin still shuffles and looks up the returned pairs.
    """
    dom = minidom.parseString(data)
    pairs = []
    for track in dom.getElementsByTagName('track'):
        names = track.getElementsByTagName('name')
        title = names[0].firstChild.data.encode('utf-8')
        artist = names[1].firstChild.data.encode('utf-8')
        pairs.append((artist, title))
    return pairs
