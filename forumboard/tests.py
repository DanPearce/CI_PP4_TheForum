"""
Tests for the forumboard app: pages, sign-in requirements and who may change what.
Run with:  SECRET_KEY=test python manage.py test
"""
from unittest import mock

import requests
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Comment, ForumBoard, ForumPost


def make_data():
    owner = User.objects.create_user('owner', 'owner@example.com', 'Sup3r-secret-pw')
    other = User.objects.create_user('other', 'other@example.com', 'Sup3r-secret-pw')
    board = ForumBoard.objects.create(name='Tech', slug='tech', about='Tech talk', approved_board=True)
    post = ForumPost.objects.create(forum_board=board, post_title='Hello world', slug='tech-hello-world',
                                    creator=owner, post_detail='First post')
    return owner, other, board, post


class PublicPageTests(TestCase):
    def setUp(self):
        self.owner, self.other, self.board, self.post = make_data()

    @mock.patch('forumboard.views.requests.get')
    def test_home_shows_headlines(self, get):
        get.return_value.json.return_value = {'articles': [
            {'title': 'Big news today', 'url': 'https://example.com/a', 'urlToImage': None,
             'description': 'x', 'publishedAt': '2026-01-01T00:00:00Z', 'source': {'name': 'S'}}]}
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Big news today')

    @mock.patch('forumboard.views.requests.get', side_effect=requests.ConnectionError)
    def test_home_still_loads_when_the_news_service_is_down(self, get):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello world')

    @mock.patch('forumboard.views.requests.get')
    def test_home_still_loads_when_the_news_service_returns_an_error(self, get):
        get.return_value.json.return_value = {'status': 'error', 'code': 'apiKeyInvalid'}
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)

    def test_boards_and_posts_are_public(self):
        for url in (reverse('all_boards'), reverse('board_detail', args=['tech']),
                    reverse('post_detail', args=['tech-hello-world']), reverse('account_login'),
                    reverse('account_signup'), reverse('contact')):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_unknown_board_and_post_are_404(self):
        self.assertEqual(self.client.get('/board/nope').status_code, 404)
        self.assertEqual(self.client.get('/nope-nope').status_code, 404)


class SignInRequiredTests(TestCase):
    """Visitors who are not signed in are sent to the login page instead of getting an error."""

    def setUp(self):
        self.owner, self.other, self.board, self.post = make_data()

    def assertRedirectsToLogin(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].startswith(reverse('account_login')))

    def test_like_follow_comment_add_post_add_board_edit_delete(self):
        self.assertRedirectsToLogin(self.client.post(reverse('post_like', args=['tech-hello-world'])))
        self.assertRedirectsToLogin(self.client.post(reverse('board_follow', args=['tech'])))
        self.assertRedirectsToLogin(self.client.post(reverse('post_detail', args=['tech-hello-world']),
                                                     {'body': 'hi'}))
        self.assertRedirectsToLogin(self.client.get(reverse('add_post', args=['Tech'])))
        self.assertRedirectsToLogin(self.client.get(reverse('add_board')))
        self.assertRedirectsToLogin(self.client.post(reverse('edit_post', args=[self.post.id])))
        self.assertRedirectsToLogin(self.client.get(reverse('delete_post', args=[self.post.id])))
        self.assertTrue(ForumPost.objects.filter(id=self.post.id).exists())
        self.assertEqual(Comment.objects.count(), 0)


class SignedInTests(TestCase):
    def setUp(self):
        self.owner, self.other, self.board, self.post = make_data()

    def test_login_with_username_and_password(self):
        response = self.client.post(reverse('account_login'), {'login': 'owner', 'password': 'Sup3r-secret-pw'})
        self.assertRedirects(response, '/', fetch_redirect_response=False)
        self.assertIn('_auth_user_id', self.client.session)

    def test_wrong_password_does_not_log_in(self):
        response = self.client.post(reverse('account_login'), {'login': 'owner', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_sign_up_creates_an_account(self):
        response = self.client.post(reverse('account_signup'), {
            'username': 'newbie', 'email': 'newbie@example.com',
            'password1': 'An0ther-g00d-pw!', 'password2': 'An0ther-g00d-pw!'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newbie').exists())

    def test_like_toggles(self):
        self.client.force_login(self.other)
        url = reverse('post_like', args=['tech-hello-world'])
        self.client.post(url)
        self.assertEqual(self.post.likes.count(), 1)
        self.client.post(url)
        self.assertEqual(self.post.likes.count(), 0)

    def test_follow_toggles(self):
        self.client.force_login(self.other)
        url = reverse('board_follow', args=['tech'])
        self.client.post(url)
        self.assertEqual(self.board.followers.count(), 1)
        self.client.post(url)
        self.assertEqual(self.board.followers.count(), 0)

    def test_comment_is_saved_for_the_signed_in_user(self):
        self.client.force_login(self.other)
        response = self.client.post(reverse('post_detail', args=['tech-hello-world']), {'body': 'Nice one'})
        self.assertEqual(response.status_code, 200)
        comment = Comment.objects.get()
        self.assertEqual((comment.body, comment.creator), ('Nice one', self.other))

    def test_invalid_comment_shows_an_error_not_a_crash(self):
        self.client.force_login(self.other)
        response = self.client.post(reverse('post_detail', args=['tech-hello-world']), {'body': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)

    def test_only_the_creator_can_delete_a_post(self):
        self.client.force_login(self.other)
        self.client.get(reverse('delete_post', args=[self.post.id]))
        self.assertTrue(ForumPost.objects.filter(id=self.post.id).exists())
        self.client.force_login(self.owner)
        self.client.get(reverse('delete_post', args=[self.post.id]))
        self.assertFalse(ForumPost.objects.filter(id=self.post.id).exists())

    def test_only_the_creator_can_edit_a_post(self):
        self.client.force_login(self.other)
        self.client.post(reverse('edit_post', args=[self.post.id]), {
            'post_title': 'Hacked', 'post_detail': 'changed', 'excerpt': 'x'})
        self.post.refresh_from_db()
        self.assertEqual(self.post.post_title, 'Hello world')
