from django.db import models
from django.contrib.auth.models import User
import bcrypt
from django import forms



class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name= "Usuario")
    name = models.CharField(max_length=255,verbose_name="Articulo")
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Precio")
    description = models.TextField(verbose_name="Descripcion")
    photo = models.ImageField(upload_to='item_photos/',null=True, blank=True,verbose_name="Imagen")
    
    def __str__(self):
        return self.name
    




class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Item  # Cambiado a 'Item' en lugar de 'Articulo'
        fields = ['user', 'name', 'price', 'description', 'photo']

    def __init__(self, *args, **kwargs):
        super(ArticuloForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({'class': 'form-control-file'})

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('El precio no puede ser negativo')
        return price
    
    
    
#Clase de la publicacion
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='available')
    
    def post_image(self):
        return self.item.photo  # Accede a la imagen del Item
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.item.name}"
    
    
#Clase de la compra
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.item.name} - {self.purchase_date}"

class UserExtension(models.Model):
    # Campos de la clase 'UserExtension'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile/', null=True, blank=True)
    
    # Campos de la clase Articulo
