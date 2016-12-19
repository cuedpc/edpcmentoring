from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from pinax.notifications.models import send

from mentoring.models import Relationship
from matching.models import Invitation

@receiver(post_save, sender=Relationship, dispatch_uid='relationship_create')
def relationship_post_save_handler(created, instance, **_):
    # Only notify if this is a new *active* relationship
    if not created: # or not instance.is_active:
        if instance.ended_on:
        # Send these if the relationship has ended
            send([instance.mentor], 'end_mentee', {'relationship': instance})
            send([instance.mentee], 'end_mentor', {'relationship': instance})
            
        return

# These will be sent via a cron on the autonag 
    if instance.is_active:
        send([instance.mentor], 'new_mentee', {'relationship': instance})
        send([instance.mentee], 'new_mentor', {'relationship': instance})
        return

## Send these if the relationship has ended
#    send([instance.mentor], 'end_mentee', {'relationship': instance})
#    send([instance.mentee], 'end_mentee', {'relationship': instance})


@receiver(post_save, sender=Invitation, dispatch_uid='invitation_create')
def invitation_post_save_handler(created, instance, **_):
    if created: 
        if not instance.mentor_response and instance.mentee_response == 'A':
        # Invite to Mentor 
            send([instance.mentor], 'invite_mentor', {'invitation': instance})
        if not instance.mentee_response and instance.mentor_response == 'A':
        # Invite to Mentee 
            send([instance.mentee], 'invite_mentee', {'invitation': instance})

    if not created:
        if instance.mentor_response == 'D' and instance.mentee_response == 'A':
        # Invite to Mentor declined notify mentee
            send([instance.mentee], 'mentor_declined', {'invitation': instance})
        if instance.mentee_response == 'D' and instance.mentor_response == 'A':
        # Invite to Mentee declined notify mentor
            send([instance.mentor], 'mentee_declined', {'invitation': instance})
            
    return




def create_notice_types(**_):
    if 'pinax.notifications' in settings.INSTALLED_APPS:
        from pinax.notifications.models import NoticeType
        print('Creating notices for autonag')
        NoticeType.create(
            'new_mentor', 'New mentor', 'you have a new mentor')
        NoticeType.create(
            'new_mentee', 'New mentee', 'you have a new mentee')
        NoticeType.create(
            'end_mentee', 'End mentee', 'A mentee relatiohip has ended')
        NoticeType.create(
            'end_mentor', 'End mentor', 'A mentor relatiohip has ended')
        NoticeType.create(
            'invite_mentor', 'Invite mentor', 'Invite a mentor to a relationship')
        NoticeType.create(
            'invite_mentee', 'Invite mentee', 'Invite a mentee to a relationship')
        NoticeType.create(
            'mentor_declined', 'Mentor declined invite', 'Invite declined by mentor')
        NoticeType.create(
            'mentee_declined', 'Mentee declined invite', 'Invite declined by mentee')
    else:
        print('Skipping creation of NoticeTypes as notification app not found')

