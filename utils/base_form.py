from django import forms


class BootstrapBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 给实例对象的每一个字段添加class
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
