from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        print("email", email)
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        print("usermanager")
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email,
                                username=username,
                                password=password,
                                )

        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserInfo(AbstractBaseUser):
    username = models.CharField(verbose_name="用户名", max_length=40, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(verbose_name="邮箱", max_length=255)
    # nickname = models.CharField(max_length=64, null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # 除了上述必填项还需要什么必填项

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser


class ResetPasswordCode(models.Model):
    user = models.ForeignKey(to="UserInfo", verbose_name="用户", on_delete=models.CASCADE)
    code = models.CharField(verbose_name="随机验证码", max_length=128)
    created = models.DateTimeField(verbose_name="发送时间", auto_now_add=True)
