from django.urls import path
from .views import *


urlpatterns = [
    path('', index_views, name='index'),
    path('register/', register, name='register'),#URLs de Registro y Login
    path('dashboard/', dashboard_view, name='dashboard'),
    path('about/', about, name='about' ),
    
    #Opciones de Perfil
    path('login/', login_autentic, name='login'),
    path('logout/',dashboard_logout, name= "logout"),
    path('profile/',profile, name= 'profile'),
    path('profile/edit/', editPerfil, name = 'editPerfil'),
    path('password/edit/', passwordedit.as_view(), name = 'passwordedit'),
    
    # URLs para Item
    path('item/', item_list, name = 'item_list'),
    path('itemview/', item_listview.as_view(), name='itemview'),
    path('item/create/', add_item, name='create_item'),
    path('item/update/<int:pk>', Itemupdateview.as_view(), name='update_item'),
    path('item/delete/<int:pk>', Item_Delete.as_view(), name='delete_item'),

    
    
    # URLs para Posts
    #path('posts/', post_list, name='post_list'),
    #path('posts/create/', create_post, name='create_post'),
    #path('posts/<int:post_id>/update/', update_post, name='update_post'),
    #path('posts/<int:post_id>/delete/', delete_post, name='delete_post'),
    #path('post/main/', post_main, name = 'post_main'),
    
    
    
    
    
]
