from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Center
from rest_framework.views import APIView
from rest_framework import status
from .serializer import CenterSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse

# View to create a new center
class CenterCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print(request.data)
        request.data['center_calendar_id'] = request.user.email
        serializer = CenterSerializer(data=request.data)
        if serializer.is_valid():
            center = serializer.save()  # Save the center to the database
            return Response(
                {
                    "message": "Center created successfully",
                    "center": CenterSerializer(center).data,  # Return the created center's data
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Invalid data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

# View to list all centers
class CenterListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        centers = Center.objects.all()  # Fetch all centers from the database
        serializer = CenterSerializer(centers, many=True)  # Serialize the queryset
        return Response(
            {"message": "Centers retrieved successfully", "centers": serializer.data},
            status=status.HTTP_200_OK
        )
        
# View to list by location all centers
class CenterByLocationListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        location = request.GET.get('location', None)
        
        if not location:
            return Response({"error": "Location parameter is required."}, status=400)
        
        centers = Center.objects.filter(location__iexact=location).values(
            "id",
            "center_name",
            "location",
            "earliest_date",
            "full_address",
            "open_from",
            "closes_at",
        )  # Fetch all centers from the database
        # serializer = CenterSerializer(centers, many=True)  # Serialize the queryset
        return JsonResponse({"centers": list(centers)}, status=200)
