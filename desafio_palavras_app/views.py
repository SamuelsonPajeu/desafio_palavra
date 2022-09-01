from rest_framework.response import Response
from rest_framework.decorators import api_view
from desafio_palavras_app import colector


@api_view(['GET'])
def getData(request):
    return Response({'data': 'Everthyng is ok!'})


@api_view(['GET'])
def getWords(request, world_name):
    return Response(colector.Colector(world_name).start())