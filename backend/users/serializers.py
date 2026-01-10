from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, PredictionHistory
from core.encryption import encrypt_data, decrypt_data
import json

User = get_user_model()

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'date_joined')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ('username', 'email', 'academic_info')

    def validate_academic_info(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Academic info must be a dictionary.")
        
        education = value.get('education', [])
        if not isinstance(education, list):
             raise serializers.ValidationError("Education must be a list.")
             
        for edu in education:
            if not isinstance(edu, dict):
                raise serializers.ValidationError("Education entry must be a dictionary.")
            
            # Required fields
            if not edu.get('degree') or not edu.get('institution') or not edu.get('year'):
                raise serializers.ValidationError("Degree, Institution, and Year are required for each education entry.")
            
            # CGPA validation
            # Now accepting strings (Ranges), so just ensure it's present or format if needed
            # CGPA validation
            # Accept float or string range
            cgpa = edu.get('cgpa')
            if cgpa:
                if isinstance(cgpa, (int, float)):
                    if cgpa < 0 or cgpa > 10:
                        raise serializers.ValidationError("CGPA must be between 0 and 10.")
                elif isinstance(cgpa, str):
                    # Try to parse string or range
                    try:
                        if '-' in cgpa or '–' in cgpa:
                             # It's a range, we accept it blindly or minimal check
                             parts = cgpa.replace('–', '-').split('-')
                             if len(parts) == 2:
                                 # rudimentary check
                                 float(parts[0])
                                 float(parts[1])
                        else:
                             # Single value string
                             val = float(cgpa)
                             if val < 0 or val > 10:
                                raise serializers.ValidationError("CGPA must be between 0 and 10.")
                    except ValueError:
                         raise serializers.ValidationError("CGPA must be a valid number or range.")
                else:
                    raise serializers.ValidationError("Invalid format for CGPA.")
            
            # Year validation
            year = str(edu.get('year'))
            if not year.isdigit() or len(year) != 4:
                raise serializers.ValidationError("Year must be a 4-digit number.")


        return value

    def to_representation(self, instance):
        """
        Decrypts academic_info when sending profile data to the client.
        """
        ret = super().to_representation(instance)
        # Check if academic_info is encrypted
        academic_info = ret.get('academic_info', {})
        if isinstance(academic_info, dict) and 'ciphertext' in academic_info:
            try:
                decrypted = decrypt_data(academic_info['ciphertext'])
                ret['academic_info'] = decrypted
            except Exception:
                # If decryption fails, return as is or empty?
                # For safety, let's keep it structurally valid but empty or error
                pass
        return ret

    def update(self, instance, validated_data):
        """
        Encrypts academic_info before saving to the database.
        """
        academic_info = validated_data.get('academic_info')
        if academic_info:
            # Validate is already done by validate_academic_info
            # Encrypt
            token = encrypt_data(academic_info)
            # Store as JSON envelope
            validated_data['academic_info'] = {'ciphertext': token}
            
        return super().update(instance, validated_data)

class PredictionHistorySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PredictionHistory
        fields = ('id', 'username', 'prediction_data', 'is_flagged', 'correction', 'rating', 'feedback_text', 'timestamp')
