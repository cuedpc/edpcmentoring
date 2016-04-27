"""
Specialised crispy form layout objects.

"""

from crispy_forms.layout import Submit as _Submit

class Submit(_Submit):
    """
    A version of the standard crispy forms Submit layout which sets the
    appropriate CSS classes for project light.

    """
    def __init__(self, *args, **kwargs):
        classes = []
        if 'css_class' in kwargs:
            classes.append(kwargs['css_class'])
        classes.append('campl-btn')

        if kwargs.get('is_primary', True):
            classes.append('campl-primary-cta')

        kwargs['css_class'] = ' '.join(classes)

        super(Submit, self).__init__(*args, **kwargs)
