from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('guest/', views.guest_access, name='guest_access'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index, name='index'),
    # Pattern API endpoints
    path('api/patterns/', views.pattern_list_create, name='pattern_list_create'),
    path('api/patterns/<int:pk>/', views.pattern_detail, name='pattern_detail'),
    path('api/patterns/share/<str:share_token>/', views.pattern_share, name='pattern_share'),
]