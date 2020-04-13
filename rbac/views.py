from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import JsonResponse
from django.views import View
from django.db.models import F

from rbac import models
from utils.response import BaseResponse
from rbac.forms import MenuForm


# Create your views here.


class RoleListView(View):
    def get(self, request):
        queryset = models.Role.objects.all()

        return render(request, 'rbac/role_list.html', locals())


class RolePermissionView(View):
    def get(self, request, role_id=None):
        return render(request, "rbac/role_permission.html", locals())


def get_permission_tree(request):
    if request.method == "GET":
        res = BaseResponse()
        role_id = request.GET.get("role_id")
        if role_id:
            permission_queryset = models.Permission.objects.all().annotate(name=F("title")).values("id",
                                                                                                   "name",
                                                                                                   "parent_id",
                                                                                                   "alias",
                                                                                                   "menu_id",
                                                                                                   "menu__title",
                                                                                                   "menu__icon",
                                                                                                   "menu__weight").distinct()
            role_permission_ids = models.Permission.objects.filter(role=role_id).values_list("id", flat=True)
            role_permission_ids = [i for i in role_permission_ids]
            print("role_permission_ids", role_permission_ids)
            all_menu_dict = {}
            all_menu_list = []
            print("permission_queryset", permission_queryset)
            for item in permission_queryset:
                menu_pk = item["menu_id"]
                if menu_pk:
                    if menu_pk not in all_menu_dict:
                        all_menu_dict[menu_pk] = {
                            "name": item["menu__title"],
                            "menu_id": item["menu_id"],
                            "children": [

                            ]
                        }
                        all_menu_list.append(all_menu_dict[menu_pk])
            permission_list = []
            for p in permission_queryset:
                permission_list.append(p)

            all_permission_list = []
            all_permission_dict = {}

            for p in permission_list:

                if p["id"] in role_permission_ids:
                    p.update({"checked": True})
                all_permission_dict[p["id"]] = p

            print("*" * 120)
            print("all_permission_dict", all_permission_dict)
            for p in permission_list:

                parent_id = p.get("parent_id")
                if parent_id:
                    all_permission_dict[parent_id].update({"children": []})
            print("====" * 120)
            print("all_permission_dict", all_permission_dict)
            for p in permission_list:
                parent_row = all_permission_dict.get(p["parent_id"])
                if not parent_row:
                    all_permission_list.append(p)
                else:
                    parent_row["children"].append(p)
            print("++" * 120)
            print("all_permission_list", all_permission_list)
            for p in all_permission_list:
                menu_id = p.get("menu_id")
                if menu_id:
                    # print('menu_id',type(menu_id))
                    # print('p',p)
                    all_menu_dict[menu_id]["children"].append(p)
                    if p.get("checked"):
                        all_menu_dict[menu_id].update({"checked": True})
            print("permission_list", permission_list)

            print("all_permission_dict", all_permission_dict)
            print("all_permission_list", all_permission_list)
            print("all_menu_dict", all_menu_dict)
            print("all_menu_list", all_menu_list)
            res.data = all_menu_list
        return JsonResponse(res.dict, safe=False)

    else:
        res = BaseResponse()
        print(request.POST)
        role_id = request.POST.get("role_id")
        permission_list = request.POST.getlist("perIds")

        role_obj = models.Role.objects.get(id=role_id)
        role_obj.permissions.set(permission_list)

        print(role_id, permission_list)
        return JsonResponse(res.dict)


class MenuView(View):
    def get(self, request):
        menu_query = models.Menu.objects.all()
        menu_id = request.GET.get("menu_id")
        if menu_id:
            from django.db.models import Q
            permission_query = models.Permission.objects.filter(Q(parent__menu_id=menu_id) | Q(menu_id=menu_id))
        else:
            permission_query = models.Permission.objects.all()

        permission_query = permission_query.values("pk",
                                                   "title",
                                                   "url",
                                                   "is_menu",
                                                   "parent_id",
                                                   "parent__alias",
                                                   "alias",
                                                   "menu_id",

                                                   "menu__title",
                                                   "menu__icon",
                                                   "menu__weight", )
        print("permission_query", permission_query)
        permission_list = []

        for item in permission_query:
            permission_list.append(item)

        all_permission_dict = {}
        all_permission_list = []

        for item in permission_list:
            all_permission_dict[item["pk"]] = item

        for item in permission_list:
            parent_id = item["parent_id"]
            if parent_id:
                all_permission_dict[parent_id].update({"children": []})

        for item in permission_list:
            parent_row = all_permission_dict.get(item["parent_id"])
            if not parent_row:
                all_permission_list.append(item)
            else:
                parent_row["children"].append(item)
        print("permission_list", permission_list)
        print("all_permission_dict", all_permission_dict)
        print("all_permission_list", all_permission_list)

        context = {
            "menu_query": menu_query,
            "all_permission_list": all_permission_list
        }
        return render(request, "rbac/menu_list.html", context)


class MenuEditView(View):
    def get(self, request, role_id=None):
        menu_obj = models.Menu.objects.filter(pk=role_id).first()
        form = MenuForm(instance=menu_obj)

        # print("form.instance", form.instance)
        context = {
            "form": form,
            "menu_obj": menu_obj
        }
        return render(request, "rbac/op_menu.html", context)

    def post(self, request, role_id=None):
        menu_obj = models.Menu.objects.filter(pk=role_id).first()
        form = MenuForm(request.POST, instance=menu_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse("rbac:menu_list"))
        context = {
            "form": form
        }
        return render(request, "rbac/op_menu.html", context)


def del_menu(request):
    if request.method == "POST":
        res = BaseResponse()
        menu_id = request.POST.get("menu_id")
        models.Menu.objects.filter(pk=menu_id).delete()
        return JsonResponse(res.dict, safe=False)
