import os
import time
import string
from pytube import YouTube
from threading import Thread
from datetime import datetime
from youtubesearchpython import VideosSearch


global downloader_output
downloader_output = []

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
            print(e)
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
    
    def _download_from_song_list(self, list_of_song_titles, output_location):

        downloader_output.append(f'Downloading to playlist: {output_location}...')
        downloader_output.append(f'Amount of songs: {len(list_of_song_titles)}')
        downloader_output.append(f'Downloading songs, please wait...')
        downloader_output.append(f'Output Location: {os.path.join(os.getcwd(), output_location)}')
        
        for song_title in list_of_song_titles:
            try:
                url = self.get_song_url_from_name(song_name=song_title)
                raw_url = url['link']
                downloader_output.append(f'URL: {raw_url}')
                try:
                    self.download_song_from_url(url, output_location)
                    downloader_output.append(f'Successfully downloaded: {song_title}')
                except Exception as e:
                    downloader_output.append(f" Failed downloading song \"{song_title}\"")
            except Exception as e:
                downloader_output.append(f" No found song with this name: \"{song_title}\"")
        downloader_output.append("Finished.")
        time.sleep(5)        
        
    
    def create_downloader(self, list_of_songs, output_directory):
        downloaderThread = Thread(target=self._download_from_song_list, args=(list_of_songs, output_directory,))
        downloaderThread.daemon = True
        downloaderThread.start()
        print(f'Started downloader thread!')
        return downloaderThread
    
    
    def create_valid_filename_from_playlist_title(self, playlist_title, interpolate_spaces=True):
        valid_chars = f'-_.() {string.ascii_letters}{string.digits}'
        valid_filename = ''.join(c for c in playlist_title if c in valid_chars)

        if interpolate_spaces:
            valid_filename = valid_filename.replace(' ', '_')
        return valid_filename

