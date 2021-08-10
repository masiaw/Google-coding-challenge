"""A video player class."""

from .video_library import VideoLibrary
import random
from.video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        # key called current_video_id which stores the id of the current video, if any, else None 
        self.extra_videos = {}
        # this will be a list of all the playlists, where every item will be a Playlist object
        self.playlists = {}

    # ======================================= PART 1 of challenge
    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_videos = self._video_library.get_all_videos()
        
        sorted_videos = sorted(all_videos, key=lambda x:x.title)
        print("Here's a list of all available videos:")

        for sorted_video in sorted_videos:
            print(str(sorted_video.title) + " (" + str(sorted_video.video_id) + ") [" + " ".join(sorted_video.tags) + "]")

    def play_video(self, video_id):
        """Plays the respective video.
        Args:
            video_id: The video_id to be played.
        """
        new_video = self._video_library.get_video(video_id)
        if not new_video:
            print("Cannot play video: Video does not exist")
            return

        current_video_id = self.extra_videos.get("current_video_id")
        if current_video_id:
            self.stop_video()
            self.extra_videos["current_video_id"] = new_video.video_id
            self.extra_videos["is_current_video_playing"] = True
            print(f"Playing video: {new_video.title}")
        else:
            self.extra_videos["current_video_id"] = new_video.video_id
            self.extra_videos["is_current_video_playing"] = True
            print(f"Playing video: {new_video.title}")


    def stop_video(self):
        """Stops the current video."""
        current_video_id = self.extra_videos.get("current_video_id")
        if not current_video_id:
            print("Cannot stop video: No video is currently playing")
            return
        current_video = self._video_library.get_video(current_video_id)
        self.extra_videos["current_video_id"] = None
        self.extra_videos["is_current_video_playing"] = None
        print(f"Stopping video: {current_video.title}")


    def play_random_video(self):
        """Plays a random video from the video library."""
        all_videos = self._video_library.get_all_videos()

        random_video = random.choice(all_videos)
        self.play_video(random_video.video_id)


    def pause_video(self):
        """Pauses the current video."""
        current_video_id = self.extra_videos.get("current_video_id")
        if not current_video_id:
            print("Cannot pause video: No video is currently playing")
        else:
            current_video = self._video_library.get_video(current_video_id)
            if self.extra_videos["is_current_video_playing"]:
                self.extra_videos["is_current_video_playing"] = False
                print(f"Pausing video: {current_video.title}")
            else:
                print(f"Video already paused: {current_video.title}")

    def continue_video(self):
        """Resumes playing the current video."""
        current_video_id = self.extra_videos.get("current_video_id")
        if not current_video_id:
            print("Cannot continue video: No video is currently playing")
            return
        
        current_video = self._video_library.get_video(current_video_id)
        if not self.extra_videos["is_current_video_playing"]:
            self.extra_videos["is_current_video_playing"] = True
            print(f"Continuing video: {current_video.title}")
        else:
            print(f"Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        current_video_id = self.extra_videos.get("current_video_id")
        if not current_video_id:
            print("No video is currently playing")
            return
        
        current_video = self._video_library.get_video(current_video_id)
        if self.extra_videos["is_current_video_playing"]:
            print("Currently playing: " + str(current_video.title)  + " (" + str(current_video.video_id) + ") [" + str(" ".join(current_video.tags)) + "]")
        else:
            print("Currently playing: " + str(current_video.title) + " (" + str(current_video.video_id) + ") [" + str(" ".join(current_video.tags)) + "] - PAUSED")

    # ======================================= PART 2 of challenge
    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        new_playlist_id = playlist_name.lower()
        if new_playlist_id in self.playlists.keys():
            print("Cannot create playlist: A playlist with the same name already exists")
            return
        
        new_playlist = Playlist(playlist_name)
        self.playlists[new_playlist_id] = new_playlist
        print(f"Successfully created new playlist: {playlist_name}")
        

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlist_id = playlist_name.lower()
        if not playlist_id in self.playlists.keys():
            print("Cannot add video to " + playlist_id + ": Playlist does not exist")
            return

        if not self._video_library.get_video(video_id):
            print(f"Cannot add video to {playlist_name}: Video does not exist")
            return

        if video_id in self.playlists[playlist_id].videos:
            print(f"Cannot add video to {playlist_name}: Video already added")
            return


        video = self._video_library.get_video(video_id)
        self.playlists[playlist_id].videos.append(video_id)
        print(f"Added video to {playlist_name}: {video.title}")
        return

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self.playlists.keys()) == 0:
            print("No playlists exist yet")
            return
        
        all_playlists = self.playlists.keys()
        sorted_playlists_names = sorted(all_playlists)

        print("Showing all playlists:")
        for sorted_playlist_name in sorted_playlists_names:
            print(self.playlists.get(sorted_playlist_name).name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_id = playlist_name.lower()
        if not playlist_id in self.playlists.keys():
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            return

        playlist = self.playlists.get(playlist_id)
        videos = playlist.videos
        if len(videos) == 0:
            print(f"Showing playlist: {playlist_name}")
            print("No videos here yet") 
            return
        

        print(f"Showing playlist: {playlist_name}")
        for video_id in videos:
            video = self._video_library.get_video(video_id)
            print(str(video.title) + " (" + str(video.video_id) + ") [" + str(" ".join(video.tags)) + "]")
        return

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist_id = playlist_name.lower()
        if not playlist_id in self.playlists.keys():
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return

        if not self._video_library.get_video(video_id):
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
            return

        if not video_id in self.playlists[playlist_id].videos:
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            return


        video = self._video_library.get_video(video_id)

        self.playlists[playlist_id].videos.remove(video_id)
        print(f"Removed video from {playlist_name}: {video.title}")
        return

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_id = playlist_name.lower()
        if not playlist_id in self.playlists.keys():
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            return
        
        self.playlists.get(playlist_id).videos = []
        print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_id = playlist_name.lower()
        if not playlist_id in self.playlists.keys():
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            return
        
        self.playlists.pop(playlist_id)
        print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        all_videos.sort(key=lambda x:x.title)
        matching_videos = []
        for video in all_videos:
            if search_term.lower() in video.title.lower():
                matching_videos.append(video)
        
        matching_videos.sort(key=lambda x:x.title)

        if len(matching_videos) == 0:
            print(f"No search results for {search_term}")
            return
        
        print("Here are the results for cat:")
        for i, matching_video in enumerate(matching_videos):
             print(f"{i+1}) " + str(matching_video.title) + " (" + str(matching_video.video_id) + ") [" + str(" ".join(matching_video.tags)) + "]")

        print("Would you like to play any of the above? If yes, specify the number of the video.\nIf your answer is not a valid number, we will assume it's a no.")
        video_number = input()

        try:
            int_video_number = int(video_number)
            if int_video_number > len(matching_videos) or int_video_number < 0:
                return
            else:
                self.play_video(matching_videos[int_video_number-1].video_id)
        except ValueError:
            return

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        if not video_tag.startswith('#'):
            print(f"No search results for {video_tag}")
            return

        all_videos = self._video_library.get_all_videos()
        matching_videos = []
        for video in all_videos:
            if video_tag.lower() in list(map(str.lower, video.tags)):
                matching_videos.append(video)
        
        matching_videos.sort(key=lambda x:x.title)

        if len(matching_videos) == 0:
            print(f"No search results for {video_tag}")
            return
        
        print(f"Here are the results for {video_tag}:")
        for i, matching_video in enumerate(matching_videos):
            print(f"{i+1}) "+ str(matching_video.title) + " (" + str(matching_video.video_id) + ") [" + str(" ".join(matching_video.tags)) + "]")

        print("Would you like to play any of the above? If yes, specify the number of the video.\nIf your answer is not a valid number, we will assume it's a no.")
        video_number = input()

        try:
            int_video_number = int(video_number)
            if int_video_number > len(matching_videos) or int_video_number < 0:
                return
            else:
                self.play_video(matching_videos[int_video_number-1].video_id)
        except ValueError:
            return

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")


    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
