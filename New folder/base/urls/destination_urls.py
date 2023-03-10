from django.urls import path
from base.views import destination_views as views

urlpatterns = [

    path('', views.getData, name="products"),

    path('create/', views.createDes, name="product-create"),
    path('upload/', views.uploadImage, name="image-upload"),

    path('<str:pk>/reviews/', views.createDesReview, name="create-review"),
    path('top/', views.getTopDes, name='top-products'),
    path('<str:pk>/', views.getData, name="product"),

    path('update/<str:pk>/', views.updateDes, name="product-update"),
    path('delete/<str:pk>/', views.deleteDes, name="product-delete"),
]
