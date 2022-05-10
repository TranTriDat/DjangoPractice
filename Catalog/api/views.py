from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer, ImageSerializer, \
    CommentSerializer, CommentCountSerializer
from ..models import Category, Product, Image, Comment
from django.db.models import Count
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from .helpers import modify_input_for_multiple_img


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet, APIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        CategoryViewSet = serializer.save()
        return super(CategoryViewSet, self).post(self, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class ProductViewSet(viewsets.ModelViewSet, APIView):
    queryset = Product.objects.all().prefetch_related('category')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'comment':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path="comment")
    def add_comment(self, request, pk):
        comment = request.data.get('comment')
        if comment:
            c = Comment.objects.create(comment=comment,
                                       product=self.get_object(),
                                       user=request.user)
            return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductView(generics.ListAPIView):
    queryset = Product.objects.all().prefetch_related('category')
    serializer_class = ProductSerializer


class ImageViewSet(generics.ListCreateAPIView):
    queryset = Image.objects.all().order_by('product')
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def post(self, request, *args, **kwargs):
        product_id = request.data['product']
        images = dict(request.data.lists())['image']

        success = True
        response = []
        print(images)
        for image in images:
            modified_data = modify_input_for_multiple_img(product_id, image)
            serializer = ImageSerializer(data=modified_data)
            print(image)
            if serializer.is_valid():
                serializer.save()
                response.append(serializer.data)
            else:
                success = False

        if success:
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)


class AllComment(generics.ListAPIView):
    serializer_class = CommentCountSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.values('comment').annotate(total=Count('user'))
