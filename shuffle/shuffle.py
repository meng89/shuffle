import os
import json
import hashlib
import random
import string
import shutil


from shuffle import audiorec


from . import itunessd
from .baseclasses import List

MUSIC = 'music'
AUDIOBOOK = 'audiobook'


def get_metadata(path):
    log = {
        # 'md5': hashlib.md5().update(open(path, 'rb').read()).hexdigest(),
        'mtime': os.path.getmtime(path),
        'size': os.path.getsize(path)
    }
    return log

# iPod_Control
#          |-- iTunes
#          |       +-- iTunesSD
#          |
#          |-- Speakable
#          |       |-- Messages
#          |       |        |-- bv00.wav
#          |       |        +-- ...
#          |       |
#          |       |-- Playlists
#          |       |        |-- 6FDA0FE117BB0640.wav
#          |       |        +-- ...
#          |       |
#          |       |-- System
#          |       |        |-- bn00.wav
#          |       |        +-- ...
#          |       |
#          |       +-- Tracks
#          |                |-- 1B8FE29DAD1ABA62.wav
#          |                +-- ...
#          |
#          |
#          |-- Sounds
#          |       |-- ASFGPN
#          |       +-- ...
#          |
#          |-- Music
#          |       |-- F00
#          |       |    |-- ACGS.mp3
#          |       |    +-- ...
#          |       |
#          |       +-- ...
#          |
#          |-- sounds_logs.json
#          |-- original_name_logs.json
#          +-- voices_logs.json
#


class Shuffle:
    def __init__(self, directory):
        self.base_dir = os.path.realpath(os.path.normpath(directory))
        self._ctrl_folder = 'iPod_Control'

        self._itunessd_path = self.base_dir + '/' + self._ctrl_folder + '/iTunes/iTunesSD'

        if os.path.exists(self._itunessd_path):
            if os.path.isfile(self._itunessd_path):
                self.itunessd = itunessd.Itunessd(open(self._itunessd_path, 'rb').read())
            else:
                raise Exception
        else:
            self.itunessd = itunessd.Itunessd()

        self.sounds = Sounds(_shuffle=self)


class Sounds:
    def __init__(self, _shuffle):
        self._shuffle = _shuffle

        self._stored_dir = 'sounds'

        self._logs_path = self._shuffle.base_dir + '/' + self._shuffle.control_folder + '/' + 'sounds_logs.json'
        self._logs = json.loads(open(self._logs_path).read())

    def __logs_del_iffilenotexists(self):
        new_logs = {}
        for path, metadata in self._logs.items():
            full_path = self._shuffle.base_dir + os.sep + path

            if os.path.exists(full_path) and os.path.isfile(full_path):
                new_logs[path] = metadata

        self._logs = new_logs

    def __logs_updata_ifsizeormtimechanged(self):
        new_logs = {}
        for path, metadata in self._logs.items():
            full_path = self._shuffle.base_dir + os.sep + path

            if os.path.getsize(full_path) == metadata['size'] and os.path.getmtime(full_path) == metadata['mtime']:
                new_logs[path] = metadata
            else:
                new_logs[path] = get_metadata(full_path)

    def __logs_update_fromtracks(self):
        not_log_tracks_filenames = []
        for track in self._shuffle.itunessd.tracks:
            if track.filename[1:] not in self._logs.keys():
                not_log_tracks_filenames.append(track.filename[1:])

        tracks_logs_notinlogs = {}
        for filename in not_log_tracks_filenames:
            tracks_logs_notinlogs[filename] = get_metadata(self._shuffle.base_dir + '/' + filename)

        self._logs.update(tracks_logs_notinlogs)

    def list(self):
        return tuple(self._logs.keys())

    def get_from_checksum(self, checksum):
        path = None
        for key, info in self._logs.items():
            if info['checksum'] == checksum:
                path = key
                break
        return path

    def add(self, path, checksum=None):
        if not audiorec.get_filetype(path):
            raise TypeError('This file type is not supported.')

        if not checksum:
            source = open(path, 'rb')
            m = hashlib.md5()
            while True:
                data = source.read(10240)
                if data:
                    m.update(data)
                else:
                    break
            source.close()
            checksum = m.hexdigest()

        path_in_ipod = None
        for PATH, metadata in self._logs:
            if metadata['checksum'] == checksum:
                path_in_ipod = PATH
                break

        if not path_in_ipod:  # Mean this file is not in ipod.

            # 1. get random filename which not use.
            while True:
                # at most 65533 files in one folder
                path_in_ipod = os.path.join(self._shuffle.base_dir, self._shuffle.control_folder,
                                            self._stored_dir, random.sample(string.ascii_uppercase, 6))

                if not os.path.exists(path_in_ipod) and path_in_ipod not in self._logs.keys():
                    break

            # 2. copy file
            target_path = self._shuffle.base_dir + '/' + path_in_ipod
            shutil.copyfile(path, target_path)

            # 3. update logs
            self._logs[path_in_ipod]['checksum'] = checksum
            self._logs[path_in_ipod].update(get_metadata(path))

        return path_in_ipod

    def remove(self, path):
        os.remove(self._shuffle.base_dir + '/' + path)
        del self._shuffle.sounds_logs[path]

    def write_logs(self):
        open(self._logs_path, 'w').write(json.dumps(self._logs))


class Tracks(List):
    pass


class Track:
    pass


class Playlists(List):
    def __init__(self):
        super().__init__()


class Playlist(List):
    def __init__(self):
        super().__init__()
