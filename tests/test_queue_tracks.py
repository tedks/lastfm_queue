"""Offline checks for the XML data consumed by the Rhythmbox queue."""

import unittest
from xml.parsers.expat import ExpatError

from queue_tracks import parse_similar_tracks


class QueueTracksTest(unittest.TestCase):
    def test_preserves_order_and_utf8_bytes(self):
        xml = (
            '<similartracks>'
            '<track><name>Caf\u00e9</name><artist><name>Artiste</name></artist></track>'
            '<track><name>Second</name><artist><name>Another</name></artist></track>'
            '</similartracks>'
        )
        self.assertEqual(
            parse_similar_tracks(xml),
            [(b'Artiste', 'Caf\u00e9'.encode('utf-8')), (b'Another', b'Second')],
        )

    def test_no_tracks_returns_empty(self):
        self.assertEqual(parse_similar_tracks('<similartracks/>'), [])

    def test_malformed_xml_fails(self):
        with self.assertRaises(ExpatError):
            parse_similar_tracks('<similartracks>')


if __name__ == '__main__':
    unittest.main()
