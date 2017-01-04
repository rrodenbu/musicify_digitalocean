from django.conf.urls import url

import meradio.views
import django.contrib.auth.views

urlpatterns = [
    url(r'^$', meradio.views.home),

    # Route for the log in page, which is handle by django authentication module for now
    url(r'log-in$', django.contrib.auth.views.login, {'template_name':'login.html'}, name='log-in'),

    # Route for the log out page, handled by django
    url(r'log-out$', meradio.views.cleanup_and_logout, name='log-out'),

    # Route for registration process
    url(r'register$', meradio.views.register, name='register'),
    url(r'email-confirm/(?P<username>\S+)/(?P<token>\S+)', meradio.views.email_confirm, name='email-confirm'),

    # Route for resetting password
    url(r'forget-password$', meradio.views.forget_password, name='forget-password'),
    url(r'password-reset/$', meradio.views.password_reset, name='password-reset'),
    url(r'password-reset/(?P<username>\S+)/(?P<token>\S+)/$', meradio.views.password_reset, name='password-reset'),
    url(r'password-reset/(?P<username>\S+)/(?P<token>\S+)', meradio.views.password_reset, name='password-reset'),
    url(r'password-confirm/(?P<username>\S+)/(?P<token>\S+)/$', meradio.views.password_confirm, name='password-confirm'),

    # Get pool of songs
    url(r'get-songs$', meradio.views.get_songs, name='get-songs'),

    # Route for explore
    url(r'explore$', meradio.views.explore, name='explore'),

    # Route for find stations.
    url(r'find-stations/$', meradio.views.find_stations, name='find-stations'),

    # Route for account settings (change password)
    url(r'settings$', meradio.views.account_settings, name='settings'),

    # Route for remove a song from the liked list
    url(r'dislike/$', meradio.views.dislike, name='dislike'),
    url(r'dislike/(?P<id>\S+)/$', meradio.views.dislike, name='dislike'),
    url(r'dislike/(?P<id>\S+)$', meradio.views.dislike, name='dislike'),

    # Route for liking a song
    url(r'like/$', meradio.views.like, name='like'),
    url(r'like/(?P<id>\S+)/$', meradio.views.like, name='like'),
    url(r'like/(?P<id>\S+)$', meradio.views.like, name='like'),

    # Route for playing song for user station
    url(r'play-song/$', meradio.views.play_user_song, name='play-user-song'),
    url(r'play-song/(?P<id>\S+)/$', meradio.views.play_user_song, name='play-user-song'),
    url(r'play-song/(?P<id>\S+)$', meradio.views.play_user_song, name='play-user-song'),

    # Route for retrieving next song for user station
    url(r'next-song/$', meradio.views.next_user_song, name='next-user-song'),
    url(r'next-song/(?P<id>\S+)/$', meradio.views.next_user_song, name='next-user-song'),
    url(r'next-song/(?P<id>\S+)$', meradio.views.next_user_song, name='next-user-song'),

    # Route for retrieving next song for user station
    url(r'prev-song/$', meradio.views.prev_user_song, name='prev-user-song'),
    url(r'prev-song/(?P<id>\S+)/$', meradio.views.prev_user_song, name='prev-user-song'),
    url(r'prev-song/(?P<id>\S+)$', meradio.views.prev_user_song, name='prev-user-song'),

    # Route for to retrieve profile avatar
    url(r'get-avatar/$', meradio.views.get_avatar, name='get-avatar'),
    url(r'get-avatar/(?P<username>\S+)/$', meradio.views.get_avatar, name='get-avatar'),
    url(r'get-avatar/(?P<username>\S+)$', meradio.views.get_avatar, name='get-avatar'),

    # Route for my station to remove song from liked playlist
    url(r'remove-song/$', meradio.views.remove_song, name='remove-song'),
    url(r'remove-song/(?P<id>\S+)/$', meradio.views.remove_song, name='remove-song'),
    url(r'remove-song/(?P<id>\S+)$', meradio.views.remove_song, name='remove-song'),

    # Route for setting twilio ip messaging
    url(r'token$', meradio.views.token, name="token"),

    # Route for favoriting a user
    url(r'(?P<username>\S+)/favorite/$', meradio.views.favorite, name='favorite'),

    # Route for unfavoriting a user
    url(r'(?P<username>\S+)/unfavorite/$', meradio.views.unfavorite, name='unfavorite'),

    # Route for searching users
    url(r'search-users/?$', meradio.views.search_users, name='search-users'),
    url(r'search-users/(?P<query>\S+)/$', meradio.views.search_users, name='search-users'),
    url(r'search-users/(?P<query>\S+)', meradio.views.search_users, name='search-users'),

    # Route to return the exact song and duration as the input user
    url(r'sync-user-song/$', meradio.views.sync_user_song, name='sync-user-song'),
    url(r'sync-user-song/(?P<username>\S+)/$', meradio.views.sync_user_song, name='sync-user-song'),
    url(r'sync-user-song/(?P<username>\S+)/', meradio.views.sync_user_song, name='sync-user-song'),

    # Route to update user's playing status in my station
    url(r'update-playing-status/?$', meradio.views.update_playing_status, name='update-playing-status'),
    url(r'update-playing-status/(?P<status>\S+)/(?P<pause_duration>\S+)/$', meradio.views.update_playing_status, name='update-playing-status'),
    url(r'update-playing-status/(?P<status>\S+)/(?P<pause_duration>\S+)', meradio.views.update_playing_status, name='update-playing-status'),

    # Route to retrieve users first name, last name and avatar for channel listeners
    url(r'retrieve-user-info/$', meradio.views.get_user_info, name='get-user-info'),
    url(r'retrieve-user-info/(?P<username>\S+)/$', meradio.views.get_user_info, name='get-user-info'),
    url(r'retrieve-user-info/(?P<username>\S+)', meradio.views.get_user_info, name='get-user-info'),

    # Route to retrieve all listeners of current channel
    url(r'listeners/$', meradio.views.get_listeners, name='get-listeners'),
    url(r'listeners/(?P<channel_id>\S+)/$', meradio.views.get_listeners, name='get-listeners'),
    url(r'listeners/(?P<channel_id>\S+)', meradio.views.get_listeners, name='get-listeners'),

    # Route to get recommendations from a user
    url(r'get-recommendations?$', meradio.views.get_recommendations, name='get-recommendations'),

    # Route to get user's favorites
    url(r'get-favorites?$', meradio.views.get_favorites, name='get-favorites'),

    # Route to change description
    url(r'change-description/?$', meradio.views.change_description, name='change-description'),

    #################################################
    # Put all generic urls down here allowing other urls to work properly
    #################################################

    # Route for user's station
    url(r'(?P<username>\S+)/$', meradio.views.user_station, name='user-station'),
]
