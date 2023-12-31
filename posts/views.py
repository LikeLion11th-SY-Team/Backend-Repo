import json,jwt
from django.shortcuts import get_object_or_404
from config.settings import SECRET_KEY

from .models import Post,Comment
from .serializers import PostSerializer,CommentCreateSerializer,CommentSerializer,PostCreateSerializer,CommentListSerializer
from users.models import User
from users.views import token_refresh

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

### CRUD 구현
### 게시판 분류를 어떻게 할 지 정해야 시작가능할 듯
### url로 나눌 것인지, ?category={id} 등으로 받아올 것인지...

class CommentView(APIView):
    def get(self, request, post_pk):
        post = get_object_or_404(Post,pk=post_pk)
        comment_list = Comment.objects.filter(post=post)
        comments = []
        for comment in comment_list:
            comments.append(CommentListSerializer(instance=comment).data)
            comments[-1].pop('commenter')
            comments[-1].pop('post')
        return Response(comments,status=status.HTTP_200_OK)

    def post(self, request, post_pk):
        try:
            # 유저 정보 체크 부분
            token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            
            #댓글 저장 부분
            post = get_object_or_404(Post, pk=post_pk)
            data = request.data
            serializer = CommentCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save(post=post,commenter=user)
                return Response(
                    {
                        "message":"Success",
                        "comment":serializer.data
                    },
                    status = status.HTTP_200_OK
                )
            return Response(
                    {
                        "message":"Comment is not valid",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            return Response({"message" : "You need to refresh"},status=status.HTTP_400_BAD_REQUEST)
            
        
    def put(self, request, comment_pk):
        try:
            # 유저 정보 체크 부분
            token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            #댓글 저장 부분
            comment = get_object_or_404(Comment,pk=comment_pk)
            serializer = CommentSerializer(instance=comment,data=request.data,partial=True)
            if serializer.is_valid(raise_exception=True) and comment.commenter==user:
                comment = serializer.save()
                return Response(
                    {
                        "message":"Success",
                        "comment":serializer.data
                    },
                    status = status.HTTP_200_OK
                )
            return Response({"message":"Comment is not valid"},status=status.HTTP_400_BAD_REQUEST)
        
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            return Response({"message" : "You need to refresh"},status=status.HTTP_400_BAD_REQUEST)
            
    

    def delete(self, request, comment_pk):
        try:
            # 유저 정보 체크 부분
            token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)

            comment = get_object_or_404(Comment, pk=comment_pk)
            if comment.commenter==user:
                comment.delete()
                return Response(
                    {
                        "message":"Success",
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "message":"Different Commenter",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            return Response({"message" : "You need to refresh"},status=status.HTTP_400_BAD_REQUEST)
            

class PostView(APIView):
    def get(self, request, category):
        posts = Post.objects.filter(category=category)
        data = PostSerializer(posts, many=True).data
        for post in data:
            post.pop('writer')
            post.pop('likes')
            post.pop('contents')
        return Response(data,status=status.HTTP_200_OK)
                
    def post(self, request):
        try:
            # 유저 정보 체크 부분
            token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            
            serializer = PostCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(writer=user)
                serializer = PostSerializer(instance=get_object_or_404(Post,pk=serializer.data["pk"]))
                data = serializer.data
                data.pop("writer")
                data.pop("likes")
                return Response(data, status=status.HTTP_200_OK)
            return Response({"message": "글 작성에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except(jwt.exceptions.ExpiredSignatureError):
            return Response({"message" : "You need to refresh"},status=status.HTTP_400_BAD_REQUEST)
            
    
    @api_view(['GET'])
    def view_detail(request, post_pk):
        token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
        if token:
            token = str(token).encode("utf-8")
        else:
            try:
                post = Post.objects.get(pk=post_pk)
            except Post.DoesNotExist:
                return Response({'message': '해당 글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

            data = PostSerializer(post).data
            data.pop("writer")
            is_like = False
            data.pop("likes")
            data["is_like"] = is_like
            return Response(data,status=status.HTTP_200_OK)
        try:
            # 유저 정보 체크 부분
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            try:
                post = Post.objects.get(pk=post_pk)
            except Post.DoesNotExist:
                return Response({'message': '해당 글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

            data = PostSerializer(post).data
            data.pop("writer")
            is_like = False
            print(data["likes"])
            if str(user) in data["likes"]:
                is_like = True    
            data.pop("likes")
            data["is_like"] = is_like
            return Response(data,status=status.HTTP_200_OK)
        except(jwt.exceptions.ExpiredSignatureError):
            return Response({"message" : "You need to refresh"},status=status.HTTP_400_BAD_REQUEST)
            
    def put(self, request, post_pk):
        try:
            # 유저 정보 체크 부분
            token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)

            try:
                post = Post.objects.get(pk=post_pk)
            except Post.DoesNotExist:
                return Response({'message': '해당 글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            if post.writer != user:
                return Response({'message': '글 수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

            serializer = PostSerializer(post, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                data = serializer.data
                data.pop("writer")
                data.pop("likes")
                return Response(data,status=status.HTTP_200_OK)
            return Response({'error': '글 수정에 실패하였습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except(jwt.exceptions.ExpiredSignatureError):
            return Response({"message" : "You need to refresh"},status=status.HTTP_400_BAD_REQUEST)
            
    def delete(self, request, post_pk):
        try:
            # 유저 정보 체크 부분
            token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)

            try:
                post = Post.objects.get(pk=post_pk)
            except Post.DoesNotExist:
                return Response({'error': '해당 글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            if post.writer != user:
                return Response({'error': '글 삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

            post.delete()
            return Response(status=status.HTTP_200_OK)
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            return Response({"message" : "You need to refresh"},status=status.HTTP_400_BAD_REQUEST)
            

@api_view(['GET'])
def like_post(request, post_pk):
    try:
        # 유저 정보 체크 부분
        token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
        if token:
            token = str(token).encode("utf-8")
        access = token
        payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)
        
        #좋아요 부분
        post = get_object_or_404(Post, pk=post_pk)
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return Response({"message":"Success"},status=status.HTTP_200_OK)
    except(jwt.exceptions.ExpiredSignatureError):
        # 토큰 만료 시 토큰 갱신
        return Response({"message" : "You need to refresh"},status=status.HTTP_400_BAD_REQUEST)
        