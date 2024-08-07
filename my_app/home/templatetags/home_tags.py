from django import template
from home.models import Category

register = template.Library()


#простые тэги
@register.simple_tag(name='get_cats')
def get_categories():
    return Category.objects.all()


#включающие теги
@register.inclusion_tag('my_app/list_categories.html')
def show_categories(sort=None):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {'cats': cats}