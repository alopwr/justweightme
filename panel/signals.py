from celery.worker.control import revoke
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .charts import generate_and_save_chart
from .models import Measurement, Profile


@receiver([post_save, post_delete], sender=Measurement)
def generate_charts(sender, instance, **kwargs):
    profile = instance.profile
    if type(profile.chart_js_code) == str and profile.chart_js_code[0] == "x":
        revoke(profile.chart_js_code.split("_")[1], terminate=True)

    profile.chart_js_code = "x_" + generate_and_save_chart.delay(profile.id).id
    profile.save()


@receiver(post_save, sender=Profile)
def increase_signature(sender, instance, **kwargs):
    instance.user.signature.signature += 1
    instance.user.signature.save()
