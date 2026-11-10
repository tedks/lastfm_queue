"""Offline checks for the XML data consumed by the Rhythmbox queue."""

import unittest
from xml.parsers.expat import ExpatError

from lastfmqueue_tracks import parse_similar_tracks, track_artist_title


class QueueTracksTest(unittest.TestCase):
    def test_preserves_order_and_utf8_bytes(self):
        xml = (
            '<similartracks>'
            '<track><name>Caf\u00e9</name><artist><name>Artiste</name></artist></track>'
            '<track><name>Second</name><artist><name>Another</name></artist></track>'
            '</similartracks>'
        )
        self.assertEqual(
            [track_artist_title(track) for track in parse_similar_tracks(xml.encode('utf-8'))],
            [(b'Artiste', 'Caf\u00e9'.encode('utf-8')), (b'Another', b'Second')],
        )

    def test_no_tracks_returns_empty(self):
        self.assertEqual(len(parse_similar_tracks('<similartracks/>')), 0)

    def test_malformed_later_track_is_parsed_only_when_reached(self):
        tracks = parse_similar_tracks(
            '<similartracks>'
            '<track><name>Good</name><artist><name>Band</name></artist></track>'
            '<track><name>Missing artist</name></track>'
            '</similartracks>'
        )
        self.assertEqual(track_artist_title(tracks[0]), (b'Band', b'Good'))
        with self.assertRaises(IndexError):
            track_artist_title(tracks[1])

    def test_malformed_xml_fails(self):
        with self.assertRaises(ExpatError):
            parse_similar_tracks('<similartracks>')


if __name__ == '__main__':
    unittest.main()
