

def get_user_agency(user):
    if hasattr(user, 'agency_profile'):
        return user.agency_profile
    elif hasattr(user, 'agent_profile'):
        return user.agent_profile.agency
    return None
