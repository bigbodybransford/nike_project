from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("listshoes/", views.listShoesPageView, name='shoes'),
    path("shoe_links/", views.get_shoe_links, name='shoe_links'),
    # path("shoe_details/", views.get_shoe_details, name='shoe_details'),
    path("shoe/<str:category>", views.get_shoe, name='shoe')
]