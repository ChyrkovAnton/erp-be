from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models import Comment
from .serializers import CommentSerializer


class CommentAPIView(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(good=self.kwargs.get('good_id'))


class CommentDeleteUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

