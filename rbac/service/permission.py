from django.conf import settings


def init(user_obj, request):
    permission_queryset = user_obj.roles.all().values(
        "permissions__pk",
        "permissions__title",
        "permissions__url",
        "permissions__is_menu",
        "permissions__parent_id",
        "permissions__parent__alias",
        "permissions__alias",
        "permissions__menu_id",

        "permissions__menu__title",
        "permissions__menu__icon",
        "permissions__menu__weight",

    ).distinct()
    print(permission_queryset)
    permission_dict = {}

    # permission_dict 格式
    #  {
    # 	1: {
    # 		'title': '客户列表',
    # 		'url': '/customer/list',
    # 		'alias': 'web:customer_list',
    # 		'pid': None,
    # 		'p_alias': None
    # 	},
    # 	2: {
    # 		'title': '添加客户',
    # 		'url': '/customer/add',
    # 		'alias': 'web:customer_add',
    # 		'pid': 1,
    # 		'p_alias': 'web:customer_list'
    # 	},
    # 	3: {
    # 		'title': '账单列表',
    # 		'url': '/payment/list',
    # 		'alias': 'web:payment_list',
    # 		'pid': None,
    # 		'p_alias': None
    # 	},
    # 	4: {
    # 		'title': '添加账单',
    # 		'url': '/payment/add',
    # 		'alias': 'web:payment_add',
    # 		'pid': 3,
    # 		'p_alias': 'web:payment_list'
    # 	}
    # }

    menu_dict = {}

    for item in permission_queryset:
        dict_key = item["permissions__pk"]
        permission_dict[dict_key] = {
            "title": item["permissions__title"],
            "url": item["permissions__url"],
            "alias": item["permissions__alias"],
            "pid": item["permissions__parent_id"],
            "p_alias": item["permissions__parent__alias"],
            "is_menu": item["permissions__is_menu"]

        }

        menu_pk = item["permissions__menu_id"]

        # menu_pk 如果有值，就是子菜单
        if menu_pk:
            if menu_pk not in menu_dict:
                menu_dict[menu_pk] = {
                    "title": item["permissions__menu__title"],
                    "icon": item["permissions__menu__icon"],
                    "weight": item["permissions__menu__weight"],
                    "children": [{
                        "id": item["permissions__pk"],
                        "title": item["permissions__title"],
                        "url": item["permissions__url"],
                        "alias": item["permissions__alias"],
                    }]
                }
            else:
                menu_dict[menu_pk]["children"].append(
                    {
                        "id": item["permissions__pk"],
                        "title": item["permissions__title"],
                        "url": item["permissions__url"],
                        "alias": item["permissions__alias"],
                    }
                )


    print("++++permission_dict", permission_dict)

    print("=" * 100)
    print(menu_dict)

    permission_key = getattr(settings, "PERMISSION_SESSION_KEY", "permission_dict")
    menu_key = getattr(settings, "MENU_SESSION_KEY", "menu_dict")
    request.session[permission_key] = permission_dict
    request.session[menu_key] = menu_dict


"""
permission_dict = {
1: {
    'title': '客户列表',
    'url': '/customer/list',
    'alias': 'web:customer_list',
    'pid': None,
    'p_alias': None
},
2: {
    'title': '添加客户',
    'url': '/customer/add',
    'alias': 'web:customer_add',
    'pid': 1,
    'p_alias': 'web:customer_list'
},
3: {
    'title': '账单列表',
    'url': '/payment/list',
    'alias': 'web:payment_list',
    'pid': None,
    'p_alias': None
},
4: {
    'title': '添加账单',
    'url': '/payment/add',
    'alias': 'web:payment_add',
    'pid': 3,
    'p_alias': 'web:payment_list'
},
5: {
    'title': '我的客户',
    'url': '/my_customer/list',
    'alias': 'web:my_customer_list',
    'pid': None,
    'p_alias': None
}
}
"""

"""
menu_dict ={
1: {
    'title': '客户管理',
    'icon': 'fa-columns',
    'weight': 10,
    'children': [{
        'id': 1,
        'title': '客户列表',
        'url': '/customer/list'
    }, {
        'id': 5,
        'title': '我的客户',
        'url': '/my_customer/list'
    }]
},
2: {
    'title': '账单管理',
    'icon': 'fa-fire',
    'weight': 10,
    'children': [{
        'id': 3,
        'title': '账单列表',
        'url': '/payment/list'
    }]
}
}   

"""
