from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Blog
from blog.serializers import BlogModelSerializer


@api_view(['GET'])
def blog_list(request):
    """
    Список блогов
    """
    list_of_blog = Blog.objects.all()
    serializer = BlogModelSerializer(list_of_blog, many=True)
    return Response(serializer.data)
