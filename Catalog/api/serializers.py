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


class CategoryListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        categories = [Category(**item) for item in validated_data]
        return Category.objects.bulk_create(categories)

    def update(self, instance, validated_data):
        category_mapping = {category.id: category for category in instance}
        data_mapping = {item['id']: item for item in validated_data}

        ret = []
        for category_id, data in data_mapping.items():
            category = category_mapping.get(category_id, None)
            if category is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(category, data))

        for category_id, category in category_mapping.items():
            if category_id not in category_mapping:
                category.delete()
        return ret


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
    image_set = ImageSerializer(many=True, read_only=True, source="image")

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category', 'category_details', "image_set"]
        ordering = ['-id']
        list_serializer_class = CategoryListSerializer


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
