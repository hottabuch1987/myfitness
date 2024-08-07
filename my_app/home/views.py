from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from .models import Product, Category, Feedback

from .forms import ContactForm
from .utils import DataMixin
from django.db.models import Q



class HomePage(ListView):
    """Главная"""
    model = Category
    template_name = 'my_app/fitnes/index.html'
    context_object_name = 'category'
    extra_context = {'title': 'Главная'}


class About(ListView):
    """О нас"""
    model = Product
    template_name = 'my_app/fitnes/about.html'
    context_object_name = 'products'
    extra_context = {'title': 'О нас'}


class Products(DataMixin, ListView):
    """Все продукты"""
    model = Product
    template_name = 'my_app/fitnes/product.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Onlain Fitness')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class Contact(DataMixin, CreateView):
    """Контакты"""
    form_class = ContactForm
    template_name = 'my_app/fitnes/contact.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Консультация')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class ShowProduct(DataMixin, DetailView):
    """Продукт"""
    model = Product
    template_name = 'my_app/fitnes/detail.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'products'
    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['products'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class ShowCategory(DataMixin, ListView):
    """Категория"""
    model = Product
    template_name = 'my_app/fitnes/category.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория | ' + str(context['products'][0].category))
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'], )


from unidecode import unidecode

class Search(ListView):
    """Поиск"""
    model = Product
    template_name = 'my_app/fitnes/search.html'

    def get_queryset(self):
        search_term = self.request.GET.get("q")

        # Преобразование русских символов в транслитерацию
        search_term_translit = unidecode(search_term)

        # Поиск с учетом транслитерации и русских слов
        queryset = Product.objects.filter(Q(name__icontains=search_term) | Q(name__icontains=search_term_translit) | Q(name__icontains=search_term))
        return queryset





