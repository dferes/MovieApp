import os
from unittest import TestCase
from models import db, User, Follows, Movie, MovieList
from user_functions import signup, authenticate
from forms import UserLoginForm

os.environ['DATABASE_URL'] = "postgresql:///MovieBuddy_test"

from app import app, CURRENT_USER_KEY, do_login

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


# global_testuser = signup(
#     username="Guy",
#     email="guy@test.com",
#     password="password",
#     user_pic_url='https://i.redd.it/js2agifhb7xx.jpg')

# global_testuser.id = 1111

# db.session.add(global_testuser)
# db.session.commit()


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

    def test_user_profile_shows_user_details(self):
        with self.client as c:
            # form = UserLoginForm(formdata={username='testuser',password='testuser'})
            
            resp = c.get(f"/users/{self.testuser_id}")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("@testuser", str(resp.data))

    def test_show_following(self):
        self.setup_followers()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURRENT_USER_KEY] = self.testuser_id

            resp = c.get(f"/users/{self.testuser_id}/following")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@abc", str(resp.data))
            self.assertIn("@efg", str(resp.data))
            self.assertNotIn("@hij", str(resp.data))
            self.assertNotIn("@testing", str(resp.data))

    def test_show_followers(self):
        self.setup_followers()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURRENT_USER_KEY] = self.testuser_id

            resp = c.get(f"/users/{self.testuser_id}/followers")

            self.assertIn("@abc", str(resp.data))
            self.assertNotIn("@efg", str(resp.data))
            self.assertNotIn("@hij", str(resp.data))
            self.assertNotIn("@testing", str(resp.data))
            
    # def test_unauthorized_following_page_access(self):
    #     self.setup_followers()
    #     with self.client as c:

    #         resp = c.get(f"/users/{self.testuser_id}/following", follow_redirects=True)
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertNotIn("@abc", str(resp.data))
    #         self.assertIn("Access unauthorized", str(resp.data))

    # def test_unauthorized_followers_page_access(self):
    #     self.setup_followers()
    #     with self.client as c:

    #         resp = c.get(f"/users/{self.testuser_id}/followers", follow_redirects=True)
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertNotIn("@abc", str(resp.data))
    #         self.assertIn("Access unauthorized", str(resp.data))

 