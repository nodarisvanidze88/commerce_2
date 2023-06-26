from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.createListing, name="create"),
    path('displaycategory',views.displayCategory, name="displaycategory"),
    path('listing/<int:id>', views.listing, name="listing"),
    path('removewatchlist/<int:id>', views.removeFromWatchlist, name="removefromwatchlist"),
    path('addwatchlist/<int:id>', views.addToWatchlist, name="addinwatchlist"),
]
