from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings

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
    path('like-question', views.like_question, name='like-question'),
    path('dislike-question', views.dislike_question, name='dislike-question'),
    path('like-answer', views.like_answer, name='like-answer'),
    path('dislike-answer', views.dislike_answer, name='dislike-answer'),
    path('correct-answer', views.correct_answer, name='correct-answer'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)