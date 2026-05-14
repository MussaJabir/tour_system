from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Booking, BookingInquiry, Package, SavedPackage
from .customer_serializers import (
    CustomerBookingListSerializer,
    CustomerBookingDetailSerializer,
    CustomerInquiryListSerializer,
    CustomerInquiryDetailSerializer,
    SavedPackageSerializer,
)


def _customer_bookings_qs(user):
    """Bookings that belong to this customer (matched by inquiry email)."""
    return (
        Booking.objects
        .select_related('package', 'inquiry')
        .filter(inquiry__customer_email=user.email)
        .order_by('-created_at')
    )


def _customer_inquiries_qs(user):
    """Inquiries submitted with this customer's email."""
    return (
        BookingInquiry.objects
        .select_related('base_package', 'custom_package')
        .filter(customer_email=user.email)
        .order_by('-created_at')
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_booking_list(request):
    """List all bookings for the authenticated customer."""
    bookings = _customer_bookings_qs(request.user)
    serializer = CustomerBookingListSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_booking_detail(request, reference):
    """Booking detail including passengers and payment history."""
    booking = get_object_or_404(
        Booking.objects.prefetch_related('passengers', 'payments'),
        booking_reference=reference,
        inquiry__customer_email=request.user.email,
    )
    serializer = CustomerBookingDetailSerializer(booking)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_inquiry_list(request):
    """List all inquiries submitted by the authenticated customer."""
    inquiries = _customer_inquiries_qs(request.user)
    serializer = CustomerInquiryListSerializer(inquiries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_inquiry_detail(request, reference):
    """Inquiry detail including custom quote link if one was sent."""
    inquiry = get_object_or_404(
        BookingInquiry.objects.select_related('base_package', 'custom_package'),
        inquiry_reference=reference,
        customer_email=request.user.email,
    )
    serializer = CustomerInquiryDetailSerializer(inquiry, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_saved_package_list(request):
    """List all packages saved by the authenticated customer."""
    saved = (
        SavedPackage.objects
        .select_related('package')
        .prefetch_related('package__destinations')
        .filter(user=request.user)
    )
    serializer = SavedPackageSerializer(saved, many=True)
    return Response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def customer_save_package(request, slug):
    """
    POST  — save a package to the customer's list.
    DELETE — remove it.
    """
    package = get_object_or_404(Package, slug=slug, is_active=True)

    if request.method == 'POST':
        saved, created = SavedPackage.objects.get_or_create(
            user=request.user, package=package,
        )
        if not created:
            return Response(
                {'detail': 'Package already saved.'},
                status=status.HTTP_200_OK,
            )
        serializer = SavedPackageSerializer(saved)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # DELETE
    deleted, _ = SavedPackage.objects.filter(
        user=request.user, package=package,
    ).delete()
    if deleted:
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'detail': 'Package was not saved.'}, status=status.HTTP_404_NOT_FOUND)
