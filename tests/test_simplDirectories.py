from unittest import TestCase
import simpl.music_directories


class TestSimplDirectories(TestCase):

    dir_list = [{'playlists': [],
                 'directory': '01-Test',
                 'files': ['Doobie Brothers - Without Love (Where would you be now).mp3',
                           'Frank Sinatra - New York New York.mp3', 'Al Jarreau - Boogie Down.wma',
                           'Curtis Mayfield - Move On Up.mp3', 'Buckshot LeFonque -Some Cow Funk (more tea, vicar).wma',
                           'Frank Sinatra - You make me feel so young.mp3', 'Frank Sinatra - The Lady is a Tramp.mp3',
                           "Frank Sinatra - I've got you under my Skin.mp3",
                           'Frank Sinatra - Nice work if you can get it.mp3', 'Earth Wind & Fire - Shinning Star.mp3',
                           'Earth Wind & Fire - Mix funk.mp3', 'Earth, Wind & Fire - Got To Get You Into My Life.mp3']},
                {'playlists': [],
                 'directory': '02-Peter und der Wolf',
                 'files': ['Peter Fox - Die Affen steigen auf den Thron.mp3', 'Peter Fox - Lok auf 2 Beinen.mp3',
                           'Peter Fox - Der letzte Tag.mp3', 'Peter Fox - Stadtaffe.mp3', 'Peter Fox - Haus am See.mp3',
                           'Peter Fox - Kopf verloren.mp3', 'Peter Fox - Das zweite Gesicht.mp3',
                           'Peter Fox - Schwinger.mp3', 'Peter Fox - Ich Steine, Du Steine.mp3',
                           'Peter Fox - Fieber.mp3', 'Peter Fox - Schuttel deinen Speck.mp3',
                           'Peter Fox - Grosshirn RMX.mp3', 'Peter Fox - Schwarz zu Blau.mp3',
                           'Peter Fox - She moved in (Miss Platnum).mp3',
                           'Peter Fox - Marry me (feat. Miss Platnum).mp3', 'Peter Fox - Aufstehn.mp3',
                           'Peter Fox - Alles Neu.mp3', 'Peter Fox - Dickes Ende.mp3']},
                {'playlists': [],
                 'directory': '03-Die_Prinzessin',
                 'files': ['01 dota_kehr - zeitgeist.mp3', '02 dota_kehr - sternschnuppen.mp3',
                           '03 dota_kehr - zauberer.mp3', '04 dota_kehr - selten_aber_manchmal.mp3',
                           '05 dota_kehr - friedberg.mp3', '06 dota_kehr - mediomelo.mp3',
                           '07 dota_kehr - kaulquappe.mp3', '08 dota_kehr - schneeknig.mp3',
                           '09 dota_kehr - nichts_neues.mp3', '10 dota_kehr - geheimnis.mp3',
                           '11 dota_kehr - erledigungszettelschreiber.mp3', '12 dota_kehr - die_drei.mp3']},
                {'playlists': ['bayern_2.m3u', 'M_94_5.ogg.m3u', 'F_M_4.pls'],
                 'directory': '04-Radio',
                 'files': []}]

    def setUp(self):
        self.directories = simpl.music_directories.SimplDirectories(self.dir_list)

    def test_folder_exists(self):
        self.assertFalse(self.directories.folder_exists(5))
        self.assertTrue(self.directories.folder_exists(4))

    def test_get_text_for_folder(self):
        self.assertEqual(self.directories.get_text_for_folder(2), "Peter und der Wolf")

    def test_get_folder_uri_for_mpd(self):
        self.assertEqual(self.directories.get_folder_uri_for_mpd(4), "04-Radio")

    def test_get_nr_of_folder_entries(self):
        pass

    def test_is_radio_folder(self):
        self.assertFalse(self.directories.is_radio_folder(2))
        self.assertTrue(self.directories.is_radio_folder(4))

    def test_get_radio_playlist_text(self):
        self.assertEqual(self.directories.get_radio_playlist_text(1, 2), "Fehler")
        self.assertEqual(self.directories.get_radio_playlist_text(4, 2), "F M 4")

    def test_get_radio_uri_for_mpd(self):
        self.assertEqual(self.directories.get_radio_uri_for_mpd(4, 0), "04-Radio/bayern_2.m3u")

    def test_get_next_radio_playlist_nr(self):
        pass

    def test_get_previous_radio_playlist_nr(self):
        pass

    def test_process_directories(self):
        pass
