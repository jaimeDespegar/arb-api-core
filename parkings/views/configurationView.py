
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import ConfigurationSerializer
from ..services.configurationService import ConfigurationService

class ConfigurationView():
    
    @api_view(['GET'])
    def getConfigurations(request, key):
        
        tasks = ConfigurationService().get({"configurationName__exact":key})
        if (tasks is None):
            tasks = []
            
        serializer = ConfigurationSerializer(tasks, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @api_view(['PUT'])    
    def updateConfiguration(request, key):
        config = ConfigurationService().get({"configurationName__exact":key})
        if (config is not None):    
            config.configurationValue = request.data['value']
            config.save()
            return Response({'message': 'configuration saved'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'configuration '+key+' not found'}, status=status.HTTP_404_NOT_FOUND)
    