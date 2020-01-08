from background_task.models import Task
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.views.decorators.csrf import csrf_exempt
import stripe
from . import tests

app_name='home'

webhookview = views.my_webhook_view


jp_patterns = [
    path('', views.jobplacements, name='jobplacements'),
    path('apply/<str:level>/', views.apply, name='apply'),
]

wp_patterns = [
    path('', views.workexperience, name='workexperience'),
    path('terms/', views.workterm, name='workterm'),
    path('pay/', views.pay, name='pay'),
    path('apply/', views.workexpform, name='workexpform'),
    path('eligibility/', views.work_experience_eligible, name='eligibility'),
    path('ISA/', views.work_experience_isa_part_1, name='isa'),
    path('sign/',views.work_experience_isa_part_2, name='workexpisa2'),
    path('profile/',views.workexprofile, name='workexprofile'),
    path('faq/',views.workexpfaq, name='workexpfaq'),
]

test_patterns = [
    path('insert_installment_payment',tests.insert_installment_data, ),
    path('insert_installment_payment/<int:breached>',tests.insert_installment_data, ),
    path('delete_installment_payment',tests.delete_installment_record, ),
]

urlpatterns = [
    # path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path('', views.index, name='index'),
    path('webhooks',  csrf_exempt(webhookview), name='my_webhook_view'),
    path('alpha/',  include(test_patterns)),
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
    path('complete_training/<slug:course>', views.completeclass, name='completeclass'),
    path('faq', views.faq, name='faq'),
    path('ulocation', views.ulocation, name='ulocation'),
    path('workexperience/', include(wp_patterns)),
    path('gainexperience', views.gainexperience, name='gainexperience'),
    path('internships', views.internships, name='internships'),
    path('jobplacements/', include(jp_patterns)),
    path('accepted', views.accepted, name='accepted'),
    path('groupCourse/',views.group_list, name='group'),
    path('fasmail/',views.fmail, name='fasmail'),
    path('subscriptionstatus', views.check_subscription_status, name='check_subscription_status'),
   # path('groupCourse', views.group, name='group'),
    path('groupCourse/<int:pk>',views.group,name='group'),
    path('groupCourse/<int:pk>/pay/', views.group_pay, name='group_pay'),
    path('access_course', views.monthly_subscription, name='monthly_subscription'),
    path('accesscourse', views.to_monthly, name='to_monthly_subscription'),
    path('logout', views.log_out, name="logout"),
    path('forgot/password', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:reset_token>/', views.reset_password, name='reset_password'),
    path('aboutus', views.contact_us, name="aboutus"),
    path('policies', views.policies, name="policies"),
    path('linux_start', views.linux_start, name='linux_start'),
    path('jobs', views.jobs, name="jobs"),
    path('jobs/feedback/', views.jobfeed, name="jobfeed"),
    path('jobs/feedback/<int:is_fulltime>', views.jobfeed, name="jobfeed"),
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
    path('tryfree/', views.tryfree, name='tryfree'),
    path('tryfree/<slug:sub_plan>/', views.tryfree, name='tryfree'),
    path('complete_training/pay/<int:class_id>/', views.full_train_pay, name='complete_pay'),
    path('user/RHCSA/order_details', views.rhcsa_order, name='rhcsa_order'),
    path('tutorials/userinterest', views.user_interest, name='user_interest'),
    path('profile_picture/update',views.upload_profile_pic,name='profile_img_upload'),
    path('timeout',views.timeout_handler,name='timeout'),
    path('combined_class/',views.combined_class,name='combined_class'),
    path('combined_class_terms/',views.combined_class_terms,name='combined_class_terms'),
    path('combined_class/pay',views.combined_class_pay,name='combined_class_pay'),
    path('career_switch/',views.career_switch,name='career_switch'),
    path('obtain_position/',views.position_detail),
    path('jobs/submitted',views.job_submitted),
    path('installments/',views.installments,name='installments'),
    path('installments/pay',views.installment_pay, name="installments_pay"),
    path('mail/status',views.mail_status, name="mail-status"),
]



