# from django.shortcuts import render

# # Create your views here.


# #Create payment function
# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def create_payment(request):
#     cashier = getattr(request.user, "pharmacycashierprofile", None)
#     if not cashier:
#         return Response({"error": "Only cashiers can record payments."}, status=403)

#     serializer = TransactionSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(cashier=cashier)
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)

# #Patient payment history

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def patient_transaction_history(request, patient_id):
#     transactions = Transaction.objects.filter(patient_id=patient_id)
#     serializer = PatientTransactionHistorySerializer(transactions, many=True)
#     return Response(serializer.data, status=200)


# #Cashier daily revenue
# from django.utils import timezone

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def cashier_daily_revenue(request):
#     cashier = getattr(request.user, "pharmacycashierprofile", None)
#     if not cashier:
#         return Response({"error": "Not authorized."}, status=403)

#     today = timezone.now().date()
#     transactions = Transaction.objects.filter(
#         cashier=cashier,
#         created_at__date=today
#     )

#     total = sum(t.amount for t in transactions)

#     return Response({
#         "cashier": f"{cashier.user.first_name}",
#         "date": str(today),
#         "total_revenue": total,
#         "transactions": TransactionSerializer(transactions, many=True).data
#     })


# #accountant Financial dashboard

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def accountant_financial_report(request):
#     accountant = getattr(request.user, "accountantprofile", None)
#     if not accountant:
#         return Response({"error": "Only accountants can view this."}, status=403)

#     transactions = Transaction.objects.all()
#     total_revenue = sum(t.amount for t in transactions)
#     overdue = transactions.filter(due_date__lt=timezone.now())

#     return Response({
#         "total_transactions": transactions.count(),
#         "total_revenue": total_revenue,
#         "overdue_invoices": overdue.count(),
#     })


# #Overdue invoice

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def overdue_invoices(request):
#     overdue = Transaction.objects.filter(due_date__lt=timezone.now())
#     serializer = TransactionSerializer(overdue, many=True)
#     return Response(serializer.data)
