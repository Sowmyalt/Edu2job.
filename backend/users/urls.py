from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


from .views import (
    RegisterView, DashboardView, PredictView, ProfileView, InsightsView,
    AdminStatsView, AdminPredictionListView, AdminPredictionUpdateView, AdminRetrainView,
    AdminUserListView, AdminUserDeleteView, PredictionFeedbackView, MyTokenObtainPairView,
    GoogleLoginView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('google/', GoogleLoginView.as_view(), name='google_login'),
    path('predict/', PredictView.as_view(), name='predict'),
    path('insights/', InsightsView.as_view(), name='insights'),
    
    # Admin URLs
    path('admin/stats/', AdminStatsView.as_view(), name='admin_stats'),
    path('admin/predictions/', AdminPredictionListView.as_view(), name='admin_predictions'),
    path('admin/predictions/<int:pk>/', AdminPredictionUpdateView.as_view(), name='admin_prediction_update'),
    path('admin/users/', AdminUserListView.as_view(), name='admin_user_list'),
    path('admin/users/<int:pk>/', AdminUserDeleteView.as_view(), name='admin_user_delete'),
    path('predictions/<int:pk>/feedback/', PredictionFeedbackView.as_view(), name='prediction_feedback'),
    path('admin/retrain/', AdminRetrainView.as_view(), name='admin_retrain'),
]
