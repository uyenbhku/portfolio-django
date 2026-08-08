from .models import Profile


def site_profile(request):
    """Expose the primary profile across all templates."""
    return {'site_profile': Profile.objects.first()}
