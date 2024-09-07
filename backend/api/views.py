from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Sum
# Restframework
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime

# Others
import json
import random

# Custom Imports
from api import serializer as api_serializer
from api import models as api_models



class MyTokenObtainPairView(TokenObtainPairView):#Héritage: TokenObtainPairView est une vue fournie par djangorestframework-simplejwt qui permet d'obtenir des tokens JWT en utilisant un couple (nom d'utilisateur ou email) et un mot de passe.
    # serializer_class: Spécifie le serializer à utiliser pour cette vue. Ici, il s'agit de TokenObtainPairSerializer qui est défini dans api_serializer. Ce serializer permet de personnaliser le token JWT en ajoutant des informations supplémentaires.
    serializer_class = api_serializer.TokenObtainPairSerializer
    
class RegisterView(generics.CreateAPIView): # est une vue générique fournie par Django REST framework qui permet de créer de nouveaux objets dans la base de données.
    queryset = api_models.User.objects.all()#Définit le queryset sur lequel cette vue opérera. Ici, il s'agit de tous les utilisateurs (User) de l'application.
    permission_classes=[AllowAny] #Spécifie les permissions requises pour accéder à cette vue. AllowAny signifie que tout le monde peut accéder à cette vue, même sans être authentifié.
    serializer_class = api_serializer.RegisterSerializer #Spécifie le serializer à utiliser pour cette vue. Ici, il s'agit de RegisterSerializer qui gère la logique de validation et de création des utilisateurs.
    
class ProfileView(generics.RetrieveUpdateAPIView): # est une vue générique fournie par Django REST framework qui permet de récupérer et de mettre à jour des objets dans la base de données.
    permission_classes = [AllowAny] #Spécifie les permissions requises pour accéder à cette vue. AllowAny signifie que tout le monde peut accéder à cette vue.
    serializer_class = api_serializer.ProfileSerializer #Spécifie le serializer à utiliser pour cette vue. Ici, il s'agit de ProfileSerializer qui gère la sérialisation et la désérialisation des objets Profile.


    # Cette méthode est utilisée pour obtenir l'objet Profile correspondant à un utilisateur spécifique. Elle extrait l'identifiant de l'utilisateur (user_id) des paramètres d'URL (kwargs), puis récupère l'utilisateur et son profil correspondant à partir de la base de données.
    def get_object(self):
        # Lorsque Django résout une URL, il extrait les paramètres capturés et les passe à la vue sous forme de dictionnaire kwargs.
        user_id = self.kwargs['user_id']
        user = api_models.User.objects.get(id=user_id)
        profile = api_models.Profile.objects.get(user=user)
        return profile

# liste de toutes les categories
class CategoryListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return api_models.Category.objects.all()
    
# tous les post d'un categorie specifique ()
class PostCategoryListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_slug = self.kwargs['category_slug'] 
        category = api_models.Category.objects.get(slug=category_slug)
        return api_models.Post.objects.filter(category=category, status="Active")
    
    
class PostListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return api_models.Post.objects.filter(status="Active")
    
"""
limitation du nombre de page servi
REST_FRAMEWORK = {
    'PAGE_SIZE': 10  # Nombre d'objets par page
}
class PostListAPIView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination  # Utilisez la pagination par page

    def get_queryset(self):
        return Post.objects.filter(status="Active").order_by('-date') 

"""  

class PostDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        slug = self.kwargs['slug']
        post = api_models.Post.objects.get(slug=slug, status="Active")
        post.view += 1
        post.save()
        return post
    
class LikePostAPIView(APIView): #our cosutme api
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    )
    
    def post(self,request):
        user_id = request.data['user_id']
        post_id = request.data['post_id']
        
        if not user_id or not post_id:
            return Response({'error': 'User ID and Post ID are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = api_models.User.objects.get(id=user_id)
        except api_models.User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            post = api_models.Post.objects.get(id=post_id)
        except api_models.Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if user in post.likes.all():
            # unlike post
            post.likes.remove(user)
            return Response ({"message":"Post desliked"} , status = status.HTTP_200_OK)
        else :
            post.likes.add(user)  
            # Create Notification
            api_models.Notification.objects.create(
                user = post.user,
                post = post,
                type = 'Like'
            )
            return Response ({"message":"Post liked"} , status = status.HTTP_200_OK)
        
        
class PostCommentAPIView(APIView):
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'comment': openapi.Schema(type=openapi.TYPE_STRING),
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                
            },
        ),
    )
    
    def post(self , request):
        post_id = request.data["post_id"]
        email = request.data["email"]
        name = request.data["name"]
        comment = request.data["comment"]
        
        if not post_id or not comment or not email or not name:
            return Response({'error': 'missed args'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = api_models.Post.objects.get(id=post_id)
        except api_models.Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        api_models.Comment.objects.create(
            post = post,
            name = name,
            email = email,
            comment = comment
        )
        api_models.Notification.objects.create(
            user = post.user,
            post = post,
            type = 'Comment'
        )
        
        return Response ({"message":"Comment sent"} , status = status.HTTP_200_OK)
        

class PostBookMarkAPIView(APIView):
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER)            
                
            },
        ),
    )
    
    def post(self , request):
        user_id = request.data['user_id']
        post_id = request.data['post_id']
        
        if not user_id or not post_id:
            return Response({'error': 'User ID and Post ID are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = api_models.User.objects.get(id=user_id)
        except api_models.User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            post = api_models.Post.objects.get(id=post_id)
        except api_models.Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        bookmark = api_models.Bookmark.objects.filter(post = post , user = user).first()
        
        if bookmark :
            bookmark.delete()
            return Response({"message":"Post Un-BookMarked"} , status= status.HTTP_200_OK)
        else:
            # create a new bookmark
            api_models.Bookmark.objects.create(
                user = user,
                post = post
            )
            # create a new notification
            api_models.Notification.objects.create(
            user = post.user,
            post = post,
            type = 'BookMark'
            )
            return Response({"message":"Post BookMared"} , status = status.HTTP_200_OK)
        
        
class DashBoardStats(generics.ListAPIView):
    serializer_class = api_serializer.DashboardStatsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = api_models.User.objects.get(id=user_id)
        
        views = api_models.Post.objects.filter(user=user).aggregate(view=Sum("view"))["view"]
        # .aggregate(view=Sum("view")) calcule la somme des vues de tous les posts de cet utilisateur. Sum("view") est une fonction d'agrégation qui additionne les valeurs du champ view.
        # ["view"] accède à la valeur de la somme des vues dans le dictionnaire retourné par aggregate.
       
        posts = api_models.Post.objects.filter(user=user).count()
        # api_models.Post.objects.filter(user=user) filtre les posts appartenant à l'utilisateur.
        # .count() compte le nombre de posts.
        
        likes = api_models.Post.objects.filter(user=user).aggregate(total_likes=Sum("likes"))["total_likes"]
        bookmarks = api_models.Bookmark.objects.filter(post__user=user).count()
        
        return [{
            "views": views,
            "posts": posts,
            "likes": likes,
            "bookmarks": bookmarks,
        }]

    def list(self, request, *args, **kwargs): #GET et retourner une liste d'objets.
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
# ces classe la sont des APIs
class DashBoardPostListApi(generics.ListAPIView):
    serializer_class =api_serializer.PostSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        
        try :
            user = api_models.User.objects.get(id= user_id)
        except api_models.User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        return  api_models.Post.objects.filter(user = user).order_by("-id")
       
       
       
class DashBoardCommentListApi(generics.ListAPIView):
    serializer_class =api_serializer.CommentSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        
        try :
            user = api_models.User.objects.get(id= user_id)
        except api_models.User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
     
        return  api_models.Comment.objects.filter(post__user = user) #post.user
       
    
class DashBoardNotificationListApi(generics.ListAPIView):
    serializer_class =api_serializer.NotificationSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):  
        user_id = self.kwargs["user_id"]
        
        try :
            user = api_models.User.objects.get(id= user_id)
        except api_models.User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
     
        return  api_models.Notification.objects.filter(user = user)
       
    
class DashBoardMarkNotificationASseenApi(APIView):
    
    def post(self, request):
        notification_id = request.data['notif_id']
        notification = api_models.Notification.objects.get(id = notification_id)
        
        notification.seen = True
        notification.save()
        return Response({"message": "notification Marked as seen"},status= status.HTTP_200_OK)        
   
  
class DashBoardReplayCommentListApi(APIView):
    
    def post(self, request):
        comment_id = request.data['comment_id']
        reply = request.data['replay']
        
        comment = api_models.Comment.objects.get(id = comment_id)
        comment.reply = reply
      
        comment.save()
        return Response({"message": "Comment response sent"},status= status.HTTP_201_CREATED)        
        
    
        
# class DashBoardReplyCommentListApi(APIView):
    

#     def post(self, request):
#         comment_id = request.data['comment_id']
#         reply_content = request.data['reply']
#         name = request.data['name']
#         email = request.data['email']

#         try:
#             parent_comment = api_models.Comment.objects.get(id=comment_id)
#         except api_models.Comment.DoesNotExist:
#             return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         reply = api_models.Comment.objects.create(
#             post=parent_comment.post,
#             parent=parent_comment,
#             comment=reply_content,
#             name=name,
#             email=email
#         )
        
#         return Response({"message": "Comment reply sent"}, status=status.HTTP_201_CREATED)

            
class DashBoardPostCreatAPIView(generics.CreateAPIView):
    serializer_class =  api_serializer.PostSerializer
    permission_classes= [AllowAny]
    
    def create(self,request,*args, **kwargs):
        print(request.data)
        
        user_id = request.data.get("user_id")
        title = request.data.get("title")
        image = request.data.get("image")
        desc = request.data.get("description")
        tags = request.data.get("tags")
        catg_id = request.data.get("category")
        post_status = request.data.get("post_status")
     
        
        try:
            user = api_models.User.objects.get(id=user_id)
        except api_models.User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            category = api_models.Category.objects.get(id = catg_id)
        except api_models.Category.DoesNotExist:
            return Response({'error': 'category not found'}, status=status.HTTP_404_NOT_FOUND)
        
        api_models.Post.objects.create(
            user = user,
            title = title,
            imagePost  = image,
            description=desc,
            status = post_status,
            tags = tags,
            category = category 
        )
         
        return Response({"message":"post created"} ,status=  status.HTTP_201_CREATED)
    
    
    
    
    
    
class DashBoardPostEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class =  api_serializer.PostSerializer
    permission_classes= [AllowAny]
    
    def get_object(self):
        user_id = self.kwargs['user_id']
        post_id = self.kwargs['post_id']
        
        try:
            user = api_models.User.objects.get(id=user_id)
        except api_models.User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            post = api_models.Post.objects.get(id= post_id, user=user)
        except api_models.Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
        return post
        
        
    def update(self , request , *args, **kwargs):
        post_instance = self.get_object()
        
        user_id = request.data.get("user_id")
        title = request.data.get("title")
        image = request.data.get("image")
        desc = request.data.get("description")
        tags = request.data.get("tags")
        catg_id = request.data.get("category")
        post_status = request.data.get("post_status")
        
        try:
            category = api_models.Category.objects.get(id = catg_id)
        except api_models.Category.DoesNotExist:
            return Response({'error': 'category not found'}, status=status.HTTP_404_NOT_FOUND)

        post_instance.title = title
        if image != "undefined":
            post_instance.imagePost = image
        post_instance.status = post_status
        post_instance.description = desc
        post_instance.tags = tags
        post_instance.save()
        
        return Response({"message": "Post updated successfullyn"},status= status.HTTP_200_OK)        
        
       
        
        
      
        
        
        
        
        
