from rest_framework import viewsets, generics
from rest_framework.views import APIView
from .serializers import StoreSerializer, StorePriceReadSerializer, StorePriceWriteSerializer
from .models import Store, StorePrice
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminRole, IsStaffRole
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
import os
from datetime import datetime


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    permission_classes = [IsAuthenticated, IsStaffRole]

class StorePriceViewSet(viewsets.ModelViewSet):
    queryset = StorePrice.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StorePriceWriteSerializer
        return StorePriceReadSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAdminRole()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return StorePrice.objects.all().order_by('-date')

class StorePriceByDate(generics.ListAPIView):
    serializer_class = StorePriceReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        date = self.request.query_params.get('date')
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        return StorePrice.objects.filter(date=date_obj)

class StorePriceCreatePilotView(APIView):
    permission_classes = [IsAdminRole]

    def post(self, request):
        data = request.data
        try:
            date = data['date']
            file = request.FILES['file']
        except:
            context = {
                "success": False,
                "message": "Missing date and/or file",
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)
        
        # Read the Excel file and specify the dtype for store_id
        df = pd.read_excel(file_path, dtype={'store_id': str})
        df = df.fillna('')

        # Populate the database
        try:
            with transaction.atomic():
                for index, row in df.iterrows():
                    store_id = row['store_id']
                    if store_id.lower() in ['nan', '']:
                        continue
                    try:
                        store_obj = Store.objects.filter(name="Pilot / Flying J", store_id=store_id).first()
                        if not store_obj:
                            raise ValueError(f"{store_id} Store not found")
                    except:
                        os.remove(file_path)
                        context = {
                            "success": False,
                            "message": f"There is no Pilot / Flying J with this store number. Please create the store {store_id} location first."
                        }
                        return Response(context, status=status.HTTP_400_BAD_REQUEST)

                    store_price = StorePrice.objects.create(
                        date=date,
                        store=store_obj,
                        retail_price=float(row['retail_price']),
                        company_price=float(row['company_price']),
                        price_1=float(row['price_1']),
                        price_2=float(row['price_2']),
                        price_3=float(row['price_3']),
                        price_4=float(row['price_4']),
                        price_5=float(row['price_5']),
                    )

            context = {
                "success": True,
                "message": "Price data imported successfully",
            }
            os.remove(file_path)
            return Response(context, status=status.HTTP_201_CREATED)
        except Exception as e:
            context = {
                "success": False,
                "message": str(e),
            }
            try:
                os.remove(file_path)
            except:
                pass
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

class StorePriceCreateLovesView(APIView):
    permission_classes = [IsAdminRole]

    def post(self, request):
        data = request.data
        try:
            date = data['date']
            file = request.FILES['file']
        except:
            context = {
                "success": False,
                "message": "Missing date and/or file",
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)
        df = pd.read_excel(file_path)

        # populate db
        try:
            with transaction.atomic():
                for index, row in df.iterrows():
                    store_id = row['store_id']
                    store_obj = Store.objects.filter(name="Loves", store_id=store_id).first()
                    store_price = StorePrice.objects.create(
                        date=date,
                        store=store_obj,
                        retail_price=float(row['retail_price']),
                        company_price=float(row['company_price']),
                        price_1=float(row['price_1']),
                        price_2=float(row['price_2']),
                        price_3=float(row['price_3']),
                        price_4=float(row['price_4']),
                        price_5=float(row['price_5']),
                    )
            context = {
                "success": True,
                "message": "Price data imported successfully",
            }
            return Response(context, status=status.HTTP_201_CREATED)
        except Exception as e:
            context = {
                "success": False,
                "message": str(e),
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

class StorePriceCheckView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request, date: str, store_name: str):
        # Validate and convert the date string to a datetime object
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        
        if store_name.lower() == "pilot":
            store_name = "Pilot / Flying J"
        elif store_name.lower() == "loves":
            store_name = "Love's"
        else:
            return Response({"error": "make sure to send pilot or loves as store name"}, status=status.HTTP_400_BAD_REQUEST)
        
        exists = StorePrice.objects.filter(date=date, store__name=date_obj).exists()
        if exists:
            return Response(True, status=status.HTTP_200_OK)
        return Response(False, status=status.HTTP_200_OK)

class StorePriceDeleteView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request, date: str, store_name: str):
        # Validate and convert the date string to a datetime object
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        
        if store_name.lower() == "pilot":
            store_name = "Pilot / Flying J"
        elif store_name.lower() == "loves":
            store_name = "Love's"
        else:
            return Response({"error": "make sure to send pilot or loves as store name"}, status=status.HTTP_400_BAD_REQUEST)

        StorePrice.objects.filter(date=date_obj, store__name=store_name).delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
