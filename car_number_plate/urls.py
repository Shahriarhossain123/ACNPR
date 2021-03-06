from . import views
from django.urls import path

app_name = 'car'
urlpatterns = [
    # car
    path('', views.IndexClassView.as_view(), name='index'),
    path('car_driver', views.Car_DriverClassView.as_view(), name='car_driver'),
    path('report', views.ReportClassView.as_view(), name='report'),
    # car/id
    #path('<int:pk>/', views.FoodDetail.as_view(), name='detail'),
    # item
    #path('item/', views.item, name='item'),
    # add
    #path('add', views.CreateItem.as_view(), name='create_item'),
    # update
    #path('update/<int:id>', views.update_item, name='update_item'),
    # Delete
    #path('delete/<int:id>', views.delete_item, name='delete_item'),
]