
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api import views as api_views

urlpatterns = [
    # Définissez ici vos patterns d'URL pour l'API
    path('user/token/', api_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', api_views.RegisterView.as_view(), name='auth_registe'),
    path('user/profile/<user_id>/', api_views.ProfileView.as_view(), name='auth_registe'),
    
    # Post Endpoints
    path('post/category/list/', api_views.CategoryListAPIView.as_view()),
    path('post/category/posts/<category_slug>/', api_views.PostCategoryListAPIView.as_view()),
    path('post/list/', api_views.PostListAPIView.as_view()),
    path('post/detail/<slug>/', api_views.PostDetailAPIView.as_view()),
    path('post/like-post/', api_views.LikePostAPIView.as_view()),
    path('post/comment-post/', api_views.PostCommentAPIView.as_view()),
    path('post/bookmark-post/', api_views.PostBookMarkAPIView.as_view()),
    
    #Dashboard
    
    path('author/dashboard/post-list/<user_id>/' , api_views.DashBoardPostListApi.as_view()),
    path('author/dashboard/stats/<user_id>/' , api_views.DashBoardStats.as_view()),
    path('author/dashboard/comment-list/<user_id>/' , api_views.DashBoardCommentListApi.as_view()),
    path('author/dashboard/Notif-list/<user_id>/' , api_views.DashBoardNotificationListApi.as_view()),
    path('author/dashboard/notif-mark/' , api_views.DashBoardMarkNotificationASseenApi.as_view()),
    path('author/dashboard/reply-comment/' , api_views.DashBoardReplayCommentListApi.as_view()),
    path('author/dashboard/post-create/' , api_views.DashBoardPostCreatAPIView.as_view()),
    path('author/dashboard/post-detail/<user_id>/<post_id>' , api_views.DashBoardPostEditAPIView.as_view())
    
    
    
    
]

"""__Parametre d'url et parametre de requet:__
    URL :
    Identification Unique : Lorsque tu veux identifier un objet spécifique de manière unique, tu utilises 
    des paramètres d'URL. Par exemple, lorsque tu accèdes à un détail spécifique d'un poste, tu utilises 
    un identifiant unique comme un slug ou pk dans l'URL pour récupérer ce poste.

    Opérations sur des Ressources Individuelles : Pour les opérations de récupération, mise à jour ou 
    suppression d'une ressource spécifique, tu utilises souvent des paramètres d'URL. Par exemple, pour 
    obtenir les détails d'un poste spécifique, tu définis une URL comme 
    path('post/detail/<slug>/', api_views.PostDetailAPIView.as_view()).
    
    REQUET
    Opérations de Création ou de Modification : Lorsque tu envoies des données pour créer ou mettre à jour 
    des objets, tu utilises généralement le corps de la requête pour envoyer ces informations. Par exemple, 
    pour commenter un poste, tu envoies des données comme post_id, email, et comment dans le corps de la 
    requête POST.

    Données Non Identifiantes : Lorsque les paramètres que tu envoies ne servent pas à identifier un objet 
    unique mais plutôt à fournir des informations nécessaires pour créer ou modifier un objet, tu les envoies
    dans le corps de la requête.
    
"""