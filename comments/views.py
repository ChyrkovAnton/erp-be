from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Comment
from user.models import User
from .serializers import CommentSerializer


class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Comment.objects.filter(good=self.kwargs.get('good_id'))


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer_class):
        parent_public_id = self.kwargs.get('public_id')
        customer_public_id = self.kwargs.get('customer')
        customer = User.objects.get(public_id=customer_public_id)
        if parent_public_id != 'undefined':
            parent = Comment.objects.get(public_id=parent_public_id)
            serializer_class.save(parent=parent, customer=customer)
        serializer_class.save(customer=customer)


class CommentDeleteUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'public_id'
    permission_classes = (IsAuthenticated,)

