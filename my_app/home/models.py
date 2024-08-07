from django.conf import settings
from django.db import models

from io import BytesIO
from PIL import Image

from django.core.files import File
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Название", max_length=255)
    image = models.ImageField(upload_to='catgory/%Y/%m/%d/', blank=True, null=True, verbose_name='фото категории')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return f'/{self.slug}/'
        return reverse('category', kwargs={'category_slug': self.slug})
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=255, verbose_name='название')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='слаг')
    description = models.TextField(blank=True, null=True, verbose_name='описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='цена')
    image = models.ImageField(upload_to='product/%Y/%m/%d/', blank=True, null=True, verbose_name='фото')
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name='миниатюра')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')
    set_products = models.CharField('Комплектация', max_length=100, default='Полная')
    video = models.FileField(upload_to='videos/%Y/%m/%d/', blank=True, null=True, verbose_name='видео')
    quantity = models.PositiveIntegerField("Количество")

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('-date_added',)

    def __str__(self):
        return f'Категория: {self.category} - продукт: {self.name}'

    def get_absolute_url(self):
        # return reverse(f'/{self.category.slug}/{self.slug}/')
        return reverse('product', kwargs={'product_slug': self.slug})

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    def get_video(self):
        if self.video:
            return f'{settings.BASE_URL}{self.video.url}'
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail


class Feedback(models.Model):
    firstname_contact = models.CharField("Имя контакта", max_length=25)
    email_contact = models.EmailField('email контакта', max_length=30)
    text_contact = models.TextField('Сообщение контакта', max_length=350)
    phone_contact = models.CharField('Телефон', max_length=12)

    def __str__(self):
        return f"{self.firstname_contact} - {self.email_contact} - {self.phone_contact}"

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"

