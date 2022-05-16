class Album:
    # attributes that represent important info about an album
    __artist = ''
    __title = ''
    __tracks = []
    __year = 0

    def __init__(self, title, artist, year, tracks):
        # initialize album with values
        self.__artist = artist
        self.__title = title
        self.__tracks = tracks
        self.__year = year
    
    def add_tracks(self, tracks):
        # add tracks if necessary
        self.__tracks.append(tracks)

    def get_tracks(self):
        # get a list of all tracks on the album
        return self.__tracks
    
    def albuminfo(self):
        # get all album metadata
        return [self.__title, self.__artist, self.__year]

class Media(Album):
    __format = '' # CD, record, tape, etc
    def __init__(self, title, artist, year, tracks, format):
        super().__init__(title, artist, year, tracks)
        self.__format = format
    
    def mediainfo(self):
        return [super().albuminfo(), self.__format]

thisAlbum = Album('The Wall', 'Pink Floyd', 1979, ['In The Flesh?', 'The Thin Ice'])
wallDisc = Media('The Wall', 'Pink Floyd', 1979, thisAlbum.get_tracks(), 'CD')
wallDisc.add_tracks('Another Brick In The Wall')
print(wallDisc.mediainfo(), wallDisc.get_tracks())
