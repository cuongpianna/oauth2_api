from app.extensions import ma
from app.user.models import UserModel


class UserSchema(ma.ModelSchema):

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)


