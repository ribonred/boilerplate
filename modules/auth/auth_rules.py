

def must_verified_email(user) -> bool:
    return user.is_active and user.email and user.email_verified
