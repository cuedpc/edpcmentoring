from django.test import TestCase
from django.utils import timezone

from cuedmembers.models import Member
from mentoring.models import Relationship

from ..forms import ReportMentorMeetingForm

class ReportMentorMeetingFormTestCase(TestCase):
    fixtures = ['cuedmembers/test_users_and_members']

    def setUp(self):
        # Create an active mentoring relationship
        m1, m2 = Member.objects.active().all()[:2]
        self.relationship = Relationship(mentor=m1.user, mentee=m2.user)
        self.relationship.save()

    def test_valid_initial_data_is_valid(self):
        f = ReportMentorMeetingForm(
            {
                'mentee': self.relationship.mentee.id,
                'duration': 30, 'held_on': timezone.now(),
            },
            mentor=self.relationship.mentor)
        self.assertTrue(f.is_valid())

    def test_requires_held_on(self):
        f = ReportMentorMeetingForm(
            {
                'mentee': self.relationship.mentee.id,
                'duration': 30,
            },
            mentor=self.relationship.mentor)
        self.assertFalse(f.is_valid())

    def test_requires_duration(self):
        f = ReportMentorMeetingForm(
            {
                'mentee': self.relationship.mentee.id,
                'held_on': timezone.now(),
            },
            mentor=self.relationship.mentor)
        self.assertFalse(f.is_valid())

    def test_requires_mentee(self):
        f = ReportMentorMeetingForm(
            {
                'duration': 30, 'held_on': timezone.now(),
            },
            mentor=self.relationship.mentor)
        self.assertFalse(f.is_valid())

    def test_requires_mentor(self):
        f = ReportMentorMeetingForm(
            {
                'mentee': self.relationship.mentee.id,
                'duration': 30, 'held_on': timezone.now(),
            })
        self.assertFalse(f.is_valid())

    def test_requires_non_zero_duration(self):
        f = ReportMentorMeetingForm(
            {
                'mentee': self.relationship.mentee.id,
                'duration': 0, 'held_on': timezone.now(),
            },
            mentor=self.relationship.mentor)
        self.assertFalse(f.is_valid())

    def test_requires_positive_duration(self):
        f = ReportMentorMeetingForm(
            {
                'mentee': self.relationship.mentee.id,
                'duration': -1, 'held_on': timezone.now(),
            },
            mentor=self.relationship.mentor)
        self.assertFalse(f.is_valid())

    def test_meeting_must_be_uniqye(self):
        f = ReportMentorMeetingForm(
            {
                'mentee': self.relationship.mentee.id,
                'duration': 30, 'held_on': timezone.now(),
            },
            mentor=self.relationship.mentor)
        self.assertTrue(f.is_valid())
        f.save()

        f = ReportMentorMeetingForm(
            {
                'mentee': self.relationship.mentee.id,
                'duration': 30, 'held_on': timezone.now(),
            },
            mentor=self.relationship.mentor)
        self.assertFalse(f.is_valid())

