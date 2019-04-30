from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.views.decorators.csrf import csrf_exempt


app_name = 'home'
tryfree = views.tryfree

jp_patterns = [
    path('', views.jobplacements, name='jobplacements'),
    path('apply/<str:level>/', views.apply, name='apply'),
    ]

wp_patterns = [
    path('', views.workexperience, name='workexperience'),
    path('terms/', views.workterm, name='workterm'),
    path('pay/', views.pay, name='pay'),
    path('apply/', views.workexpform, name='workexpform'),
    path('profile/',views.workexprofile, name='workexprofile'),
    ]


urlpatterns = [
    path('', views.index, name='index'),
    path('admin',admin.site.urls),
    path('webhooks', views.my_webhook_view, name='my_webhook_view'),
    path('login/', views.log_in, name = 'login'),
    path('signup', views.signup, name='signup'),
    path('unsubscribe', views.unsubscribe, name='unsubscribe'),
    path('selfstudy', views.selfstudy, name='selfstudy'),
    path('linux/certification', views.linux_certification, name='linux_certification'),
    path('aws/certification', views.aws_certification, name='aws_certification'),
    path('oracledb/certification', views.oracledb_certification, name='oracledb_certification'),
    path('oracledb/full_training', views.oracledb_full_training, name='oracledb_full_training'),
    path('devops/class/', views.devops_class, name='devops_class'),
    path('devops/class/pay', views.devops_pay, name='devops_pay'),
    path('linux/full_training', views.linux_full_training, name='linux_full_training'),
    path('aws/full_training', views.aws_full_training, name='aws_full_training'),
    path('faq', views.faq, name='faq'),
    path('workexperience/', include(wp_patterns)),
    path('gainexperience', views.gainexperience, name='gainexperience'),
    path('internships', views.internships, name='internships'),
    path('jobplacements/', include(jp_patterns)),
    path('accepted', views.accepted, name='accepted'),
    path('groupCourse/',views.group_list,name='group'),
    path('subscriptionstatus', views.check_subscription_status, name='check_subscription_status'),
    # path('groupCourse', views.group, name='group'),
    path('groupCourse/<int:pk>',views.group,name='group'),
    path('groupCourse/<int:pk>/pay/', views.group_pay, name='group_pay'),
    path('access_course', views.monthly_subscription, name='monthly_subscription'),
    path('logout', views.log_out, name="logout"),
    path('forgot/password', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:reset_token>/', views.reset_password, name='reset_password'),
    path('aboutus', views.aboutus, name="aboutus"),
    path('policies', views.policies, name="policies"),
    path('linux_start', views.linux_start, name='linux_start'),
    path('jobs', views.jobs, name="jobs"),
    path('jobs/feedback', views.jobfeed, name="jobfeed"),
    path('jobs/parttime/apply', views.partime, name="partime"),
    path('jobs/challenge/',views.jobchallenge, name='challenge'),
    path('jobs/challenge/<respon>/',views.jobchallenge, name='challenge'),
    path('jobs/apply/<int:job>', views.jobapplication, name="jobapplication"),
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
    path('users/orderlist', views.order_list, name='orderlist'),
    path('home/packages', views.students_packages, name='students_packages'),
    path('home/livehelp', views.live_help, name='live_help'),
    path('home/pay/livehelp', views.pay_live_help, name='pay_live_help'),
    path('home/server/service', views.server_service, name='server_service'),
    path('home/liveinstructor', views.in_person_training, name='in_person_training'),
    path('tryfree/<slug:sub_plan>/', csrf_exempt(tryfree), name='tryfree'),
    path('user/RHCSA/order_details', views.rhcsa_order, name='rhcsa_order'),
    path('tutorials/userinterest', views.user_interest, name='user_interest'),
    path('profile_picture/update',views.upload_profile_pic,name='profile_img_upload'),
]
