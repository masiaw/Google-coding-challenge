"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, name):
        # The name given by user
        self.name = name

        # ID of playlist
        self.id = self.name.lower()
        
        # A list of video_ids
        self.videos = []
