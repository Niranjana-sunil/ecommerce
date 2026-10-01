from django.urls import path
from rest_demo.views import *

urlpatterns=[
    path('userreg/',UserRegView.as_view()),
    path('userlog/',UserLoginView.as_view()),
    path('adminlog/',AdminloginView.as_view()),
    path("products/",ProductViewSet.as_view({"post": "create"})),
    path("products/<uuid:pk>/",ProductViewSet.as_view({"put": "update","patch":"partial_update"})),
    path("user/products/",ProductListView.as_view()),
    path('cartview/',CartView.as_view()),
    path('order/', OrderView.as_view()),
    path('user/logout/',UserLogoutView.as_view()),
    path("admin/users/",AdminUserView.as_view()),
    path("admin/orders/",AdminOrderView.as_view()),
    path('admin/selling/',SellingView.as_view()),
    path('admin/logout/',AdminLogoutView.as_view()),

]