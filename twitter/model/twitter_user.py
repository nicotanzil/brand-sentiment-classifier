class TwitterUser:
    def __init__(self, user):
        self.user = user

    def get_dict_data(self):
        data = {
            "screen_name": self.user.screen_name,
            "profile_image_url": self.user.profile_image_url
        }
        return data