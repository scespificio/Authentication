from django.contrib.admin.widgets import AdminFileWidget

class MultiFileWidget(AdminFileWidget):
    allow_multiple_selected = True  # ← clé pour autoriser plusieurs fichiers
    def __init__(self, attrs=None):
        attrs = {"multiple": True, **(attrs or {})}
        super().__init__(attrs)