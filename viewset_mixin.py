from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import GenericViewSet


class ModelViewSet(GenericViewSet):
    serializer_class = None
    model_class = None
    permission_classes = []
    
    def get_queryset(self):
        return self.model_class.objects.all()
    
    def get_object(self):
        object = self.model_class.objects.filter(pk=self.kwargs["id"])
        if not object:
            raise NotFound(f"{self.model_class.__name__} record not found.")
        return object.first()
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True):
        serializer.save()
        response = {
            "success": True,
            "message": f"Added {self.model_class.__name__} record.",
            "data": [serializer.data],
        }
        return Response(response, status.HTTP_201_CREATED)
        
    def list(self, request):
        queryset = self.get_queryset()
        if not queryset:
            response = {
                "success": True,
                "message": f"{self.model_class.__name__} records empty.",
            }
            return Response(response, status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        response = {
            "success": True,
            "message": f"{self.model_class.__name__} list retrieved.",
            "data": serializer.data,
        }
        return Response(response, status.HTTP_200_OK)

    def retrieve(self, request, id=None):
        object = self.get_object()
        serializer = self.get_serializer(object)
        response = {
            "success": True,
            "message": f"{self.model_class.__name__} record {id} retrieved.",
            "data": [serializer.data],
        }
        return Response(response, status.HTTP_200_OK)
        
    def update(self, request, id=None):
        object = self.get_object()
        serializer = self.get_serializer(object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True):
        serializer.save()
        response = {
            "success": True,
            "message": f"{self.model_class.__name__} ok record updated.",
            "data": [serializer.data],
        }
        return Response(response, status.HTTP_200_OK)
        
    def destroy(self, request, id=None):
        object = self.get_object()
        serializer = self.get_serializer(object)
        data = serializer.data
        object.delete()
        response = {
            "success": True,
            "message": f"{self.model_class.__name__} record {id} deleted.",
            "data":[data],
        }
        return Response(response, status.HTTP_200_OK)