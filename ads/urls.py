from django.urls import path, include
from . import views
from . import api
from rest_framework.authtoken import views as authviews


app_name = 'ads'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.user_index, name='user_index'),
    path('users/show/<int:index_user>', views.user_show, name='user_show'),
    path('users/edit/<int:index_user>', views.user_edit, name='user_edit'),
    path('users/delete/<int:index_user>', views.user_delete, name='user_delete'),
    path('users/create/', views.user_create, name='user_create'),
    path('saleads/', views.salead_index, name='salead_index'),
    path('saleads/show/<int:index_salead>', views.salead_show, name='salead_show'),
    path('saleads/edit/<int:index_salead>', views.salead_edit, name='salead_edit'),
    path('saleads/delete/<int:index_salead>', views.salead_delete, name='salead_delete'),
    path('saleads/create/', views.salead_create, name='salead_create'),
    path('test-api/users/', api.user_list),
    path('test-api/user/<int:pk>/', api.user_detail),
    path('test-api/saleads/', api.salead_list),
    path('test-api/salead/<int:pk>/', api.salead_detail),
    path('api-token-auth/', authviews.obtain_auth_token),
]
