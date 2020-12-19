"""MainPanel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from MainPanel import settings
from django.contrib import admin
from django.urls import path
from institutions.api.views import UserCreateAPIView, CurrentUserView, ObtainAPIToken, get_news

from tpo.api.views import *

from tpousers.api.views import *
from tpousers.views import correction_verification, mock_verification, get_panel

urlpatterns = [
                  path('', get_panel),

                  path('api/v1/test/', test_download_api_view),
                  path('api/v1/login/', ObtainAPIToken.as_view()),
                  path('api/v1/signup/', UserCreateAPIView.as_view()),
                  path('api/v1/tpo_list/', get_tpo_list),
                  path('api/v1/profile/', CurrentUserView.as_view()),
                  path('api/v1/order_correction/', order_correction),
                  path('api/v1/prices/', correction_price),
                  path('api/v1/correction_review/', correction_review),
                  path('api/v1/corrector_rating/', corrector_rating),
                  path('api/v1/mock_list/', get_mock_list),
                  path('api/v1/user_mock_list/', get_user_mock_list),
                  path('api/v1/order_mock/', order_mock),
                  path('api/v1/submit_reading_answers/', submit_reading_answer),
                  path('api/v1/submit_listening_answers/', submit_listening_answer),
                  path('api/v1/submit_speaking_answers/', submit_speaking_answer),
                  path('api/v1/submit_writing_answers/', submit_writing_answer),
                  path('api/v1/submit_mock_done/', submit_mock_done),
                  path('api/v1/get_news/', get_news),

                  path('verify/order/correction', correction_verification),
                  path('verify/order/mock', mock_verification),

                  path('api/v1/institute/get_reading_list/', get_reading_list),
                  path('api/v1/institute/add_reading/', add_reading),
                  path('api/v1/institute/delete_reading/', delete_reading),
                  path('api/v1/institute/edit_reading/', edit_reading),
                  path('api/v1/institute/get_reading_questions/', get_reading_questions),
                  path('api/v1/institute/delete_reading_question/', delete_reading_question),
                  path('api/v1/institute/add_reading_question/', add_reading_question),


                  path('api/v1/institute/get_listening_list/', get_listening_list),
                  path('api/v1/institute/add_listening/', add_listening),
                  path('api/v1/institute/delete_listening/', delete_listening),
                  path('api/v1/institute/edit_listening/', edit_listening),
                  path('api/v1/institute/get_listening_questions/', get_listening_questions),
                  path('api/v1/institute/delete_listening_question/', delete_listening_question),
                  # path('api/v1/institute/add_reading_question/', add_reading_question),

                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
