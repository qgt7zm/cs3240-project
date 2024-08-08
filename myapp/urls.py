from django.urls import path

from myapp import views

app_name = "myapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("admin_reports/", views.admin_reports, name="admin_reports"),
    path('user_reports/', views.user_reports, name="user_reports"),
    path('report/<int:report_id>/', views.report_view, name='report_view'),
    path('report_form/', views.report_form, name='report_form'),
    path('faq/', views.faq, name='faq'),
    path('resources/', views.resources, name='resources'),
    path('manage_profile/', views.manage_profile, name='manage_profile'),
    path('delete_report/<int:report_id>/', views.delete_report, name='delete_report'),
    path('about_us/', views.about_us, name='about_us'),
]
