from rest_framework import generics
from .models import (
    Comment,
    Like,
)
from .serializers import (
    CommentSerializer,
    CommentDetailsSerializer,
    CommentJudgmentSerializer,
    LikeSerializer,
)

class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailsView(generics.RetrieveUpdateDestroyAPIView):    #TODO: permission vase sahabesh va contributers
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'
    queryset = Comment.objects.all()
    serializer_class = CommentDetailsSerializer

    def perform_destroy(self, serializer):
        serializer.deleted = True
        serializer.save()
        return serializer

class CommentJudgmentView(generics.CreateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'
    queryset = Comment.objects.all()
    serializer_class = CommentJudgmentSerializer

    def perform_create(self, serializer):
        request_type = serializer.validated_data['request_type']
        comment = Comment.objects.get(id=self.kwargs['comment_id'])

        if request_type == 1: # accept
            comment.verified = True
        else: # reject
            comment.verified = False
            comment.deleted = True
        comment.save()

class LikeView(generics.CreateAPIView):
    lookup_field = 'comment_id'
    lookup_url_kwarg = 'comment_id'
    serializer_class = LikeSerializer

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        return Like.objects.filter(Q(comment_id = comment_id))

    def perform_create(self, serializer):
        comment = Comment.objects.get(id=self.kwargs['comment_id'])
        user = self.request.user
        serializer.save(user=user, comment=comment)

class DislikeView(generics.DestroyAPIView):
    lookup_field = 'comment_id'
    lookup_url_kwarg = 'comment_id'
    serializer_class = LikeSerializer

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        user = self.request.user
        return Like.objects.filter(Q(comment_id=comment_id) & Q(user=user))
