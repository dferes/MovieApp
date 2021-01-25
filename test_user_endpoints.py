import os
from unittest import TestCase
from models import db, User, Follows, Movie, MovieList
from user_functions import signup, authenticate
from forms import UserLoginForm, NewUserForm
from app import app, CURRENT_USER_KEY

os.environ['DATABASE_URL'] = "postgresql:///movie_buddy_test"

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):

    def setUp(self):

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = signup(username="testuser",
            email="test@test.com",
            password="testuser",
            user_pic_url='https://i.redd.it/js2agifhb7xx.jpg')
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        self.u1 = signup("abc", "test1@test.com", "password", None)
        self.u1_id = 778
        self.u1.id = self.u1_id
        
        self.u2 = signup("efg", "test2@test.com", "password", None)
        self.u2_id = 884
        self.u2.id = self.u2_id
        
        self.u3 = signup("hij", "test3@test.com", "password", None)
        self.u3_id = 42
        self.u3.id = self.u3_id

        self.u4 = signup("testing", "test4@test.com", "password", None)

        db.session.add_all([self.testuser, self.u1, self.u2, self.u3, self.u4])
        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
    
    def setup_followers(self):
        f1 = Follows(following_id=self.u1_id, followed_by_id=self.testuser_id)
        f2 = Follows(following_id=self.u2_id, followed_by_id=self.testuser_id)
        f3 = Follows(following_id=self.testuser_id, followed_by_id=self.u1_id)

        db.session.add_all([f1,f2,f3])
        db.session.commit()

    def setup_movie_lists(self):
        self.movie_list1= MovieList(owner=self.testuser_id, 
            title='List 1', 
            description='My first list',
            list_image_url='https://us.v-cdn.net/5020761/uploads/editor/dd/mr3u75prp4g56.jpg')
        
        self.movie_list1_id = 998
        self.movie_list1.id = self.movie_list1_id

        self.movie_list2= MovieList(owner=self.testuser_id, 
            title='List 2', 
            description='My second list',
            list_image_url='https://doublefeature.fm/images/covers/the-matrix.jpg')
        
        self.movie_list2_id = 999
        self.movie_list2.id = self.movie_list2_id

        db.session.add_all([self.movie_list1, self.movie_list2])
        db.session.commit()

    def retrieve_get_response(self, base, url, this_testuser_id, other_testuser_id=None, use_id_in_query=True):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURRENT_USER_KEY] = this_testuser_id
            
            if use_id_in_query:      
                if other_testuser_id:
                    return c.get(f"/{base}/{other_testuser_id}{url}") 
                
                return c.get(f"/{base}/{this_testuser_id}{url}")
            
            return c.get(f"/{base}{url}")

    def retrieve_post_request(self, data, url):
        with self.client as c:
            return c.post(url, data=data, follow_redirects=True)

    def test_this_user_profile_shows_user_details(self):
        resp = self.retrieve_get_response('users', '',  self.testuser_id)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("@testuser", str(resp.data))
        self.assertIn('Edit Profile', str(resp.data))
        self.assertIn('Delete Profile', str(resp.data))

    def test_other_user_profile_shows_their_details(self):
        resp = self.retrieve_get_response('users', '', self.testuser_id , self.u2_id)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('@efg', str(resp.data))
        self.assertIn('Follow', str(resp.data))
        self.assertNotIn('Edit Profile', str(resp.data))
        self.assertNotIn('Delete Profile', str(resp.data))

    def test_users_following_page_shows_following(self):
        self.setup_followers()
        resp = self.retrieve_get_response('users', '/following', self.testuser_id)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("@abc", str(resp.data))
        self.assertIn("@efg", str(resp.data))
        self.assertNotIn("@hij", str(resp.data))
        self.assertNotIn("@testing", str(resp.data))

    def test_users_followers_page_shows_all_followers(self):
        self.setup_followers()
        resp = self.retrieve_get_response('users', '/followers', self.testuser_id)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("@abc", str(resp.data))
        self.assertNotIn("@efg", str(resp.data))
        self.assertNotIn("@hij", str(resp.data))
        self.assertNotIn("@testing", str(resp.data))

    def test_users_show_movie_list_page_shows_all_movie_lists(self):
        self.setup_movie_lists()
        resp = self.retrieve_get_response('users', '/show-lists', self.testuser_id)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('My first list', str(resp.data))
        self.assertIn('My second list', str(resp.data))
        self.assertIn('Delete', str(resp.data))
        self.assertIn('Edit', str(resp.data))

    def test_get_new_list_form(self):
        resp = self.retrieve_get_response('users', '/new-list', self.testuser_id, use_id_in_query=False)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("get started!", str(resp.data))
        self.assertIn('Make', str(resp.data))
        self.assertIn('List Name', str(resp.data))
        self.assertIn('Description', str(resp.data))
        self.assertIn('List Image', str(resp.data))

    def test_get_edit_user_form(self):
        resp = self.retrieve_get_response('users', '/edit-profile', self.testuser_id)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Make some updates', str(resp.data))
        self.assertIn('Username', str(resp.data))
        self.assertIn('E-mail', str(resp.data))
        self.assertIn('Image URL', str(resp.data))
        self.assertIn('Edit this user!', str(resp.data))

    def test_show_details_of_specific_movie_list(self):
        self.setup_movie_lists()
        resp = self.retrieve_get_response('users', f"/lists/{self.movie_list1_id}/details", self.testuser_id)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('List 1', str(resp.data))
        self.assertIn('My first list', str(resp.data))
        self.assertIn('Delete', str(resp.data))
        self.assertIn('Edit', str(resp.data))
        self.assertIn('@testuser', str(resp.data))

    def test_get_edit_movie_list_form(self):
        self.setup_movie_lists()
        resp = self.retrieve_get_response('users', f"/lists/{self.movie_list1_id}/edit", 
            self.testuser_id, 
            self.testuser_id, use_id_in_query=False)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('make some changes', str(resp.data))
        self.assertIn('List Title', str(resp.data))
        self.assertIn('Description', str(resp.data))
        self.assertIn('List Image', str(resp.data))
        self.assertIn('Update', str(resp.data))

    def test_signup_form_post(self):
        data = {
            'username': 'userGuy',
            'email': 'userGuy@gmail.com',
            'password': 'password1',
            'user_pic_url': None
        }
        
        resp = self.retrieve_post_request(data, '/signup')

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Welcome to MovieBuddy, userGuy', str(resp.data))
        self.assertIn('@userGuy', str(resp.data))
        self.assertIn('None', str(resp.data))
        self.assertIn('Edit Profile', str(resp.data))
        
    def test_edit_user_form_post(self):
        self.retrieve_get_response('users', '',  self.testuser_id)

        data = {
            'username': 'dferes',
            'email': 'dferes23@gmail.com',
            'bio': 'This is my bio',
            'password': 'testuser'
        }
        resp = self.retrieve_post_request(data, f"/users/{self.testuser_id}/edit-profile")

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Your account has been updated.', str(resp.data))
        self.assertIn('@dferes', str(resp.data))
        self.assertIn('This is my bio', str(resp.data))

    def test_add_new_movie_list_form_post(self):
        self.retrieve_get_response('users', '',  self.testuser_id)
        data = {
            'title': 'Old Scary Movies',
            'description': 'old scary movies from the 80s',
            'list_image_url': 'https://doublefeature.fm/images/covers/the-matrix.jpg'
        }
        resp = self.retrieve_post_request(data, '/users/new-list')

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Old Scary Movies successfully created', str(resp.data))
        self.assertIn('old scary movies from the 80s', str(resp.data))

    def test_add_new_followed_user_to_this_users_followed_users(self):
        self.retrieve_get_response('users', '',  self.testuser_id)

        resp = self.retrieve_post_request(None, f"/users/follow/{self.u3_id}")

        self.assertEqual(resp.status_code, 200)
        self.assertIn('@hij', str(resp.data))
    
    def test_remove_followed_user_from_this_users_followed_users(self):
        self.setup_followers()
        self.retrieve_get_response('users', '',  self.testuser_id)

        resp = self.retrieve_post_request(None, f"/users/stop-following/{self.u2_id}")

        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('@hij', str(resp.data))
    
    def test_edit_movie_list_form_post(self):
        self.retrieve_get_response('users', '',  self.testuser_id)
        self.setup_movie_lists()

        data = {
            'title': 'Edited List Title',
            'description': 'Edited list description'
        }
        resp = self.retrieve_post_request(data, f"/users/lists/{self.movie_list1_id}/edit")

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Edited List Title', str(resp.data))
        self.assertIn('Edited list description', str(resp.data))

    # def test_add_new_movie_to_existing_movie_list_(self):
    #     self.retrieve_get_response('users', '',  self.testuser_id)
    #     self.setup_movie_lists()

    # def test_delete_user_movie_list_removes_list_from_movie_lists_page(self):

    # def test_remove_movie_from_existing_movie_list(self):

    # def test_delete_user(self):

