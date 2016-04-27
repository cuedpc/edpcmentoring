from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
import mock

from ..decorators import member_required
from ..models import Member

class MemberRequiredTestCase(TestCase):
    fixtures = ['cuedmembers/test_users_and_members']

    def setUp(self):
        self.factory = RequestFactory()
        self.mock_view = mock.Mock()
        self.mock_view.__name__ = 'mock_view' # Reqd. for Py <3
        self.wrapped_mock_view = member_required(self.mock_view)

    def test_anonmous_user(self):
        request = self.make_get_request(AnonymousUser())
        response = self.wrapped_mock_view(request)

        # The wrapped function should never be called
        self.assertFalse(self.mock_view.called)

        # The response should be a redirect
        self.assertEqual(response.status_code, 302)

    def test_non_member(self):
        request = self.make_get_request(
            User.objects.filter(cued_member__isnull=True).first()
        )
        with self.assertRaises(PermissionDenied):
            self.wrapped_mock_view(request)

    def test_inactive_member(self):
        request = self.make_get_request(
            Member.objects.inactive().first().user)
        with self.assertRaises(PermissionDenied):
            self.wrapped_mock_view(request)

    def test_active_member(self):
        request = self.make_get_request(
            Member.objects.active().first().user)
        self.wrapped_mock_view(request)

        # The wrapped function should be called
        self.assertTrue(self.mock_view.called)

    def make_get_request(self, user, path='/'):
        """
        Return a request object for the given path with the specified user.

        """
        request = self.factory.get(path)
        request.user = user
        return request
