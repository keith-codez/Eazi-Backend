# regulator/views/analytics.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count

from rentals.models import Lead, BookingRequest
from staff.models import Booking
from regulator.models import Customer


class AnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Total customers
        total_customers = Customer.objects.count()

        # Repeat customers: made more than 1 booking
        repeat_customers = Booking.objects.values('customer')\
            .annotate(booking_count=Count('id'))\
            .filter(booking_count__gt=1).count()

        # New customers: exactly 1 booking
        new_customers = Booking.objects.values('customer')\
            .annotate(booking_count=Count('id'))\
            .filter(booking_count=1).count()

        # Leads and conversions
        total_leads = Lead.objects.count()
        converted_leads = Customer.objects.filter(lead__isnull=False).count()
        conversion_rate = round((converted_leads / total_leads) * 100, 2) if total_leads else 0

        # Example chart dummy data (replace later)
        booking_frequency = [{"name": "1", "value": 20}, {"name": "2-3", "value": 40}]
        booking_duration = [{"name": "1-3 days", "value": 35}, {"name": "4-7 days", "value": 25}]
        payment_methods = [{"name": "Ecocash", "value": 50}, {"name": "Bank", "value": 30}]

        return Response({
            "summary": {
                "total_customers": total_customers,
                "repeat_customers": repeat_customers,
                "new_customers": new_customers
            },
            "conversion": {
                "leads": total_leads,
                "converted_to_customers": converted_leads,
                "conversion_rate": conversion_rate
            },
            "charts": {
                "booking_frequency": booking_frequency,
                "booking_duration": booking_duration,
                "payment_methods": payment_methods
            }
        })
