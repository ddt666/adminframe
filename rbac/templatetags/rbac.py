import re
import copy

from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag("menu.html")
def show_menu(request):
    menu_key = getattr(settings, "MENU_SESSION_KEY", "menu_dict")
    menu_dict = copy.deepcopy(request.session[menu_key])
    print("menu_dict", menu_dict)
    menu_list = sorted(menu_dict.values(), key=lambda x: x["weight"], reverse=True)
    print("#" * 120)
    print(menu_list)

    for menu in menu_list:
        menu["class"] = "dropdown"
        for child in menu["children"]:

            if hasattr(request, "current_menu_id"):
                if str(request.current_menu_id) == str(child.get("id")):
                    child["class"] = "active"
                    menu["class"] += " active"
                    break

            # if re.match(r'^{}$'.format(child["url"]), request.path_info):
            #     child["class"] = "active"
            #     menu["class"] += " active"
            #     break
    print("menu_list", menu_list)

    return {'menu_list': menu_list}


# 自定义filter 实现按钮是否显示
@register.filter()
def has_permission(request, value):
    key = getattr(settings, 'PERMISSION_SESSION_KEY', 'permission_dict')
    # 3. 当前登陆的这个人他的权限列表是什么
    print("value", value)
    permission_dict = request.session.get(key, {})
    for item in permission_dict.values():
        if value == item["alias"]:
            return True
    else:
        return False