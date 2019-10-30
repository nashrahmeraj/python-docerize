from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from .detection import object_detect


class ProcessImage(APIView):

    def post(self, request, format=None):

        file = request.data.get('file')
        filename = str(file)

        with default_storage.open('object_detection/bin/' + filename, 'wb+') as destination:  # Saves image file to disk
            for chunk in file.chunks():
                destination.write(chunk)

        image_response = object_detect('object_detection/bin/' + filename)

        return Response(json.dumps(image_response), status=status.HTTP_200_OK)
