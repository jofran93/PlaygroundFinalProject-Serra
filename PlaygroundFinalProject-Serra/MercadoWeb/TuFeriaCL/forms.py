from django import forms
from .models import Post, Item
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password  # Importa la función de validación de contraseña
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm # Esta incluye la lógica necesaria para validar el nombre de usuario y la contraseña y permitir el inicio de sesión.
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .forms import PasswordChangeForm




class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, label='Nombre', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=20, label='Apellido', widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    username = forms.CharField(label='Nombre de Usuario', max_length=30, required=True)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Repita Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email','username','password1','password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está registrado.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError('\n'.join(e.messages))
        return password
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return confirm_password
    
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        
        self.fields.pop('username')
        self.fields.pop('password')
        
        self.fields['user'] = forms.CharField(
            label="Nombre de usuario",
            widget=forms.TextInput(attrs={'autofocus': True}),
        )
        self.fields['password'] = forms.CharField(
            label="Contraseña",
            strip=False,
            widget=forms.PasswordInput,
        )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('user')
        password = cleaned_data.get('password')

        # Verificar la autenticación utilizando UserProfile
        try:
            user_profile = User.objects.get(user__username=username)
            if not user_profile.check_password(password):
                raise forms.ValidationError("Nombre de usuario o contraseña incorrectos.")
        except User.DoesNotExist:
            raise forms.ValidationError("Nombre de usuario o contraseña incorrectos.")
        
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username', 'password',
            Submit('submit', 'Iniciar sesión')
        )
        
        
        

class ItemForm(forms.ModelForm):
    user= forms.Select(attrs={'class':'form-control'})
    name=forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}), label=' Nombre del Articulo')
    price=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Precio')
    description=forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}), label='Descripcion')
    photo=forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={ 'class' : 'form-control' }), label='Imagen o Foto')
    class Meta:
        model = Item
        fields = ['user', 'name', 'price', 'description', 'photo' ]

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['user', 'name', 'price', 'description', 'photo']

    def __init__(self, *args, **kwargs):
        super(ArticuloForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({'class': 'form-control-file'})

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('El precio no puede ser negativo')
        return price        
        


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['user', 'item', 'status']
        

class editperfilform(forms.Form):

    email       = forms.EmailField(required=True, widget=forms.EmailInput(attrs={ 'class' : 'form-control' }))
    first_name  = forms.CharField(required=False, widget=forms.TextInput(attrs={ 'class' : 'form-control' }), label='Nombre')
    last_name  = forms.CharField(required=False, widget=forms.TextInput(attrs={ 'class' : 'form-control' }), label='Apellido')
    profile_picture = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={ 'class' : 'form-control' }),label='Foto De Perfil')
    phone_number = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}),label='Telefono')

class FormCambioPassword(PasswordChangeForm):

    old_password  = forms.CharField(widget=forms.PasswordInput(attrs={ 'class' : 'form-control' }), label='Password actual')
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={ 'class' : 'form-control' }), label='Password nuevo')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={ 'class' : 'form-control' }), label='Confirmar password')

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']