# API Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1. Test if API is Working

Open your browser or use cURL:

```bash
# Browser
http://localhost/api/v1/destinations/

# cURL
curl http://localhost/api/v1/destinations/

# Pretty print with jq
curl http://localhost/api/v1/destinations/ | jq
```

### 2. Import Postman Collection

1. Open Postman
2. Click **Import** → **File**
3. Select `Tour_System_API.postman_collection.json`
4. Set environment variable: `base_url` = `http://localhost/api/v1`

### 3. Test Basic Endpoints

#### Get All Destinations
```http
GET /api/v1/destinations/
```

#### Search for Serengeti
```http
GET /api/v1/destinations/?search=serengeti
```

#### Get Wildlife Packages
```http
GET /api/v1/packages/?package_category=wildlife
```

#### Get 5-Star Lodges
```http
GET /api/v1/accommodations/?star_rating=5&accommodation_type=lodge
```

---

## 📱 Flutter Integration Example

### Install HTTP Package
```yaml
# pubspec.yaml
dependencies:
  http: ^1.1.0
```

### Create API Service
```dart
// lib/services/api_service.dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'http://YOUR_IP:80/api/v1';
  
  // Get all destinations
  Future<List<dynamic>> getDestinations({int page = 1}) async {
    final response = await http.get(
      Uri.parse('$baseUrl/destinations/?page=$page'),
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['results'];
    } else {
      throw Exception('Failed to load destinations');
    }
  }
  
  // Get single destination
  Future<Map<String, dynamic>> getDestination(String slug) async {
    final response = await http.get(
      Uri.parse('$baseUrl/destinations/$slug/'),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load destination');
    }
  }
  
  // Search destinations
  Future<List<dynamic>> searchDestinations(String query) async {
    final response = await http.get(
      Uri.parse('$baseUrl/destinations/?search=$query'),
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['results'];
    } else {
      throw Exception('Search failed');
    }
  }
  
  // Get packages
  Future<List<dynamic>> getPackages({
    String? category,
    double? minPrice,
    double? maxPrice,
    int page = 1,
  }) async {
    String url = '$baseUrl/packages/?page=$page';
    if (category != null) url += '&package_category=$category';
    if (minPrice != null) url += '&min_price=$minPrice';
    if (maxPrice != null) url += '&max_price=$maxPrice';
    
    final response = await http.get(Uri.parse(url));
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['results'];
    } else {
      throw Exception('Failed to load packages');
    }
  }
}
```

### Use in Widget
```dart
// lib/screens/destinations_screen.dart
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class DestinationsScreen extends StatefulWidget {
  @override
  _DestinationsScreenState createState() => _DestinationsScreenState();
}

class _DestinationsScreenState extends State<DestinationsScreen> {
  final ApiService _apiService = ApiService();
  List<dynamic> destinations = [];
  bool isLoading = true;
  
  @override
  void initState() {
    super.initState();
    loadDestinations();
  }
  
  Future<void> loadDestinations() async {
    try {
      final data = await _apiService.getDestinations();
      setState(() {
        destinations = data;
        isLoading = false;
      });
    } catch (e) {
      print('Error: $e');
      setState(() {
        isLoading = false;
      });
    }
  }
  
  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return Scaffold(
        appBar: AppBar(title: Text('Destinations')),
        body: Center(child: CircularProgressIndicator()),
      );
    }
    
    return Scaffold(
      appBar: AppBar(title: Text('Destinations')),
      body: ListView.builder(
        itemCount: destinations.length,
        itemBuilder: (context, index) {
          final dest = destinations[index];
          return ListTile(
            leading: Image.network(
              dest['featured_image'],
              width: 50,
              height: 50,
              fit: BoxFit.cover,
              errorBuilder: (context, error, stackTrace) =>
                  Icon(Icons.image_not_supported),
            ),
            title: Text(dest['name']),
            subtitle: Text(dest['short_description']),
            trailing: Text('${dest['view_count']} views'),
            onTap: () {
              // Navigate to detail screen
            },
          );
        },
      ),
    );
  }
}
```

---

## 🔑 Important Notes for Mobile Development

### 1. **Use Your Computer's IP Address**
Don't use `localhost` or `127.0.0.1` in your Flutter app. Use your actual IP:

```dart
// ❌ Wrong
static const String baseUrl = 'http://localhost/api/v1';

// ✅ Correct (replace with your actual IP)
static const String baseUrl = 'http://192.168.1.100/api/v1';
```

Find your IP:
```bash
# Linux
ip addr show | grep inet

# Your Docker API is accessible at:
http://YOUR_IP:80/api/v1
```

### 2. **Handle Pagination**
All list endpoints return paginated data:

```dart
Future<void> loadMore() async {
  if (nextPage != null) {
    final data = await _apiService.getDestinations(page: nextPage);
    setState(() {
      destinations.addAll(data);
    });
  }
}
```

### 3. **Cache Data**
Use packages like `shared_preferences` or `hive` to cache API responses:

```dart
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

Future<void> cacheDestinations(List<dynamic> destinations) async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setString('destinations', json.encode(destinations));
}

Future<List<dynamic>?> getCachedDestinations() async {
  final prefs = await SharedPreferences.getInstance();
  final cached = prefs.getString('destinations');
  if (cached != null) {
    return json.decode(cached);
  }
  return null;
}
```

### 4. **Handle Errors**
```dart
try {
  final data = await _apiService.getDestinations();
  // Success
} on http.ClientException {
  // Network error
  showError('No internet connection');
} catch (e) {
  // Other errors
  showError('Something went wrong');
}
```

### 5. **Optimize Image Loading**
Use `cached_network_image` for better performance:

```yaml
dependencies:
  cached_network_image: ^3.3.0
```

```dart
import 'package:cached_network_image/cached_network_image.dart';

CachedNetworkImage(
  imageUrl: destination['featured_image'],
  placeholder: (context, url) => CircularProgressIndicator(),
  errorWidget: (context, url, error) => Icon(Icons.error),
)
```

---

## 📊 API Performance Tips

### 1. **Use Filtering**
Don't fetch everything, use filters:

```dart
// ❌ Bad: Fetch all packages then filter in app
final allPackages = await getPackages();
final wildlife = allPackages.where((p) => p['category'] == 'wildlife');

// ✅ Good: Filter on server
final wildlife = await getPackages(category: 'wildlife');
```

### 2. **Lazy Load Images**
Load images only when needed:

```dart
ListView.builder(
  itemBuilder: (context, index) {
    // Image loads only when visible
    return Image.network(destinations[index]['featured_image']);
  },
)
```

### 3. **Implement Pull-to-Refresh**
```dart
RefreshIndicator(
  onRefresh: () async {
    await loadDestinations();
  },
  child: ListView.builder(...),
)
```

---

## 🐛 Testing Checklist

- [ ] Can fetch destinations list
- [ ] Can fetch single destination details
- [ ] Can search destinations
- [ ] Can filter by country/region
- [ ] Can fetch activities
- [ ] Can fetch accommodations
- [ ] Can fetch packages
- [ ] Can filter packages by category
- [ ] Can handle pagination
- [ ] Images load correctly
- [ ] Error handling works
- [ ] Network timeout handling
- [ ] Cache works offline

---

## 🔧 Troubleshooting

### Issue: Can't connect to API from Flutter
**Solution**: 
1. Make sure you're using your computer's IP, not `localhost`
2. Ensure both devices are on the same network
3. Check firewall settings

### Issue: Images not loading
**Solution**:
1. Check image URLs are absolute (including domain)
2. Use `http://YOUR_IP/media/...` format
3. Handle missing images with errorBuilder

### Issue: CORS errors (if using web)
**Solution**: Add CORS headers in Django settings:

```python
# settings.py
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE
CORS_ALLOW_ALL_ORIGINS = True  # For development only
```

---

## 📚 Next Steps

1. **Authentication**: Add user login/registration
2. **Bookings**: Implement booking submission
3. **Payments**: Integrate payment gateway
4. **Push Notifications**: Add Firebase for notifications
5. **Offline Mode**: Implement local database with SQLite/Hive

---

## 📞 Support

- **Full Documentation**: See `API_DOCUMENTATION.md`
- **Postman Collection**: Import `Tour_System_API.postman_collection.json`
- **API Browsable Interface**: Visit `http://localhost/api/v1/` in browser

---

**Last Updated**: November 15, 2025

