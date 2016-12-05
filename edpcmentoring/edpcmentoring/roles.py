#Configure the roles used by the application:

from rolepermissions.roles import AbstractUserRole


class MatchMaker(AbstractUserRole):
    '''
    Note the role is referenced in string snake case match_maker
    '''
    available_permissions = {
        'add_invitation': True,
        'update_invitation' : True,
        'make_matches' : True, # attempt to shoe horn in a role
    }


