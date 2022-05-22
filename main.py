import sys
import json
import time
import platform
import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread
from tkinter import messagebox
from tkinter.constants import *

from src.playlist_bot import *

APP_NAME = "Playlist Bot"


class TopWindow:

    def __init__(self, top=None):

        _bgcolor = '#d9d9d9'
        _fgcolor = '#000000'
        _compcolor = 'gray40'
        _ana1color = '#c3c3c3'
        _ana2color = 'beige'
        _tabfg1 = 'black' 
        _tabfg2 = 'black' 
        _tabbg1 = 'grey75' 
        _tabbg2 = 'grey89' 
        _bgmode = 'light' 

        top.geometry("800x500+1143+218")
        top.minsize(1, 1)
        top.maxsize(2929, 1250)
        top.resizable(1,  1)
        top.title(APP_NAME)
        top.configure(background="#121212")
        top.configure(highlightcolor="black")

        self.top = top
        self.playlist_name = tk.StringVar()
        self.songs = []
        self.output_playlist_filename = ''
        
        # frame with app buttons
        self.controlFrame = tk.Frame(self.top)
        self.controlFrame.place(relx=0.013, rely=0.06, relheight=0.91, relwidth=0.231)
        self.controlFrame.configure(relief='solid')
        self.controlFrame.configure(borderwidth="2")
        self.controlFrame.configure(relief="solid")
        self.controlFrame.configure(background="#404040")

        # button that links to create a list page
        self.createListButton = tk.Button(self.controlFrame)
        self.createListButton.place(relx=0.054, rely=0.022, height=33, width=163)
        self.createListButton.configure(activebackground="#bd87ff")
        self.createListButton.configure(background="#BB86FC")
        self.createListButton.configure(compound='left')
        self.createListButton.configure(relief="flat")
        self.createListButton.configure(text='''Create New''', command=lambda: Pages.create_playlist(self))

        # save song list page (not required)
        self.saveSongListButton = tk.Button(self.controlFrame)
        self.saveSongListButton.place(relx=0.054, rely=0.11, height=33, width=163)
        self.saveSongListButton.configure(activebackground="#bd87ff")
        self.saveSongListButton.configure(background="#BB86FC")
        self.saveSongListButton.configure(borderwidth="2")
        self.saveSongListButton.configure(compound='left')
        self.saveSongListButton.configure(relief="flat")
        self.saveSongListButton.configure(text='''Save List''', command=lambda: Pages.save_song_list(self, self.playlist_name.get()))

        # create playlist from song list button
        self.createPlaylistButton = tk.Button(self.controlFrame)
        self.createPlaylistButton.place(relx=0.054, rely=0.242, height=33, width=163)
        self.createPlaylistButton.configure(activebackground="#7350af")
        self.createPlaylistButton.configure(activeforeground="white")
        self.createPlaylistButton.configure(background="#3700B3")
        self.createPlaylistButton.configure(borderwidth="2")
        self.createPlaylistButton.configure(compound='left')
        self.createPlaylistButton.configure(font="-family {DejaVu Sans} -size 11 -weight bold")
        self.createPlaylistButton.configure(foreground="#ffffff")
        self.createPlaylistButton.configure(relief="flat")
        self.createPlaylistButton.configure(text='''Run Bot''', command=lambda: Pages.generate_playlist(self, self.playlist_name.get()))

        # button to show help menu
        self.helpButton = tk.Button(self.controlFrame)
        self.helpButton.place(relx=0.054, rely=0.923, height=23, width=163)
        self.helpButton.configure(activebackground="#ccffd0")
        self.helpButton.configure(background="#b5e2b9")
        self.helpButton.configure(borderwidth="2")
        self.helpButton.configure(compound='left')
        self.helpButton.configure(relief="flat")
        self.helpButton.configure(text='''Help''', command=lambda: Pages.help_page(self))

        # content frame - shows data on each page
        self.contentFrame = tk.Frame(self.top)
        self.contentFrame.place(relx=0.25, rely=0.06, relheight=0.91, relwidth=0.744)
        self.contentFrame.configure(relief='solid')
        self.contentFrame.configure(borderwidth="2")
        self.contentFrame.configure(relief="solid")
        self.contentFrame.configure(background="#404040")
        
        # show help page by default
        Pages.help_page(self)
        
        
    # clear all existing eidgets in content frame
    def clear_content_frame(self):
        for widgets in self.contentFrame.winfo_children():
                widgets.destroy()

    # add a song to the song list, and update result
    def add_song(self, song_name):
        self.songs.append(song_name.strip())
        print(song_name)
        self.songTitlesListBox.insert(len(self.songs), song_name)
        self.clear_song_entry()

    # clear the entry widget with song names 
    def clear_song_entry(self):
        self.songNameEntry.delete(0, END)
    
    # daemon that catches new output from downloader thread
    # and updates scrolled display with new content since they can not be updated
    def output_daemon(self, downloaderThread):
        last_printed_index = 0
        while True:
            
            if downloaderThread.is_alive():
                current_dl_len = len(downloader_output)
                if current_dl_len > last_printed_index:
                    self.draw_output_listbox(downloader_output)
                    last_printed_index = len(downloader_output)
            else:
                break
    
    def persist_song_list(self, output_file, list_of_songs):
        if not os.path.isdir(os.path.join(os.getcwd(), output_file)):
            os.mkdir(os.path.join(os.getcwd(), output_file))

        try:
            f = open(os.path.join(os.getcwd(), output_file, 'song_list.txt'), 'a')
            for song in list_of_songs:
                f.write(f'{song}\n')
            f.close()
        except Exception as e:
            print(e)
            
    
    # updates downloader output listbox with new content
    # completely re-draws since they can not be updated (i think)
    def draw_output_listbox(self, list_of_output):
        self.downloaderOutputListBox = ScrolledListBox(self.contentFrame)
        self.downloaderOutputListBox.place(relx=0.017, rely=0.11, relheight=0.853, relwidth=0.968)
        self.downloaderOutputListBox.configure(background="white")
        self.downloaderOutputListBox.configure(cursor="xterm")
        self.downloaderOutputListBox.configure(font="TkFixedFont")
        self.downloaderOutputListBox.configure(highlightcolor="#d9d9d9")
        self.downloaderOutputListBox.configure(selectbackground="#c4c4c4")

        for i in range(0, len(list_of_output)-1):
            self.downloaderOutputListBox.insert(i, list_of_output[i])


# updates content frame with widgets for each page
class Pages(TopWindow):

    # enter song names on this page to form a playlist
    # also give playlist a name
    def create_playlist(self):
        self.clear_content_frame()
    
        self.outputPlaylistLabel = tk.Label(self.contentFrame)
        self.outputPlaylistLabel.place(relx=0.017, rely=0.044, height=21, width=129)
        self.outputPlaylistLabel.configure(activebackground="#f9f9f9")
        self.outputPlaylistLabel.configure(anchor='w')
        self.outputPlaylistLabel.configure(background="#404040")
        self.outputPlaylistLabel.configure(compound='left')
        self.outputPlaylistLabel.configure(font="-family {DejaVu Sans} -size 11 -weight bold")
        self.outputPlaylistLabel.configure(foreground="#f7f7f7")
        self.outputPlaylistLabel.configure(text='''Playlist Name:''')

        
        self.playlistNameEntry = tk.Entry(self.contentFrame, textvariable=self.playlist_name)
        self.playlistNameEntry.place(relx=0.252, rely=0.044, height=23, relwidth=0.43)
        self.playlistNameEntry.configure(background="#f7f7f7")
        self.playlistNameEntry.configure(cursor="fleur")
        self.playlistNameEntry.configure(font="TkFixedFont")
        self.playlistNameEntry.configure(relief="solid")

        self.songTitlesListBox = ScrolledListBox(self.contentFrame)
        self.songTitlesListBox.place(relx=0.017, rely=0.22, relheight=0.765, relwidth=0.968)
        self.songTitlesListBox.configure(background="white")
        self.songTitlesListBox.configure(cursor="xterm")
        self.songTitlesListBox.configure(font="TkFixedFont")
        self.songTitlesListBox.configure(highlightcolor="#d9d9d9")
        self.songTitlesListBox.configure(selectbackground="#c4c4c4")

        self.tmp_song = tk.StringVar()
        self.songNameEntry = tk.Entry(self.contentFrame, textvariable=self.tmp_song)
        self.songNameEntry.place(relx=0.185, rely=0.154, height=23, relwidth=0.716)
        self.songNameEntry.configure(background="white")
        self.songNameEntry.configure(font="TkFixedFont")
        self.songNameEntry.configure(relief="solid")

        self.Label1 = tk.Label(self.contentFrame)
        self.Label1.place(relx=0.017, rely=0.154, height=21, width=89)
        self.Label1.configure(anchor='w')
        self.Label1.configure(background="#404040")
        self.Label1.configure(compound='left')
        self.Label1.configure(font="-family {DejaVu Sans} -size 10 -weight bold")
        self.Label1.configure(foreground="#f7f7f7")
        self.Label1.configure(text='''Song Name:''')

        self.addSongButton = tk.Button(self.contentFrame)
        self.addSongButton.place(relx=0.908, rely=0.154, height=23, width=43)
        self.addSongButton.configure(activebackground="beige")
        self.addSongButton.configure(background="#BB86FC")
        self.addSongButton.configure(borderwidth="2")
        self.addSongButton.configure(compound='left')
        self.addSongButton.configure(relief="flat")
        self.addSongButton.configure(text='''Add''', command=lambda: self.add_song(self.tmp_song.get()))
    
    # save song list so that is persists
    def save_song_list(self, playlist_name):

        if playlist_name == '':
            messagebox.showerror('error', 'You need to name your playlist!')
            Pages.create_playlist(self)
            return

        print(f'Creating new playlist: {playlist_name}...')
        print(f'No. Songs: {len(self.songs)}')
        print(f'Songs: {json.dumps(self.songs, indent=2)}')

        self.persist_song_list(playlist_name, self.songs)
        messagebox.showinfo('Saved!', f'There will be a \'song_list.txt\' in the playlist output directory. Click \'Run Bot\' to finish.')
        
    # generate local playlist of MP3 files from song titles
    def generate_playlist(self, playlist_name):
        self.clear_content_frame()
        
        if playlist_name == '':
            messagebox.showerror('Error!', 'You need to name your playlist!')
            Pages.create_playlist(self)
            return
        
        playlist_bot = PlaylistBot()
        self.output_playlist_filename = playlist_bot.create_valid_filename_from_playlist_title(playlist_name)
        print(f'Valid Filename: {self.output_playlist_filename}')

        self.downloaderOutputListBox = ScrolledListBox(self.contentFrame)
        self.downloaderOutputListBox.place(relx=0.017, rely=0.11, relheight=0.853, relwidth=0.968)
        self.downloaderOutputListBox.configure(background="white")
        self.downloaderOutputListBox.configure(cursor="xterm")
        self.downloaderOutputListBox.configure(font="TkFixedFont")
        self.downloaderOutputListBox.configure(highlightcolor="#d9d9d9")
        self.downloaderOutputListBox.configure(selectbackground="#c4c4c4")

        self.creatingPlaylistLabel = tk.Label(self.contentFrame)
        self.creatingPlaylistLabel.place(relx=0.017, rely=0.022, height=31, width=169)
        self.creatingPlaylistLabel.configure(activebackground="#f9f9f9")
        self.creatingPlaylistLabel.configure(anchor='w')
        self.creatingPlaylistLabel.configure(background="#404040")
        self.creatingPlaylistLabel.configure(compound='left')
        self.creatingPlaylistLabel.configure(font="-family {DejaVu Sans} -size 11 -weight bold")
        self.creatingPlaylistLabel.configure(foreground="#f7f7f7")
        self.creatingPlaylistLabel.configure(text='''Creating Playlist:''')

        self.newPlaylistNameLabelValue = tk.Label(self.contentFrame)
        self.newPlaylistNameLabelValue.place(relx=0.286, rely=0.022, height=31, width=389)
        self.newPlaylistNameLabelValue.configure(activebackground="#f9f9f9")
        self.newPlaylistNameLabelValue.configure(anchor='w')
        self.newPlaylistNameLabelValue.configure(background="#404040")
        self.newPlaylistNameLabelValue.configure(compound='left')
        self.newPlaylistNameLabelValue.configure(font="-family {DejaVu Sans} -size 11 -weight bold")
        self.newPlaylistNameLabelValue.configure(foreground="#BB86FC")
        self.newPlaylistNameLabelValue.configure(text=playlist_name)

        # starts output daemon so the frame finishes drawing. 
        # directly calling will postpone the page being drawn
        downloaderThread = playlist_bot.create_downloader(self.songs, self.output_playlist_filename)
        outputThread = Thread(target=self.output_daemon, args=(downloaderThread,))
        outputThread.daemon = True
        outputThread.start()   
        
    # page to show help content
    # not user interaction here
    def help_page(self):
        self.clear_content_frame()
        self.helpPageLabel = tk.Label(self.contentFrame)
        self.helpPageLabel.place(relx=0.017, rely=0.022, height=21, width=49)
        self.helpPageLabel.configure(activebackground="#f9f9f9")
        self.helpPageLabel.configure(anchor='w')
        self.helpPageLabel.configure(background="#404040")
        self.helpPageLabel.configure(compound='left')
        self.helpPageLabel.configure(font="-family {DejaVu Sans} -size 12 -weight bold")
        self.helpPageLabel.configure(foreground="#f7f7f7")
        self.helpPageLabel.configure(text='''Help''')

        self.helpContentFrame = tk.Frame(self.contentFrame)
        self.helpContentFrame.place(relx=0.017, rely=0.088, relheight=0.89, relwidth=0.966)
        self.helpContentFrame.configure(relief='solid')
        self.helpContentFrame.configure(borderwidth="2")
        self.helpContentFrame.configure(relief="solid")
        self.helpContentFrame.configure(background="#515151")

        self.helpCreatePlaylistHeader = tk.Label(self.helpContentFrame)
        self.helpCreatePlaylistHeader.place(relx=0.017, rely=0.025, height=21, width=189)
        self.helpCreatePlaylistHeader.configure(activebackground="#f9f9f9")
        self.helpCreatePlaylistHeader.configure(anchor='w')
        self.helpCreatePlaylistHeader.configure(background="#515151")
        self.helpCreatePlaylistHeader.configure(compound='left')
        self.helpCreatePlaylistHeader.configure(font="-family {DejaVu Sans} -size 10 -weight bold")
        self.helpCreatePlaylistHeader.configure(foreground="#f7f7f7")
        self.helpCreatePlaylistHeader.configure(text='''Creating a new playlist''')

        self.createPlaylistHelpInstructions = tk.Message(self.helpContentFrame)
        self.createPlaylistHelpInstructions.place(relx=0.035, rely=0.099, relheight=0.323, relwidth=0.925)
        self.createPlaylistHelpInstructions.configure(background="#515151")
        self.createPlaylistHelpInstructions.configure(font="-family {DejaVu Sans} -size 11")
        self.createPlaylistHelpInstructions.configure(foreground="#f7f7f7")
        self.createPlaylistHelpInstructions.configure(padx="1")
        self.createPlaylistHelpInstructions.configure(pady="1")
        self.createPlaylistHelpInstructions.configure(text='''To create a new playlist, click the "Create New" button at the top left. You will be prompted to name your playlist before adding the song names. Please give the playlist a unique name so it may save properly on your filesystem. Once you have typed the name, in the second entry box, type the title of one song at a time proceeded by the "Add" button. The songs will appear in the box below as you add them. Make sure to include the song artist and song title in each entry.''')
        self.createPlaylistHelpInstructions.configure(width=532)

        self.helpGeneratingPlaylistHeader_1 = tk.Label(self.helpContentFrame)
        self.helpGeneratingPlaylistHeader_1.place(relx=0.017, rely=0.469, height=21, width=229)
        self.helpGeneratingPlaylistHeader_1.configure(activebackground="#f9f9f9")
        self.helpGeneratingPlaylistHeader_1.configure(anchor='w')
        self.helpGeneratingPlaylistHeader_1.configure(background="#515151")
        self.helpGeneratingPlaylistHeader_1.configure(compound='left')
        self.helpGeneratingPlaylistHeader_1.configure(font="-family {DejaVu Sans} -size 10 -weight bold")
        self.helpGeneratingPlaylistHeader_1.configure(foreground="#f7f7f7")
        self.helpGeneratingPlaylistHeader_1.configure(text='''Generating your new playlist''')

        self.generatePlaylistHelpInstructions_1 = tk.Message(self.helpContentFrame)
        self.generatePlaylistHelpInstructions_1.place(relx=0.035, rely=0.543, relheight=0.274, relwidth=0.925)
        self.generatePlaylistHelpInstructions_1.configure(background="#515151")
        self.generatePlaylistHelpInstructions_1.configure(font="-family {DejaVu Sans} -size 11")
        self.generatePlaylistHelpInstructions_1.configure(foreground="#f7f7f7")
        self.generatePlaylistHelpInstructions_1.configure(padx="1")
        self.generatePlaylistHelpInstructions_1.configure(pady="1")
        self.generatePlaylistHelpInstructions_1.configure(text='''Once you have finished entering all the songs you wish to download,  to generate your playlist as actual MP3 files on your local machine, click the "Run Bot" button to automatically download each song. The output will show the status of each song on the screen as it attempts to download it. The logs will remain persistent after the download is completed and you may open the playlist folder to review it later.''')
        self.generatePlaylistHelpInstructions_1.configure(width=532)

        self.enjoyLabel = tk.Label(self.helpContentFrame)
        self.enjoyLabel.place(relx=0.852, rely=0.84, height=21, width=69)
        self.enjoyLabel.configure(activebackground="#f9f9f9")
        self.enjoyLabel.configure(anchor='w')
        self.enjoyLabel.configure(background="#515151")
        self.enjoyLabel.configure(compound='left')
        self.enjoyLabel.configure(font="-family {DejaVu Sans} -size 13 -weight bold")
        self.enjoyLabel.configure(foreground="#f7f7f7")
        self.enjoyLabel.configure(text='''Enjoy!''')

        self.appVersionLabel = tk.Label(self.helpContentFrame)
        self.appVersionLabel.place(relx=0.017, rely=0.938, height=21, width=69)
        self.appVersionLabel.configure(activebackground="#f9f9f9")
        self.appVersionLabel.configure(anchor='w')
        self.appVersionLabel.configure(background="#515151")
        self.appVersionLabel.configure(compound='left')
        self.appVersionLabel.configure(font="-family {DejaVu Sans} -size 10 -weight bold")
        self.appVersionLabel.configure(text='''Version:''')

        self.appVersionValueLabel = tk.Label(self.helpContentFrame)
        self.appVersionValueLabel.place(relx=0.157, rely=0.938, height=21, width=380)
        self.appVersionValueLabel.configure(activebackground="#f9f9f9")
        self.appVersionValueLabel.configure(anchor='w')
        self.appVersionValueLabel.configure(background="#515151")
        self.appVersionValueLabel.configure(compound='left')
        self.appVersionValueLabel.configure(text='''v1.1.69 - Developed by Jocelyn <jocelyn@techjosie.com>''')

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    # Configure the scrollbars for a widget.
    def __init__(self, master):

        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    # Creates a ttk Frame with a given master, and use this new frame to
    # place the scrollbars and the widget.
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, tk.Listbox):
    # A standard Tkinter Listbox widget with scrollbars that will
    # automatically show/hide as needed.
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)
    def size_(self):
        sz = tk.Listbox.size(self)
        return sz

def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')


if __name__ == '__main__':
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    global _top1, _w1
    _top1 = root
    _w1 = TopWindow(_top1)
    root.mainloop()
