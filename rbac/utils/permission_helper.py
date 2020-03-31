def get_current_menu_id(current_permission_item, permission_dict):
    print("current_permission_item", current_permission_item)
    print("permission_dict", permission_dict)
    permission_id = current_permission_item[0]
    parent_id = current_permission_item[1].get("pid")

    print("parent_id", parent_id)
    # 父权限有值说明是子权限
    if parent_id:
        parent_p = permission_dict.get(str(parent_id))
        print(parent_p.get("is_menu"))
        # 如果父权限是菜单，就展开父权限的菜单
        if parent_p.get("is_menu"):
            print("找到了", parent_id)
            return parent_id
        # 如果父权限不是菜单，继续找父权限的父权限
        else:
            return get_current_menu_id((parent_id, parent_p), permission_dict)
    else:
        # pid没值说明是父权限，让父权限的菜单展开
        return permission_id


if __name__ == '__main__':
    permission_dict = {
        1: {'title': '客户列表', 'url': '/customer/list', 'alias': 'web:customer_list', 'pid': None, 'p_alias': None,
            'is_menu': True},
        2: {'title': '添加客户', 'url': '/customer/add', 'alias': 'web:customer_add', 'pid': 1,
            'p_alias': 'web:customer_list', 'is_menu': False},
        3: {'title': '账单列表', 'url': '/payment/list', 'alias': 'web:payment_list', 'pid': None, 'p_alias': None,
            'is_menu': True},
        4: {'title': '添加账单', 'url': '/payment/add', 'alias': 'web:payment_add', 'pid': 3, 'p_alias': 'web:payment_list',
            'is_menu': False},
        5: {'title': '我的客户', 'url': '/my_customer/list', 'alias': 'web:my_customer_list', 'pid': None, 'p_alias': None,
            'is_menu': True},
        6: {'title': '我的客户2', 'url': '/my_customer/list2', 'alias': 'web:my_customer_list2', 'pid': 2,
            'p_alias': 'web:customer_add', 'is_menu': False},
    }
    current_item = (
    1, {'title': '客户列表', 'url': '/customer/list', 'alias': 'web:customer_list', 'pid': None, 'p_alias': None,
        'is_menu': True}
    )
    current_menu_id = get_current_menu_id(current_item, permission_dict)
    print(current_menu_id)
