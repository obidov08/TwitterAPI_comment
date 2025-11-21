from rest_framework.views import APIView
from TwitterAPI.utils import  CustomResponse
from TwitterAPI.serializers import PostCreatedSerializer, MediaSerializer
from TwitterAPI.permissions import IsAuthenticatedAndDone, IsAuthenticatedAndAuthor, IsAuthenticatedAndAuthorForMedia
from rest_framework.parsers import MultiPartParser, FormParser
from TwitterAPI.models import Post, Media
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema(tags=['Post'])
class CreatedPostAPIView(APIView):
    serializer_class = PostCreatedSerializer
    permission_classes = [IsAuthenticatedAndDone, ]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=user)

        return CustomResponse.success(
            status=True,
            message='Post created successfully.',
            data=request.data
        )
    
@extend_schema(tags=['Post'])
class UpdateDeleteAPIView(APIView):
    serializer_class = PostCreatedSerializer
    permission_classes = [IsAuthenticatedAndAuthor, ]

    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = self.serializer_class(post, data=request.data)
            serializer.is_valid(raise_exception=True)
        except:
            return CustomResponse.error(
            status=False,
            message="post doesn't exist."
        )
         

        serializer.save()
        return CustomResponse.success(
            status=True,
            message="Post update successfully.",
            data=serializer.data
        )
    

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
        except:
            return CustomResponse.error(
            status=False,
            message="post doesn't exist."
        )
         
        return CustomResponse.success(
            status=True,
            message="Post updated successfully.",
        )
        

@extend_schema(tags=['Post'])
class CreatedMediaAPIView(APIView):
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticatedAndDone, ]
    parser_classes = [MultiPartParser, FormParser]


    @extend_schema(
            request={
                'multipart/formdata': {
                    'type': 'object',
                    'properties': {
                        'post': {
                            'type': 'integer',
                        },
                        'media': {
                            'type': "string",
                            'format': 'binary',
                        }
                    }
                }
            },
            responses={200: OpenApiTypes.OBJECT}
    )

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return CustomResponse.success(
            status=True,
            message='Media created successfully.',
            data=request.data
        )
        

@extend_schema(tags=['Post'])
class DeleteMediaAPIView(APIView):
    permission_classes = [IsAuthenticatedAndAuthorForMedia, ]

    @extend_schema(
            request={
                'application/json': {
                    'type': 'object',
                    'properties': {
                        'pk': {
                            'type': 'integer',
                        },
                    }
                }
            },
            responses={200: OpenApiTypes.OBJECT}
    )

    def delete(self, request, pk):
        try:
            media = Media.objects.get(pk)
            media.delete()
        except:
            return CustomResponse.error(
                status=False,
                message='Media doesn\'t exist.'
            )

        return CustomResponse.success(
            status=True,
            message='Media created successfully',
        )
    