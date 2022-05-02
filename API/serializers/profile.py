"""API > serializers > profile.py"""
# DRF IMPORTS
from rest_framework import serializers
# CORE IMPORTS
from Core.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for One-to-One Profile model"""
    class Meta:
        """Meta class"""
        model = Profile
        fields = '__all__'
        read_only_fields = ('user', 'is_active', )


class ImageSerializer(serializers.ModelSerializer):
    """Serializer for the Image field in the Profile model"""
    class Meta:
        """Meta class"""
        model = Profile
        fields = ('image', )
