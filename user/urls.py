from django.urls import path
from .views import LoginView, user_detail_view, user_update_view, user_delete_view, \
    user_create_view, user_redirect_view

app_name = "users"
urlpatterns = [
    path("<int:pk>/", view=user_update_view, name="user_update"),
    path("login/", view=LoginView.as_view(), name="user_login"),
    path("register/", user_create_view, name="register"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("<pk>/delete/", view=user_delete_view, name="delete"),
]
