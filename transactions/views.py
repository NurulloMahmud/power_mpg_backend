from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from django.core.files.storage import FileSystemStorage
from django.utils.dateparse import parse_date
from django.db import transaction
from django.db.models import Sum
from .models import Transaction
from price_management.models import Store, StorePrice
from card_management.models import Card
from users.permissions import IsAdminRole
import pandas as pd
from datetime import datetime

from .serializers import (
    TransactionListAdminSerializer, TransactionListSerializer,
)


class TransactionCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request):
        from accounts.models import Account

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
        df = pd.read_excel(file_path, dtype={'card': str})
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
                    invoice_number = row['invoice']
                    location_name = row['location_name']
                    city = row['city']
                    state = row['state']
                    item = row['item']
                    unit_price = row['unit_price']
                    quantity = row['qty']
                    amount = row['amt']
                    unit_number = row['unit']
                except Exception as e:
                    context = {
                        "success": False,
                        "error": f"File has missing required fields in row {index+2}, {e}",
                    }
                    # delete the uploaded file
                    try:
                        fs.delete(filename)
                    except:
                        pass
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
                
                store_name = "Love's" if "loves" in location_name.lower() else "Pilot / Flying J"
                store_id = ""
                for char in location_name:
                    if char.isdigit():
                        store_id += str(char)

                # Check if store exists
                if store_id:
                    if store_name != "Love's" and len(store_id) == 2:
                        store_id = "0" + str(store_id)
                    elif store_name != "Love's" and len(store_id) == 1:
                        store_id = "00" + str(store_id)

                    store_obj = Store.objects.filter(name=store_name, store_id=store_id).first()
                if not store_obj:
                    store_obj = Store.objects.filter(name=store_name, city=city.capitalize(), state=state).first()
                
                print(f"name: {store_name}, id: {store_id}, obj: {store_obj}")

                if not store_obj:
                    context = {
                        "success": False,
                        "error": f"Store not found in row {index+2}",
                    }
                    try:
                        fs.delete(filename)
                    except:
                        pass
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
                # check if the card exists
                card_obj = Card.objects.filter(last_digits=card).first()
                if not card_obj:
                    context = {
                        "success": False,
                        "error": f"Card not found in row {index+2}, {card}",
                    }
                    try:
                        fs.delete(filename)
                    except:
                        pass
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                store_price_obj = StorePrice.objects.filter(store=store_obj, date=date).first()
                if not store_price_obj:
                    context = {
                        "success": False,
                        "error": f"Store price not found in row {index+2}",
                    }
                    try:
                        fs.delete(filename)
                    except:
                        pass
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
                new_transaction = Transaction.objects.create(
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

                # adjust the account balance accordingly
                try:
                    account = Account.objects.filter(company=new_transaction.card.company).first()
                    account.balance -= new_transaction.client_amount
                    account.save()
                except:
                    context = {
                        "success": False,
                        "error": f"Failed to adjust account balance, make sure {new_transaction.company} has an account opened",
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

        context = {
            "success": True,
            "message": "Transactions created successfully",
        }
        try:
            fs.delete(filename)
        except:
            pass
        return Response(context, status=status.HTTP_200_OK)

class TransactionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()

    def get_serializer_class(self):
        if self.request.user.role == "admin":
            return TransactionListAdminSerializer
        return TransactionListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        if self.request.user.role == "client":
            queryset = queryset.filter(card__company=self.request.user.company)

        company_id = self.request.query_params.get('company_id', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if company_id:
            queryset = queryset.filter(card__company__id=company_id)
        if start_date:
            queryset = queryset.filter(date__gte=parse_date(start_date))
        if end_date:
            queryset = queryset.filter(date__lte=parse_date(end_date))

        return queryset

class TransactionAmountSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company_id = request.query_params.get('company_id', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        if request.user.role == "client":
            company_id = request.user.company.id

        if not start_date or not end_date:
            context = {
                "success": False,
                "message": "Missing start_date and/or end_date",
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        if start_date is None or end_date is None:
            context = {
                "success": False,
                "message": "Invalid date format",
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        queryset = Transaction.objects.filter(date__gte=start_date, date__lte=end_date)
        if company_id:
            queryset = queryset.filter(card__company__id=company_id)

        total_retail_amount = queryset.aggregate(Sum('retail_amount'))['retail_amount__sum'] or 0.0
        total_client_amount = queryset.aggregate(Sum('client_amount'))['client_amount__sum'] or 0.0
        total_paid_amount = queryset.filter(debt=0).aggregate(Sum('client_amount'))['client_amount__sum'] or 0.0
        total_debt_amount = queryset.filter(debt__gt=0).aggregate(Sum('debt'))['debt__sum'] or 0.0
        total_client_profit = queryset.aggregate(Sum('client_profit'))['client_profit__sum'] or 0.0

        context = {
            "success": True,
            "total_retail_amount": total_retail_amount,
            "total_client_amount": total_client_amount,
            "total_paid_amount": total_paid_amount,
            "total_debt_amount": total_debt_amount,
            "total_client_profit": total_client_profit,
        }

        return Response(context, status=status.HTTP_200_OK)

