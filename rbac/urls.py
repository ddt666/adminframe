from django.urls import path, re_path
from . import views

app_name = "rbac"

urlpatterns = [
    path('role/list', views.RoleListView.as_view(), name="role_list"),

    path('menu_list', views.MenuView.as_view(), name="menu_list"),
    path('add_menu', views.MenuEditView.as_view(), name="add_menu"),
    re_path(r'edit_menu/(?P<role_id>\d+)', views.MenuEditView.as_view(), name="edit_menu"),
    path("del_menu", views.del_menu, name="del_menu"),

    path('getPermissionTree', views.get_permission_tree, name="get_permission_tree"),

    re_path(r'role/(?P<role_id>\d+)/rbac', views.RolePermissionView.as_view(), name="role_permission"),

]
