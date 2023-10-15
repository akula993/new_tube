from django import template
from django.utils import timesince

register = template.Library()

@register.filter
def format_duration(duration):
    days = duration.days
    seconds = duration.total_seconds()
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    formatted_duration = ""

    if days > 0:
        formatted_duration += f"{int(days)} дней, "

    if hours > 0:
        formatted_duration += f"{int(hours)} часов, "

    if minutes > 0:
        formatted_duration += f"{int(minutes)} минут, "

    formatted_duration += f"{int(seconds)} секунд"

    return formatted_duration