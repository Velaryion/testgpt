import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from transmission import send_to_transmission, save_transmission, find_transmission

class TransmissionTests(unittest.TestCase):
    def test_dispatch_without_shell(self):
        with tempfile.TemporaryDirectory() as directory:
            exe=Path(directory)/'Transmission with spaces.exe'; exe.touch()
            url='magnet:?xt=urn:btih:'+'a'*40+'&dn=Anime%20test'
            with patch('transmission.subprocess.Popen') as popen:
                send_to_transmission(str(exe),url)
                popen.assert_called_once_with([str(exe),url],shell=False)
    def test_torrent_url(self):
        with tempfile.NamedTemporaryFile() as exe:
            with patch('transmission.subprocess.Popen') as popen:
                send_to_transmission(exe.name,'https://nyaa.si/download/1.torrent')
                self.assertEqual(popen.call_args.args[0][1],'https://nyaa.si/download/1.torrent')
    def test_missing_executable(self):
        with self.assertRaises(ValueError): send_to_transmission('', 'magnet:?xt=urn:btih:'+'a'*40)
    def test_settings_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            exe=Path(directory)/'transmission-qt.exe'; exe.touch()
            settings=Path(directory)/'settings.json'
            with patch('transmission.config_file',return_value=settings):
                save_transmission(str(exe))
                self.assertEqual(find_transmission(),str(exe))
                self.assertEqual(json.loads(settings.read_text())['transmission'],str(exe))
