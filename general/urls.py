from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('mytools', views.mytools, name='mytools'),
    path('tools/new', views.tool_new, name='tool_new'),
    path('tools', views.tools, name='tools'),
    path('tools/<int:id_tool>/edit', views.tool_edit, name='tool_edit'),
    path('tools/<int:id_tool>/delete', views.tool_delete, name='tool_delete'),
    path('tools/<int:id_tool>', views.tool_update, name='tool_update'),
    path('categories', views.categories, name='categories'),
    path('categories/new', views.category_new, name='new_category'),
    path('categories/<int:id_category>', views.category_update, name='category_update'),
    path('categories/<int:id_category>/delete', views.category_delete, name='category_delete'),
    path('search', views.search, name='search'),
    path('order', views.order, name='order'),
    path('ranking', views.ranking, name='ranking'),
    path('survey', views.survey, name='survey'),
    path('survey/delete', views.delete_survey, name='delete_survey'),
]