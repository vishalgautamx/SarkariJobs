from django.contrib import admin
from django.urls import path
admin.site.site_header= "SarkariJobs Admin"
admin.site.site_title="SarkariJobs Admin"
admin.site.index_title="SarkariJobs Dashboard"
urlpatters={
    path("admin/",admin.site.urls),
}