from django.db import models
from account.models import UserInfo


# Create your models here.


class Menu(models.Model):
    """
    一级菜单
    """
    title = models.CharField(max_length=32, unique=True, verbose_name='标题')
    icon = models.CharField(max_length=32, verbose_name='图标', null=True, blank=True)
    weight = models.IntegerField(default=10, verbose_name='权重')

    # is_single = models.BooleanField(verbose_name="是否是单独菜单",default=False)

    # url = models.CharField(max_length=32, verbose_name='菜单url', null=True, blank=True)

    class Meta:
        verbose_name = '菜单表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    有关联Menu的是二级菜单
    没有关联Menu的不是二级菜单，是不可以做菜单的权限


    """
    title = models.CharField(max_length=32, verbose_name='标题')
    url = models.CharField(max_length=32, verbose_name='权限')
    menu = models.ForeignKey('Menu', null=True, blank=True, verbose_name='菜单', on_delete=models.CASCADE)
    is_menu = models.BooleanField(default=False, verbose_name='是否是菜单')
    parent = models.ForeignKey('Permission', null=True, blank=True, verbose_name='父权限', on_delete=models.CASCADE)
    alias = models.CharField(max_length=32, null=True, blank=True, unique=True, verbose_name='URL别名')

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Role(models.Model):
    name = models.CharField(max_length=32, verbose_name='角色名称')
    permissions = models.ManyToManyField(to='Permission', verbose_name='角色所拥有的权限', blank=True)
    user = models.ManyToManyField(to=UserInfo, related_name='roles', verbose_name="用户")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = verbose_name
