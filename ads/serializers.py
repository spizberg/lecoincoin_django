from .models import SaleAd, WebsiteUser, Illustration
from rest_framework import serializers
from .utils import create_illustrations, delete_illustrations


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    # saleads = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    password = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = WebsiteUser
        fields = ['id', 'username', 'password', 'email']
        read_only_fields = ['id']

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email', '')
        return WebsiteUser.objects.create_user(username=username, password=password, email=email)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username')
        instance.set_password(validated_data.get('password'))
        instance.email = validated_data.get('username', '')
        instance.save()
        return instance


class IllustrationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Illustration
        fields = ["filename"]

    def to_representation(self, instance):
        return instance.filename


# Serializers define the API representation.
class SaleAdSerializer(serializers.HyperlinkedModelSerializer):
    # author = UserSerializer(read_only=True)
    author = serializers.SlugRelatedField(queryset=WebsiteUser.objects.all(), slug_field='id')
    illustrations = IllustrationSerializer(many=True, read_only=True)
    illustrations_files = serializers.ListField(child=serializers.FileField(), write_only=True, required=False,
                                                allow_empty=True)

    class Meta:
        model = SaleAd
        fields = ['id', 'title', 'price', 'description', 'author', 'illustrations', 'illustrations_files']
        read_only_fields = ['id']

    def create(self, validated_data):
        title = validated_data.get('title')
        price = validated_data.get('price')
        description = validated_data.get('description')
        author = validated_data.get('author')
        salead = SaleAd.objects.create(title=title, price=price, description=description, author=author)
        illustrations = create_illustrations(validated_data.get('illustrations_files'))
        salead.illustrations.add(*illustrations, bulk=False)
        return salead

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.price = validated_data.get('price')
        instance.description = validated_data.get('description')
        instance.author = validated_data.get('author')
        if validated_data.get('illustrations_files') is not None:
            delete_illustrations(list(instance.illustrations))
            illustrations = create_illustrations(validated_data.get('illustrations_files'))
            instance.illustrations.add(*illustrations, bulk=False)
        instance.save()
        return instance
