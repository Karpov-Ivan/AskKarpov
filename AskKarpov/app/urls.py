from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot', views.hot_question, name='hot-question'),
    path('tag/<tag_name>', views.tag, name='tag'),
    path('question/<int:question_id>', views.question, name='question'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('ask', views.ask, name='ask'),
    path('settings', views.settings, name='settings'),
]