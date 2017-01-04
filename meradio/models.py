from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

# To get the duration, a difference between 2 datetimes
from datetime import timedelta

# To access datetime field
from datetime import datetime


# To store the profile of a song from Spotify
class Song(models.Model):
    # Song ID got from Spotify

    track_id = models.CharField(max_length=200,
                                unique=True)

    name = models.CharField(max_length=200)

    # To store the duration of a song in seconds
    length = models.IntegerField(default=0)

    # To store the album of the song
    album = models.CharField(max_length=200)

    # To store the album artworks
    cover = models.ImageField(upload_to='media/album-artworks',
                              default='album-artworks/default/musicify-icon.png',
                              blank=True)

    # To store the artist of the song
    artist = models.CharField(max_length=200)

    # To store the preview of the song
    preview = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

# This is the music profile for each user
# It extends the following fields from django authentication module
# username, password, first_name, last_name, email
class Profile(models.Model):
    # Map with the User model from django authentication module
    # Upon deletion in the module, the profile is removed
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user')

    # Current song that the user is playing
    song = models.ForeignKey(Song,
                             blank=True,
                             null=True,
                             related_name='current_song')

    # Start time of the current song
    start_time = models.DateTimeField(blank=True,
                                      null=True)

    # This field stores the people who the current user starred
    favorites = models.ManyToManyField(User,
                                       blank=True,
                                       related_name='favorites')
    
    # This field stores the description of the current user
    # By default the description is ""
    description = models.CharField(max_length=120,
                                   default="")

    # This field is to stored the current status of a user
    # Status includes: online, listening, private, public, etc. (TBD)
    status = models.CharField(max_length=20,
                              default='Stopped')

    # This field is to track the duration where user pauses his song
    pause_duration = models.FloatField(default='0')

    # To store the songs that a user likes
    liked = models.ManyToManyField(Song,
                                   blank=True,
                                   related_name='liked')

    # To store the songs that a user dislike
    disliked = models.ManyToManyField(Song,
                                      blank=True,
                                      related_name='disliked')

    # To store a token for newly registered user
    # and handle 'forgot password'
    token = models.CharField(max_length=420)

    # To store the temporary password when user request to change or forget
    password_temp = models.CharField(max_length=420,
                                     default='',
                                     blank=True)

    # To store the current genre preferences (TBD)
    preferences = models.CharField(max_length=420,
                                   default='',
                                   blank=True)

    # To store the profile picture
    avatar = models.ImageField(upload_to='media/profile-photos',
                               default='profile-photos/default/musicify-icon.png',
                               blank=True)


    def __unicode__(self):
        return self.token


# To store the information of a message
class Message(models.Model):
    # Each message belongs to a specific user
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    # Current server time when the message created
    created_time = models.DateTimeField(auto_now_add=True)

    # The content of the message
    msg = models.CharField(max_length=200)

    def __unicode__(self):
        return self.msg


class Chat(models.Model):
    # Current server time when the song starts
    start_time = models.DateTimeField(auto_now_add=True)

    # To reference the host of the chat room
    host = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='host')

    # To reference the remaining users in the chat room
    # By default, there is no listener
    listeners = models.ManyToManyField(User,
                                       blank=True,
                                       related_name='listeners')

    # The messages associated with this chat
    messages = models.ManyToManyField(Message,
                                      blank=True)

    # Current song in the chat
    # Only one song is associated with a chat at one time
    current_song = models.OneToOneField(Song,
                                        on_delete=models.CASCADE)

    def __unicode__(self):
        return self.host.username
