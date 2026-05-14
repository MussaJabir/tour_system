from rest_framework import serializers

from .models import Booking, Passenger, Payment, BookingInquiry, SavedPackage
from .serializers import PackageListSerializer


class CustomerPassengerSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Passenger
        fields = ['id', 'full_name', 'first_name', 'last_name', 'is_lead_passenger']


class CustomerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment_type', 'amount', 'currency', 'payment_method', 'status', 'received_at']


class CustomerBookingListSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='package.name', read_only=True)
    package_slug = serializers.CharField(source='package.slug', read_only=True)
    total_paid = serializers.ReadOnlyField()
    balance_due = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'booking_reference', 'package_name', 'package_slug',
            'departure_date', 'num_adults', 'num_children',
            'status', 'status_display',
            'quoted_price', 'currency',
            'total_paid', 'balance_due',
            'created_at',
        ]


class CustomerBookingDetailSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='package.name', read_only=True)
    package_slug = serializers.CharField(source='package.slug', read_only=True)
    total_paid = serializers.ReadOnlyField()
    balance_due = serializers.ReadOnlyField()
    is_fully_paid = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    passengers = CustomerPassengerSerializer(many=True, read_only=True)
    payments = CustomerPaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = [
            'booking_reference', 'package_name', 'package_slug',
            'departure_date', 'return_date',
            'num_adults', 'num_children',
            'status', 'status_display',
            'quoted_price', 'deposit_amount', 'currency',
            'total_paid', 'balance_due', 'is_fully_paid',
            'special_requirements',
            'passengers', 'payments',
            'created_at', 'updated_at',
        ]


class CustomerInquiryListSerializer(serializers.ModelSerializer):
    package_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = BookingInquiry
        fields = [
            'inquiry_reference', 'package_name',
            'status', 'status_display',
            'preferred_travel_date',
            'number_of_adults', 'number_of_children',
            'created_at',
        ]

    def get_package_name(self, obj):
        return obj.base_package.name if obj.base_package else None


class CustomerInquiryDetailSerializer(serializers.ModelSerializer):
    package_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    custom_quote_url = serializers.SerializerMethodField()

    class Meta:
        model = BookingInquiry
        fields = [
            'inquiry_reference', 'package_name',
            'status', 'status_display',
            'preferred_travel_date', 'flexible_dates',
            'number_of_adults', 'number_of_children', 'number_of_infants',
            'budget_range', 'accommodation_preference',
            'dietary_requirements', 'special_requests',
            'custom_quote_url',
            'created_at', 'updated_at',
        ]

    def get_package_name(self, obj):
        return obj.base_package.name if obj.base_package else None

    def get_custom_quote_url(self, obj):
        """Return the secure quote URL if a quote has been sent to this customer."""
        if obj.custom_package and obj.custom_package.status == 'sent':
            request = self.context.get('request')
            from django.urls import reverse
            path = reverse('packages:custom_package_view', kwargs={'token': obj.custom_package.access_token})
            return request.build_absolute_uri(path) if request else path
        return None


class SavedPackageSerializer(serializers.ModelSerializer):
    package = PackageListSerializer(read_only=True)

    class Meta:
        model = SavedPackage
        fields = ['id', 'package', 'created_at']
