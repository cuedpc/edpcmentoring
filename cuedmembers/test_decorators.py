from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
import mock

from .decorators import member_required
from .middleware import MemberMiddleware
from .models import Member

class MemberRequiredTestCase(TestCase):
    fixtures = ['cuedmembers/test_users', 'cuedmembers/test_members']

    def setUp(self):
        self.factory = RequestFactory()

    def test_anonmous_user(self):
        func = mock.Mock()
        wrapped_func = member_required(func)
        request = self.make_get_request(AnonymousUser())
        response = wrapped_func(request)

        # The wrapped function should never be called
        self.assertFalse(func.called)

        # The response should be a redirect
        self.assertEqual(response.status_code, 302)

    def test_non_member(self):
        func = mock.Mock()
        wrapped_func = member_required(func)
        request = self.make_get_request(
            User.objects.filter(cued_member__isnull=True).first()
        )
        with self.assertRaises(PermissionDenied):
            wrapped_func(request)

    def test_inactive_member(self):
        func = mock.Mock()
        wrapped_func = member_required(func)
        request = self.make_get_request(
            Member.objects.inactive().first().user)
        with self.assertRaises(PermissionDenied):
            wrapped_func(request)

    def test_active_member(self):
        func = mock.Mock()
        wrapped_func = member_required(func)
        request = self.make_get_request(
            Member.objects.active().first().user)
        wrapped_func(request)

        # The wrapped function should be called
        self.assertTrue(func.called)

    def make_get_request(self, user, path='/'):
        """
        Return a request object for the given path with the specified user.

        """
        request = self.factory.get(path)
        request.user = user

        # Simulate middleware.
        MemberMiddleware().process_request(request)

        return request
