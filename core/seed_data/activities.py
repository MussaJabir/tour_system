"""
Activity seed data. `destination_slug` is resolved to a Destination FK by
the seed command. `image_slug` matches a file in core/seed_data/images/
under the `image_dir` subfolder (typically wildlife/).
"""

ACTIVITIES = [
    # ----- Serengeti -----
    {
        "name": "Serengeti Morning Game Drive",
        "destination_slug": "serengeti-national-park",
        "category": "safari",
        "difficulty": "easy",
        "duration": "4.0",
        "duration_unit": "hours",
        "price_per_person": "180.00",
        "short_description": "Dawn game drive when predators are most active — leave camp at sunrise for 4 hours in an open 4x4.",
        "description": (
            "Set out at first light in a custom-fitted open-sided 4x4 with your private guide, when the air is cool and the "
            "Serengeti's lions, leopards and cheetah are at their most active. Coffee and pastries are taken in the bush, "
            "often while watching a hunting cat. Routes vary by season — in the south during calving, we follow the wildebeest; "
            "in the north between July and October, the Mara River is the focus; in central Seronera, year-round resident game "
            "is the staple. Returns to camp around 11am for brunch and rest before an afternoon game drive."
        ),
        "requirements": "None — suitable for all ages and fitness levels. Warm jacket for early start.",
        "included_items": "Open-sided 4x4 vehicle, professional guide, bottled water, snacks, park entry fees.",
        "excluded_items": "Tips for guides, alcoholic drinks, personal expenses.",
        "best_season": "Year-round; northern Mara crossings July-October, southern calving Jan-March.",
        "image_slug": "crossroad-car-safari-scene",
        "image_dir": "wildlife",
        "is_featured": True,
    },
    {
        "name": "Serengeti Hot Air Balloon Safari",
        "destination_slug": "serengeti-national-park",
        "category": "adventure",
        "difficulty": "easy",
        "duration": "4.0",
        "duration_unit": "hours",
        "price_per_person": "580.00",
        "short_description": "Float silently over the plains at dawn — followed by a champagne breakfast in the bush.",
        "description": (
            "A bucket-list experience: pre-dawn pickup, balloon inflation, and a one-hour silent flight over the Serengeti "
            "plains as the sun rises. From 300 metres up you see wildebeest herds stretching to the horizon, lions on a "
            "kopje, and elephants moving through the acacia woodland. The flight lands on the plains, where a full sparkling "
            "wine breakfast has been set up in the open — eggs, bacon, fresh fruit, pastries — before a game drive back to "
            "your camp. Operates in central Seronera year-round and in Ndutu (Dec-March) and Kogatende/Mara (Jun-Oct) "
            "seasonally."
        ),
        "requirements": "Minimum age 7. Mobility to climb in/out of basket. Not advised if pregnant.",
        "included_items": "Balloon flight, champagne bush breakfast, transfers from camp, certificate of flight.",
        "excluded_items": "Tips for pilot and ground crew, park fees (if not in package).",
        "best_season": "Year-round in Seronera; seasonal in north and south.",
        "image_slug": "serengeti-baloon-safari",
        "image_dir": "wildlife",
        "is_featured": True,
    },
    {
        "name": "Serengeti Walking Safari",
        "destination_slug": "serengeti-national-park",
        "category": "adventure",
        "difficulty": "moderate",
        "duration": "3.0",
        "duration_unit": "hours",
        "price_per_person": "120.00",
        "short_description": "Walk through the Serengeti's wildest corners with an armed guide — see the bush at ground level.",
        "description": (
            "Available only in selected conservancies and private concessions bordering the national park (Singita Grumeti, "
            "Lamai Wedge), walking safari brings you into the Serengeti at human pace. An armed park ranger walks at the front, "
            "your private guide reads tracks and signs in the bush, and the focus shifts from big-game ticking to the smaller "
            "stuff you miss from a vehicle — termite mounds, tracks, scat, medicinal plants, dung beetles. Group size is "
            "limited to 6 for safety."
        ),
        "requirements": "Moderate fitness. Long trousers, closed shoes, neutral colours.",
        "included_items": "Guide, armed ranger, drinks, snacks.",
        "excluded_items": "Park / conservancy fees if separate.",
        "best_season": "Dry season (June - October) for best visibility.",
        "image_slug": "gwen-weustink-i3c1ssxj1i8-unsplash",
        "image_dir": "wildlife",
        "is_featured": False,
    },

    # ----- Ngorongoro -----
    {
        "name": "Ngorongoro Crater Floor Day Drive",
        "destination_slug": "ngorongoro-crater",
        "category": "safari",
        "difficulty": "easy",
        "duration": "8.0",
        "duration_unit": "hours",
        "price_per_person": "295.00",
        "short_description": "Full-day descent into the crater — see all of the Big Five in one day, with a packed lunch on the floor.",
        "description": (
            "Leave your rim lodge before dawn for the steep descent road into the crater, arriving on the floor as wildlife "
            "is at its most active. Spend the full day game viewing across grassland, soda lake (with flamingos), and acacia "
            "forest — the crater is one of very few places where you can realistically see lion, elephant, buffalo, leopard "
            "and the endangered black rhino in a single drive. A packed lunch is enjoyed at one of the official picnic sites "
            "(famously, with hippos watching). The ascent road returns to the rim by mid-afternoon."
        ),
        "requirements": "None.",
        "included_items": "4x4 vehicle, guide, packed lunch, water, crater entry fees.",
        "excluded_items": "Tips, alcoholic drinks.",
        "best_season": "Year-round — June-October has the clearest weather.",
        "image_slug": "ngorongoro-1-qkuw7clsyvkqvsw4gyiiymgnk4t56wxk40t8cjip30",
        "image_dir": "wildlife",
        "is_featured": True,
    },
    {
        "name": "Maasai Village Cultural Visit",
        "destination_slug": "ngorongoro-crater",
        "category": "cultural",
        "difficulty": "easy",
        "duration": "2.0",
        "duration_unit": "hours",
        "price_per_person": "55.00",
        "short_description": "Visit a working Maasai boma — see traditional dances, enter a mud-and-dung house, and meet the elders.",
        "description": (
            "Maasai bomas around Ngorongoro welcome guided visits as part of an income-sharing arrangement with the conservation "
            "authority. You'll be greeted with the famous adamu (jumping) dance, walk through the thorn-fence enclosure that "
            "protects livestock from predators at night, step inside a traditional mud-and-dung dwelling, and speak with the "
            "village elders through your guide. Some communities also offer brief workshops in beadwork or fire-making. "
            "Photographs are welcomed (a small contribution per family photographed is customary)."
        ),
        "requirements": "Respectful clothing. Photographs welcome with permission.",
        "included_items": "Village entry fee, translator-guide.",
        "excluded_items": "Beadwork purchases, photo tips.",
        "best_season": "Year-round.",
        "image_slug": "202302afr-tanzania-maasai-village-ngorongoro-conservation-area",
        "image_dir": "wildlife",
        "is_featured": False,
    },

    # ----- Tarangire -----
    {
        "name": "Tarangire Game Drive with Baobabs",
        "destination_slug": "tarangire-national-park",
        "category": "safari",
        "difficulty": "easy",
        "duration": "5.0",
        "duration_unit": "hours",
        "price_per_person": "165.00",
        "short_description": "Half-day among ancient baobab trees and Tarangire's famous elephant herds.",
        "description": (
            "Tarangire is best known for two things — enormous elephant herds (some of the largest in northern Tanzania) and "
            "centuries-old baobab trees. This half-day game drive focuses on the Tarangire River and the open plains around it, "
            "where wildlife concentrates in the dry season. Expect elephants, giraffe, zebra, wildebeest, lion (often in trees) "
            "and excellent birdlife. Light is best in the early morning or late afternoon — your camp will time it to suit."
        ),
        "requirements": "None.",
        "included_items": "Open 4x4, guide, water, park fees.",
        "excluded_items": "Tips, lunch (unless full-day).",
        "best_season": "June - October — dry season concentrates wildlife at the river.",
        "image_slug": "tarangire-national-park-5",
        "image_dir": "wildlife",
        "is_featured": True,
    },
    {
        "name": "Tarangire South Night Game Drive",
        "destination_slug": "tarangire-national-park",
        "category": "wildlife",
        "difficulty": "easy",
        "duration": "3.0",
        "duration_unit": "hours",
        "price_per_person": "145.00",
        "short_description": "After-dark drive in private concessions — see the nocturnal world unavailable elsewhere in TZ.",
        "description": (
            "Night drives are not permitted inside national parks but ARE allowed in the private concessions bordering "
            "Tarangire's south (e.g. Manyara Ranch, Randilen WMA). Equipped with red-filter spotlights, your guide sweeps the "
            "bush for creatures invisible by day: porcupine, civet, genet, bushbaby, white-tailed mongoose, aardwolf, leopards "
            "on the prowl, hunting lion. The experience is profoundly different from a daytime drive — the silence, the eyes "
            "in the dark, the sense of being in someone else's domain."
        ),
        "requirements": "Warm jacket (cold once the sun is down).",
        "included_items": "Vehicle, guide, spotlight, water/drinks.",
        "excluded_items": "Concession fees if separate, tips.",
        "best_season": "Year-round — drier months for better visibility.",
        "image_slug": "into-the-night-",
        "image_dir": "wildlife",
        "is_featured": False,
    },

    # ----- Lake Manyara -----
    {
        "name": "Lake Manyara Game Drive",
        "destination_slug": "lake-manyara-national-park",
        "category": "safari",
        "difficulty": "easy",
        "duration": "4.0",
        "duration_unit": "hours",
        "price_per_person": "140.00",
        "short_description": "Game drive through groundwater forest, savannah and the alkaline lakeshore.",
        "description": (
            "Lake Manyara is famously the home of tree-climbing lions — though sightings are not guaranteed, the lush "
            "groundwater forest and acacia woodland are excellent for elephant, baboon (the largest troops anywhere), buffalo, "
            "giraffe and birdlife. Seasonal flamingo flocks turn the lake's northern shore pink. The drive typically opens "
            "or closes a Northern Circuit safari, paired with Tarangire on the same loop."
        ),
        "requirements": "None.",
        "included_items": "4x4, guide, water, park fees.",
        "excluded_items": "Tips.",
        "best_season": "June - October for game; November - June for birds.",
        "image_slug": "Tarangire-National-Park-7",
        "image_dir": "wildlife",
        "is_featured": False,
    },
    {
        "name": "Manyara Treetop Walkway",
        "destination_slug": "lake-manyara-national-park",
        "category": "adventure",
        "difficulty": "easy",
        "duration": "1.5",
        "duration_unit": "hours",
        "price_per_person": "65.00",
        "short_description": "East Africa's longest canopy walkway — 370 m of suspended bridges through groundwater forest.",
        "description": (
            "A separate attraction inside Lake Manyara National Park, the treetop walkway is a 370 m series of suspension "
            "bridges weaving through the canopy of the groundwater forest, with the longest span at 18 m high. From the "
            "platforms you can see vervet and blue monkeys, baboons, hornbills, turacos and forest birds at eye level. "
            "Suitable for all ages — a great morning activity en route to game drives."
        ),
        "requirements": "None — not for those with severe fear of heights.",
        "included_items": "Entry fee, guide.",
        "excluded_items": "Photography tips.",
        "best_season": "Year-round.",
        "image_slug": "fluffy-hummingbird-wallpaper-1920x1080",
        "image_dir": "wildlife",
        "is_featured": False,
    },

    # ----- Kilimanjaro -----
    {
        "name": "Mount Kilimanjaro — 7-Day Machame Route",
        "destination_slug": "mount-kilimanjaro",
        "category": "hiking",
        "difficulty": "challenging",
        "duration": "7.0",
        "duration_unit": "days",
        "price_per_person": "2150.00",
        "short_description": "The popular 'Whiskey Route' — scenic, varied, and the highest success rate of the shorter itineraries.",
        "description": (
            "The Machame Route is Kilimanjaro's most popular climb, taking 7 days from Machame Gate to Uhuru Peak at 5,895 m "
            "and back via the Mweka descent. It is more scenic and varied than the older Marangu route, passes through all "
            "five climate zones, and offers the 'climb high, sleep low' acclimatisation principle on the Lava Tower day. "
            "Summit night begins around midnight to reach the rim at sunrise. Sleeping is in tents (porters carry and set up "
            "everything), meals are prepared by the camp cook. Success rate on 7 days is roughly 85 percent."
        ),
        "requirements": "Strong fitness, willingness to camp, ability to walk 5-7 hours daily.",
        "included_items": "All park fees, professional mountain guide and porters, all camping gear, all meals on the mountain, transfers to/from the gate.",
        "excluded_items": "Tips for crew (USD 250-350 per climber typical), personal trekking gear, sleeping bag rental.",
        "best_season": "January - mid-March and June - October.",
        "image_slug": "mount-kilimanjaro-1",
        "image_dir": "destinations",
        "is_featured": True,
    },
    {
        "name": "Mount Kilimanjaro — 8-Day Lemosho Route",
        "destination_slug": "mount-kilimanjaro",
        "category": "hiking",
        "difficulty": "challenging",
        "duration": "8.0",
        "duration_unit": "days",
        "price_per_person": "2750.00",
        "short_description": "The most scenic route with the highest summit success rate — recommended for first-time climbers.",
        "description": (
            "The 8-day Lemosho Route is considered the gold standard for Kilimanjaro — it offers the best acclimatisation "
            "profile (and therefore the highest summit success rate, ~90 percent), beautiful and varied scenery, and lower "
            "tourist traffic than Machame. Starting from the western Lemosho gate, climbers walk through rainforest and "
            "moorland before joining the southern circuit. The extra day is used to acclimatise around Karanga Camp before "
            "the summit attempt from Barafu. Crew, equipment and inclusions match the 7-day Machame package; the price "
            "premium reflects the longer duration."
        ),
        "requirements": "Strong fitness, ability to walk 5-7 hours daily, willingness to camp.",
        "included_items": "All park fees, professional mountain guide and porters, all camping gear, all meals on the mountain, transfers.",
        "excluded_items": "Tips for crew (USD 280-380 per climber typical), personal trekking gear, sleeping bag rental.",
        "best_season": "January - mid-March and June - October.",
        "image_slug": "mount-kilimanjaro-3",
        "image_dir": "destinations",
        "is_featured": False,
    },
    {
        "name": "Materuni Waterfalls + Coffee Tour",
        "destination_slug": "mount-kilimanjaro",
        "category": "cultural",
        "difficulty": "easy",
        "duration": "5.0",
        "duration_unit": "hours",
        "price_per_person": "75.00",
        "short_description": "Day trip from Moshi — hike to a 90 m waterfall and learn coffee-making with a Chagga family.",
        "description": (
            "The Materuni village sits on Kilimanjaro's lower slopes near Moshi. The half-day excursion involves a 45-minute "
            "hike through banana and coffee plantations to the 90 m Materuni Waterfall (with optional cold swim at the base), "
            "followed by a hands-on coffee experience with a Chagga family — picking ripe beans, peeling, roasting over a fire, "
            "and grinding by hand to drink fresh. A traditional lunch is included. A great rest-day activity before or after "
            "a climb, or a half-day from Moshi or Arusha."
        ),
        "requirements": "Easy walking; non-slip shoes for the waterfall path.",
        "included_items": "Transfers, village guide, coffee experience, lunch.",
        "excluded_items": "Tips, coffee purchases.",
        "best_season": "Year-round.",
        "image_slug": "materuni-waterfalls",
        "image_dir": "wildlife",
        "is_featured": False,
    },

    # ----- Arusha NP -----
    {
        "name": "Arusha National Park Canoe Safari",
        "destination_slug": "arusha-national-park",
        "category": "water_sports",
        "difficulty": "easy",
        "duration": "2.0",
        "duration_unit": "hours",
        "price_per_person": "85.00",
        "short_description": "Paddle a Canadian canoe through the Momella Lakes — flamingos, hippos and waterbirds at eye level.",
        "description": (
            "Arusha National Park is the only park in northern Tanzania where canoeing is permitted. You set off in a stable "
            "Canadian-style canoe with an armed ranger across the alkaline Big Momella Lake, drifting past pink flamingo flocks, "
            "hippos snorting in the shallows, fish eagles overhead and giraffe coming to drink at the shore. A great half-day "
            "activity for stopover travellers flying in or out of Kilimanjaro International, just 35 minutes from the airport."
        ),
        "requirements": "Basic swimming ability. Sun protection.",
        "included_items": "Canoe, paddles, life jacket, ranger, park fees.",
        "excluded_items": "Transfers, tips.",
        "best_season": "Year-round.",
        "image_slug": "momella-lakes",
        "image_dir": "wildlife",
        "is_featured": False,
    },

    # ----- Selous / Nyerere -----
    {
        "name": "Rufiji River Boat Safari",
        "destination_slug": "selous-game-reserve-nyerere-national-park",
        "category": "water_sports",
        "difficulty": "easy",
        "duration": "3.0",
        "duration_unit": "hours",
        "price_per_person": "120.00",
        "short_description": "Float down the Rufiji past elephant herds, hippo pods and basking crocodile — the only major TZ park where boats are allowed.",
        "description": (
            "The Rufiji River is the lifeblood of the Nyerere National Park (former Selous Game Reserve). A flat-bottomed "
            "boat with a quiet outboard motor takes you through riverine forest, past herds of elephant drinking at the bank, "
            "pods of hippo, large saltwater crocodiles sunning on sand banks, and outstanding birdlife — fish eagle, African "
            "skimmer, pied kingfisher, malachite kingfisher. Best taken in the late afternoon for sunset light and golden water."
        ),
        "requirements": "None.",
        "included_items": "Boat, guide, drinks/snacks.",
        "excluded_items": "Park fees if separate, tips.",
        "best_season": "June - October (water levels predictable).",
        "image_slug": "rufiji-river-boat-safari",
        "image_dir": "activities",
        "is_featured": True,
    },
    {
        "name": "Selous Walking Safari",
        "destination_slug": "selous-game-reserve-nyerere-national-park",
        "category": "adventure",
        "difficulty": "moderate",
        "duration": "4.0",
        "duration_unit": "hours",
        "price_per_person": "150.00",
        "short_description": "Half-day walking safari in the Selous bush — get out of the vehicle and into the wild on foot.",
        "description": (
            "Walking safari has been a Selous tradition since the reserve's earliest days. With an armed ranger leading and your "
            "guide alongside, you walk in single file through miombo woodland and along sand rivers, learning to read tracks, "
            "identify medicinal plants, and approach wildlife on foot — at safe distances. Buffalo, giraffe, elephant and "
            "antelope are commonly seen. Group size is limited to 6; you must be 14 or older."
        ),
        "requirements": "Moderate fitness. Neutral colours, closed shoes, long trousers, age 14+.",
        "included_items": "Guide, ranger, drinks/snacks, park fees.",
        "excluded_items": "Tips.",
        "best_season": "June - October.",
        "image_slug": "savannah-sunset",
        "image_dir": "wildlife",
        "is_featured": False,
    },

    # ----- Ruaha -----
    {
        "name": "Ruaha Game Drive",
        "destination_slug": "ruaha-national-park",
        "category": "safari",
        "difficulty": "easy",
        "duration": "5.0",
        "duration_unit": "hours",
        "price_per_person": "175.00",
        "short_description": "Half-day drive through baobab country — best big-cat density in Tanzania and East-meets-South antelope species.",
        "description": (
            "Ruaha holds an estimated 10 percent of Africa's remaining lions and one of the highest leopard densities anywhere. "
            "A morning or afternoon game drive focuses on the Great Ruaha River (in the dry season), the Mwagusi sand river, "
            "or the open Mbomipa Plains. The wildlife mix is unique to East Africa: greater kudu, lesser kudu, sable and roan "
            "antelope appear alongside zebra, giraffe and elephant. Crowds are virtually non-existent."
        ),
        "requirements": "None.",
        "included_items": "Open 4x4, guide, water, park fees.",
        "excluded_items": "Tips.",
        "best_season": "June - November.",
        "image_slug": "common-zebra-7247714--340",
        "image_dir": "wildlife",
        "is_featured": False,
    },

    # ----- Saadani -----
    {
        "name": "Saadani Beach + Bush Combination",
        "destination_slug": "saadani-national-park",
        "category": "wildlife",
        "difficulty": "easy",
        "duration": "1.0",
        "duration_unit": "days",
        "price_per_person": "265.00",
        "short_description": "Morning game drive among elephant and giraffe, afternoon swim in the Indian Ocean — only possible at Saadani.",
        "description": (
            "Saadani is the only park in East Africa where the bush genuinely meets the sea. The day starts with a 3-hour "
            "morning game drive (elephant, buffalo, giraffe, sable antelope, lion if you're lucky), returns to the lodge "
            "for brunch, then offers the afternoon free for a swim in the Indian Ocean or a Wami River boat safari (hippo, "
            "croc, mangrove kingfisher). Sea turtles nest on the beaches between May and October."
        ),
        "requirements": "None.",
        "included_items": "4x4 game drive, ranger fees, boat safari, park fees.",
        "excluded_items": "Accommodation, tips.",
        "best_season": "June - February.",
        "image_slug": "saadani-national-park-1",
        "image_dir": "wildlife",
        "is_featured": False,
    },

    # ----- Mahale -----
    {
        "name": "Mahale Chimpanzee Trekking",
        "destination_slug": "mahale-mountains-national-park",
        "category": "wildlife",
        "difficulty": "moderate",
        "duration": "4.0",
        "duration_unit": "hours",
        "price_per_person": "200.00",
        "short_description": "Trek into the forest with rangers to find — and sit with — a wild habituated chimpanzee community.",
        "description": (
            "The M-group chimpanzees of Mahale have been studied since 1965 and are fully habituated. With a maximum group "
            "size of 6 and a strict 1-hour observation limit, the experience is intimate. Trekking time varies from 30 minutes "
            "to 5+ hours depending on where the chimps slept the previous night; rangers monitor them daily. The forest is "
            "humid and steep, with leeches and roots underfoot — but the encounter, watching them groom, climb, hunt or "
            "tumble in play, is what people remember for life. Maximum 12 trekking permits per day."
        ),
        "requirements": "Moderate fitness, ability to walk up steep forest trails 1-5 hours. Age 12+. No recent illness (chimps are vulnerable to human diseases).",
        "included_items": "Permit, ranger, park guide.",
        "excluded_items": "Lodge transfers, tips.",
        "best_season": "July - October.",
        "image_slug": "Mahale Mountains National Park1".lower().replace(' ', '-'),
        "image_dir": "wildlife",
        "is_featured": True,
    },

    # ----- Gombe -----
    {
        "name": "Gombe Chimpanzee Trekking",
        "destination_slug": "gombe-stream-national-park",
        "category": "wildlife",
        "difficulty": "moderate",
        "duration": "4.0",
        "duration_unit": "hours",
        "price_per_person": "180.00",
        "short_description": "Track the Kasekela community — the chimps Jane Goodall has studied since 1960.",
        "description": (
            "Gombe's tiny size and the Kasekela community's deep habituation make it one of the most reliable chimp encounters "
            "anywhere. Trails up the steep forested ridges are well-maintained but demanding. A guide and ranger lead small "
            "groups (max 6) to wherever the chimps are that morning. Add-ons include a visit to the Jane Goodall research "
            "centre and a swim in Lake Tanganyika to cool off after the trek."
        ),
        "requirements": "Moderate fitness, age 12+, no recent illness.",
        "included_items": "Permit, ranger, park guide.",
        "excluded_items": "Lodge transfers, tips.",
        "best_season": "July - October and December - February.",
        "image_slug": "gombe-stream-national-park-1",
        "image_dir": "destinations",
        "is_featured": False,
    },

    # ----- Zanzibar Stone Town -----
    {
        "name": "Stone Town Walking Tour",
        "destination_slug": "zanzibar-stone-town",
        "category": "cultural",
        "difficulty": "easy",
        "duration": "3.0",
        "duration_unit": "hours",
        "price_per_person": "45.00",
        "short_description": "A guided walk through the UNESCO old town — slave market, Sultan's palace, carved doors, spice market.",
        "description": (
            "A local guide leads you through Stone Town's narrow alleys, explaining the layers of Swahili, Arab, Indian and "
            "European influence. Stops include the Anglican Cathedral and former slave market site, the House of Wonders, "
            "the Old Fort, Freddie Mercury's birthplace, the carved Zanzibari doors district, and the Darajani Market (fish, "
            "spices, fruit). The tour finishes at the Forodhani Gardens, where you can stay on for the famous evening street "
            "food market."
        ),
        "requirements": "Comfortable walking shoes. Modest dress (this is a Muslim community).",
        "included_items": "Guide, bottled water, entry fees to House of Wonders + slave market memorial.",
        "excluded_items": "Lunch, tips.",
        "best_season": "Year-round.",
        "image_slug": "stone-town-walking-tour",
        "image_dir": "activities",
        "is_featured": True,
    },
    {
        "name": "Zanzibar Spice Tour",
        "destination_slug": "zanzibar-stone-town",
        "category": "cultural",
        "difficulty": "easy",
        "duration": "4.0",
        "duration_unit": "hours",
        "price_per_person": "55.00",
        "short_description": "Visit working spice plantations — see, smell and taste the cloves, nutmeg, cinnamon and vanilla that made Zanzibar famous.",
        "description": (
            "Zanzibar earned its 'Spice Island' nickname in the 19th century when it produced most of the world's cloves. "
            "The spice tour visits a working plantation outside Stone Town, where the guide pulls leaves, bark and roots from "
            "the trees and asks you to identify them by smell or taste — pepper, ginger, cinnamon, turmeric, vanilla, lemongrass, "
            "ylang-ylang. A traditional Swahili lunch is included, and small plant-based spice purchases are available at the "
            "end. Often combined with a Stone Town walking tour the same day."
        ),
        "requirements": "None.",
        "included_items": "Transfers from Stone Town, guide, plantation entry, Swahili lunch.",
        "excluded_items": "Tips, spice purchases.",
        "best_season": "Year-round.",
        "image_slug": "zanzibar",
        "image_dir": "wildlife",
        "is_featured": False,
    },
    {
        "name": "Sunset Dhow Cruise",
        "destination_slug": "zanzibar-stone-town",
        "category": "relaxation",
        "difficulty": "easy",
        "duration": "2.5",
        "duration_unit": "hours",
        "price_per_person": "50.00",
        "short_description": "Sail a traditional dhow around Stone Town at golden hour — drinks and small bites on board.",
        "description": (
            "Board a traditional Swahili dhow (handcrafted wooden sailing boat) from the Stone Town waterfront. Sail past "
            "Changuu (Prison) Island, Bawe Island and the old port as the sun drops behind the historic skyline. Snacks and "
            "drinks (soft drinks, beer, wine) are served on board. A romantic and uncomplicated end-of-day activity, often "
            "the highlight of a couples' or honeymoon stay."
        ),
        "requirements": "Basic swimming ability advised; sun protection.",
        "included_items": "Dhow, captain, snacks, drinks.",
        "excluded_items": "Tips.",
        "best_season": "Year-round; calmer water June-October.",
        "image_slug": "one-fishing-boat-water-indian-ocean-zanzibar-tanzania",
        "image_dir": "wildlife",
        "is_featured": True,
    },

    # ----- Pemba -----
    {
        "name": "Pemba Channel Scuba Diving",
        "destination_slug": "pemba-island",
        "category": "water_sports",
        "difficulty": "moderate",
        "duration": "5.0",
        "duration_unit": "hours",
        "price_per_person": "180.00",
        "short_description": "Two-tank dive on the Pemba Channel walls — big fish, healthy coral, almost no divers in the water.",
        "description": (
            "The Pemba Channel between Pemba Island and the African mainland drops to over 800 m and offers some of the "
            "best diving in the Indian Ocean. Wall dives at sites like Misali Island feature large pelagics (kingfish, jacks, "
            "tuna, occasional reef sharks), spectacular soft and hard coral, and visibility consistently above 25 m. Two "
            "tank dives, with surface interval and lunch on a beach or boat. Suitable for certified divers; PADI courses "
            "available on the island."
        ),
        "requirements": "Open Water certification minimum. Advanced certification for deeper walls.",
        "included_items": "Boat, dive master, tanks, weights, lunch.",
        "excluded_items": "Gear rental (BCD/regulator), tips, certification courses.",
        "best_season": "October - April (best visibility); diving possible year-round.",
        "image_slug": "pemba-island-1",
        "image_dir": "destinations",
        "is_featured": False,
    },

    # ----- Mafia -----
    {
        "name": "Whale Shark Snorkelling at Mafia",
        "destination_slug": "mafia-island",
        "category": "water_sports",
        "difficulty": "moderate",
        "duration": "5.0",
        "duration_unit": "hours",
        "price_per_person": "165.00",
        "short_description": "Boat out to find whale sharks in shallow Mafia waters — snorkel beside the world's largest fish.",
        "description": (
            "Between October and March, whale sharks gather in the warm shallow waters off Mafia Island's west coast to "
            "feed on plankton. A morning boat trip (typically 3-5 hours) heads out with snorkel guides to find them — usually "
            "in groups of 2-10 individuals — and slip into the water beside them. The animals are non-threatening filter "
            "feeders (5-9 metres in length) and the encounter is calm but unforgettable. Ethical-encounter codes apply: no "
            "touching, no flash photography, a maximum number of swimmers per shark at a time."
        ),
        "requirements": "Confident swimmer, ability to snorkel for 30+ minutes at a time.",
        "included_items": "Boat, snorkel gear, guide, water.",
        "excluded_items": "Marine park fees, tips.",
        "best_season": "October - March (whale shark aggregation).",
        "image_slug": "mafia-island-5",
        "image_dir": "wildlife",
        "is_featured": True,
    },

    # ----- Lake Victoria / Rubondo -----
    {
        "name": "Lake Victoria Sport Fishing",
        "destination_slug": "lake-victoria",
        "category": "water_sports",
        "difficulty": "easy",
        "duration": "6.0",
        "duration_unit": "hours",
        "price_per_person": "195.00",
        "short_description": "Troll the lake for Nile perch — fish of 50 kg+ are routinely caught, 100 kg+ is a regular trophy.",
        "description": (
            "Lake Victoria is one of the world's premier sport fishing destinations. Nile perch grow to over 200 kg in "
            "these waters, and 50-80 kg fish are commonly caught year-round. A morning charter departs from Mwanza or a "
            "Rubondo Island camp, trolling deep-running lures and live bait. Tackle is provided; catch-and-release is the "
            "norm for trophy fish. Tilapia and other species are kept for lunch on board."
        ),
        "requirements": "None — no fishing experience needed.",
        "included_items": "Boat charter, captain, tackle, bait, lunch.",
        "excluded_items": "Fishing license (purchased locally), tips.",
        "best_season": "Year-round; best in calmer months June-September.",
        "image_slug": "lake-victoria-2",
        "image_dir": "destinations",
        "is_featured": False,
    },

    # ----- Cross-park -----
    {
        "name": "Maasai Mara Migration Game Drive",
        "destination_slug": "maasai-mara-national-reserve",
        "category": "safari",
        "difficulty": "easy",
        "duration": "5.0",
        "duration_unit": "hours",
        "price_per_person": "210.00",
        "short_description": "Drive the Mara during the river-crossing season — herds, predators, and the famous crossings.",
        "description": (
            "Between July and October, the wildebeest migration moves through the Mara, crossing the Mara River in waves "
            "that draw crocodile attacks and lion ambushes. A morning or full-day drive in the reserve or the surrounding "
            "conservancies positions you for the crossings. Outside migration months, the Mara remains one of Africa's best "
            "big-cat reserves year-round."
        ),
        "requirements": "None.",
        "included_items": "Open 4x4, guide, water, reserve fees.",
        "excluded_items": "Tips.",
        "best_season": "July - October.",
        "image_slug": "kaskaz-mara-camp",
        "image_dir": "accommodations",
        "is_featured": False,
    },
    {
        "name": "Volcanoes NP Gorilla Trek",
        "destination_slug": "volcanoes-national-park",
        "category": "wildlife",
        "difficulty": "challenging",
        "duration": "6.0",
        "duration_unit": "hours",
        "price_per_person": "1500.00",
        "short_description": "Trek into the bamboo forest to spend one hour with a habituated mountain gorilla family.",
        "description": (
            "The flagship Rwanda experience. Permits ($1,500 per person) are issued the day before the trek; you're assigned "
            "to one of several habituated gorilla families. After a briefing at the park headquarters, you drive to the "
            "trailhead with porters and trackers. The hike to find the gorillas can take from 30 minutes to 5+ hours, often "
            "up steep, muddy bamboo slopes. Once located, you have exactly one hour to observe and photograph (no flash). "
            "Maximum 8 trekkers per family per day."
        ),
        "requirements": "Strong fitness, sturdy hiking shoes, rain gear. Age 15+. No active illness.",
        "included_items": "Permit, guide, ranger, tracker, transport from briefing centre.",
        "excluded_items": "Porter fees ($20-30 typical), tips for crew (USD 50+ total), accommodation.",
        "best_season": "June - September and December - February.",
        "image_slug": None,
        "image_dir": None,
        "is_featured": True,
    },
]
