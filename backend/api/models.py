
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.html import mark_safe
from django.utils.text import slugify

from shortuuid.django_fields import ShortUUIDField
import shortuuid


class User(AbstractUser):
    username = models.CharField(unique=True , max_length=100)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=100, null=True, blank=True)
   
    USERNAME_FIELD ='email' #USERNAME_FIELD : Définit le champ utilisé comme identifiant unique pour l'authentification. Ici, il est défini comme email au lieu du username par défaut.
    REQUIRED_FIELDS = ['username'] #: Liste des champs supplémentaires requis lors de la création d'un superutilisateur. Ici, le username est requis.
    
    def __str__(self):
        return self.username
    
    
    def save(self, *args, **kwargs):
        email_username, mobile = self.email.split("@")
        if self.fullname == "" or self.fullname == None:
            self.fullname = email_username
        if self.username == "" or self.username == None:
            self.username = email_username  
    
        super(User, self).save(*args, **kwargs)
        
    def get_profile_image_url(self):
        if hasattr(self, 'profile') and self.profile.image: #if hasattr(self, 'profile') vérifie si l'instance (probablement un User) possède un attribut profile
            return self.profile.image.url
        return None
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    image = models.FileField(upload_to='user_image/' , default="default/default-user.png " , null=True , blank=True)
    fullname = models.CharField(max_length=100 , blank=True,null = True)
    bio = models.CharField(max_length=100 , blank=True,null = True)
    about = models.CharField(max_length=100 , blank=True,null = True)
    author = models.BooleanField(default=False)
    country = models.CharField(max_length=100 , blank=True,null = True)
    facebook = models.CharField(max_length=100 , blank=True,null = True)
    twitter = models.CharField(max_length=100 , blank=True,null = True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    def __str__(self):
        if self.fullname:
            return str(self.fullname)
        else:
            return str(self.user.fullname)
    

    def save(self, *args, **kwargs):
        if self.fullname == "" or self.fullname == None:
            self.fullname = self.user.fullname
        super(Profile, self).save(*args, **kwargs) #Python 2:En Python 2, l'appel à super nécessite des arguments : la classe actuelle et self (l'instance actuelle).
    # super(Category, self).save(*args, **kwargs): Cette syntaxe indique à Python d'appeler la méthode save de la classe parente de Category, en passant self comme instance courante.
    
    
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
        
    """Objectif : Cette fonction est exécutée après la création d'un nouvel utilisateur.
Paramètres :
sender : Le modèle qui envoie le signal (User dans ce cas).
instance : L'instance du modèle qui vient d'être créée.
created : Un booléen indiquant si une nouvelle instance a été créée (True) ou si une instance existante a été mise à jour (False).
*args et **kwargs : Arguments supplémentaires passés au signal.
Fonctionnalité : Si une nouvelle instance de User est créée (created est True), une nouvelle instance de Profile est créée avec le nouvel utilisateur comme référence (user=instance).
    """
def save_user_profile(sender, instance, *args, **kwargs):
    instance.profile.save()
    
    """Objectif : Ces lignes connectent les fonctions de gestion des signaux create_user_profile et save_user_profile aux signaux post_save émis par le modèle User.
Fonctionnalité : Chaque fois qu'un utilisateur est créé ou sauvegardé :
create_user_profile est appelé après la création d'un utilisateur.
save_user_profile est appelé après la sauvegarde d'un utilisateur.
    """
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

"""Ce mécanisme garantit que chaque utilisateur a toujours un profil associé, et que toute modification apportée à l'utilisateur est répercutée sur son profil. C'est une manière pratique et efficace de gérer des modèles associés dans Django.
"""
    



class Category(models.Model):
    title = models.CharField(max_length=100 )
    imageCtg = models.FileField(upload_to='imageCtg/' , null=True , blank=True)
    slug = models.SlugField(unique=True , blank=True , null=True)
    
    
    """_META classe_
    La classe Meta dans un modèle Django est utilisée pour fournir des options de configuration supplémentaires pour le modèle
    
    """
    # class Meta :
    #     verbose_name_plural = "Category"
        
    def  __str__(self):
        return self.title
    
    def save(self, *args  , **kwargs):
        if self.slug == "" or self.slug == None :
            self.slug = slugify(self.title)
        super(Category ,self).save(*args, **kwargs)
        
        
    #Ensuite, dans votre modèle Category, vous pouvez définir la méthode postCount pour compter le nombre de posts associés à chaque catégorie.
    def post_count(self):
        return Post.objects.filter(category=self).count()
        
        
        
class Post(models.Model):
    
    STATUS = (
        ("Active","Active"),
        ("Draft","Draft"),
        ("Disable","Disable"),        
    )
    
    # ForeignKey : Crée une relation plusieurs-à-un avec le modèle
    user = models.ForeignKey(User , on_delete= models.CASCADE)
    profile = models.ForeignKey(Profile , on_delete= models.CASCADE , null = True , blank=True)
    category = models.ForeignKey(Category , on_delete= models.CASCADE , null = True , blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True , blank=True) #signifie que le champ n'est pas obligatoire
    imagePost  = models.FileField(upload_to='imagePost/' , null=True , blank=True)
    slug = models.SlugField(unique=True , null= True , blank=True)
    status = models.CharField(choices=STATUS , max_length=100 , default="Active")
    view = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True , related_name="likes_user")
    date = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=100,null=True)
    
    class Meta :
        ordering =  ["-date"] #ordering : Définit l'ordre par défaut des enregistrements lorsque vous effectuez des requêtes. Vous pouvez spécifier un ou plusieurs champs pour trier les résultats.
        verbose_name_plural = "Post"
        
    def  __str__(self):
        return self.title
    
    def save(self, *args  , **kwargs):
        if self.slug == "" or self.slug == None :
            self.slug = slugify(self.title) +"-" + shortuuid.uuid()[:2]
        # Automatically set profile based on user if not provided
        if not self.profile:
            self.profile = Profile.objects.get(user=self.user)
        elif self.profile.user != self.user:
            raise ValueError("Le profil ne correspond pas à l'utilisateur.")
        
        super(Post ,self).save(*args, **kwargs)
        
    def comments(self):
        return Comment.objects.filter(post=self)
        
        
class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    comment= models.TextField(null=True,blank=True)
    replay = models.TextField(null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    
    def  __str__(self):
        return self.post.title
    
    class Meta :
        ordering =  ["-date"] #ordering : Définit l'ordre par défaut des enregistrements lorsque vous effectuez des requêtes. Vous pouvez spécifier un ou plusieurs champs pour trier les résultats.
        verbose_name_plural = "Comment"
     
# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
#     name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100)  # Utilisation de EmailField pour la validation
#     comment = models.TextField(null=True, blank=True)
#     date = models.DateField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.name} on {self.post.title}"
    
#     class Meta:
#         #ordering : Définit l'ordre par défaut des enregistrements lorsque vous effectuez des requêtes. Vous pouvez spécifier un ou plusieurs champs pour trier les résultats.
#         ordering = ["-date"] 
#         verbose_name_plural = "Comments"

#     def get_replies(self):
#         return self.replies.all()
       
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} - {self.user.username}"
    
    class Meta:
        verbose_name_plural = "Bookmark"
        
        
class Notification(models.Model):
    NOTI_TYPE = ( ("Like", "Like"), ("Comment", "Comment"), ("Bookmark", "Bookmark"))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=NOTI_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =  ["-date"]
        verbose_name_plural = "Notification"
    
    def __str__(self):
        if self.post:
            return f"{self.type} - {self.post.title}"
        else:
            return "Notification"
   