"""
Context processors for foodify_project
"""
from django.conf import settings


def settings_context(request):
    """
    Make certain settings available to all templates
    """
    return {
        'GEOAPIFY_API_KEY': settings.GEOAPIFY_API_KEY,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    }
