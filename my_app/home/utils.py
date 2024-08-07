from django.db.models import Count
from django.core.cache import cache
from .models import Category

menu = [
        {'title': 'Главная', 'url_name': 'index'},
        {'title': 'Категория', 'url_name': 'products'},
        {'title': 'Избранное', 'url_name': 'cart'},
        {'title': 'Связаться', 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs
        category = cache.get('category')
        if not category:
            category = Category.objects.annotate(Count('products'))
            cache.set('category', category, 60 * 3)

        context['menu'] = menu
        context['category'] = category
        return context
