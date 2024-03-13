from django.urls import path
from . import views



urlpatterns =[
    path("api/v1/home", views.Home, name="Home"),
    #path("women/", views.GetWomenCategory, name="Mencategory"),
    #path("login/", views.Login_user, name="Login_user"),
    path("api/v1/register", views.RegisterUser, name="register_user"),
    path("api/v1/login", views.C_Login.as_view(), name="login"),
    path("api/v1/addproduct", views.Add_product.as_view(), name="addproduct"),

    #Update_user  RegisterUser, C_Login, Add_product
]