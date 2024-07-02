from app import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


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
    path('search', views.search, name='search'),
    path('autocomplete', views.autocomplete, name='autocomplete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)