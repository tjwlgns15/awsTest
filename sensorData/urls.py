from sensorData import views, tests
from django.urls import path, include



urlpatterns = [
    path('', views.SensorDataHome.as_view()),
    path('list1/', views.SensorDataListView.as_view()),
    path('update/', views.Update.as_view(), name='update'),

    # test
    path('test/', tests.Test1.as_view(), name='test'),
    path('test2/', tests.Test2.as_view(), name='test2'),

    # Arduino
    path('toggle_light/<str:command>/', views.toggle_light, name='toggle_light'),



]
