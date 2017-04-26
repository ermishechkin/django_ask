from ask.models import Profile

def add_profile(request):
    if request.user.is_authenticated():
        request.profile = Profile.objects.filter(user = request.user).first()
    return []

class ProfileMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            request.profile = Profile.objects.filter(user = request.user).first()
        else:
            request.profile = None
