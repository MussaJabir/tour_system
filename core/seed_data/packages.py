"""
Tour package seed data. Each package has an `itinerary` list — each entry
becomes a PackageItinerary row. `destination_slugs` are M2M lookups;
`accommodation_slug` on an itinerary entry is the FK for that night's stay.
"""

PACKAGES = [
    # =========================================================================
    {
        "name": "Northern Circuit Classic — 7 Days",
        "category": "wildlife",
        "difficulty": "easy",
        "duration_days": 7,
        "duration_nights": 6,
        "group_min": 2,
        "group_max": 8,
        "price_per_person": "2950.00",
        "currency": "USD",
        "destination_slugs": [
            "tarangire-national-park",
            "lake-manyara-national-park",
            "serengeti-national-park",
            "ngorongoro-crater",
        ],
        "short_description": "The quintessential Tanzanian safari — Tarangire's elephants, Manyara's tree-climbing lions, the Serengeti plains and the Ngorongoro Crater in seven unhurried days.",
        "description": (
            "Our flagship Northern Circuit covers the four classic parks of northern Tanzania in seven days, with two "
            "full nights in the Serengeti to make the most of the wildlife capital of Africa. The pace is unhurried — "
            "you spend each morning and afternoon out in the bush with your private guide in an open-sided 4x4, returning "
            "to mid-range tented camps and lodges for the night. This itinerary works year-round, with the Serengeti "
            "delivering exceptional wildlife in every season. Suitable for first-time safari travellers, families with "
            "children over 8, and couples."
        ),
        "highlights": (
            "Two nights in central Serengeti — heart of big-cat country\n"
            "Full day in the Ngorongoro Crater — chance to see all of the Big Five\n"
            "Tarangire's famous elephant herds and ancient baobab trees\n"
            "Optional hot-air balloon safari upgrade\n"
            "Private guide and 4x4 throughout"
        ),
        "included": (
            "All park and conservation fees\n"
            "Six nights accommodation as specified (mid-range tented camps and lodges)\n"
            "Private custom-fitted 4x4 with pop-up roof and English-speaking guide\n"
            "All meals on safari (breakfast, lunch, dinner) and water\n"
            "Airport transfers (KIA)\n"
            "Game drives as per itinerary\n"
            "Government taxes"
        ),
        "excluded": (
            "International flights\n"
            "Tanzania entry visa ($50-100 depending on nationality)\n"
            "Travel insurance (required)\n"
            "Tips for guide and lodge staff ($15-25/day pp recommended)\n"
            "Alcoholic and premium drinks\n"
            "Optional balloon safari ($580/pp)\n"
            "Personal expenses"
        ),
        "requirements": "Valid passport (6+ months), Yellow Fever certificate if arriving from a YF country, malaria prophylaxis recommended, basic mobility for 4x4 entry/exit.",
        "is_featured": True,
        "is_customizable": True,
        "image_slug": "serengeti-national-park-2",
        "image_dir": "destinations",
        "itinerary": [
            {
                "day": 1, "title": "Arrival in Arusha",
                "description": "Met at Kilimanjaro International Airport and transferred to your Arusha lodge (~30 min). Welcome dinner and trip briefing with your guide. Overnight at a coffee-plantation lodge in the foothills of Mt Meru.",
                "accommodation_slug": "legendary-lodge", "breakfast": False, "lunch": False, "dinner": True,
                "highlights": "Welcome briefing, recovery from international flights",
            },
            {
                "day": 2, "title": "Tarangire National Park",
                "description": "After breakfast, drive 2.5 hours to Tarangire National Park (lunch en route). Afternoon game drive among the baobabs and along the river — Tarangire is home to northern Tanzania's largest elephant herds.",
                "accommodation_slug": "tarangire-safari-lodge", "breakfast": True, "lunch": True, "dinner": True,
                "highlights": "Elephant herds, baobab trees, sunset over the Tarangire River",
            },
            {
                "day": 3, "title": "Tarangire to Serengeti via Ngorongoro Highlands",
                "description": "Full-day drive into the Serengeti via the Ngorongoro Conservation Area highlands, with a picnic lunch on the way. Afternoon game drive into the central Serengeti.",
                "accommodation_slug": "serengeti-serena-safari-lodge", "breakfast": True, "lunch": True, "dinner": True,
                "highlights": "Highland scenery, first Serengeti game drive, Maasai villages en route",
            },
            {
                "day": 4, "title": "Full Day Serengeti",
                "description": "Full day of game viewing in the central Serengeti with morning and afternoon drives. Optional hot-air balloon safari at dawn (+$580). Picnic lunch in the bush.",
                "accommodation_slug": "serengeti-serena-safari-lodge", "breakfast": True, "lunch": True, "dinner": True,
                "highlights": "Big-cat encounters, optional balloon, picnic lunch in the bush",
            },
            {
                "day": 5, "title": "Serengeti to Ngorongoro Crater Rim",
                "description": "Morning game drive in the Serengeti, then drive to the Ngorongoro Crater rim, arriving in the afternoon for crater-rim views and sunset.",
                "accommodation_slug": "ngorongoro-serena-safari-lodge", "breakfast": True, "lunch": True, "dinner": True,
                "highlights": "Crater rim arrival, sunset over the crater",
            },
            {
                "day": 6, "title": "Ngorongoro Crater Floor",
                "description": "Descend at dawn into the Ngorongoro Crater for a full day of game viewing — your best chance to see all of the Big Five in a single day, including the rare black rhino. Picnic lunch on the crater floor.",
                "accommodation_slug": "ngorongoro-serena-safari-lodge", "breakfast": True, "lunch": True, "dinner": True,
                "highlights": "Black rhino, Big Five day, picnic with hippos",
            },
            {
                "day": 7, "title": "Departure",
                "description": "After breakfast, drive back to Arusha (~3.5 hours) for your onward flight. Day-use room available for late departures.",
                "accommodation_slug": None, "breakfast": True, "lunch": False, "dinner": False,
                "highlights": "Transfer to airport",
            },
        ],
    },

    # =========================================================================
    {
        "name": "Great Migration Special — 9 Days",
        "category": "wildlife",
        "difficulty": "easy",
        "duration_days": 9,
        "duration_nights": 8,
        "group_min": 2,
        "group_max": 6,
        "price_per_person": "6850.00",
        "currency": "USD",
        "destination_slugs": [
            "tarangire-national-park",
            "ngorongoro-crater",
            "serengeti-national-park",
        ],
        "short_description": "Position yourself at the northern Serengeti for the Mara River wildebeest crossings — one of nature's greatest spectacles, with three full nights at a migration-focused camp.",
        "description": (
            "Designed for the July-October crossing season, this itinerary places you at a high-end camp in the northern "
            "Serengeti's Kogatende area for three full nights — the heart of the river-crossing zone. Crossings are "
            "unpredictable but bunching herds, predator activity and the eventual river-charge dramas make these the most "
            "intense game-viewing days available anywhere. Mid-itinerary nights in the central Serengeti and Ngorongoro "
            "ensure you don't miss the rest of the ecosystem."
        ),
        "highlights": (
            "Three nights at a Mara River crossing-focused luxury camp\n"
            "Two nights central Serengeti for resident big cats\n"
            "Full day in Ngorongoro Crater\n"
            "Tarangire as the warm-up\n"
            "Private guide, premium camps throughout"
        ),
        "included": (
            "All park and conservation fees\n"
            "Eight nights luxury tented camps and lodges\n"
            "Private custom 4x4 + English-speaking professional guide\n"
            "Internal flight from northern Serengeti to Arusha\n"
            "All meals, water, soft drinks\n"
            "Airport transfers"
        ),
        "excluded": (
            "International flights\n"
            "Visa\n"
            "Insurance\n"
            "Tips ($25-35/day pp recommended)\n"
            "Premium alcoholic drinks\n"
            "Personal expenses"
        ),
        "requirements": "Valid passport, suitable for fitness levels normal-to-moderate. Best booked 9+ months in advance.",
        "is_featured": True,
        "is_customizable": True,
        "image_slug": "serengeti-national-park-3",
        "image_dir": "destinations",
        "itinerary": [
            {"day": 1, "title": "Arrival in Arusha", "description": "Met at KIA airport, transfer to garden lodge for overnight and briefing.", "accommodation_slug": "rivertrees-country-inn", "breakfast": False, "lunch": False, "dinner": True, "highlights": "Welcome briefing"},
            {"day": 2, "title": "Tarangire National Park", "description": "Drive to Tarangire (2.5 hrs). Afternoon game drive among elephant herds and baobabs.", "accommodation_slug": "sanctuary-swala", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Elephant viewing, premium tented camp"},
            {"day": 3, "title": "Tarangire to Ngorongoro Highlands", "description": "Morning game drive Tarangire, transfer to Ngorongoro Crater rim for sunset.", "accommodation_slug": "andbeyond-ngorongoro-crater-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Highland scenery, crater rim arrival"},
            {"day": 4, "title": "Ngorongoro Crater Floor", "description": "Full day in the crater — Big Five viewing, including black rhino. Picnic on the floor.", "accommodation_slug": "andbeyond-ngorongoro-crater-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Big Five day, black rhino"},
            {"day": 5, "title": "Fly to Northern Serengeti", "description": "Drive to Manyara airstrip, light aircraft to Kogatende. Afternoon game drive — Mara River area.", "accommodation_slug": "sayari-camp", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Internal flight, first migration drive"},
            {"day": 6, "title": "Mara River Crossings", "description": "Full day at the river. Crossings can happen anytime; the camp's guides watch the herds bunching and position you when crossing looks imminent.", "accommodation_slug": "sayari-camp", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Wildebeest crossings, crocodile attacks"},
            {"day": 7, "title": "Northern Serengeti continued", "description": "Another full day in the Lamai Wedge — additional crossing chances, plus resident cats and elephants.", "accommodation_slug": "sayari-camp", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Repeat crossings, leopard, lion prides"},
            {"day": 8, "title": "Fly to central Serengeti — game drive day", "description": "Light aircraft to central Seronera. Afternoon game drive for big-cat encounters in the heart of the park.", "accommodation_slug": "lemala-ewanjan-tented-camp", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Central plains, resident lions"},
            {"day": 9, "title": "Fly to Arusha and depart", "description": "Morning game drive, fly to Arusha, transfer to KIA for international departure.", "accommodation_slug": None, "breakfast": True, "lunch": False, "dinner": False, "highlights": "Onward connection"},
        ],
    },

    # =========================================================================
    {
        "name": "Southern Circuit Discovery — 8 Days",
        "category": "adventure",
        "difficulty": "moderate",
        "duration_days": 8,
        "duration_nights": 7,
        "group_min": 2,
        "group_max": 6,
        "price_per_person": "4250.00",
        "currency": "USD",
        "destination_slugs": [
            "selous-game-reserve-nyerere-national-park",
            "ruaha-national-park",
        ],
        "short_description": "Off the beaten path — Africa's largest game reserve and the wildest park you've never heard of. Boat safari, walking safari, and almost no crowds.",
        "description": (
            "This 8-day Southern Circuit combines Tanzania's two great southern parks — Nyerere (formerly Selous) and "
            "Ruaha — with boat, walking and night-drive activities not available in the more popular northern circuit. "
            "Expect lower wildlife density on average but exceptional variety, including African wild dog, large lion "
            "prides, and the unique East-South Africa species overlap at Ruaha. Internal light-aircraft flights between "
            "the parks; intimate camps throughout."
        ),
        "highlights": (
            "Boat safari on the Rufiji River — only major TZ park where boats are allowed\n"
            "Walking safari with armed ranger in both parks\n"
            "African wild dog viewing (Selous is one of the best sites in Africa)\n"
            "10% of Africa's lion population — Ruaha\n"
            "Very few other vehicles compared to the Northern Circuit"
        ),
        "included": (
            "All park fees\n"
            "Seven nights at premium tented camps\n"
            "Two internal light-aircraft flights (Dar-Selous-Ruaha-Dar)\n"
            "All meals, water, soft drinks\n"
            "Game drives, boat safaris, walking safaris as per itinerary\n"
            "English-speaking professional guide\n"
            "Dar es Salaam airport transfers"
        ),
        "excluded": (
            "International flights\n"
            "Visa\n"
            "Insurance\n"
            "Tips ($20-30/day pp)\n"
            "Premium alcoholic drinks\n"
            "Personal expenses"
        ),
        "requirements": "Moderate fitness for walking safari (15-18 km / day possible). No history of cardiac issues.",
        "is_featured": True,
        "is_customizable": True,
        "image_slug": "selous-game-reserve-1",
        "image_dir": "destinations",
        "itinerary": [
            {"day": 1, "title": "Arrival Dar es Salaam, fly to Selous", "description": "Met at Dar airport, light aircraft to Selous (45 min). Afternoon boat safari on the Rufiji.", "accommodation_slug": "roho-ya-selous", "breakfast": False, "lunch": True, "dinner": True, "highlights": "First boat safari, hippo, crocodile"},
            {"day": 2, "title": "Selous full day", "description": "Morning walking safari, afternoon game drive. Sundowner overlooking the river.", "accommodation_slug": "roho-ya-selous", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Walking safari, wild dog if lucky"},
            {"day": 3, "title": "Selous game drives + boat", "description": "Morning game drive looking for African wild dog. Afternoon boat safari at golden hour.", "accommodation_slug": "roho-ya-selous", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Wild dog focus, sunset boat"},
            {"day": 4, "title": "Fly to Ruaha", "description": "Morning flight via Dar to Ruaha (3 hours total). Afternoon game drive into Ruaha's baobab country.", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "First Ruaha drive, lion country"},
            {"day": 5, "title": "Ruaha full day", "description": "Full day exploring the Mwagusi sand river and Mbomipa plains. Excellent lion and leopard chances.", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Lion prides, leopard, sable/roan antelope"},
            {"day": 6, "title": "Ruaha walking + drives", "description": "Morning walking safari, afternoon game drive. Picnic lunch at a remote spot.", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Walking safari, tracks and signs"},
            {"day": 7, "title": "Ruaha to Dar", "description": "Morning game drive, fly back to Dar. Overnight in Dar for late international departure.", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Internal flight, Dar overnight"},
            {"day": 8, "title": "Departure", "description": "Transfer to airport for onward flight.", "accommodation_slug": None, "breakfast": True, "lunch": False, "dinner": False, "highlights": "Departure"},
        ],
    },

    # =========================================================================
    {
        "name": "Kilimanjaro + Safari Combo — 13 Days",
        "category": "trekking",
        "difficulty": "challenging",
        "duration_days": 13,
        "duration_nights": 12,
        "group_min": 2,
        "group_max": 8,
        "price_per_person": "5350.00",
        "currency": "USD",
        "destination_slugs": [
            "mount-kilimanjaro",
            "tarangire-national-park",
            "ngorongoro-crater",
            "serengeti-national-park",
        ],
        "short_description": "Summit Kilimanjaro then go on safari — the bucket-list combo. 8-day Lemosho climb (the highest-success route) followed by a 4-day Northern Circuit safari.",
        "description": (
            "This combination knocks two East African bucket-list experiences off in a single trip — eight days climbing "
            "Mount Kilimanjaro via the scenic Lemosho route (the highest summit-success route), followed by a 4-day Northern "
            "Circuit safari to celebrate. A rest day at a Moshi lodge after summit makes the transition possible. The "
            "physical demands of the climb mean this is recommended only for travellers with strong fitness; the safari "
            "afterwards is genuinely relaxing."
        ),
        "highlights": (
            "Summit Uhuru Peak at 5,895 m — Africa's highest point\n"
            "8-day Lemosho route — ~90% summit success rate\n"
            "Full 4-day safari to celebrate including a Ngorongoro Crater day\n"
            "Professional mountain guides + porters throughout\n"
            "Quality safari camps for the recovery week"
        ),
        "included": (
            "Park fees, hut/camping fees on Kilimanjaro\n"
            "Mountain guide, porters, cook for the 8-day Lemosho climb\n"
            "All meals on mountain, all camping equipment\n"
            "Transfers from Moshi airport\n"
            "12 nights total accommodation\n"
            "4x4 safari with private guide for the safari days\n"
            "All safari meals, park fees, game drives"
        ),
        "excluded": (
            "International flights\n"
            "Personal trekking gear (or rental locally ~$150 for the kit)\n"
            "Tips for mountain crew (USD 280-380 per climber) and safari guide ($15-25/day)\n"
            "Insurance (must cover trekking to 6,000 m)\n"
            "Visa\n"
            "Personal expenses"
        ),
        "requirements": "Strong fitness — ability to walk 5-8 hours daily at altitude. Travel insurance covering trekking to 6,000 m is mandatory. Pre-climb medical check recommended.",
        "is_featured": True,
        "is_customizable": True,
        "image_slug": "mount-kilimanjaro-2",
        "image_dir": "destinations",
        "itinerary": [
            {"day": 1, "title": "Arrival in Moshi", "description": "Met at KIA, transfer to Moshi/Kilimanjaro foothills lodge for climb briefing, gear check, and recovery from international flights.", "accommodation_slug": "kaliwa-lodge", "breakfast": False, "lunch": False, "dinner": True, "highlights": "Briefing, gear check"},
            {"day": 2, "title": "Lemosho Gate to Mti Mkubwa", "description": "Drive to Lemosho gate, register, hike through rainforest 3-4 hrs to first camp at Mti Mkubwa (2,650 m).", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Rainforest, first camp"},
            {"day": 3, "title": "Mti Mkubwa to Shira 1", "description": "Climb through heather to Shira Plateau, 5-7 hrs. Camp at 3,500 m. Views of summit emerge.", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Heath zone, summit views"},
            {"day": 4, "title": "Shira 1 to Shira 2", "description": "Cross the Shira plateau, 4-5 hrs. Camp at 3,850 m. Acclimatisation walk in afternoon.", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Acclimatisation walk"},
            {"day": 5, "title": "Shira 2 to Lava Tower to Barranco", "description": "Climb to Lava Tower (4,640 m) for lunch — climb high, sleep low. Descend to Barranco (3,950 m).", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Climb high sleep low, Lava Tower"},
            {"day": 6, "title": "Barranco Wall + Karanga Camp", "description": "Scramble up the Barranco Wall (3-4 hrs) — fun, exposed but non-technical. Camp at Karanga (4,000 m).", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Barranco Wall scramble"},
            {"day": 7, "title": "Karanga to Barafu", "description": "Climb to base camp at Barafu (4,700 m). Rest, eat, sleep early for midnight summit push.", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Pre-summit rest"},
            {"day": 8, "title": "Summit Day — Uhuru Peak", "description": "Midnight start. Climb to Stella Point (5,756 m) for sunrise, then Uhuru Peak (5,895 m). Descend all the way to Mweka Camp (3,100 m).", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Uhuru Peak summit, 5,895 m"},
            {"day": 9, "title": "Mweka Camp to Mweka Gate", "description": "Descend to Mweka Gate (3-4 hrs). Transfer to Moshi lodge for shower, swim, sleep.", "accommodation_slug": "kaliwa-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Descent and recovery"},
            {"day": 10, "title": "Recovery + transfer to Tarangire", "description": "Drive to Tarangire (3 hrs). Afternoon game drive — the elephants make a calming counter-point after the climb.", "accommodation_slug": "tarangire-safari-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "First game drive"},
            {"day": 11, "title": "Tarangire to Ngorongoro to Serengeti", "description": "Long drive through Ngorongoro Highlands to central Serengeti, with picnic lunch.", "accommodation_slug": "serengeti-serena-safari-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Cross-country drive, first Serengeti drive"},
            {"day": 12, "title": "Serengeti to Ngorongoro Crater Floor", "description": "Morning game drive Serengeti, drive to crater rim, full crater floor day on the way to Karatu.", "accommodation_slug": "ngorongoro-serena-safari-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Crater Big Five day"},
            {"day": 13, "title": "Return to Arusha and depart", "description": "Drive back to Arusha (~3 hrs). Onward flight.", "accommodation_slug": None, "breakfast": True, "lunch": False, "dinner": False, "highlights": "Trip end"},
        ],
    },

    # =========================================================================
    {
        "name": "Zanzibar Beach Combo — 5 Days",
        "category": "beach",
        "difficulty": "easy",
        "duration_days": 5,
        "duration_nights": 4,
        "group_min": 1,
        "group_max": 10,
        "price_per_person": "1450.00",
        "currency": "USD",
        "destination_slugs": [
            "zanzibar-stone-town",
        ],
        "short_description": "Five-day Zanzibar extension — one cultural night in Stone Town followed by three nights at a luxury beach resort. The classic post-safari unwind.",
        "description": (
            "This 5-day Zanzibar package is the natural post-safari extension. Begin in Stone Town for a guided walking "
            "tour, spice tour and sunset dhow cruise — soak up the UNESCO heritage of the old quarter and learn how "
            "Zanzibar earned its 'Spice Island' name. Then transfer to a luxury beach resort on the eastern or northern "
            "coast for three days of doing nothing — swimming, diving, snorkelling, or just lying on the powdery sand."
        ),
        "highlights": (
            "Stone Town walking tour + spice plantation visit\n"
            "Sunset dhow cruise from Stone Town\n"
            "Three nights at a 5-star beach resort\n"
            "Optional diving / snorkelling / dolphin tour add-ons\n"
            "Easy connection from northern Tanzania safari"
        ),
        "included": (
            "Four nights accommodation (1 Stone Town + 3 beach)\n"
            "Airport transfers (ZNZ)\n"
            "Stone Town walking tour\n"
            "Spice tour with lunch\n"
            "Sunset dhow cruise\n"
            "Beach resort half-board OR all-inclusive (configurable)"
        ),
        "excluded": (
            "International flights or Zanzibar Air ticket from Arusha (~$250 one-way)\n"
            "Zanzibar visa-on-arrival ($50)\n"
            "Tips, alcoholic drinks\n"
            "Diving, kitesurf, dolphin tour fees\n"
            "Personal expenses"
        ),
        "requirements": "Modest clothing for Stone Town (Muslim quarter). Sun protection.",
        "is_featured": True,
        "is_customizable": True,
        "image_slug": "zanzibar-stone-town-1",
        "image_dir": "destinations",
        "itinerary": [
            {"day": 1, "title": "Arrival in Zanzibar", "description": "Met at ZNZ airport, transfer to Stone Town hotel. Afternoon walking tour of Stone Town.", "accommodation_slug": "park-hyatt-zanzibar", "breakfast": False, "lunch": False, "dinner": False, "highlights": "Stone Town walking tour"},
            {"day": 2, "title": "Spice tour + dhow cruise", "description": "Morning spice plantation tour. Afternoon free. Sunset dhow cruise from Stone Town waterfront.", "accommodation_slug": "park-hyatt-zanzibar", "breakfast": True, "lunch": True, "dinner": False, "highlights": "Spice tour, dhow sunset"},
            {"day": 3, "title": "Transfer to beach", "description": "Morning transfer to your chosen beach resort (~1.5 hrs). Afternoon at leisure on the beach.", "accommodation_slug": "zuri-zanzibar", "breakfast": True, "lunch": False, "dinner": True, "highlights": "Beach arrival, swimming"},
            {"day": 4, "title": "Beach day", "description": "Full day at leisure. Optional snorkelling, diving, kitesurfing, or dolphin tour for separate fee.", "accommodation_slug": "zuri-zanzibar", "breakfast": True, "lunch": False, "dinner": True, "highlights": "Beach activities or do nothing"},
            {"day": 5, "title": "Transfer and departure", "description": "Transfer to ZNZ airport (~1.5 hrs) for onward flight.", "accommodation_slug": None, "breakfast": True, "lunch": False, "dinner": False, "highlights": "Departure"},
        ],
    },

    # =========================================================================
    {
        "name": "Tanzania Honeymoon Safari + Zanzibar — 10 Days",
        "category": "honeymoon",
        "difficulty": "easy",
        "duration_days": 10,
        "duration_nights": 9,
        "group_min": 2,
        "group_max": 2,
        "price_per_person": "7950.00",
        "currency": "USD",
        "destination_slugs": [
            "tarangire-national-park",
            "ngorongoro-crater",
            "serengeti-national-park",
            "zanzibar-stone-town",
        ],
        "short_description": "Six nights of luxury Tanzanian safari followed by three nights at a romantic boutique beach property on Zanzibar. Champagne, candlelit bush dinners, and a private guide throughout.",
        "description": (
            "This honeymoon itinerary pairs a six-night premium Northern Circuit safari with three nights at one of "
            "Zanzibar's most romantic boutique beach resorts. Couples-only camps and lodges throughout, candlelit bush "
            "dinners, hot-air balloon over the Serengeti included, and a private 4x4 + guide for total flexibility. Ends "
            "with a sunset dhow cruise and a final couples spa treatment at the beach."
        ),
        "highlights": (
            "Hot-air balloon flight over the Serengeti — INCLUDED\n"
            "Couples spa treatment at the beach resort\n"
            "Bush dinner under the stars\n"
            "Private 4x4 + guide entire safari\n"
            "Premium tented camps and the Crater Lodge\n"
            "Sunset dhow cruise from Stone Town"
        ),
        "included": (
            "All international transfers\n"
            "Six nights premium tented camps and the Ngorongoro Crater Lodge\n"
            "Three nights honeymoon-suite at a Zanzibar boutique resort\n"
            "Hot-air balloon safari with champagne bush breakfast\n"
            "All meals, water, soft drinks (premium drinks at beach all-inclusive)\n"
            "Private 4x4 + professional guide throughout safari\n"
            "Park fees, transfers, internal flight Serengeti to Zanzibar"
        ),
        "excluded": (
            "International flights\n"
            "Visa for Tanzania + Zanzibar\n"
            "Insurance\n"
            "Tips ($30-50/day pp for premium product)\n"
            "Premium alcoholic drinks on safari\n"
            "Diving / additional activities on Zanzibar"
        ),
        "requirements": "Just two valid passports and an appetite for romance.",
        "is_featured": True,
        "is_customizable": True,
        "image_slug": "ngorongoro-crater-4",
        "image_dir": "destinations",
        "itinerary": [
            {"day": 1, "title": "Arrival in Arusha", "description": "Met at KIA, transfer to coffee-plantation lodge. Welcome champagne and dinner.", "accommodation_slug": "legendary-lodge", "breakfast": False, "lunch": False, "dinner": True, "highlights": "Welcome champagne dinner"},
            {"day": 2, "title": "Tarangire National Park", "description": "Drive to Tarangire, afternoon game drive among elephant herds. Sundowner at a private spot.", "accommodation_slug": "sanctuary-swala", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Sundowner, elephants"},
            {"day": 3, "title": "Tarangire to Ngorongoro Crater Lodge", "description": "Morning game drive Tarangire. Drive to crater rim. Arrive at andBeyond Crater Lodge for sunset on the rim.", "accommodation_slug": "andbeyond-ngorongoro-crater-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Crater Lodge arrival"},
            {"day": 4, "title": "Crater floor day + transfer to Serengeti", "description": "Morning descent into the crater for Big Five viewing. Lunch on the rim, afternoon drive to central Serengeti.", "accommodation_slug": "dunia-camp", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Crater Big Five day"},
            {"day": 5, "title": "Serengeti with balloon safari", "description": "Pre-dawn hot-air balloon flight over the plains, champagne bush breakfast on landing. Afternoon game drive.", "accommodation_slug": "dunia-camp", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Hot-air balloon + champagne"},
            {"day": 6, "title": "Full day Serengeti + bush dinner", "description": "Full day game drives. Surprise candlelit bush dinner under the stars in the evening.", "accommodation_slug": "dunia-camp", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Bush dinner under the stars"},
            {"day": 7, "title": "Fly Serengeti to Zanzibar", "description": "Morning game drive, light aircraft Serengeti → Zanzibar (with refuel stop). Arrive at beach resort for sunset.", "accommodation_slug": "zuri-zanzibar", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Internal flight to coast"},
            {"day": 8, "title": "Beach day + couples spa", "description": "Beach morning, couples spa treatment in the afternoon, sunset cocktails on the beach.", "accommodation_slug": "zuri-zanzibar", "breakfast": True, "lunch": False, "dinner": True, "highlights": "Couples spa"},
            {"day": 9, "title": "Beach day + sunset dhow", "description": "Beach morning. Afternoon transfer to Stone Town for a private sunset dhow cruise.", "accommodation_slug": "zuri-zanzibar", "breakfast": True, "lunch": False, "dinner": True, "highlights": "Private dhow sunset"},
            {"day": 10, "title": "Departure", "description": "Transfer to ZNZ airport for onward flight.", "accommodation_slug": None, "breakfast": True, "lunch": False, "dinner": False, "highlights": "Departure"},
        ],
    },

    # =========================================================================
    {
        "name": "Family Safari — 8 Days",
        "category": "family",
        "difficulty": "easy",
        "duration_days": 8,
        "duration_nights": 7,
        "group_min": 3,
        "group_max": 10,
        "price_per_person": "3450.00",
        "currency": "USD",
        "destination_slugs": [
            "tarangire-national-park",
            "ngorongoro-crater",
            "serengeti-national-park",
        ],
        "short_description": "Designed for families with children 6+ — interconnecting family rooms, kid-friendly game drives, balloon optional, treetop walkway, and proper rest mornings.",
        "description": (
            "Built around the realities of safari with children — slightly shorter game-drive days, properties with pools "
            "and kids' programmes, family rooms or interconnecting doubles throughout, and the option to add genuinely "
            "kid-engaging activities like the Lake Manyara treetop walkway and a Maasai village school visit. Includes "
            "a guide who is trained to keep children engaged on game drives and a custom packed-lunch programme."
        ),
        "highlights": (
            "Family rooms and pools at every lodge\n"
            "Kid-engaged guide with junior ranger materials\n"
            "Optional Maasai school visit\n"
            "Lake Manyara Treetop Walkway\n"
            "Crater day with hippo picnic\n"
            "Free for children under 6 (no game-drive fees)"
        ),
        "included": (
            "Seven nights family-room accommodation\n"
            "Private 4x4 with experienced child-friendly guide\n"
            "All meals + kids' menus on request\n"
            "Park fees, junior ranger packs\n"
            "Airport transfers"
        ),
        "excluded": (
            "International flights\n"
            "Visa\n"
            "Insurance\n"
            "Tips ($15-25/day pp)\n"
            "Balloon safari ($580/pp from age 7)"
        ),
        "requirements": "Children must be 6+. Yellow Fever certificate where applicable.",
        "is_featured": False,
        "is_customizable": True,
        "image_slug": "tarangire-national-park-3",
        "image_dir": "destinations",
        "itinerary": [
            {"day": 1, "title": "Arrive Arusha", "description": "Arrival, transfer to family-friendly lodge near KIA airport. Pool, briefing.", "accommodation_slug": "arusha-coffee-lodge", "breakfast": False, "lunch": False, "dinner": True, "highlights": "Arrival"},
            {"day": 2, "title": "Tarangire", "description": "Drive to Tarangire. Afternoon game drive — elephants are the kids' highlight.", "accommodation_slug": "tarangire-safari-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Elephants, first big-five"},
            {"day": 3, "title": "Manyara + Treetop Walkway", "description": "Manyara morning game drive + Treetop Walkway (great for kids). Drive to Ngorongoro.", "accommodation_slug": "ngorongoro-serena-safari-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Treetop Walkway"},
            {"day": 4, "title": "Ngorongoro Crater + Maasai school visit", "description": "Morning crater floor (Big Five). Afternoon optional Maasai village school visit.", "accommodation_slug": "ngorongoro-serena-safari-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Maasai school"},
            {"day": 5, "title": "Drive to Serengeti", "description": "Drive to central Serengeti via Olduvai Gorge (the Cradle of Mankind museum stop for older kids).", "accommodation_slug": "four-seasons-serengeti-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Cradle of Mankind, Four Seasons"},
            {"day": 6, "title": "Full day Serengeti — Four Seasons", "description": "Family-friendly Serengeti day with Discovery Centre + pool time built into the schedule.", "accommodation_slug": "four-seasons-serengeti-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Discovery Centre"},
            {"day": 7, "title": "Final Serengeti drive", "description": "Half-day game drive. Light aircraft to Arusha. Last-night lodge near airport.", "accommodation_slug": "arusha-coffee-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Final drive"},
            {"day": 8, "title": "Departure", "description": "Transfer to KIA for departure.", "accommodation_slug": None, "breakfast": True, "lunch": False, "dinner": False, "highlights": "Departure"},
        ],
    },

    # =========================================================================
    {
        "name": "Mahale Chimps + Katavi Wilderness — 8 Days",
        "category": "adventure",
        "difficulty": "moderate",
        "duration_days": 8,
        "duration_nights": 7,
        "group_min": 2,
        "group_max": 4,
        "price_per_person": "8950.00",
        "currency": "USD",
        "destination_slugs": [
            "mahale-mountains-national-park",
            "katavi-national-park",
        ],
        "short_description": "Tanzania's wildest combination — habituated chimpanzees in Mahale's lakeside forest, then Katavi's superpods of hippo and huge buffalo herds. Maximum 4 guests, light-aircraft access only.",
        "description": (
            "This itinerary connects Tanzania's two most remote parks — Mahale Mountains (chimpanzee trekking on the shore "
            "of Lake Tanganyika) and Katavi (extraordinary dry-season concentrations of hippo, buffalo and lion). Both are "
            "accessible only by light aircraft and host very few visitors. Combined, you get a fully off-grid week — no "
            "WiFi, no other tourists — in two of the wildest places left in Africa."
        ),
        "highlights": (
            "Chimpanzee trekking with the habituated M-group at Mahale\n"
            "Kayaking and swimming in Lake Tanganyika\n"
            "Katavi's superpods of hippo (hundreds in single mud pools)\n"
            "Walking safari and old-school fly camping in Katavi\n"
            "Light-aircraft access — both parks isolated"
        ),
        "included": (
            "All park, conservation and chimp permit fees\n"
            "Seven nights at small camps (Greystoke Mahale + a Katavi camp)\n"
            "All meals, water, soft drinks, beer/house wine\n"
            "Internal flights Arusha → Mahale → Katavi → Arusha\n"
            "All activities (chimp trekking, walking, drives, kayak)\n"
            "Professional guide throughout"
        ),
        "excluded": (
            "International flights\n"
            "Visa, insurance\n"
            "Premium spirits\n"
            "Tips ($30-50/day pp)\n"
            "Personal expenses"
        ),
        "requirements": "Moderate fitness for steep forest trails. Age 12+ for chimp trekking. Travellers should be comfortable being totally off-grid.",
        "is_featured": False,
        "is_customizable": True,
        "image_slug": "mahale-mountains-national-park-2",
        "image_dir": "destinations",
        "itinerary": [
            {"day": 1, "title": "Arusha arrival", "description": "Arrival KIA, garden lodge for overnight before remote flights.", "accommodation_slug": "rivertrees-country-inn", "breakfast": False, "lunch": False, "dinner": True, "highlights": "Pre-flight overnight"},
            {"day": 2, "title": "Fly to Mahale", "description": "Light aircraft to Mahale (4 hrs incl. refuel). Boat transfer to camp. Lake swim, sunset over Lake Tanganyika.", "accommodation_slug": "greystoke-mahale", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Arrival in the wildest place in Tanzania"},
            {"day": 3, "title": "Chimpanzee trekking day 1", "description": "Morning trek to find the M-group chimps. 1 hour with them. Afternoon: lake activities (kayak, snorkel, swim).", "accommodation_slug": "greystoke-mahale", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Chimps + lake afternoon"},
            {"day": 4, "title": "Chimpanzee trekking day 2", "description": "Another chimp trek (a second day often yields very different observations). Afternoon hike to a waterfall.", "accommodation_slug": "greystoke-mahale", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Chimps again, waterfall"},
            {"day": 5, "title": "Fly to Katavi", "description": "Light aircraft to Katavi. Afternoon game drive — the Katuma sand river hippos are unforgettable.", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Katavi arrival, hippo super-pods"},
            {"day": 6, "title": "Katavi full day", "description": "Morning walking safari, afternoon game drive. Massive buffalo herds and lion prides hunt them.", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Walking safari, buffalo herds"},
            {"day": 7, "title": "Katavi + return", "description": "Final morning drive in Katavi. Fly back to Arusha. Overnight lodge before departure.", "accommodation_slug": "rivertrees-country-inn", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Last Katavi drive"},
            {"day": 8, "title": "Departure", "description": "Transfer to KIA.", "accommodation_slug": None, "breakfast": True, "lunch": False, "dinner": False, "highlights": "Departure"},
        ],
    },

    # =========================================================================
    {
        "name": "Best of East Africa — 14 Days",
        "category": "luxury",
        "difficulty": "moderate",
        "duration_days": 14,
        "duration_nights": 13,
        "group_min": 2,
        "group_max": 6,
        "price_per_person": "13500.00",
        "currency": "USD",
        "destination_slugs": [
            "serengeti-national-park",
            "ngorongoro-crater",
            "maasai-mara-national-reserve",
            "volcanoes-national-park",
        ],
        "short_description": "Tanzania's Serengeti and Ngorongoro, Kenya's Masai Mara, and Rwanda's mountain gorillas. The ultimate East African circuit — luxury throughout, two weeks, one private guide team.",
        "description": (
            "The premier safari itinerary across East Africa — combining the Serengeti and Ngorongoro Crater of northern "
            "Tanzania, the Maasai Mara of Kenya (timed during migration if possible), and a gorilla trek in Rwanda's "
            "Volcanoes National Park. Includes private charter flights between countries, premium lodges and camps "
            "throughout, and a single guide team coordinating the entire 14 days. The most comprehensive East African "
            "wildlife experience available."
        ),
        "highlights": (
            "Mountain gorilla trek in Rwanda — life-list experience\n"
            "Wildebeest migration in BOTH Serengeti and Maasai Mara (if timed July-October)\n"
            "Ngorongoro Crater full day with the Big Five\n"
            "Private guide team + charter flights between countries\n"
            "Premium camps and lodges throughout"
        ),
        "included": (
            "All international charter flights between TZ → KE → RW (private aircraft)\n"
            "Gorilla trekking permit ($1,500 incl.)\n"
            "13 nights premium accommodation\n"
            "All meals, premium drinks (camp-dependent)\n"
            "Private guide team and 4x4\n"
            "All park / conservation fees and visas"
        ),
        "excluded": (
            "International flights to/from East Africa\n"
            "Insurance covering gorilla trekking + safari\n"
            "Tips ($40-60/day pp for premium product)\n"
            "Personal expenses"
        ),
        "requirements": "Strong fitness for gorilla trek (up to 8 hrs steep muddy walking). Age 15+ for gorilla trek. Travel insurance is mandatory.",
        "is_featured": True,
        "is_customizable": True,
        "image_slug": "serengeti-national-park-5",
        "image_dir": "destinations",
        "itinerary": [
            {"day": 1, "title": "Arrival Arusha", "description": "Met at KIA, transfer to a coffee plantation lodge.", "accommodation_slug": "legendary-lodge", "breakfast": False, "lunch": False, "dinner": True, "highlights": "Welcome"},
            {"day": 2, "title": "Fly to central Serengeti", "description": "Light aircraft from Arusha, afternoon game drive central Serengeti.", "accommodation_slug": "namiri-plains-serengeti", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Serengeti arrival"},
            {"day": 3, "title": "Serengeti full day", "description": "Big-cat focus in eastern plains — Namiri Plains is best for cheetah.", "accommodation_slug": "namiri-plains-serengeti", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Cheetah, lion"},
            {"day": 4, "title": "Fly to northern Serengeti", "description": "Drive/fly to Kogatende. Afternoon Mara River drive.", "accommodation_slug": "sayari-camp", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Migration positioning"},
            {"day": 5, "title": "Mara River crossings (TZ side)", "description": "Full day on the Mara River for crossings.", "accommodation_slug": "sayari-camp", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Crossings"},
            {"day": 6, "title": "Charter to Maasai Mara (Kenya side)", "description": "Private charter to Kenya. Afternoon Mara game drive (conservancy side).", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Cross-border, Kenya Mara"},
            {"day": 7, "title": "Mara conservancies full day", "description": "Off-road driving + night drives in private conservancies.", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Off-road + night drive"},
            {"day": 8, "title": "Mara to Ngorongoro Crater", "description": "Charter back to Tanzania, transfer to Crater Lodge for sunset.", "accommodation_slug": "andbeyond-ngorongoro-crater-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Crater Lodge arrival"},
            {"day": 9, "title": "Ngorongoro Crater floor", "description": "Big Five day on the crater floor.", "accommodation_slug": "andbeyond-ngorongoro-crater-lodge", "breakfast": True, "lunch": True, "dinner": True, "highlights": "Black rhino"},
            {"day": 10, "title": "Charter to Kigali, Rwanda", "description": "Long charter day to Kigali. Transfer to gorilla park base.", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Cross-border"},
            {"day": 11, "title": "Gorilla trek day 1", "description": "Pre-dawn briefing, trek to a habituated gorilla family. 1 hour with the gorillas.", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Mountain gorillas"},
            {"day": 12, "title": "Gorilla trek day 2 (second permit)", "description": "Second gorilla trek — different family. Equally life-changing.", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Second gorilla trek"},
            {"day": 13, "title": "Cultural day or rest", "description": "Visit Dian Fossey research camp or golden monkey track. Transfer to Kigali.", "accommodation_slug": None, "breakfast": True, "lunch": True, "dinner": True, "highlights": "Cultural day"},
            {"day": 14, "title": "Depart Kigali", "description": "Onward flight from Kigali International.", "accommodation_slug": None, "breakfast": True, "lunch": False, "dinner": False, "highlights": "Departure"},
        ],
    },
]
