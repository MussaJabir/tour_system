# Tour System API Documentation

## Overview
Welcome to the Tour System API documentation. This RESTful API is built with Django REST Framework and provides comprehensive endpoints for managing tours, destinations, accommodations, activities, and bookings.

**Base URL**: `http://localhost/api/v1/`  
**Production URL**: `https://yourdomain.com/api/v1/`

---

## Table of Contents
1. [Authentication](#authentication)
2. [Rate Limiting](#rate-limiting)
3. [Pagination](#pagination)
4. [Filtering & Search](#filtering--search)
5. [Response Format](#response-format)
6. [Error Handling](#error-handling)
7. [Endpoints](#endpoints)
   - [Destinations](#destinations-api)
   - [Activities](#activities-api)
   - [Accommodations](#accommodations-api)
   - [Packages](#packages-api)
8. [Postman Collection](#postman-collection)

---

## Authentication

### Current Setup
- **Type**: Session Authentication
- **Read Access**: Public (no authentication required)
- **Write Access**: Requires authentication (staff/admin users)

### For Mobile Apps (Recommended Addition)
For your Flutter app, you should add **Token Authentication**:

```bash
# Login to get token (you'll need to add this endpoint)
POST /api/v1/auth/login/
{
  "username": "your_username",
  "password": "your_password"
}

# Response
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  }
}

# Use token in headers
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

## Rate Limiting

**Anonymous Users**: 100 requests/hour  
**Authenticated Users**: 1000 requests/hour

When rate limit is exceeded, you'll receive:
```json
{
  "detail": "Request was throttled. Expected available in 3600 seconds."
}
```

---

## Pagination

All list endpoints are paginated with **20 items per page** by default.

### Request
```
GET /api/v1/destinations/?page=2
```

### Response Structure
```json
{
  "count": 150,
  "next": "http://localhost/api/v1/destinations/?page=3",
  "previous": "http://localhost/api/v1/destinations/?page=1",
  "results": [
    { /* destination object */ }
  ]
}
```

### Custom Page Size
```
GET /api/v1/destinations/?page_size=50
```

---

## Filtering & Search

### Filtering
```
# Filter by specific fields
GET /api/v1/destinations/?country=Tanzania
GET /api/v1/destinations/?is_featured=true
GET /api/v1/accommodations/?accommodation_type=lodge
```

### Search
```
# Search across multiple fields
GET /api/v1/destinations/?search=serengeti
GET /api/v1/activities/?search=safari
```

### Ordering
```
# Order by specific fields (use - for descending)
GET /api/v1/destinations/?ordering=name
GET /api/v1/destinations/?ordering=-view_count
GET /api/v1/packages/?ordering=-created_at
```

### Combined Filters
```
GET /api/v1/destinations/?country=Tanzania&is_featured=true&ordering=-view_count
```

---

## Response Format

### Success Response (200 OK)
```json
{
  "id": 1,
  "name": "Serengeti National Park",
  "slug": "serengeti-national-park",
  "description": "...",
  "created_at": "2025-11-15T10:30:00Z"
}
```

### Created Response (201 Created)
```json
{
  "id": 5,
  "name": "New Destination",
  "slug": "new-destination",
  "message": "Created successfully"
}
```

---

## Error Handling

### 400 Bad Request
```json
{
  "field_name": [
    "This field is required."
  ]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

---

# Endpoints

## Destinations API

### 1. List All Destinations
**Endpoint**: `GET /api/v1/destinations/`  
**Authentication**: Not required  
**Description**: Get paginated list of all active destinations

#### Request
```bash
curl -X GET "http://localhost/api/v1/destinations/" \
  -H "Accept: application/json"
```

#### Response (200 OK)
```json
{
  "count": 25,
  "next": "http://localhost/api/v1/destinations/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Serengeti National Park",
      "slug": "serengeti-national-park",
      "short_description": "Home to the Great Migration",
      "country": "Tanzania",
      "region": "Northern Circuit",
      "featured_image": "http://localhost/media/destinations/serengeti.jpg",
      "is_featured": true,
      "view_count": 1250,
      "absolute_url": "/destinations/serengeti-national-park/",
      "image_count": 15
    }
  ]
}
```

### 2. Get Single Destination
**Endpoint**: `GET /api/v1/destinations/{slug}/`  
**Authentication**: Not required

#### Request
```bash
curl -X GET "http://localhost/api/v1/destinations/serengeti-national-park/" \
  -H "Accept: application/json"
```

#### Response (200 OK)
```json
{
  "id": 1,
  "name": "Serengeti National Park",
  "slug": "serengeti-national-park",
  "description": "Detailed description...",
  "short_description": "Home to the Great Migration",
  "country": "Tanzania",
  "region": "Northern Circuit",
  "latitude": "-2.3333",
  "longitude": "34.8333",
  "best_time_to_visit": "June to October",
  "climate": "Tropical savanna climate",
  "featured_image": "http://localhost/media/destinations/serengeti.jpg",
  "video_url": "https://youtube.com/watch?v=...",
  "is_featured": true,
  "is_active": true,
  "view_count": 1250,
  "gallery_images": [
    {
      "id": 1,
      "image": "http://localhost/media/destination_images/serengeti_1.jpg",
      "caption": "Wildebeest migration",
      "order": 1,
      "uploaded_at": "2025-11-15T10:30:00Z"
    }
  ],
  "accommodation_count": 12,
  "activity_count": 8,
  "package_count": 5,
  "created_at": "2025-11-01T10:00:00Z",
  "updated_at": "2025-11-15T10:30:00Z"
}
```

### 3. Get Featured Destinations
**Endpoint**: `GET /api/v1/destinations/featured/`  
**Authentication**: Not required

#### Request
```bash
curl -X GET "http://localhost/api/v1/destinations/featured/" \
  -H "Accept: application/json"
```

#### Response (200 OK)
```json
[
  {
    "id": 1,
    "name": "Serengeti National Park",
    "slug": "serengeti-national-park",
    "short_description": "Home to the Great Migration",
    "featured_image": "http://localhost/media/destinations/serengeti.jpg",
    "view_count": 1250
  }
]
```

### 4. Search Destinations
**Endpoint**: `GET /api/v1/destinations/?search={query}`  
**Authentication**: Not required

#### Request
```bash
curl -X GET "http://localhost/api/v1/destinations/?search=serengeti" \
  -H "Accept: application/json"
```

### 5. Filter Destinations
**Endpoint**: `GET /api/v1/destinations/?{filter_param}={value}`  
**Authentication**: Not required

#### Available Filters
- `country` - Filter by country (e.g., Tanzania, Kenya)
- `region` - Filter by region
- `is_featured` - true/false

#### Request Examples
```bash
# Get all destinations in Tanzania
curl -X GET "http://localhost/api/v1/destinations/?country=Tanzania"

# Get all featured destinations
curl -X GET "http://localhost/api/v1/destinations/?is_featured=true"

# Get destinations in Northern Circuit region
curl -X GET "http://localhost/api/v1/destinations/?region=Northern%20Circuit"
```

### 6. Create Destination (Admin Only)
**Endpoint**: `POST /api/v1/destinations/`  
**Authentication**: Required (Staff)

#### Request
```bash
curl -X POST "http://localhost/api/v1/destinations/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{
    "name": "Ngorongoro Crater",
    "description": "A large volcanic caldera...",
    "short_description": "UNESCO World Heritage Site",
    "country": "Tanzania",
    "region": "Northern Circuit",
    "latitude": "-3.1745",
    "longitude": "35.5562",
    "best_time_to_visit": "Year-round",
    "is_featured": true
  }'
```

#### Response (201 Created)
```json
{
  "id": 26,
  "name": "Ngorongoro Crater",
  "slug": "ngorongoro-crater",
  "message": "Destination created successfully"
}
```

### 7. Update Destination (Admin Only)
**Endpoint**: `PUT /api/v1/destinations/{slug}/` or `PATCH /api/v1/destinations/{slug}/`  
**Authentication**: Required (Staff)

#### Request (PATCH - partial update)
```bash
curl -X PATCH "http://localhost/api/v1/destinations/ngorongoro-crater/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{
    "is_featured": false,
    "view_count": 100
  }'
```

### 8. Delete Destination (Admin Only)
**Endpoint**: `DELETE /api/v1/destinations/{slug}/`  
**Authentication**: Required (Staff)

#### Request
```bash
curl -X DELETE "http://localhost/api/v1/destinations/ngorongoro-crater/" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

#### Response (204 No Content)

---

## Activities API

### 1. List All Activities
**Endpoint**: `GET /api/v1/activities/`  
**Authentication**: Not required

#### Request
```bash
curl -X GET "http://localhost/api/v1/activities/" \
  -H "Accept: application/json"
```

#### Response (200 OK)
```json
{
  "count": 30,
  "next": "http://localhost/api/v1/activities/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Game Drive",
      "slug": "game-drive",
      "short_description": "Experience wildlife up close",
      "activity_type": "wildlife",
      "duration": "4-6 hours",
      "difficulty_level": "easy",
      "min_age": 5,
      "featured_image": "http://localhost/media/activities/game_drive.jpg",
      "is_featured": true,
      "view_count": 856,
      "destination": {
        "id": 1,
        "name": "Serengeti National Park",
        "slug": "serengeti-national-park"
      }
    }
  ]
}
```

### 2. Get Single Activity
**Endpoint**: `GET /api/v1/activities/{slug}/`  
**Authentication**: Not required

#### Response (200 OK)
```json
{
  "id": 1,
  "name": "Game Drive",
  "slug": "game-drive",
  "description": "Full description...",
  "short_description": "Experience wildlife up close",
  "activity_type": "wildlife",
  "duration": "4-6 hours",
  "difficulty_level": "easy",
  "min_age": 5,
  "max_group_size": 6,
  "included_items": "Park fees, Guide, Refreshments",
  "excluded_items": "Personal expenses",
  "requirements": "Valid passport, Comfortable clothing",
  "featured_image": "http://localhost/media/activities/game_drive.jpg",
  "video_url": null,
  "is_featured": true,
  "is_active": true,
  "view_count": 856,
  "destination": {
    "id": 1,
    "name": "Serengeti National Park",
    "slug": "serengeti-national-park",
    "country": "Tanzania"
  },
  "gallery_images": [
    {
      "id": 5,
      "image": "http://localhost/media/activity_images/game_drive_1.jpg",
      "caption": "Lion sighting",
      "order": 1
    }
  ],
  "created_at": "2025-11-01T10:00:00Z",
  "updated_at": "2025-11-15T10:30:00Z"
}
```

### 3. Filter Activities
**Available Filters**:
- `activity_type` - wildlife, cultural, adventure, water_sports, etc.
- `difficulty_level` - easy, moderate, challenging, extreme
- `destination` - Filter by destination ID
- `is_featured` - true/false

#### Request Examples
```bash
# Get all wildlife activities
curl -X GET "http://localhost/api/v1/activities/?activity_type=wildlife"

# Get easy activities
curl -X GET "http://localhost/api/v1/activities/?difficulty_level=easy"

# Get activities for a specific destination
curl -X GET "http://localhost/api/v1/activities/?destination=1"
```

---

## Accommodations API

### 1. List All Accommodations
**Endpoint**: `GET /api/v1/accommodations/`  
**Authentication**: Not required

#### Request
```bash
curl -X GET "http://localhost/api/v1/accommodations/" \
  -H "Accept: application/json"
```

#### Response (200 OK)
```json
{
  "count": 45,
  "next": "http://localhost/api/v1/accommodations/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Serena Safari Lodge",
      "slug": "serena-safari-lodge",
      "short_description": "Luxury lodge in the heart of Serengeti",
      "accommodation_type": "lodge",
      "star_rating": 5,
      "destination": {
        "id": 1,
        "name": "Serengeti National Park",
        "slug": "serengeti-national-park"
      },
      "price_per_night_min": 350.00,
      "price_per_night_max": 650.00,
      "currency": "USD",
      "featured_image": "http://localhost/media/accommodations/serena_lodge.jpg",
      "is_featured": true,
      "view_count": 432,
      "total_rooms": 75,
      "available_rooms_count": 12
    }
  ]
}
```

### 2. Get Single Accommodation
**Endpoint**: `GET /api/v1/accommodations/{slug}/`  
**Authentication**: Not required

#### Response (200 OK)
```json
{
  "id": 1,
  "name": "Serena Safari Lodge",
  "slug": "serena-safari-lodge",
  "description": "Full description...",
  "short_description": "Luxury lodge in the heart of Serengeti",
  "accommodation_type": "lodge",
  "star_rating": 5,
  "destination": {
    "id": 1,
    "name": "Serengeti National Park",
    "slug": "serengeti-national-park"
  },
  "address": "Central Serengeti, Tanzania",
  "latitude": "-2.3333",
  "longitude": "34.8333",
  "phone": "+255 123 456 789",
  "email": "info@serenalodge.com",
  "website": "https://serenalodge.com",
  "total_rooms": 75,
  "price_per_night_min": 350.00,
  "price_per_night_max": 650.00,
  "currency": "USD",
  "check_in_time": "2:00 PM",
  "check_out_time": "11:00 AM",
  "amenities": "WiFi, Swimming Pool, Restaurant, Bar, Spa",
  "policies": "Cancellation policy...",
  "featured_image": "http://localhost/media/accommodations/serena_lodge.jpg",
  "video_url": "https://youtube.com/watch?v=...",
  "is_featured": true,
  "is_active": true,
  "view_count": 432,
  "gallery_images": [
    {
      "id": 10,
      "image": "http://localhost/media/accommodation_images/serena_1.jpg",
      "caption": "Main lobby",
      "order": 1
    }
  ],
  "rooms": [
    {
      "id": 1,
      "name": "Deluxe Room",
      "room_type": "deluxe",
      "description": "Spacious room with park views",
      "max_occupancy": 2,
      "bed_type": "king",
      "number_of_beds": 1,
      "size_sqm": 45,
      "price_per_night": 350.00,
      "amenities": "AC, TV, Mini-bar, Safe",
      "is_available": true,
      "image": "http://localhost/media/rooms/deluxe_room.jpg"
    }
  ],
  "created_at": "2025-11-01T10:00:00Z",
  "updated_at": "2025-11-15T10:30:00Z"
}
```

### 3. Filter Accommodations
**Available Filters**:
- `accommodation_type` - hotel, lodge, camp, resort, guesthouse, other
- `star_rating` - 1, 2, 3, 4, 5
- `destination` - Filter by destination ID
- `is_featured` - true/false
- `min_price` - Minimum price per night
- `max_price` - Maximum price per night

#### Request Examples
```bash
# Get all lodges
curl -X GET "http://localhost/api/v1/accommodations/?accommodation_type=lodge"

# Get 5-star accommodations
curl -X GET "http://localhost/api/v1/accommodations/?star_rating=5"

# Get accommodations within price range
curl -X GET "http://localhost/api/v1/accommodations/?min_price=200&max_price=500"
```

### 4. List Rooms
**Endpoint**: `GET /api/v1/rooms/`  
**Authentication**: Not required

#### Request
```bash
curl -X GET "http://localhost/api/v1/rooms/?accommodation=1" \
  -H "Accept: application/json"
```

---

## Packages API

### 1. List All Packages
**Endpoint**: `GET /api/v1/packages/`  
**Authentication**: Not required

#### Request
```bash
curl -X GET "http://localhost/api/v1/packages/" \
  -H "Accept: application/json"
```

#### Response (200 OK)
```json
{
  "count": 20,
  "next": "http://localhost/api/v1/packages/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "5-Day Serengeti Safari",
      "slug": "5-day-serengeti-safari",
      "short_description": "Experience the best of Serengeti",
      "duration_days": 5,
      "duration_nights": 4,
      "price_per_person": 2500.00,
      "currency": "USD",
      "destinations": [
        {
          "id": 1,
          "name": "Serengeti National Park",
          "slug": "serengeti-national-park"
        }
      ],
      "featured_image": "http://localhost/media/packages/serengeti_safari.jpg",
      "is_featured": true,
      "view_count": 678,
      "difficulty_level": "moderate",
      "package_category": "wildlife",
      "group_size_min": 2,
      "group_size_max": 6
    }
  ]
}
```

### 2. Get Single Package
**Endpoint**: `GET /api/v1/packages/{slug}/`  
**Authentication**: Not required

#### Response (200 OK)
```json
{
  "id": 1,
  "name": "5-Day Serengeti Safari",
  "slug": "5-day-serengeti-safari",
  "description": "Full detailed description...",
  "short_description": "Experience the best of Serengeti",
  "duration_days": 5,
  "duration_nights": 4,
  "price_per_person": 2500.00,
  "currency": "USD",
  "destinations": [
    {
      "id": 1,
      "name": "Serengeti National Park",
      "slug": "serengeti-national-park",
      "country": "Tanzania"
    }
  ],
  "included_items": "Accommodation, Meals, Park fees, Guide",
  "excluded_items": "International flights, Visa, Tips",
  "requirements": "Valid passport, Yellow fever certificate",
  "terms_and_conditions": "Full terms...",
  "cancellation_policy": "Free cancellation 30 days before...",
  "featured_image": "http://localhost/media/packages/serengeti_safari.jpg",
  "video_url": "https://youtube.com/watch?v=...",
  "is_featured": true,
  "is_active": true,
  "view_count": 678,
  "difficulty_level": "moderate",
  "package_category": "wildlife",
  "group_size_min": 2,
  "group_size_max": 6,
  "max_bookings": 50,
  "available_bookings": 35,
  "is_customizable": true,
  "itineraries": [
    {
      "id": 1,
      "day_number": 1,
      "end_day_number": null,
      "day_display": "Day 1",
      "title": "Arrival in Arusha",
      "description": "Meet and greet at the airport...",
      "location": "Arusha",
      "accommodation": {
        "id": 5,
        "name": "Arusha Coffee Lodge",
        "type": "lodge"
      },
      "activities": "City tour, Welcome dinner",
      "breakfast_included": false,
      "lunch_included": true,
      "dinner_included": true,
      "transport_details": "Private 4x4 Land Cruiser",
      "distance": "50km",
      "drive_time": "1 hour",
      "featured_image": "http://localhost/media/itinerary/day1.jpg",
      "order": 1
    }
  ],
  "gallery_images": [
    {
      "id": 15,
      "image": "http://localhost/media/package_images/safari_1.jpg",
      "caption": "Lions in Serengeti",
      "order": 1
    }
  ],
  "created_at": "2025-11-01T10:00:00Z",
  "updated_at": "2025-11-15T10:30:00Z"
}
```

### 3. Filter Packages
**Available Filters**:
- `package_category` - wildlife, cultural, adventure, honeymoon, family, luxury, budget
- `difficulty_level` - easy, moderate, challenging, extreme
- `min_price` - Minimum price per person
- `max_price` - Maximum price per person
- `duration_days` - Filter by duration
- `is_featured` - true/false
- `is_customizable` - true/false

#### Request Examples
```bash
# Get wildlife packages
curl -X GET "http://localhost/api/v1/packages/?package_category=wildlife"

# Get packages within price range
curl -X GET "http://localhost/api/v1/packages/?min_price=2000&max_price=3000"

# Get 5-day packages
curl -X GET "http://localhost/api/v1/packages/?duration_days=5"

# Get customizable packages
curl -X GET "http://localhost/api/v1/packages/?is_customizable=true"
```

### 4. Get Package Itineraries
**Endpoint**: `GET /api/v1/package-itineraries/?package={package_id}`  
**Authentication**: Not required

#### Request
```bash
curl -X GET "http://localhost/api/v1/package-itineraries/?package=1" \
  -H "Accept: application/json"
```

### 5. Submit Booking Inquiry
**Endpoint**: `POST /api/v1/booking-inquiry/`  
**Authentication**: Not required (Public)

#### Request
```bash
curl -X POST "http://localhost/api/v1/booking-inquiry/" \
  -H "Content-Type: application/json" \
  -d '{
    "base_package": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "country": "USA",
    "number_of_adults": 2,
    "number_of_children": 1,
    "preferred_start_date": "2025-12-15",
    "message": "Looking forward to this trip!",
    "special_requirements": "Vegetarian meals"
  }'
```

#### Response (201 Created)
```json
{
  "id": 50,
  "inquiry_reference": "INQ-20251115-00050",
  "message": "Inquiry submitted successfully. We'll contact you within 24 hours."
}
```

---

## Image Management APIs

### Destination Images
**Endpoint**: `GET /api/v1/destination-images/?destination={destination_id}`

### Activity Images
**Endpoint**: `GET /api/v1/activity-images/?activity={activity_id}`

### Accommodation Images
**Endpoint**: `GET /api/v1/accommodation-images/?accommodation={accommodation_id}`

---

## Postman Collection

### Quick Import
Create a Postman collection with these settings:

**Collection Name**: Tour System API  
**Base URL Variable**: `{{base_url}}` = `http://localhost/api/v1`

### Example Requests for Postman

#### 1. Get All Destinations
```
GET {{base_url}}/destinations/
```

#### 2. Search Destinations
```
GET {{base_url}}/destinations/?search=serengeti
```

#### 3. Get Single Destination
```
GET {{base_url}}/destinations/serengeti-national-park/
```

#### 4. Filter Packages by Category
```
GET {{base_url}}/packages/?package_category=wildlife&is_featured=true
```

#### 5. Submit Booking Inquiry
```
POST {{base_url}}/booking-inquiry/
Body (JSON):
{
  "base_package": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "number_of_adults": 2,
  "preferred_start_date": "2025-12-15"
}
```

### Postman Environment Variables
```json
{
  "base_url": "http://localhost/api/v1",
  "auth_token": "YOUR_TOKEN_HERE"
}
```

---

## Performance & Optimization

### Can APIs Handle Large Requests?

**YES**, but with considerations:

1. **Pagination**: All list endpoints are paginated (20 items/page)
2. **Rate Limiting**: 
   - Anonymous: 100 requests/hour
   - Authenticated: 1000 requests/hour
3. **Database Indexing**: All models have proper database indexes on:
   - slug fields
   - foreign keys
   - frequently filtered fields
4. **Image Optimization**: Images should be properly sized on the backend

### Best Practices for Mobile Apps

1. **Use Pagination**: Don't try to fetch all records at once
2. **Cache Responses**: Cache frequently accessed data (destinations, activities)
3. **Lazy Load Images**: Load images on demand, not all at once
4. **Use Filtering**: Fetch only what you need
5. **Handle Rate Limits**: Implement exponential backoff
6. **Optimize Queries**: Use specific endpoints rather than fetching everything

---

## Recommended Improvements for Mobile App

### 1. Add Token Authentication
Currently using session auth. For mobile apps, add:

```python
# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # Add this
        'rest_framework.authentication.SessionAuthentication',
    ],
}
```

### 2. Add User Registration & Login Endpoints
Create endpoints for:
- `/api/v1/auth/register/`
- `/api/v1/auth/login/`
- `/api/v1/auth/logout/`
- `/api/v1/auth/profile/`

### 3. Add Booking Management
- `POST /api/v1/bookings/` - Create booking
- `GET /api/v1/bookings/` - List user's bookings
- `GET /api/v1/bookings/{id}/` - Booking details
- `PATCH /api/v1/bookings/{id}/cancel/` - Cancel booking

### 4. Add Payment Integration
- `POST /api/v1/payments/` - Process payment
- `GET /api/v1/payments/{id}/status/` - Payment status

### 5. Add Reviews & Ratings
- `POST /api/v1/reviews/` - Submit review
- `GET /api/v1/reviews/?package={id}` - Get package reviews

---

## Testing the API

### Using cURL
```bash
# Test if API is working
curl http://localhost/api/v1/destinations/

# Pretty print with jq
curl http://localhost/api/v1/destinations/ | jq
```

### Using Python
```python
import requests

# Get all destinations
response = requests.get('http://localhost/api/v1/destinations/')
destinations = response.json()

print(f"Total: {destinations['count']}")
for dest in destinations['results']:
    print(f"- {dest['name']}")
```

### Using Flutter (Dart)
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<List<dynamic>> fetchDestinations() async {
  final response = await http.get(
    Uri.parse('http://localhost/api/v1/destinations/'),
  );

  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    return data['results'];
  } else {
    throw Exception('Failed to load destinations');
  }
}
```

---

## Support & Contact

For API issues or questions:
- **Documentation**: This file
- **API Browsable Interface**: `http://localhost/api/v1/` (in browser)
- **Backend Team**: Your team

---

## Changelog

### Version 1.0.0 (2025-11-15)
- Initial API release
- Destinations, Activities, Accommodations, Packages endpoints
- Pagination, filtering, search support
- Rate limiting implemented

---

**Last Updated**: November 15, 2025  
**API Version**: 1.0.0  
**Django Version**: 5.1.3  
**DRF Version**: 3.15.2

