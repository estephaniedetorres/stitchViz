from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Pattern

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class PatternSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Pattern
        fields = ('id', 'user', 'username', 'user_email', 'name', 'description', 'grid_size', 
                  'craft_type', 'pattern_mode', 'pattern_data', 'current_row', 'current_col', 'pattern_instructions', 
                  'parsed_rows', 'stitch_count', 'stitch_target', 'row_history', 
                  'share_token', 'is_public', 'created_at', 'updated_at')
        read_only_fields = ('user', 'share_token', 'created_at', 'updated_at')
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)