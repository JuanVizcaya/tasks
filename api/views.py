from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Task
from api.serialaizers import TaskSerializer


class TaskAPI(APIView):
    def get(self, request):
        if 'q' not in request.query_params:
            return Response(
                    {'error': 'Insufficient parameters', 'q': 'Required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        q = request.query_params.get('q')
        
        # qs = Task.objects.filter(filesType = filesType)
        # serializedData = UploadFilesListSerializer(qs, many=True)
        # return Response({'count': len(serializedData.data),'statusRequest': 'ok', 'data': serializedData.data}, status=status.HTTP_200_OK)