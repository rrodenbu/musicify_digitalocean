from django.test import TestCase, Client
from meradio.models import *
import datetime

class MeRadioModelsTest(TestCase):

	#Tests creating a new song and adding to database.
	def test_get_songs(self):
		self.assertTrue(Song.objects.all().count() == 0)
		new_song = Song(track_id='track id',
                        name='song name',
                        length=1000,  # seconds
                        album='album name',
                        cover='album-artworks/default/musicify-icon.png',
                        artist='song artist',
                        preview='song preview')
		new_song.save()
		self.assertTrue(Song.objects.all().count() == 1)
		self.assertTrue(Song.objects.filter(track_id__contains ='track id'))
		self.assertTrue(Song.objects.filter(name__contains ='song name'))
		self.assertTrue(Song.objects.filter(length__contains =1000))
		self.assertTrue(Song.objects.filter(album__contains ='album name'))
		self.assertTrue(Song.objects.filter(cover__contains ='album-artworks/default/musicify-icon.png'))
		self.assertTrue(Song.objects.filter(artist__contains ='song artist'))
		self.assertTrue(Song.objects.filter(preview__contains ='song preview'))


	#Tests creating a new user and adding to database.
	def test_register(self):
		self.assertTrue(User.objects.all().count() == 0)
		new_user = User.objects.create_user(username='username',
                                        	password='password',
                                        	first_name='first name',
                                        	last_name='last name',
                                        	email='email@gmail.com')
		new_user.save()
		self.assertTrue(User.objects.all().count() == 1)
		self.assertTrue(User.objects.filter(username__contains ='username'))
		self.assertTrue(User.objects.filter(password__contains =''))
		self.assertTrue(User.objects.filter(first_name__contains ='first name'))
		self.assertTrue(User.objects.filter(last_name__contains ='last name'))
		self.assertTrue(User.objects.filter(email__contains ='email@gmail.com'))


	#Tests creating a new profile and adding to database.
	def test_profile(self):

		self.assertTrue(User.objects.all().count() == 0)
		new_user = User.objects.create_user(username='username',
                                        	password='password',
                                        	first_name='first name',
                                        	last_name='last name',
                                        	email='email@gmail.com')
		new_user.save()
		self.assertTrue(User.objects.all().count() == 1)

		self.assertTrue(Song.objects.all().count() == 0)
		new_song = Song(track_id='track id',
                        name='song name',
                        length=1000,  # seconds
                        album='album name',
                        cover='album-artworks/default/musicify-icon.png',
                        artist='song artist',
                        preview='song preview')
		new_song.save()
		self.assertTrue(Song.objects.all().count() == 1)

		self.assertTrue(Profile.objects.all().count() == 0)
		new_profile = Profile(user=new_user,
							  song=new_song,
							  start_time=datetime.datetime.now(),
							  # favorites='',
							  description='description',
							  status='status',
							  pause_duration='3.2',
							  # liked='',
							  # disliked='',
							  token='token',
							  password_temp='temporary password',
							  preferences='preferences',
							  avatar='profile-photos/default/musicify-icon.png')
		new_profile.save()
		self.assertTrue(Profile.objects.all().count() == 1)
		self.assertTrue(Profile.objects.filter(description__contains='description'))
		self.assertTrue(Profile.objects.filter(status__contains='status'))
		self.assertTrue(Profile.objects.filter(pause_duration__contains='3.2'))
		self.assertTrue(Profile.objects.filter(token__contains='token'))
		self.assertTrue(Profile.objects.filter(password_temp__contains='temporary password'))
		self.assertTrue(Profile.objects.filter(preferences__contains='preferences'))
		self.assertTrue(Profile.objects.filter(avatar__contains='profile-photos/default/musicify-icon.png'))


class TodoListTest(TestCase):

	fixtures = ['sample_data']

	def test_home_page(self):
		client = Client()       # results in an HTTP 200 (OK) response.
		response = client.get('/musicify/')
		self.assertEqual(response.status_code, 200)

	def test_explore(self):
		client = Client()
		response = client.get('/musicify/explore/')
		self.assertNotEqual(response.content, '{}')

	def test_get_recommendations(self):
		client = Client()
		response = client.get('/musicify/get-recommendations/')
		self.assertNotEqual(response.content, '{}')

	def test_user_station(self):
		client = Client()
		response = client.get('/musicify/user-station/rrodenbu')
		self.assertNotEqual(response.content, '{}') 

	def test_find_stations(self):
		client = Client()
		response = client.get('/musicify/find-stations/')
		self.assertEqual(response.status_code, 302) # URL Redirect

	def test_account_settings(self):
		client = Client()
		response = client.get('/musicify/account_settings/')
		print response.content
		self.assertEqual(response.status_code, 302) # URL Redirect

	def test_like(self):
		client = Client()
		response = client.get('/musicify/like/track_id')
		self.assertNotEqual(response.content, '{}') 

	def test_dislike(self):
		client = Client()
		response = client.get('/musicify/dislike/track_id')
		self.assertNotEqual(response.content, '{}')

	def test_get_avatar(self):
		client = Client()
		response = client.get('/musicify/get-avatar/username')
		self.assertNotEqual(response.content, '{}')

	def test_next_user_song(self):
		client = Client()
		response = client.get('/musicify/next-user-song/track_id')
		self.assertNotEqual(response.content, '{}')

	def test_prev_user_song(self):
		client = Client()
		response = client.get('/musicify/next-prev-song/track_id')
		self.assertNotEqual(response.content, '{}')

	def test_play_user_song(self):
		client = Client()
		response = client.get('/musicify/play_user_song/track_id')
		self.assertNotEqual(response.content, '{}')

	def test_remove_song(self):
		client = Client()
		response = client.get('/musicify/remove_song/track_id')
		self.assertEqual(response.status_code, 301) # Blank URL Redirect

	def test_favorite(self):
		client = Client()
		response = client.get('/musicify/favorite/username')
		print response.content
		self.assertEqual(response.status_code, 301) # URL Redirect

	def test_unfavorite(self):
		client = Client()
		response = client.get('/musicify/unfavorite/username')
		print response.content
		self.assertEqual(response.status_code, 301) # URL Redirect

	def test_search_users(self):
		client = Client()
		response = client.get('/musicify/search_users/query')
		self.assertNotEqual(response.content, '{}')







		


