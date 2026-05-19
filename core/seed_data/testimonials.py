"""
Testimonial seed data — short reviews from imagined past clients.
Realistic names + countries, neutral ratings. Tour operators can keep,
edit or delete these once real reviews flow in.
"""

TESTIMONIALS = [
    {
        "customer_name": "Sarah Mitchell",
        "customer_location": "London, United Kingdom",
        "rating": 5,
        "quote": (
            "Honestly the trip of a lifetime. The Northern Circuit blew us away — our guide Daniel knew exactly where to "
            "find the lions and gave us a hot-air balloon morning we'll never forget. The Crater Lodge was magical. "
            "Already planning our return."
        ),
        "is_featured": True,
    },
    {
        "customer_name": "Marcus & Emma Bauer",
        "customer_location": "Munich, Germany",
        "rating": 5,
        "quote": (
            "We did the 10-day honeymoon combo with a luxury beach extension at Zuri Zanzibar. Every detail was handled "
            "perfectly. The bush dinner under the stars was the highlight of our wedding year. Vielen Dank!"
        ),
        "is_featured": True,
    },
    {
        "customer_name": "Janet Roberts",
        "customer_location": "Sydney, Australia",
        "rating": 5,
        "quote": (
            "Climbed Kilimanjaro and added a 4-day safari afterwards. The mountain crew were extraordinary — couldn't "
            "have made it to Uhuru without them. The safari afterwards was the perfect reward."
        ),
        "is_featured": False,
    },
    {
        "customer_name": "Pierre & Sophie Lambert",
        "customer_location": "Paris, France",
        "rating": 5,
        "quote": (
            "Notre safari dans le Selous était au-delà de toutes nos attentes. Le boat safari sur le Rufiji a été un "
            "moment magique. Merci pour cette aventure exceptionnelle!"
        ),
        "is_featured": True,
    },
    {
        "customer_name": "Hiroshi Tanaka",
        "customer_location": "Tokyo, Japan",
        "rating": 5,
        "quote": (
            "Family safari with two children aged 8 and 11 — the team's planning for kids was brilliant. The Treetop "
            "Walkway and Maasai school visit made it special for them. Thank you!"
        ),
        "is_featured": False,
    },
    {
        "customer_name": "Amelia Chen",
        "customer_location": "Singapore",
        "rating": 4,
        "quote": (
            "Migration special at Sayari Camp during August. Saw two river crossings in three days — exactly what we "
            "came for. Light aircraft connections were smooth. One small note — the central Serengeti day felt slightly "
            "rushed; otherwise perfect."
        ),
        "is_featured": False,
    },
    {
        "customer_name": "James O'Sullivan",
        "customer_location": "Dublin, Ireland",
        "rating": 5,
        "quote": (
            "The Mahale + Katavi combo was unlike anything I've experienced. Sitting two metres from a wild chimpanzee "
            "in the forest is a different category of memory. Greystoke Mahale is special."
        ),
        "is_featured": False,
    },
    {
        "customer_name": "Lisa Andersson",
        "customer_location": "Stockholm, Sweden",
        "rating": 5,
        "quote": (
            "We chose Tanzania over Kenya because we wanted less-crowded parks. The team built us a custom 9-day southern "
            "itinerary and we saw maybe 4 other vehicles all week. Heaven."
        ),
        "is_featured": False,
    },
    {
        "customer_name": "David & Helen Park",
        "customer_location": "Toronto, Canada",
        "rating": 5,
        "quote": (
            "Best of East Africa — Tanzania, Kenya AND Rwanda gorillas. Two weeks of life-list experiences with one "
            "guide team coordinating everything. Worth every penny."
        ),
        "is_featured": True,
    },
    {
        "customer_name": "Aisha Mwangi",
        "customer_location": "Nairobi, Kenya",
        "rating": 5,
        "quote": (
            "As a Kenyan I've done many safaris, but the Tanzanian Southern Circuit was a revelation. Ruaha's lions, "
            "Selous's wild dogs — both worth the extra effort to get there. Highly recommend."
        ),
        "is_featured": False,
    },
]
