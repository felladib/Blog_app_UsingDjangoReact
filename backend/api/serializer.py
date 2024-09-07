from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api import models as api_models


# geneation des token JWT (refresh , access)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls , user): #user: L'utilisateur pour lequel le token est généré.
        token = super().get_token(user) #Cela génère un token standard avec les claims par défaut (comme user_id, username, exp etc.).
        
        token['fullname'] = user.fullname #: Ajoute un nouveau champ fullname au payload du token, en y mettant la valeur de user.fullname. Cela permet d'inclure le nom complet de l'utilisateur dans le token.
        token['email'] = user.email
        token['username'] = user.username
         
        return token




# Cette classe est utilisée pour gérer l'enregistrement des nouveaux utilisateurs.
class RegisterSerializer(serializers.ModelSerializer):
    # Définit les champs pour le serializer, y compris password et password2.
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = api_models.User
        fields = ['fullname', 'email', 'password', 'password2']
        
    # Vérifie si les mots de passe fournis correspondent. Si ce n'est pas le cas, une erreur de validation est levée.  
    def validate(self, attrs):
        # Vérifie si les mots de passe correspondent.
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"Password" :"password fields didn't match."})
        
        return attrs
    
    
    #Crée un nouvel utilisateur avec les données validées, génère un nom d'utilisateur basé sur l'adresse email et définit le mot de passe en utilisant la méthode set_password pour le hachage.
    def create(self, validated_data):
        # Crée un nouvel utilisateur avec les données validées
        user = api_models.User.objects.create(
            fullname=validated_data['fullname'],
            email=validated_data['email']
        )
        
        email_username, mobile = user.email.split("@")
        user.username = email_username
        
        user.set_password(validated_data['password'])
        user.save()
        
        return user
    
    
    
    
class UserSerializer(serializers.ModelSerializer):
    # Indique que tous les champs du modèle User seront inclus dans le serializer.
    class Meta:
        model = api_models.User
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Profile
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    # Elle inclut une méthode personnalisée pour compter le nombre de posts dans chaque catégorie.
    def get_post_count(self,category):
        return category.post.count()
        
    class Meta:
        model = api_models.Category
        # Le paramètre fields dans la classe Meta d'un serializer spécifie quels champs du modèle doivent être inclus dans la sortie sérialisée.
        fields = ["id","title","imageCtg", "slug","post_count"]
 
        
# class CommentSerializer(serializers.ModelSerializer):
#     replies = serializers.SerializerMethodField()

#     class Meta:
#         model = api_models.Comment
#         fields = "__all__"

#     def __init__(self, *args, **kwargs):
#         super(CommentSerializer, self).__init__(*args, **kwargs)
#         request = self.context.get("request")
#         if request and request.method == "POST":
#             self.Meta.depth = 0
#         else:
#             self.Meta.depth = 1

#     def get_replies(self, obj):
#         if obj.replies.exists():
#             return CommentSerializer(obj.replies.all(), many=True, context=self.context).data
#         return []

#     def create(self, validated_data):
#         if "parent" in validated_data:
#             parent = validated_data.pop("parent")
#             return api_models.Comment.objects.create(parent=parent, **validated_data)
#         return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        # Spécifie que ce serializer est pour le modèle Comment.
        model = api_models.Comment
        # Indique que tous les champs du modèle Comment doivent être inclus dans la sérialisation.
        fields = "__all__"
        
    # Change la profondeur de sérialisation en fonction de la méthode HTTP de la requête. Si c'est une requête POST, la profondeur est 0, sinon, elle est 1.
    def __init__(self , *args, **kwargs):
        super(CommentSerializer , self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else :
            self.Meta.Depth = 1
        """_summary_
     
            Le constructeur de la classe. Il modifie la profondeur (depth) de la sérialisation en fonction de la méthode HTTP de la requête :
            Si la méthode est POST, la profondeur est définie à 0, ce qui signifie que seules les données de base sont sérialisées sans suivre les relations.
            Pour d'autres méthodes (comme GET), la profondeur est définie à 1, ce qui inclut des informations supplémentaires sur les relations.
        """
    


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True ,read_only=True )
    class Meta:
        model = api_models.Post
        fields = "__all__"
        
        
    def __init__(self , *args, **kwargs): #__init__ est une méthode spéciale de Python utilisée ici pour modifier la profondeur de sérialisation (Meta.depth) en fonction de la méthode HTTP de la requête (POST ou autre).
        super(PostSerializer , self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
    


class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Bookmark
        fields = "__all__"
    def __init__(self , *args, **kwargs):
        super(BookMarkSerializer , self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else :
            self.Meta.Depth = 1
    

            
            
class NotificationSerializer(serializers.ModelSerializer):  

    class Meta:
        model = api_models.Notification
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(NotificationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            

class DashboardStatsSerializer(serializers.Serializer):
    views = serializers.IntegerField()
    posts = serializers.IntegerField()
    likes = serializers.IntegerField()
    bookmarks = serializers.IntegerField()


















    """_what SUPER mean_
            class Parent:
                def greet(self):
                    print("Hello from Parent")

            class Child(Parent):
                def greet(self):
                    print("Hello from Child")
                    super().greet()  # Appelle la méthode greet() de la classe Parent

            child = Child()
            child.greet()
            
            _res_
            Hello from Child
            Hello from Parent

            __self vs cls__
                self est utilisé pour faire référence à l'instance actuelle de la classe. Il est utilisé dans les méthodes d'instance.
                cls est utilisé pour faire référence à la classe actuelle elle-même. Il est utilisé dans les méthodes de classe.
        
            class MyClass:
                def instance_method(self):
                    return 'instance method called', self

            obj = MyClass()
            print(obj.instance_method())

            class MyClass:
                class_variable = 'class variable'

                @classmethod
                def class_method(cls):
                    return 'class method called', cls

            print(MyClass.class_method())

        
        
    """
    
    """
    depth :
        1. depth dans les serializers
        Le paramètre depth dans la classe Meta d'un serializer Django permet de contrôler la profondeur de sérialisation des relations.

        Exemple :
        Supposons que nous ayons les modèles suivants :
        class Author(models.Model):
            name = models.CharField(max_length=100)

        class Book(models.Model):
            title = models.CharField(max_length=100)
            author = models.ForeignKey(Author, on_delete=models.CASCADE)
       
        class BookSerializer(serializers.ModelSerializer):
            class Meta:
                model = Book
                fields = "__all__"
                depth = 1
                
        => Avec depth = 1, lorsque nous sérialisons un livre, l'auteur sera également sérialisé en profondeur d'un niveau, ce qui signifie que nous obtiendrons des détails sur l'auteur, et pas seulement l'ID de l'auteur.

    """