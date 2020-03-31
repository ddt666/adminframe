import re

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import HttpResponse

from rbac.utils import permission_helper


class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 当前请求url
        current_url = request.path_info
        print("current_url", current_url)

        # 如果在白名单里直接放行
        for url in getattr(settings, "WHITE_URLS", []):
            if re.match(r'^{}$'.format(url), current_url):
                return

        permission_key = getattr(settings, "PERMISSION_SESSION_KEY", "permission_dict")
        permission_dict = request.session.get(permission_key, [])
        print("-----取permission_dict", permission_dict)
        for k, v in permission_dict.items():
            if re.match(r'^{}$'.format(v['url']), current_url):
                current_menu_id = permission_helper.get_current_menu_id((k, v), permission_dict)
                request.current_menu_id = current_menu_id

                return
        else:
            return HttpResponse("没有权限")
