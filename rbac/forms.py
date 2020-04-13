from utils.base_form import BootstrapBaseForm
from rbac import models


class MenuForm(BootstrapBaseForm):
    class Meta:
        model = models.Menu
        fields = "__all__"
