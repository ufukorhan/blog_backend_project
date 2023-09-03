from django.contrib.auth.models import User

class UserService(object):
    def create_user(self, username: str, password: str):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            instance: User = User.objects.create_user(username=username, password=password)
            return instance

    def update_user(self, instance, **fields):
        for key, value in fields.items():
            setattr(instance, key, value)
            instance.save()
        return instance        
