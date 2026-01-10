from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Profile, PredictionHistory
from .serializers import (
    RegisterSerializer, UserSerializer, ProfileSerializer, 
    PredictionHistorySerializer, MyTokenObtainPairSerializer
)
from .ml import CareerPredictor
from core.encryption import decrypt_data
import datetime

User = get_user_model()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        # Create profile if not exists
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

class DashboardView(generics.ListAPIView):
    serializer_class = PredictionHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return PredictionHistory.objects.filter(user=self.request.user).order_by('-timestamp')

class GoogleLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Simulating finding/creating user from email
        email = request.data.get('email') 
        if not email:
            return Response({'error': 'Email required for placeholder auth'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user with this email already exists
        user = User.objects.filter(email=email).first()
        if user:
            # User exists, just log them in
            pass
        else:
            # User doesn't exist, create new one
            # Use email as username, but handle potential username collision if needed
            user = User.objects.create_user(username=email, email=email)
        
        refresh = RefreshToken.for_user(user)
        
        # Add custom claims manually or via serializer
        token = refresh.access_token
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff

        return Response({
            'refresh': str(refresh),
            'access': str(token),
            'user': UserSerializer(user).data
        })


class PredictView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # 1. Get User Profile Data
        try:
            profile = request.user.profile
            academic_info = profile.academic_info
            
            # Decrypt if necessary
            if isinstance(academic_info, dict) and 'ciphertext' in academic_info:
                academic_info = decrypt_data(academic_info['ciphertext'])
                
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        # 2. Extract features from request or profile
        # Allow overriding profile data with request data
        data = request.data.copy()
        
        # We need: Degree, Specialization, College_Name, CGPA, Certificates, Graduation_Year
        # Try to pull from academic_info first
        edu_list = academic_info.get('education', [])
        latest_edu = edu_list[0] if edu_list else {}
        
        degree = data.get('degree') or latest_edu.get('degree')
        specialization = data.get('specialization') or latest_edu.get('specialization')
        college_name = data.get('institution') or latest_edu.get('institution')
        cgpa = data.get('cgpa') or latest_edu.get('cgpa') or data.get('gpa') or academic_info.get('gpa')
        year = data.get('year') or latest_edu.get('year')
        
        # Certificates count
        certs_list = academic_info.get('certificates', [])
        certificates_count = len(certs_list)

        if not degree or not specialization:
             # Just a warning or fallback?
             pass

        # Prepare for ML model
        user_features = {
            'Degree': degree,
            'Specialization': specialization,
            'College_Name': college_name,
            'CGPA': cgpa,
            'Certificates': certificates_count,
            'Graduation_Year': year
        }

        # 3. Predict
        predictor = CareerPredictor()
        predictions_list = predictor.predict(user_features)

        # 4. Save to History
        # We save the full list or just top one? Let's save full list
        # Identify top prediction for simple access
        top_prediction = predictions_list[0]['role'] if predictions_list else "Unknown"

        history_entry = PredictionHistory.objects.create(
            user=request.user,
            prediction_data={
                'input': user_features,
                'result': top_prediction, # Backward compat in case we query simple string
                'details': predictions_list
            }
        )

        return Response({
            "prediction": top_prediction, # Keep for backward compatibility if FE expects simple string key
            "top_prediction": top_prediction,
            "predictions": predictions_list,
            "history_id": history_entry.id
        })

from .insights import CareerInsights

class InsightsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        insights = CareerInsights()
        
        # 1. Global Role Distribution
        role_dist = insights.get_role_distribution()
        
        # 2. Insights based on User's Major (if available in profile)
        user_degree = None
        try:
            if hasattr(request.user, 'profile'):
                profile = request.user.profile
                academic_info = profile.academic_info
                
                # Check decryption
                if isinstance(academic_info, dict) and 'ciphertext' in academic_info:
                    from core.encryption import decrypt_data
                    academic_info = decrypt_data(academic_info['ciphertext'])
                
                edu_list = academic_info.get('education', [])
                if edu_list:
                    # Use the most recent degree
                    user_degree = edu_list[0].get('degree')
        except Exception as e:
            print(f"Error getting user degree: {e}")
            pass
            
        # Get trends, filtering by user degree if found
        degree_trends = insights.get_degree_trends(degree_filter=user_degree)
        
        # 3. Personalized Market Insights (New)
        raw_token = request.headers.get('Authorization', '').split(' ')[1] if 'Authorization' in request.headers else None
        
        # We need the profile dictionary, we can use the serialized data for clean format
        from .serializers import ProfileSerializer
        profile = None
        if hasattr(request.user, 'profile'):
             profile_data = ProfileSerializer(request.user.profile).data
             # Decrypt handled by serializer
             profile = profile_data
        
        personalized_data = {}
        if profile:
             personalized_data = insights.get_personalized_insights(profile)

        return Response({
            "role_distribution": role_dist,
            "degree_trends": degree_trends,
            "personalized": personalized_data
        })

# --- Admin Views ---
from rest_framework.parsers import MultiPartParser, FormParser
import os
from django.conf import settings

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class AdminStatsView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminUser)

    def get(self, request):
        total_users = User.objects.count()
        total_predictions = PredictionHistory.objects.count()
        flagged_predictions = PredictionHistory.objects.filter(is_flagged=True).count()
        
        return Response({
            "total_users": total_users,
            "total_predictions": total_predictions,
            "flagged_predictions": flagged_predictions
        })

class AdminPredictionListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminUser)
    serializer_class = PredictionHistorySerializer
    queryset = PredictionHistory.objects.all().order_by('-timestamp')

class AdminPredictionUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminUser)
    serializer_class = PredictionHistorySerializer
    queryset = PredictionHistory.objects.all()

class AdminUserListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminUser)
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-date_joined')

class AdminUserDeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminUser)
    queryset = User.objects.all()

class AdminRetrainView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminUser)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file_obj = request.FILES.get('file')
        include_feedback = request.data.get('include_feedback') == 'true'
        
        dataset_dir = os.path.join(os.path.dirname(__file__), '..', 'dataset')
        os.makedirs(dataset_dir, exist_ok=True)
        file_path = os.path.join(dataset_dir, 'career_prediction_dataset.csv')
        
        # 1. Handle File Upload (Optional now)
        if file_obj:
            try:
                with open(file_path, 'wb+') as destination:
                    for chunk in file_obj.chunks():
                        destination.write(chunk)
            except Exception as e:
                return Response({"error": f"Failed to save file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif not os.path.exists(file_path):
             return Response({"error": "No file provided and no existing dataset found."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Integrate Feedback if requested
        feedback_count = 0
        if include_feedback:
            try:
                import pandas as pd
                # Load current dataset
                df = pd.read_csv(file_path)
                
                # Fetch relevant feedback
                # Logic: Rating >= 4 (Reinforce) OR Correction exists (Correct)
                # Note: If correction exists, use it as Job_Role. Else use result.
                
                from django.db.models import Q
                feedback_items = PredictionHistory.objects.filter(
                    Q(rating__gte=4) | Q(correction__isnull=False)
                ).exclude(correction='') # Filter out empty corrections just in case
                
                new_data = []
                for item in feedback_items:
                    input_data = item.prediction_data.get('input', {})
                    
                    # Determine Ground Truth Role
                    role = item.correction if item.correction else item.prediction_data.get('result')
                    
                    if role and input_data:
                         # Normalize keys to match CSV expected format
                         row = {
                             'Degree': input_data.get('Degree'),
                             'Specialization': input_data.get('Specialization'),
                             'College_Name': input_data.get('College_Name'),
                             'College_Type': 'N/A', # Add default for missing column
                             'CGPA': input_data.get('CGPA'),
                             'Certificates': input_data.get('Certificates'),
                             'Graduation_Year': input_data.get('Graduation_Year'),
                             'Job_Role': role
                         }
                         new_data.append(row)
                
                if new_data:
                    feedback_df = pd.DataFrame(new_data)
                    # Align columns
                    feedback_df = feedback_df[df.columns] 
                    
                    # Append and Save
                    df_combined = pd.concat([df, feedback_df], ignore_index=True)
                    df_combined.to_csv(file_path, index=False)
                    feedback_count = len(new_data)
                    
            except Exception as e:
                print(f"Error integrating feedback: {e}")
                # Continue with minimal failure, or error out? Let's error for visibility
                return Response({"error": f"Failed to integrate feedback: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # 3. Retrain Model
            predictor = CareerPredictor()
            predictor.train_model()
            
            msg = "Model retrained successfully."
            if feedback_count > 0:
                msg += f" Included {feedback_count} user feedback samples."
            
            return Response({"message": msg})
        except Exception as e:
            return Response({"error": f"Failed to retrain model: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PredictionFeedbackView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PredictionHistorySerializer
    queryset = PredictionHistory.objects.all()

    def get_queryset(self):
        # Users can only update their own predictions
        return self.queryset.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Only allow updating rating and feedback_text
        # We can enforce this by validating fields or just picking them from request data here manually if we want to be strict,
        # but UpdateAPIView with serializer will do basic validation.
        # Ideally, we should use a specific serializer or restrict fields in 'data'.
        
        # Create a partial update with specific fields
        data = {
            'rating': request.data.get('rating'),
            'feedback_text': request.data.get('feedback_text')
        }
        
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
