from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from base.models import Data, Review
from base.serializers import DataSerializer

from rest_framework import status


@api_view(['GET'])
def getData(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    des = Data.objects.filter(
        name__icontains=query).order_by('-createdAt')

    page = request.query_params.get('page')
    paginator = Paginator(des, 5)

    try:
        des = paginator.page(page)
    except PageNotAnInteger:
        des = paginator.page(1)
    except EmptyPage:
        des = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = DataSerializer(des, many=True)
    return Response({'des': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def getTopDes(request):
    des = des.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = DataSerializer(des, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getDes(request, pk):
    des = Data.objects.get(_id=pk)
    serializer = DataSerializer(des, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createDes(request):
    user = request.user

    des = Data.objects.create(
        user=user,
        name='Sample Name',
        destination='Sample Destination',
        state='Sample State',
        city='Sample city',
        category='Sample Category',
        description='',
    )

    serializer = DataSerializer(des, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateDes(request, pk):
    data = request.data
    des = Data.objects.get(_id=pk)

    des.name = data['name']
    des.destination = data['destination']
    des.state = data['state']
    des.city = data['city']
    des.category = data['category']
    des.description = data['description']

    des.save()

    serializer = DataSerializer(des, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteDes(request, pk):
    des = Data.objects.get(_id=pk)
    des.delete()
    return Response('Destination Deleted')


@api_view(['POST'])
def uploadImage(request):
    data = request.data

    Destination_id = data['destination_id']
    des = Data.objects.get(_id=Destination_id)

    Data.image = request.FILES.get('image')
    des.save()

    return Response('Image was uploaded')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createDesReview(request, pk):
    user = request.user
    des = Data.objects.get(_id=pk)
    data = request.data

    # 1 - Review already exists
    alreadyExists = des.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 2 - No Rating or 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            des=des,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = des.review_set.all()
        des.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        des.rating = total / len(reviews)
        des.save()

        return Response('Review Added')
