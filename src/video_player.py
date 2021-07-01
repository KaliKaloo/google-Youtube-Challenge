"""A video player class."""
from hashlib import new
from .video_library import VideoLibrary
from .video_playlist import Playlist
import random

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.current_video_id = " "
        self.current_video_title = " "
        self.current_video_tags = " "
        self.player_status = None

        self.playlists = {}

####################### PART 1 ##############################


    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")


    def show_all_videos(self):
        all_videos = self._video_library.get_all_videos()
        sorted_videos = sorted(all_videos, key=lambda x:x.title)
        print("Here's a list of all available videos:")
        for sorted_video in sorted_videos:
            print(sorted_video)


    def play_video(self, video_id):
        video_to_play = self._video_library.get_video(video_id)

        if(video_to_play):
            if(self.current_video_title != " "):
                print("Stopping video:", self.current_video_title)

            print("Playing video:", video_to_play.title)
            self.current_video_id = video_to_play.video_id
            self.current_video_title = video_to_play.title
            self.current_video_tags = ' '.join(video_to_play.tags)
            self.player_status = "PLAY"
        else:
            print("Cannot play video: Video does not exist")


    def stop_video(self):
        """Stops the current video."""
        if(self.current_video_title != " "):
            print("Stopping video:", self.current_video_title)
            self.current_video_id = " "
            self.current_video_title = " "
            self.current_video_tags = " "
            self.player_status = "STOP"
        else:
            print("Cannot stop video: No video is currently playing")


    def play_random_video(self):
        """Plays a random video from the video library."""
        all_videos = self._video_library.get_all_videos()
        random_video = random.choice(all_videos).video_id
        self.play_video(random_video)


    def pause_video(self):
        """Pauses the current video."""
        if(self.player_status == "PLAY"):
            print("Pausing video:", self.current_video_title)
            self.player_status = "PAUSED"
        elif (self.player_status == "PAUSED"):
            print("Video already paused:", self.current_video_title)
        else:
            print("Cannot pause video: No video is currently playing")


    def continue_video(self):
        """Resumes playing the current video."""
        if(self.player_status == "PAUSED"):
            print("Continuing video:", self.current_video_title)
            self.player_status = "PLAY"
        elif(self.player_status == "PLAY"):
            print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")


    def show_playing(self):
        """Displays video currently playing."""
        if (self.player_status == "PLAY" ):
            print("Currently playing:", self.current_video_title, f"({self.current_video_id})", f"[{self.current_video_tags}]")

        elif(self.player_status == "PAUSED"):
            print("Currently playing:", self.current_video_title, f"({self.current_video_id})", f"[{self.current_video_tags}] - PAUSED")
        else:
            print("No video is currently playing")
            

####################### PART 2 ##############################


    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.
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
        """
        playlist_id = playlist_name.lower()
        if not playlist_id in self.playlists.keys():
            print("Cannot add video to another_playlist: Playlist does not exist")
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
            print(self._video_library.get_video(video_id))
        return


    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.
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
        """
        playlist_id = playlist_name.lower()
        if not playlist_id in self.playlists.keys():
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            return
        
        self.playlists.pop(playlist_id)
        print(f"Deleted playlist: {playlist_name}")


####################### PART 3 ##############################


    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.
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
        
        print(f"Here are the results for {search_term}:")
        for i, matching_video in enumerate(matching_videos):
            print(f"{i+1}) {str(matching_video)}")

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
            print(f"{i+1}) {str(matching_video)}")

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


####################### PART 4 ##############################


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
