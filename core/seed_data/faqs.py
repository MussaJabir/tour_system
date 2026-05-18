"""
FAQ seed data — common questions from Tanzania safari customers, with
honest neutral answers. Operators should edit these to reflect their
own policies before going live.
"""

# FAQ category choices in core.models.FAQ:
#   general, booking, payment, destinations, travel, safety, cancellation
FAQS = [
    {
        "category": "booking",
        "question": "How far in advance should I book my Tanzanian safari?",
        "answer": (
            "For peak migration season (July-October) we recommend booking 9-12 months in advance — the best camps and "
            "guides fill up early. For shoulder seasons (November-December, February-March) 4-6 months is usually fine. "
            "Last-minute bookings (under 2 months) are sometimes possible but choice of lodges becomes very limited."
        ),
        "is_featured": True,
        "order": 1,
    },
    {
        "category": "cancellation",
        "question": "What is your cancellation policy?",
        "answer": (
            "Cancellation terms depend on the lodges we've reserved on your behalf — most lodges have a tiered policy: "
            "full refund 60+ days before arrival, 50% refund 30-59 days before, no refund within 29 days. We pass these "
            "terms through transparently and strongly recommend travel insurance that includes trip cancellation cover."
        ),
        "is_featured": True,
        "order": 2,
    },
    {
        "category": "travel",
        "question": "When is the best time to visit Tanzania?",
        "answer": (
            "It depends on what you want to see. July-October: peak migration river crossings in the northern Serengeti, "
            "dry season game viewing across all parks (best for first-time visitors). January-March: wildebeest calving "
            "in southern Serengeti, also dry. April-May: long rains — many camps close, but rates drop and the bush is "
            "stunningly green. June: shoulder season, excellent value. November: short rains, often brief afternoon showers."
        ),
        "is_featured": True,
        "order": 3,
    },
    {
        "category": "travel",
        "question": "Do I need a visa for Tanzania?",
        "answer": (
            "Most nationalities need a visa. Tanzania offers visa-on-arrival at Kilimanjaro International (KIA), Julius "
            "Nyerere International (DAR) and Zanzibar International (ZNZ) for around USD $50 (USD $100 for US citizens). "
            "Bring crisp USD bills printed after 2009. E-visas are also available in advance — recommended for "
            "smoother arrival. Check the latest visa requirements for your nationality before travelling."
        ),
        "is_featured": False,
        "order": 4,
    },
    {
        "category": "safety",
        "question": "What vaccinations do I need?",
        "answer": (
            "Yellow Fever vaccination certificate is required if arriving from a Yellow Fever-endemic country (most of "
            "Africa and parts of South America). Recommended (not required) vaccinations include Hepatitis A and B, "
            "typhoid, tetanus, and routine boosters. Malaria prophylaxis is strongly recommended — talk to your travel "
            "doctor 6 weeks before departure. We are not medical professionals; always consult a qualified travel clinic."
        ),
        "is_featured": True,
        "order": 5,
    },
    {
        "category": "safety",
        "question": "Is Tanzania safe for tourists?",
        "answer": (
            "Tanzania is one of East Africa's most stable countries and tourism is the second-largest contributor to "
            "GDP. Crime against tourists is rare in safari areas. Common-sense precautions apply in Dar es Salaam and "
            "Arusha (don't flash valuables, use registered taxis at night). On safari you are with a professional guide "
            "at all times. Most issues travellers face are health-related (stomach bugs, sun) — drink bottled water, "
            "wear sunscreen, take it easy on local food the first day."
        ),
        "is_featured": False,
        "order": 6,
    },
    {
        "category": "payment",
        "question": "What currency should I bring?",
        "answer": (
            "US Dollars are widely accepted for safari payments, park fees and large transactions. Bring crisp notes "
            "printed after 2009 — older notes are often refused. Tanzanian Shillings (TZS) are useful for small "
            "purchases, tips at local restaurants and curio markets. ATMs are available in major towns. Most lodges "
            "accept Visa/Mastercard, but expect 3-5% surcharges. Tips for guides and lodge staff are best in USD cash."
        ),
        "is_featured": False,
        "order": 7,
    },
    {
        "category": "payment",
        "question": "How much should I tip?",
        "answer": (
            "Tipping is expected and meaningful for the local economy. Guidelines per person per day: safari guide "
            "$15-25, lodge staff $10-15 (pooled tip given to the camp manager). For Kilimanjaro climbs: $250-350 total "
            "across the crew per climber. For Rwanda gorilla trek: $20-30 for the porter, $10-15 for the tracker, "
            "$10-15 for the ranger team. Carry a stack of small USD bills."
        ),
        "is_featured": False,
        "order": 8,
    },
    {
        "category": "travel",
        "question": "What should I pack for a safari?",
        "answer": (
            "Neutral colours (beige, olive, khaki) — avoid bright colours and pure white. Layers for cool mornings and "
            "warm midday. Long sleeves and trousers for early/late game drives (mosquitoes, sun). Closed-toe shoes for "
            "walking safaris. Wide-brimmed hat, sunglasses, high-SPF sunscreen, insect repellent with DEET. Binoculars "
            "essential — share between two people is fine. Camera with a 300mm+ zoom lens highly recommended. Small "
            "torch / headlamp for tent camps."
        ),
        "is_featured": True,
        "order": 9,
    },
    {
        "category": "travel",
        "question": "What's the airport situation? Where do I fly in?",
        "answer": (
            "For northern Tanzania safaris (Serengeti, Ngorongoro, Tarangire, Manyara) fly into Kilimanjaro International "
            "Airport (JRO/KIA) — 30 minutes from Arusha town. For Kilimanjaro climbs, also KIA. For southern Tanzania "
            "(Selous/Nyerere, Ruaha, Mikumi) fly into Julius Nyerere International (DAR) in Dar es Salaam. For Zanzibar, "
            "fly into Zanzibar International (ZNZ). Light-aircraft connections between safari camps are common — we book "
            "these as part of your itinerary."
        ),
        "is_featured": False,
        "order": 10,
    },
    {
        "category": "travel",
        "question": "Can I do a self-drive safari in Tanzania?",
        "answer": (
            "Technically yes, in some parks, but it is not recommended for first-time visitors. Roads are often unmarked, "
            "ranger checkpoints require paperwork, recovery from a stuck vehicle is on you, and a professional guide is "
            "the difference between seeing a lion and driving past one. We exclusively use professional guide-driven "
            "open-sided 4x4s."
        ),
        "is_featured": False,
        "order": 11,
    },
    {
        "category": "general",
        "question": "Can you customise an itinerary for me?",
        "answer": (
            "Yes — every itinerary on our site is a starting point. We routinely build fully bespoke trips around our "
            "clients' budget, travel dates, fitness level, special interests (photography, birding, families, religious "
            "groups, etc.), and special-occasion needs (honeymoons, anniversaries). Send us an enquiry with your "
            "preferred dates and a budget range and we'll come back to you within 24 hours."
        ),
        "is_featured": True,
        "order": 12,
    },
]
