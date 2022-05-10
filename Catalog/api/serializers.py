from rest_framework import serializers
from ..models import Category, Product, Image, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'image']
        ordering = ['-id']

    def create(self, validated_data):
        category = Category(**validated_data)
        category.save()
        return category


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'product', 'image')
        ordering = ['-id']

    def create(self, validated_data):
        image = Image(**validated_data)
        image.save()
        return image


class ProductSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(many=True, read_only=True, source="category")
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        image = Image.objects.filter(product=obj)
        return ImageSerializer(image, many=True, read_only=False).data

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category', 'image', 'category_details']
        ordering = ['-id']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'created_date', 'updated_date']


class CommentCountSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    comment = serializers.CharField(max_length=2000)

    class Meta:
        model = Comment
        fields = ['total', 'comment', 'product', 'user']
