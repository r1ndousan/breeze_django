def user_role_flags(request):
    user = request.user
    is_manager = False
    is_client = False
    if user.is_authenticated:
        try:
            role = getattr(user, 'profile', None) and user.profile.role
        except Exception:
            role = None
        is_manager = user.is_superuser or (role == 'manager')
        is_client = (role == 'client') or (not user.is_superuser and role != 'manager')
    return {
        'is_manager': is_manager,
        'is_client': is_client,
    }
