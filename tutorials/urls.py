from django.urls import re_path
from tutorials import views

urlpatterns=[
  re_path(r'^api/tutorials$',views.tutorials_list),
  re_path(r'^api/tutorials/(?P<title>[0-9]+)$',views.tutorial_detail),
  re_path(r'^api/tutorials/published$',views.tutorial_list_published)
]

# (?P<匹配的字段名>正则表达式) 代表一个匹配参数