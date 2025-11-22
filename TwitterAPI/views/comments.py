from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from TwitterAPI.serializers.comments import CommentSerializer
from TwitterAPI.models.comments import Comments
from TwitterAPI.utils import CustomResponse
from rest_framework.exceptions import PermissionDenied, NotFound



class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                status=True,
                message="Comment added successfully",
                data=serializer.data
            )
        return CustomResponse.error(
            status=False,
            message="Validation error",
            data=serializer.errors
        )

class CommentListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, post_id):
        comments = Comments.objects.filter(post_id=post_id).select_related('user').prefetch_related('replies')
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                status=True,
                message='Comments fetched',
                data=serializer.data
            )

class CommentUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        comment = self.get_object(pk, request.user)
        serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                status=True,
                message='Comment updated',
                data=serializer.data
            )
        return CustomResponse.error(
            status=False,
            message='Validation error',
            data=serializer.errors
        )
    
    def delete(self, request, pk):
        comment = self.get_object(pk, request.user)
        comment.delete()
        return CustomResponse.success(
            status=True,
            message='Comment deleted'
        )
    
    def get_object(self, pk, user):
        try:
            comment = Comments.objects.get(pk=pk)
            if comment.user != user:
                raise PermissionDenied("You can only edit/delete your own comments")
            return comment
        except Comments.DoesNotExist:
            raise NotFound("Comment not found.")
        
class ReplyCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        try:
            parent_comment = Comments.objects.get(id=comment_id)
        except Comments.DoesNotExist:
            return CustomResponse.error(status=False, message="Parent comment not found")
        
        serializer = CommentCreateView(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, parent=parent_comment, post=parent_comment.post)
            return CustomResponse.error(
                status=True,
                message="Reply added successfully",
                data=serializer.data,
            )
        return CustomResponse.error(
            status=False,
            message="Validation error",
            data=serializer.data
        )