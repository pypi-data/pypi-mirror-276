from .getMe import GetMe
from .getUserProfilePhotos import GetUserProfilePhotos

class User(GetMe, GetUserProfilePhotos):
    pass
