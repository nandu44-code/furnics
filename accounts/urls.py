from django.urls import path
from . import views


urlpatterns = [
    
      path('user-login',views.user_login,name='user_login'),
      path('user-signup',views.user_signup,name='user_signup'),
      path('user-logout',views.user_logout,name='user_logout'),

      path('send-otp',views.send_otp,name='send_otp'),
      path('user-otp',views.otp_verification,name="user_otp"),
      path('user-resend-otp',views.otp_resend,name="user_otp_resend"),
      
      path('user-forgot-pass',views.forgot_pass,name="forgot_pass"),
      path('user-reset-pass',views.reset_pass,name="reset_pass"),
      path('user-forgot-pass-otp',views.forgot_pass_otp,name="forgot_pass_otp"),
      # path('forgot-pass-otp-resend',views.fogot_pass_otp_resend,name="forgot_pass_otp_resend")
]


