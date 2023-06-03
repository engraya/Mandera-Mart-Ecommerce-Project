from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("store", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('category/<slug:val>', views.CategoryView.as_view(), name="category"),
    path('categoryTitle/<val>', views.CategoryTitle.as_view(), name="categoryTitle"),


    path('home', views.homePage, name='homePage'),
    path('registerPage', views.registerPage, name="registerPage"),
    path('loginPage', views.loginPage, name="loginPage"),
    path('logoutPage', views.logoutPage, name="logoutPage"),
    path('userAccount', views.userAccountPage, name="profile"),

    path('mainPage', views.mainPage, name="mainPage"),
    path('checkoutPage', views.checkoutPage, name="checkoutPage"),
    path('productDetailsPage', views.productDeatilsPage, name="productDeatilsPage"),
    path('main', views.mainPage, name="main"),
    path('', views.landingPage, name="landing"),


    path('contactPage', views.contactPage, name="contactPage"),
    path('addProductPage', views.addProduct, name="addProduct"),

    path('paymentComplete', views.paymentComplete, name="paymentComplete"),

    path('newsletter/', views.index, name='index'),
    path('validate/', views.validate_email, name='validate_email'),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="store/registration/password_reset_form.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="store/registration/password_reset_sent.html"), name="password_reset_sent"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="store/registration/password_reset_confrm.html"), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="store/registration/password_reset_complete.html"), name="password_reset_complete"),
]
