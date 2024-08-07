from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from .models import Product, Category, Feedback
from django.shortcuts import get_object_or_404
from .forms import ContactForm
from .utils import DataMixin
from django.db.models import Q
from .tasks import send_contact_email


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
        c_def = self.get_user_context(title='Программы')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class Contact(DataMixin, CreateView):
    """Контакты"""
    form_class = ContactForm
    template_name = 'my_app/fitnes/contact.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_slug = self.kwargs.get('product_slug')
        product = get_object_or_404(Product, slug=product_slug)
        context['product_slug'] = product_slug  # Передаем slug продукта в контекст
        context['product_name'] = product.name 
        return context

    def form_valid(self, form):
        # Получаем slug из скрытого поля
        product_slug = self.request.POST.get('product_slug')
        form.instance.product = get_object_or_404(Product, slug=product_slug)  # Привязываем товар
        # Отправка email через Celery
        email_subject = 'Здравствуйте! Вы оформили заказ на сайте Online Fitness'
        email_body = f'После оплаты программы Вам придут файлы. Ваш заказ : {form.instance.product.name}.'
        user_email = form.cleaned_data.get('email_contact')  # Получаем email пользователя из формы
        # Запускаем задачу отправки email
        print(email_subject, email_body, user_email)
        send_contact_email.delay(email_subject, email_body, user_email)


        return super().form_valid(form)


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





