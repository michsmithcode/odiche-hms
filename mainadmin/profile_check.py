def check_profile_complete(profile):
    if hasattr(profile, "is_profile_complete"):
        return profile.is_profile_complete
    return False
