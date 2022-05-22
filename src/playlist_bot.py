from logging.config import valid_ident
import os
import string
from pytube import YouTube
from datetime import datetime
from youtubesearchpython import VideosSearch

class ProcessLogger:

    log_file = 'session.log'

    def timestamp(self):
        today = datetime.now()
        timestamp = today.strftime("%H:%M:%S")
        return timestamp

    def entry(self, content):
        try:
            print(f"[{self.timestamp()}] {content}")
            f = open(self.log_file, 'a')
            f.write(f"[{self.timestamp()}] {content}\n")
            f.close()
        except Exception as e:
            # print(e)
            pass

class PlaylistBot:

    def get_song_url_from_name(self, song_name):
        videosSearch = VideosSearch(song_name, limit = 2)       

        result = videosSearch.result()['result'][0]

        data = {
            'link': result['link'],
            'name': str(result['title'])
        }
        
        return data
    
    def download_song_from_url(self, url, playlist_dir):
        log  = ProcessLogger()        

        yt = YouTube(url['link'])
        video = yt.streams.filter(only_audio=True).first()

        # check for destination to save file
        destination = playlist_dir
        out_file = video.download(output_path=destination)

        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        log.entry(yt.title + " has been successfully downloaded.")

    def load_input_songs_by_name(self, text_file, output_location):
        log  = ProcessLogger()        
        if not os.path.isfile(text_file):
            print(f" {text_file} is not a valid file.")
            exit()
        
        try:
            name_file = open(text_file, 'r')
            all_entries = name_file.readlines()
            name_file.close()
            print(f" Read from file: {text_file}")
        except Exception as e:
            print(f" Error reading from file: {text_file}\n{e}")
            exit()

        for song_title in all_entries:
            try:
                url = self.get_song_url_from_name(song_name=song_title)

                try:
                    self.download_song_from_url(url, output_location)
                except Exception as e:
                    log.entry(f" Failed downloading song \"{song_title}\"")
            except Exception as e:
                log.entry(f" No found song with this name: \"{song_title}\"")
                continue
        print(" Finished.")
    
    def create_valid_filename_from_playlist_title(self, playlist_title, interpolate_spaces=True):
        valid_chars = f'-_.() {string.ascii_letters}{string.digits}'
        valid_filename = ''.join(c for c in playlist_title if c in valid_chars)

        if interpolate_spaces:
            valid_filename = valid_filename.replace(' ', '_')
        return valid_filename

