from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
import mock

from .decorators import staff_member_required
from .middleware import StaffMemberMiddleware
from .models import StaffMember

class StaffRequiredTestCase(TestCase):
    fixtures = ['test_staff_and_users']

    def setUp(self):
        self.factory = RequestFactory()
        self.non_staff_user = User.objects.filter(
            staffmember__isnull=True).first()
        self.active_staff_user = StaffMember.objects.active().first().user
        self.departed_staff_user = StaffMember.objects.filter(
            departed_on__isnull=False).first().user

    def test_anonmous_user(self):
        func = mock.Mock()
        wrapped_func = staff_member_required(func)
        request = self.make_get_request(AnonymousUser())
        response = wrapped_func(request)

        # The wrapped function should never be called
        self.assertFalse(func.called)

        # The response should be a redirect
        self.assertEqual(response.status_code, 302)

    def test_non_staff_user(self):
        func = mock.Mock()
        wrapped_func = staff_member_required(func)
        request = self.make_get_request(self.non_staff_user)
        with self.assertRaises(PermissionDenied):
            wrapped_func(request)

    def test_departed_staff_user(self):
        func = mock.Mock()
        wrapped_func = staff_member_required(func)
        request = self.make_get_request(self.departed_staff_user)
        with self.assertRaises(PermissionDenied):
            wrapped_func(request)

    def test_active_staff_user(self):
        func = mock.Mock()
        wrapped_func = staff_member_required(func)
        request = self.make_get_request(self.active_staff_user)
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
        StaffMemberMiddleware().process_request(request)

        return request
