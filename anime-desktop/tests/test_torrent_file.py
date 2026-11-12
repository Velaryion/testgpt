from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from torrent_file import validate_file
from transmission import send_file_to_transmission
from union_browser import is_tracker

class TorrentFileTests(unittest.TestCase):
    def test_local_transmission_dispatch(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'Private anime.torrent'
            path.write_bytes(b'd4:infod6:lengthi1e4:name4:test12:piece lengthi16384e6:pieces20:aaaaaaaaaaaaaaaaaaaaee')
            exe=Path(directory)/'Transmission.exe';exe.touch()
            self.assertEqual(validate_file(path),path.resolve())
            with patch('transmission.subprocess.Popen') as popen:
                send_file_to_transmission(str(exe),path)
                popen.assert_called_once_with([str(exe),str(path.resolve())],shell=False)
    def test_login_html_corrupt_and_non_torrent_rejected(self):
        for data in [b'<html>Login</html>',b'de',b'd4:infoleee',b'd4:infodeeJUNK',b'd4:infod',b'i1e',b'd4:infoi1ee']:
            with self.subTest(data=data),tempfile.TemporaryDirectory() as directory:
                path=Path(directory)/'bad.torrent';path.write_bytes(data)
                with self.assertRaises(ValueError): validate_file(path)
    def test_only_tracker_origin(self):
        self.assertTrue(is_tracker('https://torrent.unionfansub.com/browse.php'))
        for url in ['https://evil.example/browse.php','http://torrent.unionfansub.com/','https://torrent.unionfansub.com.evil.example/','https://user:pass@torrent.unionfansub.com/']:
            self.assertFalse(is_tracker(url))
