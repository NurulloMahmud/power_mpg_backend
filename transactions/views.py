from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from .models import Transaction
from users.permissions import IsAdminRole
import pandas as pd
import os



class TransactionCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request):
        try:
            file = request.FILES['file']
        except:
            context = {
                "success": False,
                "message": "Missing file",
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        # Read the Excel file and specify the dtype for store_id
        df = pd.read_excel(file_path, dtype={'store_id': str})
        df = df.fillna('')

        # Populate the database