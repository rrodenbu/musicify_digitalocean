from django.shortcuts import render

# Use this to ensure the CSRF decorator is usable
# to give the token for later requests
from django.views.decorators.csrf import ensure_csrf_cookie

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Use this to enable render and redirect action
from django.shortcuts import render, redirect

# Used to enable database transaction
from django.db import transaction


# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Used to access all models and forms
from meradio.models import *
from meradio.forms import *

# Used to send email using django console backend
from django.core.mail import send_mail

# Used for redirect url with reverse
from django.core.urlresolvers import reverse

# Used to manually create HttpResponses or raise Http404 exception
from django.http import HttpResponse, Http404

# Used to create a token from hash of random number
import random
import hashlib
import json

# Framework to use Spotify API in python.
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Helper function to guess a MIME type from a file name
from mimetypes import guess_type

# Used to get an object from a model
from django.shortcuts import get_object_or_404

# Settings.py variables: twilio
from django.conf import settings

# Twilio
from django.http import JsonResponse

# Framework to use twilio API
from twilio.access_token import AccessToken, IpMessagingGrant
from twilio.rest.ip_messaging import TwilioIpMessagingClient
from twilio import TwilioRestException

# To access django sessions
from django.contrib.sessions.models import Session

# To access timezone.now()
from django.utils import timezone

# Used for complex lookup
from django.db.models import Q

# To access datetime functions
import datetime

# Used to cleanup and log out user
from django.contrib.auth.views import login, logout, logout_then_login

# Create your views here.


"""Name: cleanup_and_logout
   Author: Nguyen Dinh
   Description: display a homepage if the user is not logged in
   Version: 1.0.0
   Reviewer:
"""
@login_required
@transaction.atomic
def cleanup_and_logout(request):
    # Update the user's playing status to stopped
    profile = get_object_or_404(Profile, user=request.user)
    profile.status = 'Stopped'
    profile.pause_duration = 0
    profile.save()

    response = logout(request)
    return redirect('log-in')


"""Name: home
   Author: Nguyen Dinh
   Description: display a homepage if the user is not logged in
   Version: 1.0.0
   Reviewer:
"""
@ensure_csrf_cookie
def home(request):
    # If the user is logged_in, direct mystation
    if request.user.is_authenticated():
        return redirect('user-station', request.user.username)

    # If the user is not logged in, display default home page
    return render(request, 'home.html')

"""Name: register
   Author: Nguyen Dinh
   Description: Allows user to register for an account
   Input: username, password2, password1, email
   Output: create an account, an empty profile, then send confirmation
   Version: 1.0.0
   Reviewer:
"""
@transaction.atomic
def register(request):
    # Context after processing the request
    context = {}

    # Display the registering page again if the method is not POST
    if request.method != 'POST':
        context['form'] = RegistrationForm()
        return render(request, 'registration.html', context)

    # A list of errors encountered during the operation
    messages = []
    context['messages'] = messages

    # Use django form to handle input validation
    registration_form = RegistrationForm(request.POST)
    context['form'] = registration_form

    # Validate the form
    if not registration_form.is_valid():
        return render(request, 'registration.html', context)

    # this is the token to verify account
    token = hashlib.md5(str(random.randint(1000, 9000)).encode()).hexdigest()

    # Create the new user from valid form data
    new_user = User.objects.create_user(username=request.POST['username'],
                                        password=request.POST['password1'],
                                        first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'],
                                        email=request.POST['email'])
    new_user.is_active = False
    new_user.save()

    # Create an empty profile for the registered user
    new_profile = Profile(user=User.objects.get(username=request.POST['username']))
    data = {}
    data['token'] = token
    profile_form = ProfileForm(data, instance=new_profile)
    profile_form.save()

    # To send email to user
    email_body = '''
        Welcome to Musicify. Please click the link below to verify your address in order to complete the registration of your account:

        http://%s%s
        ''' % (request.get_host(), reverse('email-confirm', args=(request.POST['username'], token)))
    send_mail(subject='Verify your email address',
              message=email_body,
              from_email='musicify.t254@gmail.com',
              recipient_list=[request.POST['email']])
    messages.append('An email has been sent to ' + request.POST['email'] + ' with a verification link. Please check.')

    return render(request, 'registration.html', context)


"""Name: email_confirm
   Author: Nguyen Dinh
   Description: Handle email confirmation for new user
   Input: username, token
   Output: activate the account, then redirect to the home page
   Version: 1.0.0
   Reviewer:
"""
@transaction.atomic
def email_confirm(request, username='', token=''):
    try:
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        if profile.token == token:
            user.is_active = True
            user.save()
            login(request, user)
            user = authenticate(username=username, password=user.password)
        else:
            return HttpResponse('Incorrect validation token for ' + username)
    except:
        return HttpResponse('Unable to validate the information for ' + username)

    return redirect(reverse('home'))


"""Name: forget_password
   Author: Nguyen Dinh
   Description: Allow an existing user to enter a new password, then
       send a confirmation with token to verify
   Input: username, password1, password2
   Output: save the password to a temp pass, then send email
   Version: 1.0.0
   Reviewer:
"""
@transaction.atomic
def forget_password(request):
    context = {}
    messages = []
    error_messages = []

    # If this is not a post method, simply display the email form
    if not request.method == 'POST':
        context['form'] = SendEmailForm()
        return render(request, 'send-email.html', context)

    form = SendEmailForm(request.POST)
    context['form'] = form
    context['messages'] = messages
    context['error_messages'] = error_messages

    # If the form is valid, proceed.
    # If not, return with errors from the form
    if form.is_valid():
        user = get_object_or_404(User, email=form.cleaned_data['email'])

        # Change the token to reset password
        # And add the password to temp
        token = hashlib.md5(str(random.randint(1000, 9000)).encode()).hexdigest()
        profile = get_object_or_404(Profile, user=user)

        profile.token = token
        profile.save()

        # To send email to user to reset password
        email_body = '''
                        Please click the one-time link below to reset your password in Musicify:

                        http://%s%s
                        ''' % (request.get_host(),
                               reverse('password-reset',
                                       args=(user.username, token)))
        send_mail(subject='Verify your identification',
                  message=email_body,
                  from_email='musicify.t254@gmail.com',
                  recipient_list=[user.email])

        messages.append(
            'An email has been sent to ' + user.email + ' with a verification link. Please select the link to reset password.')

        return render(request, 'send-email.html', context)

    else:
        error_messages.append('There is no account affiliated with this email.')
        return render(request, 'send-email.html', context)

"""Name: password_reset
   Author: Nguyen Dinh, Judy Mai
   Description: Handle email confirmation and change password
   Input: username, token
   Output: activate the account, also reset password form
   Version: 1.0.0
   Reviewer:
"""
def password_reset(request, username='', token=''):
    try:
        context = {}
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        if profile.token == token:
            # log the user out from any active session
            response = logout(request)
  
            # Reset the playing status as well
            profile.status = 'Stopped'
            profile.pause_duration = 0
   
            profile.save()
             
            return password_confirm(request, username, token)
        else:
            return HttpResponse('Invalid validation token for ' + username)
    except:
        if username=='':
            return HttpResponse('Unable to validate the information for the input username.')
        else:
            return HttpResponse('Unable to validate the information for '+username+'.')

"""Name: password_confirm
   Author: Nguyen Dinh
   Description: Handle email confirmation for new user
   Input: username
   Output: activate the account, then redirect to the home page
   Version: 1.0.0
   Reviewer:
"""
@transaction.atomic
def password_confirm(request, username, token):
    context = {}
    messages = []
    error_messages = []

    context['username'] = username
    context['token'] = token
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
 
    # log the user out from any active session
    response = logout(request)
 
    if profile.token == token:
        # log the user out from any active session
        response = logout(request)
      
        # Reset the playing status as well
        profile.status = 'Stopped'
        profile.pause_duration = 0
   
        profile.save()

        # If this is not a post method, simply display the password form
        if request.method == 'GET':
            form = ForgetPasswordForm()
            context['form'] = form
            return render(request, 'resetpw.html', context)

    #POST with valid token
        form = ForgetPasswordForm(request.POST)
        context['form'] = form
        context['messages'] = messages
        context['error_messages'] = error_messages

        # If the form is valid, proceed.
        # If not, return with errors from the form
        if form.is_valid():
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Generate a random token to prevent the previous one from being reused
            profile.token = hashlib.md5(str(random.randint(1, 9)).encode()).hexdigest()
            profile.save()

            messages.append("Password has been reset, please login again")
            return render(request, 'reset-pw-done.html', context)
        else:
            # invalid form
            error_messages.append("Passwords don't match, please try again")
            return render(request, 'resetpw.html', context)
    else:
        # invalid token
        return HttpResponse('Invalid validation token for ' + username + '. Please try again.')        
  
"""Name: get_songs
   Author: Riley Rodenburg
   Description: Get new releases from Spotify api
   Input: username
   Output: Retrieve songs from Spotify and save to db.
   Version: 1.0.0
   Reviewer:
"""
@transaction.atomic
@login_required
def get_songs(request):

    client_credentials_manager = SpotifyClientCredentials(client_id=settings.CLIENT_ID,
                                                          client_secret=settings.CLIENT_SCERECT)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Only get songs if the user is 'admin'
    if request.user.username == 'admin':
        # Calling Spotify API & retrieving top-songs playlist
        results = sp.category_playlists(category_id="toplists", 
                                        country=None, 
                                        limit=1, 
                                        offset=0)
        all_top_playlists = results['playlists']['items']
        
        for playlist in all_top_playlists:
            playlist_id = playlist.get('id')
            playlist_tracks = sp.user_playlist("spotify", 
                                          playlist_id,
                                          fields="tracks,next")
            all_tracks = playlist_tracks['tracks']['items']

            # Add all the songs to the database
            for track in all_tracks:
                song = track['track']
                # If the song is not in the db, add it
                if Song.objects.filter(track_id=song['id']).count() == 0:

                    if(song['id'] and 
                       song['name'] and 
                       song['duration_ms'] and 
                       song['album']['name'] and 
                       song['album']['images'][0]['url'] and 
                       song['artists'][0]['name'] and 
                       song['preview_url']):

                        new_song = Song(track_id=song['id'],
                                        name=song['name'],
                                        length=song['duration_ms'] / 1000,  # seconds
                                        album=song['album']['name'],
                                        cover=song['album']['images'][0]['url'],
                                        artist=song['artists'][0]['name'],
                                        preview=song['preview_url'])
                        new_song.save()
        return redirect('user-station', request.user.username);
    else:
        return HttpResponse("You are not authorized to perform this action")


"""Name: explore
   Author: Riley Rodenburg
   Description: Allows user to discover new music.
   Input: -
   Output: Data for first song to display to user.
   Version: 1.0.0
   Reviewer:
"""
@login_required
def explore(request):
    context = {}
    song = Song.objects.order_by('?').first() #randomize song
    context['song'] = song
    return render(request, 'exploremusic.html', context)


"""Name: my_station
   Author: Judy
   Description: Allows user to listen to liked selected music and recommended songs.
   Input: -
   Output: Data for first song to display to user.
   Version: 1.0.0
   Reviewer:
"""
@login_required
def my_station(request):
    context = {}
    profile = get_object_or_404(Profile, user=request.user)
    context['profile'] = profile

    # initial random song to populate page
    song = profile.liked.order_by('?').first()
    context['song'] = song


    # description form
    form = DescriptionForm(request.POST)
    context['description_form'] = form

    # Update song and start time to the DB
    update_user_song(profile, song)

    #if profile.status == "Stopped":
    #    return render(request, 'mystation.html', context)
    #else:
    #    return render(request, 'mystation_alt.html', context)

    return render(request, 'mystation.html', context)


"""Name: get_recommendations
   Author: Nguyen
   Description: get recommendations from a user
   Input:
   Output: Data for current song and time to display to user.
   Version: 1.0.0
   Reviewer: Nguyen Dinh
"""
@login_required
@transaction.atomic
def get_recommendations(request):
    profile = get_object_or_404(Profile, user=request.user)
    liked_songs = profile.liked
    context = {}

    if liked_songs.all().count() != 0:
        client_credentials_manager = SpotifyClientCredentials(client_id=settings.CLIENT_ID,
                                                              client_secret=settings.CLIENT_SCERECT)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        recommended_song = {}
        recommended_songs = []
        track_seeds = []

        for liked_song in liked_songs.all():
            track_seeds.append(liked_song.track_id)

        results = sp.recommendations(seed_tracks=track_seeds, limit=20)
        all_tracks = results['tracks']

        for track in all_tracks:

            # Get song info from result
            recommended_song['track_id'] = track['id']
            recommended_song['name'] = track['name']
            recommended_song['length'] = track['duration_ms'] / 1000
            recommended_song['album'] = track['album']['name']
            recommended_song['cover'] = track['album']['images'][0]['url']
            recommended_song['artist'] = track['artists'][0]['name']
            recommended_song['preview'] = track['preview_url']

            # Put the song into the db as well
            if Song.objects.filter(track_id=track['id']).count() == 0:
                # Put to recommended list if is not in the db
                if (track['id'] and
                        track['name'] and
                        track['duration_ms'] and
                        track['album']['name'] and
                        track['album']['images'][0]['url'] and
                        track['artists'][0]['name'] and
                        track['preview_url']):
                    new_song = Song(track_id=track['id'],
                                    name=track['name'],
                                    length=track['duration_ms'] / 1000,  # seconds
                                    album=track['album']['name'],
                                    cover=track['album']['images'][0]['url'],
                                    artist=track['artists'][0]['name'],
                                    preview=track['preview_url'])
                    new_song.save()
                    recommended_songs.append(recommended_song.copy())
            else:
                # Only put song iff it is not in user's liked and dislike pool
                song_to_check = get_object_or_404(Song, track_id=track['id'])
                if not song_to_check in profile.disliked.all() and not song_to_check in profile.liked.all():
                    recommended_songs.append(recommended_song.copy())

            context['songs'] = recommended_songs

    return render(request, 'songs.json', context, content_type='application/json')

"""Name: user_station
   Author: Judy, Nguyen
   Description: Allows logged-in user to listen to a specific user's liked music
   Input: -
   Output: Data for current song and time to display to user.
   Version: 1.0.0
   Reviewer: Nguyen Dinh
"""
@login_required
def user_station(request, username):
    context = {}
    if username == 'admin' and not request.user.username=='admin':
        raise Http404
    if request.user.username == username:
        return my_station(request)

    my_profile = get_object_or_404(Profile, user=request.user)

    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    context['profile'] = profile

    # determine if following the user or not
    if user in my_profile.favorites.all():
        is_favorite = True
    else:
        is_favorite = False

    context['is_favorite'] = is_favorite
    
    return render(request, 'userstation.html', context)


"""Name: find_stations
   Author: Judy Mai
   Description: Page where user can view favorites and find new stations
   Input: n/a
   Output: n/a
   Version: 1.0.0
   Reviewer:
"""
@login_required
def find_stations(request):
    return render(request, 'find-stations.html')


"""Name: account_settings
   Author: Riley Rodenburg
   Description: Allows user to update info on their account
   Input: first_name, last_name, username, password2, password1, avatar
   Output: Updated account information.
   Version: 1.0.0
   Reviewer:
"""
@login_required
@transaction.atomic
def account_settings(request):
    context = {}

    # Retrieve user information
    user = get_object_or_404(User, username__exact=request.user.username)
    profile = get_object_or_404(Profile, user=user)

    # Display the setting page with user's info if the method is not POST
    if request.method != 'POST':
        data = {}
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['email'] = user.email
        data['description'] = profile.description
        context['form'] = AccountSettingsForm(data)
        context['avatar'] = profile.avatar
        return render(request, 'accountsettings.html', context)

    # A list of errors encountered during the operation
    messages = []
    context['messages'] = messages

    # Use django form to handle input validation
    account_settings_form = AccountSettingsForm(request.POST, request.FILES)

    # Validate the form
    if not account_settings_form.is_valid():
        print("invalid content")
        context['form'] = AccountSettingsForm()
        return render(request, 'accountsettings.html', context)

    # If the user change anything, update it
    if 'first_name' in request.POST and request.POST['first_name']:
        user.first_name = request.POST['first_name']
    if 'last_name' in request.POST and request.POST['last_name']:
        user.last_name = request.POST['last_name']
    if 'email' in request.POST and request.POST['email']:
        user.email = request.POST['email']
    if 'password1' in request.POST and request.POST['password1']:
        user.set_password(request.POST['password1'])
    if 'description' in request.POST and request.POST['description']:
        profile.description = request.POST['description']
    if 'avatar' in request.FILES and request.FILES['avatar']:
        profile.avatar = account_settings_form.cleaned_data['avatar']

    # Save the changes
    profile.save()
    user.save()

    return redirect('user-station', request.user.username);


"""Name: like
   Author: Nguyen Dinh
   Description: Add the current track to a pool of liked songs
   Input: username, track id
   Output: add the track id to liked and return the next track from the id
        If there is no next track, return blank json
   Version: 1.0.0
   Reviewer:
"""
@login_required
@transaction.atomic
def like(request, id=''):
    context = {}
    song_to_like = get_object_or_404(Song, track_id=id)
    user_profile = get_object_or_404(Profile, user=request.user)
    user_profile.liked.add(song_to_like)
    user_profile.disliked.remove(song_to_like)
    user_profile.save()
    next_songs = Song.objects.order_by('?')

    # Return the first song that is not in liked or disliked
    for song in next_songs:
        if not song in user_profile.liked.all() and not song in user_profile.disliked.all():
            context['song'] = song
            return render(request, 'song.json', context, content_type='application/json')

    # return the file in JSON
    # return a random song if all of the songs are either liked or disliked
    print("all songs played, need to get new set of songs")
    next_song = next_songs.first()
    context['song'] = next_song
    return render(request, 'song.json', context, content_type='application/json')


"""Name: dislike
   Author: Nguyen Dinh
   Description: Remove the current track from a pool of liked songs
   Input: username, track id
   Output: add the track id to disliked and return the next track from the id
        If there is no next track, return blank json
   Version: 1.0.0
   Reviewer:
"""
@login_required
@transaction.atomic
def dislike(request, id=''):
    context = {}
    song_to_dislike = get_object_or_404(Song, track_id=id)
    user_profile = get_object_or_404(Profile, user=request.user)
    user_profile.liked.remove(song_to_dislike)
    user_profile.disliked.add(song_to_dislike)
    user_profile.save()
    next_songs = Song.objects.order_by('?')

    # Return the first song that is not in liked or disliked
    for song in next_songs:
        if not song in user_profile.liked.all() and not song in user_profile.disliked.all():
            context['song'] = song
            return render(request, 'song.json', context, content_type='application/json')

    # return the file in JSON
    # return a random song if all of the songs are either liked or disliked
    next_song = next_songs.first()

    context['song'] = next_song
    return render(request, 'song.json', context, content_type='application/json')


"""Name: get_avatar
   Author: Riley Rodenburg
   Description: Retrieve profile picture
   Input: username
   Output: return http response of picture
   Version: 1.0.0
   Reviewer:
"""
@login_required
def get_avatar(request, username=''):
    # to make sure that the user input the correct username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    # if user did not upload any image, raise a 404
    if not profile.avatar:
        raise Http404

    # send back the photo data to the browser
    # if no file found, raise a 404
    try:
        content_type = guess_type(profile.avatar.name)
        return HttpResponse(profile.avatar, content_type=content_type)
    except IOError:
        raise Http404


"""Name: next_user_song
   Author: Judy Mai & Riley Rodenburg
   Description: Retrieve and return the next song to play on user's station
   Input: username, track id
   Output: return a random next track of the user from the id
        If there is no next track, return blank json
   Version: 1.0.0
   Reviewer:
"""
@login_required
@transaction.atomic
def next_user_song(request, id=''):
    context = {}
    current_song = get_object_or_404(Song, track_id=id)
    user_profile = get_object_or_404(Profile, user=request.user)
    next_song = user_profile.liked.all().filter(id__gt=current_song.id).first()

    # end of playlist, reshuffle songs and choose new song.
    if(next_song is None): 
      next_song = user_profile.liked.order_by('?').first()


    context['song'] = next_song

    # Update song and current time to display in user's station
    update_user_song(user_profile, next_song)

    # return the file in JSON
    return render(request, 'song.json', context, content_type='application/json')


"""Name: prev_user_song
   Author: Riley Rodenburg
   Description: Retrieve and return the previous song to play on user's station
   Input: username, track id
   Output: return last played song.
        If there is no next track, return blank json
   Version: 1.0.0
   Reviewer:
"""
@login_required
@transaction.atomic
def prev_user_song(request, id=''):
    context = {}
    current_song = get_object_or_404(Song, track_id=id)
    user_profile = get_object_or_404(Profile, user=request.user)
    prev_song = user_profile.liked.all().filter(id__lt=current_song.id).order_by('-id').first()

    # end of playlist, reshuffle songs and choose new song.
    if(prev_song is None): 
      prev_song = user_profile.liked.order_by('?').first()

    context['song'] = prev_song

    # Update song and current time to display in user's station
    update_user_song(user_profile, prev_song)

    # return the file in JSON
    return render(request, 'song.json', context, content_type='application/json')


"""Name: play_user_song
   Author: Judy Mai
   Description: Retrieve and return the given song to play on user's station
   Input: username, track id
   Output: return the track from the id
        If there is no next track, return blank json
   Version: 1.0.0
   Reviewer:
"""
@login_required
@transaction.atomic
def play_user_song(request, id=''):
    context = {}

    user_profile = get_object_or_404(Profile, user=request.user)
    context['profile'] = user_profile

    requested_song = get_object_or_404(Song, track_id=id)
    context['song'] = requested_song

    # Update song and current time to display in user's station
    update_user_song(user_profile, requested_song)

    return render(request, 'song.json', context, content_type='application/json')


"""Name: remove_song
   Author: Riley Rodenburg
   Description: Remove song selected on mystation in like playlist
   Input: username, track id
   Output: return nothing
   Version: 1.0.0
   Reviewer:
"""
@login_required
@transaction.atomic
def remove_song(request, id=''):

    song_to_remove = get_object_or_404(Song, track_id=id)
    user_profile = get_object_or_404(Profile, user=request.user)
    user_profile.liked.remove(song_to_remove)
    user_profile.save()

    return HttpResponse('')


"""Name: token
   Author: Riley Rodenburg
   Description: Gather twilio crudentials.
   Input: username, track id
   Output: return nothing
   Version: 1.0.0
   Reviewer:
"""
@login_required
def token(request):
    device_id = request.GET.get('device', 'unknown')
    identity = request.GET.get('identity', 'guest').encode('utf-8')
    endpoint_id = "grumblr:{0}:{1}".format(device_id, identity)
    token = AccessToken(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_API_KEY,
                        settings.TWILIO_API_SECRET, identity)
    grant = IpMessagingGrant()
    grant.service_sid = settings.TWILIO_IPM_SERVICE_SID
    grant.endpoint_id = endpoint_id
    token.add_grant(grant)
    response = {'identity': identity, 'token': token.to_jwt()}
    return JsonResponse(response)


"""Name: favorite
   Author: Judy Mai
   Description: Follow the user if not already
   Input: username
   Output: n/a
   Version: 1.0.0
   Reviewer:
"""
@login_required
@transaction.atomic
def favorite(request, username):
    my_profile = get_object_or_404(Profile, user=request.user)
    user = get_object_or_404(User, username=username)

    # ignore self
    if username == request.user.username:
        return redirect('user-station', username)

    # check to make sure not already followed 
    already_favorited = my_profile.favorites.filter(username=username)
    if (already_favorited.count() == 0):
        my_profile.favorites.add(user)
        my_profile.save()

    return redirect('user-station', username)


"""Name: unfavorite
   Author: Judy Mai
   Description: Unfavorite the user if already favorited
   Input: username
   Output: n/a
   Version: 1.0.0
   Reviewer:
"""
@login_required
@transaction.atomic
def unfavorite(request, username):
    my_profile = get_object_or_404(Profile, user=request.user)
    user = get_object_or_404(User, username=username)

    # ignore self
    if username == request.user.username:
        return redirect('user-station', username)

    # check to make sure already followed 
    already_favorited = my_profile.favorites.filter(username=username)
    if (already_favorited.count() > 0):
        my_profile.favorites.remove(user)
        my_profile.save()

    return redirect('user-station', username)


"""Name: search_users
   Author: Nguyen Dinh
   Description: get and return currently logged in user
   Input: optional query for searching
   Output: a list of username, first name, last name, status, is followed by the current user
   Version: 1.0.0
   Reviewer:
"""
@login_required
def search_users(request, query=''):

    # Get all active sessions in the DB
    sessions = Session.objects.all()

    profile = get_object_or_404(Profile,user=request.user)
    uid_list = []
    users = []
    user = {}
    context = {}

    # Extract ids of logged in users
    for session in sessions:
        if session.expire_date >= timezone.now():
            data = session.get_decoded()
            uid_list.append(data.get('_auth_user_id', None))

    # Filter the result from db
    search_result = User.objects.filter(Q(username__istartswith=query)
                                        | Q(first_name__icontains=query)
                                        | Q(last_name__icontains=query)).exclude(username='admin')

    # Get a list of first name and last name of logged in users
    authenticated_users = search_result.filter(id__in=uid_list)
    for authenticated_user in authenticated_users:
        user['username'] = authenticated_user.username
        user['first_name'] = authenticated_user.first_name
        user['last_name'] = authenticated_user.last_name
        user['status'] = 'loggedin'

        # Check if the current active user is in request user's favorites
        if authenticated_user in profile.favorites.all():
            user['in_favorite'] = 'yes'
        else:
            user['in_favorite'] = 'no'

        # Check if the user is currently live or not
        profile_of_result = get_object_or_404(Profile, user=authenticated_user)
        if profile_of_result.status == 'Stopped':
            user['is_live'] = 'no'
        else:
            user['is_live'] = 'yes'

        users.append(user.copy())

    # Get a list of first name and last name of logged out users
    unauthenticated_users = search_result.exclude(id__in=uid_list)
    for unauthenticated_user in unauthenticated_users:
        user['username'] = unauthenticated_user.username
        user['first_name'] = unauthenticated_user.first_name
        user['last_name'] = unauthenticated_user.last_name
        user['status'] = 'loggedout'

        # Check if the current active user is in request user's favorites
        if unauthenticated_user in profile.favorites.all():
            user['in_favorite'] = 'yes'
        else:
            user['in_favorite'] = 'no'

        user['is_live'] = 'no'
        users.append(user.copy())

    context['users'] = users

    return render(request, 'users.json', context, content_type='application/json')


"""Name: get_favorites
   Author: Nguyen Dinh
   Description: return current favorites from user
   Input: n/a
   Output: rendered users.json
   Version: 1.0.0
   Reviewer:
"""
@login_required
def get_favorites(request):
    users = []
    user = {}
    context = {}
    profile = get_object_or_404(Profile, user=request.user)

    # Get a list of logged in user from session
    sessions = Session.objects.all()
    uid_list = []
    for session in sessions:
        if session.expire_date >= timezone.now():
            data = session.get_decoded()
            uid_list.append(data.get('_auth_user_id', None))
    authenticated_users = User.objects.filter(id__in=uid_list)

    for favorite in profile.favorites.all():
        user['username'] = favorite.username
        user['first_name'] = favorite.first_name
        user['last_name'] = favorite.last_name
        user['in_favorite'] = 'yes'
        if favorite in authenticated_users:
            user['status'] = 'loggedin'
            favorite_profile = get_object_or_404(Profile, user=favorite)
            if favorite_profile.status == 'Stopped':
                user['is_live'] = 'no'
            else:
                user['is_live'] = 'yes'
        else:
            user['status'] = 'loggedout'
            user['is_live'] = 'no'

        users.append(user.copy())

    context['users'] = users

    return render(request, 'users.json', context, content_type='application/json')


"""Name: sync_user_song
   Author: Nguyen Dinh
   Description: return current played song from username
   Input: username
   Output: song object and starting point
   Version: 1.0.0
   Reviewer:
"""
@login_required
def sync_user_song(request, username=''):
    context = {}

    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    # Get current song from user's profile and start_time to calculate start_play_time
    if profile.start_time and profile.song:
        current_start_time = (datetime.datetime.now() - profile.start_time.replace(tzinfo=None)).total_seconds() + profile.pause_duration
        current_song = profile.song
        context['current_start_time'] = current_start_time
        context['song'] = current_song
        context['status'] = profile.status

    return render(request, 'song.json', context, content_type='application/json')


"""Name: update_playing_status
   Author: Nguyen Dinh
   Description: return current played song from username
   Input: username
   Output: song object and starting point
   Version: 1.0.0
   Reviewer:
"""
@login_required
@transaction.atomic
def update_playing_status(request, status='', pause_duration='0'):
    profile = get_object_or_404(Profile, user=request.user)
    # If the inputs are validated, save them
    if status == 'Playing' \
            or status == 'Paused' \
            or status == 'Stopped':
        profile.status = status

        # Try to convert to float to make sure the input is a number
        try:
            val = float(pause_duration)
            if val >= 0:
                original_val = profile.pause_duration
                profile.pause_duration = original_val + val
            else:
                return HttpResponse('Invalid input')
        except ValueError:
            return HttpResponse('Invalid input')
    else:
        return HttpResponse('Invalid input')

    profile.save()
    return HttpResponse('Update completed: ' + profile.status)


"""Name: update_user_song
   Author: Nguyen Dinh
   Description: helper function to update the current song and
        start time in user's profile
   Input: profile, song
   Output: -
   Version: 1.0.0
   Reviewer:
"""
@transaction.atomic
def update_user_song(profile, song):
    profile.song = song
    profile.start_time = datetime.datetime.now()
    profile.pause_duration = 0
    profile.save()


"""Name: get_user_info
   Author: Riley Rodenburg
   Description: retrieve users first name, last name and avatar
   Input: username
   Output: -
   Version: 1.0.0
   Reviewer:
"""
@login_required
def get_user_info(request, username=''):
  context = {}
  user = get_object_or_404(User, username=username)
  profile = get_object_or_404(Profile, user=user)
  context['avatar'] = profile.avatar
  context['first_name'] = user.first_name
  context['last_name'] = user.last_name

  return render(request, 'usersinfo.json', context, content_type='application/json')


"""Name: get_listeners
   Author: Riley Rodenburg
   Description: retrieve users first name, last name and avatar
   Input: username
   Output: -
   Version: 1.0.0
   Reviewer:
"""
@login_required
def get_listeners(request, channel_id=''):
  if channel_id=='':
    raise Http404
  context = {}

  try:
      token = settings.TWILIO_AUTH_TOKEN
      client = TwilioIpMessagingClient(settings.TWILIO_ACCOUNT_SID, token)
      service = client.services.get(sid=settings.TWILIO_IPM_SERVICE_SID)
      channel = service.channels.get(sid=channel_id)
      members = []

      users = []
      user = {}
      for m in channel.members.list():
          members.append(m.identity)

          active_user = User.objects.filter(username__exact=m.identity).first()
          user['username'] = active_user.username
          user['first_name'] = active_user.first_name
          user['last_name'] = active_user.last_name
          users.append(user.copy())

      context['users'] = users
  except TwilioRestException:
      raise Http404

  return render(request, 'users.json', context, content_type='application/json')

 
"""Name: change_description
   Author: Judy Mai
   Description: change user's description to given description
   Input: request with description
   Output: -
   Version: 1.0.0
   Reviewer:
"""
@login_required
@transaction.atomic
def change_description(request):

    form = DescriptionForm(request.POST)
    if not form.is_valid():
        return HttpResponse("")

    else:
        description = form.cleaned_data['description']
        profile = get_object_or_404(Profile, user=request.user)
        profile.description = description
        profile.save()

        return HttpResponse(form.cleaned_data['description'])
    

