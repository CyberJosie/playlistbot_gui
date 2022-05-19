
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import playlistbot_gui_support

import os
from pytube import YouTube
from datetime import datetime
from youtubesearchpython import VideosSearch


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

        yt = YouTube(url['link'])
        video = yt.streams.filter(only_audio=True).first()

        # check for destination to save file
        destination = playlist_dir
        out_file = video.download(output_path=destination)

        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)


class BackPanel:

        
        
        def __init__(self, top=None):
                _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
                _fgcolor = '#000000'  # X11 color: 'black'
                _compcolor = 'gray40' # X11 color: #666666
                _ana1color = '#c3c3c3' # Closest X11 color: 'gray76'
                _ana2color = 'beige' # X11 color: #f5f5dc
                _tabfg1 = 'black' 
                _tabfg2 = 'black' 
                _tabbg1 = 'grey75' 
                _tabbg2 = 'grey89' 
                _bgmode = 'light'

                self.song_list = []
                self.console_data = ''

                top.geometry("400x400+1172+276")
                top.minsize(1, 1)
                top.maxsize(2929, 1250)
                top.resizable(1,  1)
                top.title("Playlist Bot")
                top.configure(background="#303030")
                top.configure(highlightcolor="black")

                self.top = top
                self.controlFrame = tk.Frame(self.top)
                self.controlFrame.place(relx=0.013, rely=0.025, relheight=0.363
                        , relwidth=0.965)
                self.controlFrame.configure(relief='groove')
                self.controlFrame.configure(borderwidth="2")
                self.controlFrame.configure(relief="groove")
                self.controlFrame.configure(background="#2b2d35")

                self.path_to_input = tk.StringVar()
                self.inputFileEntry = tk.Entry(self.controlFrame, textvariable=self.path_to_input)
                self.inputFileEntry.place(relx=0.026, rely=0.207, height=23
                        , relwidth=0.948)
                self.inputFileEntry.configure(background="white")
                self.inputFileEntry.configure(font="TkFixedFont")
                self.inputFileEntry.configure(selectbackground="#c4c4c4")

                self.Label1 = tk.Label(self.controlFrame)
                self.Label1.place(relx=0.023, rely=0.069, height=18, width=204)
                self.Label1.configure(activebackground="#f9f9f9")
                self.Label1.configure(anchor='w')
                self.Label1.configure(background="#2b2d35")
                self.Label1.configure(compound='left')
                self.Label1.configure(font="-family {DejaVu Sans} -size 10 -weight bold")
                self.Label1.configure(foreground="#ffffff")
                self.Label1.configure(text='''Enter path to input file:''')

                self.loadInputButton = tk.Button(self.controlFrame)
                self.loadInputButton.place(relx=0.674, rely=0.483, height=23, width=113)
                self.loadInputButton.configure(activebackground="beige")
                self.loadInputButton.configure(background="#ccc7d8")
                self.loadInputButton.configure(borderwidth="2")
                self.loadInputButton.configure(compound='left')
                self.loadInputButton.configure(relief="flat")
                self.loadInputButton.configure(text='''Load Input''', command=lambda: self.load_file(self.path_to_input.get()))

                self.createPlaylistButton = tk.Button(self.controlFrame)
                self.createPlaylistButton.place(relx=0.674, rely=0.69, height=33
                        , width=113)
                self.createPlaylistButton.configure(activebackground="beige")
                self.createPlaylistButton.configure(background="#bed8c2")
                self.createPlaylistButton.configure(borderwidth="2")
                self.createPlaylistButton.configure(compound='left')
                self.createPlaylistButton.configure(relief="flat")
                self.createPlaylistButton.configure(text='''Create Playlist''', command=self.create_playlist)

                self.outputFrame = tk.Frame(self.top)
                self.outputFrame.place(relx=0.013, rely=0.4, relheight=0.563
                        , relwidth=0.97)
                self.outputFrame.configure(relief='groove')
                self.outputFrame.configure(borderwidth="2")
                self.outputFrame.configure(relief="groove")
                self.outputFrame.configure(background="#000000")

                # self.console_output = tk.StringVar()
                self.console_output = tk.StringVar()
                
                self.outputTextBox = tk.Label(self.outputFrame, textvariable=self.console_output, justify=LEFT)
                self.outputTextBox.place(relx=0.026, rely=0.044, height=201, width=374)
                self.outputTextBox.configure(activebackground="#f9f9f9")
                self.outputTextBox.configure(anchor='nw')
                self.outputTextBox.configure(background="#0c0c0c")
                self.outputTextBox.configure(compound='left')
                self.outputTextBox.configure(font="-family {DejaVu Sans} -size 10")
                self.outputTextBox.configure(foreground="#5fc3e8")
                self.console_output.set(self.console_data)
                # self.outputTextBox.configure(text=self.console_output)
        
        def add_output(self, output_text):
                self.console_data += f"{output_text}\n"
                self.console_output.set(self.console_data)
                self.outputFrame.update()
        
        def load_file(self, path_to_file):
                # output = ""

                ignored_lines = [
                        ' ',
                        '',
                        '\n',
                        '\r\n',
                        '\t\n',
                ]

                print(path_to_file)
                # output += f'Loading: {path_to_file}..'
                self.add_output(f'Loading: {path_to_file}..')

                if not os.path.isfile(path_to_file):
                        # output = f"{path_to_file} does\'nt exist."
                        self.add_output(f"{path_to_file} does\'nt exist.")
                        return
                        
                
                try:
                        name_file = open(path_to_file, 'r')
                        all_entries = name_file.readlines()
                        name_file.close()
                        
                        # output += f"Loaded: {path_to_file}."
                        self.add_output(f"Loaded: {path_to_file}.")
                except Exception as e:
                        # output = f" Error reading from file: {path_to_file}"
                        self.add_output(f" Error reading from file: {path_to_file}")
                        print(e)


                cleaned_data = []
                for song_name in all_entries:
                        if song_name not in ignored_lines:
                                cleaned_data.append(song_name.strip())


                self.song_list = cleaned_data
                print(cleaned_data)
        
        def create_playlist(self):
                pb = PlaylistBot()
                output_location = f"{len(self.song_list)}-{str(round(time.time()))}"
                
                # output = f'Downloading {len(self.song_list)} songs..\n'

                self.add_output(f'Downloading {len(self.song_list)} songs..')
                for song_title in self.song_list:
                        try:
                                url = pb.get_song_url_from_name(song_name=song_title)
                                try:
                                        pb.download_song_from_url(url, output_location)
                                        
                                        # output+=f'Downloaded: {song_title}'
                                        print(f'Downloaded: {song_title}')
                                        self.add_output(f'Downloaded: {song_title}')
                                except Exception as e:
                                        output+=f"Failed: \"{song_title}\""
                                        self.add_output(f"Failed: \"{song_title}\"")
                        except Exception as e:
                                # output+=f"Failed: \"{song_title}\"\n"
                                print(e)
                                self.add_output(f"Failed: \"{song_title}\"")
                                continue
                self.add_output(f"Finished. {len(self.song_list)} songs.")
                self.add_output(f"Saved to: {output_location}")

def start_up():
    playlistbot_gui_support.main()

if __name__ == '__main__':
    playlistbot_gui_support.main()




