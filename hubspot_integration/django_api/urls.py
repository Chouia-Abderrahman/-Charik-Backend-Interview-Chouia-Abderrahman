from django.urls import path
from .views import (CreateContactAPIView,
                    CreateDealAPIView,
                    AssociateContactWithDealAPIView,
                    RetrieveContactsAndDealsAPIView)

urlpatterns = [
    path('contacts/create/', CreateContactAPIView.as_view()),
    path('deals/create/', CreateDealAPIView.as_view()),
    path('deals/associate/', AssociateContactWithDealAPIView.as_view()),
    path('contacts/', RetrieveContactsAndDealsAPIView.as_view()),
]