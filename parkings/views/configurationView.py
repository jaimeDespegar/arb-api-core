
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models.configuration import Configuration
from ..serializers import ConfigurationSerializer

class ConfigurationView():
    
    @api_view(['GET'])
    def getConfigurations(request, key):
        try:
            tasks = Configuration.objects.get(configurationName=key)
        except Configuration.DoesNotExist:
            tasks = []
            
        serializer = ConfigurationSerializer(tasks, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @api_view(['PUT'])    
    def updateConfiguration(request, key):
        try:
            config = Configuration.objects.get(configurationName=key)
            config.configurationValue = request.data['value']
            config.save()
            return Response({'message': 'configuration saved'}, status=status.HTTP_200_OK)
        except Configuration.DoesNotExist:
            return Response({'message': 'configuration '+key+' not found'}, status=status.HTTP_404_NOT_FOUND)  

    