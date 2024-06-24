from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from .models import Transaction
from price_management.models import Store, StorePrice
from users.models import Company
from card_management.models import Card
from users.permissions import IsAdminRole
import pandas as pd
import os
from datetime import datetime


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
        with transaction.atomic():
            for index, row in df.iterrows():
                try:
                    card = row['card']
                    date = row['date']
                    date = datetime.strptime(date, '%Y-%m-%d').date()
                    time = row['time']
                    time = datetime.strptime(time, "%H:%M").time()
                    invoice_number = row['invoice_number']
                    location_name = row['location_name']
                    city = row['city']
                    state = row['state']
                    item = row['item']
                    unit_price = row['unit_price']
                    quantity = row['qty']
                    amount = row['amt']
                    unit_number = row['unit_number']
                except:
                    context = {
                        "success": False,
                        "error": f"File has missing required fields in row {index+2}",
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
                
                store_name = "Love's" if "loves" in location_name.lower() else "Pilot / Flying J"
                # Check if store exists
                store_obj = Store.objects.filter(name=store_name, city=city, state=state).first()
                if not store_obj:
                    context = {
                        "success": False,
                        "error": f"Store not found in row {index+2}",
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
                # check if the card exists
                card_obj = Card.objects.filter(last_digits=card).first()
                if not card_obj:
                    context = {
                        "success": False,
                        "error": f"Card not found in row {index+2}",
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                store_price_obj = StorePrice.objects.filter(store=store_obj, date=date).first()
                if not store_price_obj:
                    context = {
                        "success": False,
                        "error": f"Store price not found in row {index+2}",
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
                
                # find client's price based on their category
                client_category = card_obj.company.price_category
                if client_category == 1:
                    client_price = store_price_obj.price_1
                elif client_category == 2:
                    client_price = store_price_obj.price_2
                elif client_category == 3:
                    client_price = store_price_obj.price_3
                elif client_category == 4:
                    client_price = store_price_obj.price_4
                elif client_category == 5:
                    client_price = store_price_obj.price_5
                
                # create transaction
                Transaction.objects.create(
                    store=store_obj,
                    card=card_obj,
                    driver=card_obj.driver,
                    company=card_obj.company.name,
                    invoice_number=invoice_number,
                    date=date,
                    time=time,
                    unit_number=unit_number,
                    location_name=location_name,
                    retail_price=unit_price,
                    client_price=client_price,
                    company_price=store_price_obj.company_price,
                    quantity=quantity,
                    item=item,
                    retail_amount=amount,
                )

        context = {
            "success": True,
            "message": "Transactions created successfully",
        }
        return Response(context, status=status.HTTP_200_OK)
