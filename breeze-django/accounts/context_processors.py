def user_role(request):
    user = request.user
    role = None
    if user.is_authenticated:
        # безопасно: user может не иметь profile (но у нас сигнал создаёт)
        role = getattr(user, 'profile', None)
        role = role.role if role else None
    return {
        'user_role': role,
        'is_manager': user.is_authenticated and (role == 'manager' or user.is_superuser),
    }
