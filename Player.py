from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from os import listdir, path

class ChooseFile(FloatLayout):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)

class AudioPlayer(Widget):
    #folder location
    directory = ''
    #current file playing
    nowPlaying = ''
    #List to hold songs
    songs = []
    #List to hold paths
    pathList = []
    #Temporary Song List
    temp_songList = []
    #List of songs paths
    songPath = []

    def dismiss_popup(self):
        self._popup.dismiss()

    def fileSelect(self):
        content = ChooseFile(select = self.select, cancel = self.dismiss_popup)
        self._popup = Popup(title = 'Select folder', content= content, size_hint = (0.9, 0.9))
        self._popup.open()

    def select(self, path):
        self.directory = path
        self.ids.direct.text = self.directory
        if not self.directory in self.pathList:
            self.pathList.append(self.directory)
            self.getSongs()
            self.dismiss_popup()
        else:
            self.dismiss_popup()
    
    def browse(self):
        #Text entered by user
        self.directory = self.ids.direct.text

        if (self.directory == '') or self.directory in self.pathList:
            self.fileSelect()
        else:
            self.pathList.append(self.directory)
            self.getSongs()

    def getSongs(self):
        if not self.directory.endswith('/'):
            self.directory += '/'

        #Check if the directory exists
        if not path.exists(self.directory):
            self.ids.status.text = 'Folder not found'
            self.ids.status.color = (1,0,0,1)
        else:
            self.ids.status.text = ''
            self.ids.scroll.bind(minimum_height = self.ids.scroll.setter('height'))

            #get mp3 files from directory
            for fl in listdir(self.directory):
                if fl.endswith('.mp3'):
                    if not fl in self.songs:
                        self.temp_songList.append(fl)
                        self.songPath.append(self.directory)

            #If in chosen directory are no mp3 files
            if self.temp_songList == [] and self.directory != '':
                self.ids.status.text = 'No Music Found'
                self.ids.status.color = (1,0,0,1)
            
            self.temp_songList.sort()
            for song in self.temp_songList:
                def playSong(btn):
                    try:
                        self.nowPlaying.stop()
                        self.ids.toggle_play_btn.text = '||'
                    except:
                        pass
                    finally:
                        self.currentSong_index = self.songs.index(btn.text + '.mp3')
                        self.nowPlaying = SoundLoader.load(self.songPath[self.currentSong_index] + btn.text + '.mp3')
                        self.nowPlaying.play()
                        self.ids.currentPlay.text = btn.text
                        self.ids.status.text = ''

                #Song button label
                btn = Button(text = song[:-4], size_hint_x = 1, on_press = playSong)

                #Label song colors
                btn.background_color = (61/255, 61/255, 63/255, 1)

                #Add btn and icon to Scroll Layout
                self.ids.scroll.add_widget(btn)
            self.songs.extend(self.temp_songList)
            self.temp_songList.clear()

    def prev_song(self):
        if self.currentSong_index == 0:
            self.currentSong_index = len(self.songs)
        self.nowPlaying.stop()
        self.nowPlaying = SoundLoader.load(self.songPath[self.currentSong_index - 1] + self.songs[self.currentSong_index - 1])
        self.nowPlaying.play()
        self.ids.toggle_play_btn.text = '||'
        self.currentSong_index = self.currentSong_index - 1
        self.ids.currentPlay.text = self.songs[self.currentSong_index][:-4]

    def toggle_play(self):
        if self.nowPlaying.state == 'stop':
            self.nowPlaying.play()
            self.ids.toggle_play_btn.text = '||'
        else:
            self.nowPlaying.stop()
            self.ids.toggle_play_btn.text = '#'

    def next_song(self):
        if self.currentSong_index == (len(self.songs) - 1):
            self.currentSong_index = -1
        self.nowPlaying.stop()
        self.nowPlaying = SoundLoader.load(self.songPath[self.currentSong_index + 1] + self.songs[self.currentSong_index + 1])
        self.nowPlaying.play()
        self.ids.toggle_play_btn.text = '||'
        self.currentSong_index = self.currentSong_index + 1
        self.ids.currentPlay.text = self.songs[self.currentSong_index][:-4]

    def clearInput(self):
        self.songs.clear()
        self.ids.direct.text = ''
        self.ids.scroll.clear_widgets()
        self.pathList.clear()
        self.songPath.clear()

class PlayerApp(App):
    def build(self):
        player = AudioPlayer()
        self.title = 'Audio Player'
        self.icon = 'wicon.png'
        return player


if __name__ == '__main__':
    PlayerApp().run()