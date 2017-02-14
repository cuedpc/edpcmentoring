Notifying and reminding users
=============================

The :py:mod:`autonag` application takes care of notifying users of events
they should be aware of and reminding them of tasks they have yet to complete.

.. automodule:: autonag
    :members:
    
Configuring emails to be sent (rather than logged in the EMAIL LOG: E-mails table)
---------------------------------------------------------------------------------

In the settings.py file removes comments from ::

    #PINAX_NOTIFICATIONS_BACKENDS=[("email", "pinax.notifications.backends.email.EmailBackend"),]


Where are the notification configured and how are they triggered?
-----------------------------------------------------------------

On startup autonag/signalhandlers.py will create and load the notice types available to the application::

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
            ...
        else:
            print('Skipping creation of NoticeTypes as notification app not found')

The notificaton system then expects to find templates for each message in edpcmentoring/templates/pinax/notifications eg::

    edpcmentoring/templates/pinax/notifications/new_mentor/short.txt
    edpcmentoring/templates/pinax/notifications/new_mentor/full.txt
    
**short.txt** is used for the subject of the message, **full.txt** contains the content.

Messages are sent to users by calling send(<user>,<NoticeType>,<dictoinary>)::

    send([instance.relationship.mentor], 'new_meeting', {'relationship': instance.relationship})
    send([instance.relationship.mentee], 'new_meeting', {'relationship': instance.relationship})

Where the dictionary can be accessed in the message templates (short.txt,full.txt)

The send commands are to be called in autonag/signalhanlders.py during interception of event signals, eg a new meeting was registered; send summary of all meeting to mentee and mentor::

    
    @receiver(post_save, sender=Meeting, dispatch_uid='meeting_create')
    def meeting_post_save_handler(created, instance, **_):
        ''' A new meeting has been registered 
        '''
        if created: 
            send([instance.relationship.mentor], 'new_meeting', {'relationship': instance.relationship})
            send([instance.relationship.mentee], 'new_meeting', {'relationship': instance.relationship})

        return


    
