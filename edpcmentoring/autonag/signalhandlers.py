from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from pinax.notifications.models import send

from mentoring.models import Relationship

@receiver(post_save, sender=Relationship, dispatch_uid='relationship_create')
def relationship_post_save_handler(created, instance, **_):
    # Only notify if this is a new *active* relationship
    if not created or not instance.is_active:
        return

    send([instance.mentor], 'new_mentee', {'relationship': instance})
    send([instance.mentee], 'new_mentor', {'relationship': instance})

def create_notice_types(**_):
    if 'pinax.notifications' in settings.INSTALLED_APPS:
        from pinax.notifications.models import NoticeType
        print('Creating notices for autonag')
        NoticeType.create(
            'new_mentor', 'New mentor', 'you have a new mentor')
        NoticeType.create(
            'new_mentee', 'New mentee', 'you have a new mentee')
    else:
        print('Skipping creation of NoticeTypes as notification app not found')
