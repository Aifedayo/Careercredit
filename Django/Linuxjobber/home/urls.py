from django.urls import path, include, re_path
from . import views

app_name = 'home'

jp_patterns = [
    path('', views.jobplacements, name='jobplacements'),
    path('apply/<str:level>/', views.apply, name='apply'),
    ]

wp_patterns = [
    path('', views.workexperience, name='workexperience'),
    path('pay/', views.pay, name='pay'),
    ]


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.log_in, name = 'login'),
    path('signup', views.signup, name='signup'),
    path('selfstudy', views.selfstudy, name='selfstudy'),
    path('faq', views.faq, name='faq'),
    path('linux_certification', views.linux_certification, name='linux_certification'),
    path('workexperience/', include(wp_patterns)),
    path('gainexperience', views.gainexperience, name='gainexperience'),
    path('internships', views.internships, name='internships'),
    path('jobplacements/', include(jp_patterns)),
    path('accepted', views.accepted, name='accepted'),
    path('groupCourse', views.group, name='group'),
    path('groupCourse/pay/', views.group_pay, name='group_pay'),
    path('groupCourse/success/', views.group_success, name='group_success'),
    path('access_course', views.monthly_subscription, name='monthly_subscription'),
    path('logout', views.log_out, name="logout"),
    path('forgot/password', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:u_id>/', views.reset_password, name='reset_password'),
    path('aboutus', views.aboutus, name="aboutus"),
    path('policies', views.policies, name="policies"),
    path('jobs', views.jobs, name="jobs"),
    path('jobs/apply', views.jobapplication, name="jobapplication"),
    path('resume', views.resume, name="resume"),
    path('resumeservice', views.resumeservice, name="resume"),
    path('resumeservice/pay', views.resumepay, name="resumepay"),
    path('resumeservice/upload', views.resumeupload, name="resumeupload"),
    path('companys/contact', views.contact_us, name='contact_us'),
    path('companys/location', views.location, name='location'),
    path('user/account/settings', views.account_settings, name='account_settings'),
    path('user/account/ec2dashboard/', views.ec2dashboard, name="ec2dashboard"),
    path('user/account/ec2dashboard/<command>/', views.ec2dashboard, name="ec2dashboard"),
    path('user/account/startmachine/<machine_id>/', views.startmachine, name='startmachine'),
    path('user/account/stopmachine/<machine_id>/', views.stopmachine, name='stopmachine'),
    path('users/orderlist', views.order_list, name='orderlist')
]
