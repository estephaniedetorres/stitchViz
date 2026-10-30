from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import RegisterSerializer, PatternSerializer
from .models import Pattern
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def index(request):
    return render(request, 'stitchViz/index.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to find user by email or username
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            # Try authenticating with email as username
            username = email
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['guest'] = False
            return redirect('guest_access')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'stitchViz/login.html')
    
    return render(request, 'stitchViz/login.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'stitchViz/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'stitchViz/signup.html')
        
        # Create username from email
        username = email.split('@')[0]
        # Ensure username is unique
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            request.session['guest'] = False
            messages.success(request, 'Account created successfully!')
            return redirect('guest_access')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'stitchViz/signup.html')
    
    return render(request, 'stitchViz/signup.html')

def guest_access(request):
    if not request.user.is_authenticated:
        request.session['guest'] = True
    return render(request, 'stitchViz/guest_access.html')

def logout_view(request):
    logout(request)
    return redirect('index')

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# Pattern API Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def pattern_list_create(request):
    """List all patterns for authenticated user or create a new pattern"""
    if request.method == 'GET':
        patterns = Pattern.objects.filter(user=request.user)
        serializer = PatternSerializer(patterns, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PatternSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def pattern_detail(request, pk):
    """Retrieve, update or delete a specific pattern"""
    try:
        pattern = Pattern.objects.get(pk=pk, user=request.user)
    except Pattern.DoesNotExist:
        return Response({'error': 'Pattern not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PatternSerializer(pattern)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PatternSerializer(pattern, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        pattern.delete()
        return Response({'message': 'Pattern deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def pattern_share(request, share_token):
    """View shared pattern (public access, no authentication required)"""
    pattern = get_object_or_404(Pattern, share_token=share_token, is_public=True)
    serializer = PatternSerializer(pattern)
    return Response(serializer.data)