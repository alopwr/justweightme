from django.apps import AppConfig


class PanelConfig(AppConfig):
    name = 'panel'

    def ready(self):
        import panel.signals