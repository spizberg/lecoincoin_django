from .models import SaleAd, WebsiteUser
from .serializers import UserSerializer, SaleAdSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def user_list(request):
    """
    List all users in application or create new user

    @param request:
    """
    if request.method == 'GET':
        users = WebsiteUser.objects.all()
        multiple_users = True
        if request.query_params.get('username'):
            users = WebsiteUser.objects.get(username=request.query_params.get('username'))
            multiple_users = False
        serializer = UserSerializer(users, many=multiple_users)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def user_detail(request, pk: int):
    """
    Get information on a user, modify this user or delete him from database
    @param request:
    @param pk:
    @return:
    """
    try:
        user = WebsiteUser.objects.get(pk=pk)
    except WebsiteUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def salead_list(request):
    """
    List all sale ads in application or create new sale ad

    @param request:
    """
    if request.method == 'GET':
        saleads = SaleAd.objects.all()
        serializer = SaleAdSerializer(saleads, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SaleAdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data['id'], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def salead_detail(request, pk: int):
    """
    Retrieve, update or delete a sale ad.
    """
    try:
        salead = SaleAd.objects.get(pk=pk)
    except SaleAd.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SaleAdSerializer(salead)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # if len(request.data.get('illustrations_files')) == 0:
        #     request.data.update({'illustrations_files': []})
        print(request.data)
        serializer = SaleAdSerializer(salead, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        salead.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
