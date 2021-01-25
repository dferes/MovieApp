import os
from unittest import TestCase
from models import db, User, Follows, Movie, MovieList
from user_functions import signup, authenticate
from forms import UserLoginForm
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
        list1= MovieList(owner=self.testuser_id, 
            title='List 1', 
            description='My first list',
            list_image_url='https://us.v-cdn.net/5020761/uploads/editor/dd/mr3u75prp4g56.jpg')
        
        self.movie_list1_id = 998
        list1.id = self.movie_list1_id

        list2= MovieList(owner=self.testuser_id, 
            title='List 2', 
            description='My second list',
            list_image_url='https://doublefeature.fm/images/covers/the-matrix.jpg')
        
        self.movie_list2_id = 999
        list2.id = self.movie_list2_id

        db.session.add_all([list1, list2])
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


    def test_show_details_of_specific_movie_list(self):
        self.setup_movie_lists()
        resp = self.retrieve_get_response('users', f"/lists/{self.movie_list1_id}/details", self.testuser_id)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('List 1', str(resp.data))
        self.assertIn('My first list', str(resp.data))
        self.assertIn('Delete', str(resp.data))
        self.assertIn('Edit', str(resp.data))
        self.assertIn('@testuser', str(resp.data))
