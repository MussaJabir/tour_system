"""
Destination seed data. Coords are real (Google Maps / Wikipedia).
`image_slug` matches the filename stem in core/seed_data/images/destinations/
— the seed command appends `-1.jpg` to find the hero image, and `-2`, `-3`
… for gallery shots if present.
`gallery_count` is the number of gallery images to attach (after the hero).
`image_dir` is which subfolder under images/ to look in.
"""

DESTINATIONS = [
    # ===================== TANZANIA — Northern Circuit =====================
    {
        "name": "Serengeti National Park",
        "country": "Tanzania",
        "region": "Northern Circuit",
        "latitude": -2.3333,
        "longitude": 34.8333,
        "short_description": "The crown jewel of African safari — endless plains, the Great Migration, and the densest big-cat population on the continent.",
        "description": (
            "Serengeti National Park covers 14,750 km² of golden grassland, acacia woodland and granite kopjes in northern Tanzania. "
            "It is the stage for one of nature's greatest shows — the Great Migration of nearly two million wildebeest, zebra and gazelle "
            "that loops between the Serengeti and Kenya's Masai Mara every year, calving in the south from January to March before "
            "thundering north across the Grumeti and Mara rivers from June to October. Beyond the migration, the Serengeti hosts "
            "the highest concentration of large predators in Africa: roughly 3,000 lions, 1,000 leopards, and significant cheetah, "
            "spotted hyena and African wild dog populations. Eastern, central, southern and western sectors each have a distinct "
            "character — Seronera in the centre offers reliable year-round wildlife, the Mara River corridor in the north delivers "
            "the dramatic river-crossings between July and October, and Ndutu in the south is the heart of the calving season."
        ),
        "best_time_to_visit": "Year-round; Jun-Oct (Mara crossings), Jan-Mar (calving)",
        "climate": "Two rainy seasons: short rains in November, long rains March-May. Cool nights year-round (10-15°C), warm days (24-29°C). Altitude 1,200-1,800 m moderates the heat.",
        "wildlife": "Wildebeest, zebra, Thomson's & Grant's gazelle, eland, topi, hartebeest, giraffe, elephant, buffalo, lion, leopard, cheetah, spotted hyena, African wild dog, black rhino (Moru kopjes), serval, caracal, over 500 bird species.",
        "image_slug": "serengeti-national-park",
        "gallery_count": 7,
        "image_dir": "destinations",
        "is_featured": True,
    },
    {
        "name": "Ngorongoro Crater",
        "country": "Tanzania",
        "region": "Northern Circuit",
        "latitude": -3.1667,
        "longitude": 35.5833,
        "short_description": "A 600 m deep volcanic caldera teeming with wildlife — the closest thing to Eden on Earth, and one of the best places anywhere to see black rhino.",
        "description": (
            "The Ngorongoro Crater is the world's largest unflooded, unbroken volcanic caldera — a 260 km² natural amphitheatre "
            "with walls rising 600 metres above its floor. Inside, a self-contained ecosystem of grassland, forest, swamp and "
            "a soda lake supports an extraordinary density of wildlife: roughly 25,000 large mammals including all of the Big Five "
            "in a single day's drive. The crater's resident black rhino population is one of the few places in East Africa where "
            "sightings are almost guaranteed. Maasai herders share the wider Ngorongoro Conservation Area, walking their cattle "
            "alongside wildebeest and zebra in a coexistence that is unique on the continent. The rim, perched 2,300 m above sea "
            "level, is cool and often misty; lodges along it offer cinematic views down into the bowl."
        ),
        "best_time_to_visit": "Year-round; June-October for clearest crater views, calving in February",
        "climate": "Cool highland climate. Rim is cold (5-15°C at night), the crater floor is warmer (15-25°C). Mist on the rim most mornings.",
        "wildlife": "Black rhino, lion (including the famous Ngorongoro maned lions), elephant, buffalo, leopard, cheetah, spotted hyena, wildebeest, zebra, hippo, flamingo, eland, jackal, serval.",
        "image_slug": "ngorongoro-crater",
        "gallery_count": 5,
        "image_dir": "destinations",
        "is_featured": True,
    },
    {
        "name": "Tarangire National Park",
        "country": "Tanzania",
        "region": "Northern Circuit",
        "latitude": -4.0333,
        "longitude": 35.9667,
        "short_description": "Ancient baobab country with the largest elephant herds in northern Tanzania — and a fraction of the crowds.",
        "description": (
            "Tarangire National Park spans 2,850 km² of acacia woodland, riverine forest and sweeping savannah punctuated by "
            "iconic baobab trees centuries old. Named after the Tarangire River that runs through it, the park comes alive "
            "in the dry season (June to October) when wildlife from the surrounding Maasai Steppe converges on the river to drink. "
            "Tarangire is famous for its elephant population — herds of 200 or more are commonly seen — and for its high density "
            "of giraffe, zebra, wildebeest, lion and leopard. It is a quieter, less-visited park than the Serengeti or Ngorongoro, "
            "making it a favourite for travellers who want a wilder, more solitary safari experience without sacrificing wildlife density."
        ),
        "best_time_to_visit": "June - October (dry season) for the best wildlife concentrations at the river",
        "climate": "Warm year-round (20-30°C). Dry June-October. Short rains November, long rains March-May.",
        "wildlife": "Elephant (largest herds in northern Tanzania), giraffe, zebra, wildebeest, lion, leopard, cheetah, eland, oryx, lesser kudu, fringe-eared oryx, over 550 bird species including yellow-collared lovebird.",
        "image_slug": "tarangire-national-park",
        "gallery_count": 6,
        "image_dir": "destinations",
        "is_featured": True,
    },
    {
        "name": "Lake Manyara National Park",
        "country": "Tanzania",
        "region": "Northern Circuit",
        "latitude": -3.5833,
        "longitude": 35.8333,
        "short_description": "A jewel of a park beneath the Rift Valley escarpment — tree-climbing lions, flamingos and groundwater forest.",
        "description": (
            "Lake Manyara National Park stretches along the base of the Great Rift Valley escarpment, with a shallow alkaline "
            "lake covering two-thirds of its 330 km². The park combines five distinct ecosystems in a remarkably compact area: "
            "groundwater forest fed by springs, acacia woodland, open grassland, the soda lake itself and steep escarpment cliffs. "
            "It is famously home to tree-climbing lions that drape themselves along the branches of acacia trees, large troops "
            "of olive baboons (the highest concentration anywhere), and seasonal flocks of flamingos that turn the lake's "
            "northern shore pink. The park is a popular first-day stop on the Northern Circuit, often combined with Tarangire "
            "or visited en route to Ngorongoro."
        ),
        "best_time_to_visit": "July - October for game viewing, November - June for birdlife",
        "climate": "Warm tropical climate. 18-28°C year-round. Heaviest rains April-May.",
        "wildlife": "Tree-climbing lion, elephant, hippo, buffalo, giraffe, baboon (largest troops in Africa), blue monkey, bushbuck, impala, over 400 bird species, seasonal flamingo.",
        "image_slug": "lake-manyara-national-park",
        "gallery_count": 3,
        "image_dir": "destinations",
        "is_featured": False,
    },
    {
        "name": "Arusha National Park",
        "country": "Tanzania",
        "region": "Northern Circuit",
        "latitude": -3.2500,
        "longitude": 36.8333,
        "short_description": "A compact safari park on the slopes of Mount Meru — ideal for a half-day game drive or canoe safari before heading to the Serengeti.",
        "description": (
            "Arusha National Park, just 40 km from Arusha town and right next to Kilimanjaro International Airport, packs "
            "extraordinary diversity into 552 km². The park is dominated by Mount Meru, Tanzania's second-highest peak at "
            "4,566 m, with the Momella Lakes (a chain of seven alkaline lakes that change colour with the algae blooms) and "
            "the Ngurdoto Crater (a perfect miniature caldera). It is the only place in northern Tanzania where canoe safaris "
            "are offered, paddling among hippos and waterbirds. Wildlife includes black-and-white colobus monkey, giraffe, "
            "zebra, buffalo, warthog and flamingo, though no lion — making walking safaris and biking possible."
        ),
        "best_time_to_visit": "June - February for clearest views of Meru and Kilimanjaro",
        "climate": "Cool highland (15-25°C). Mt Meru creates rain shadows; eastern slopes wetter.",
        "wildlife": "Black-and-white colobus monkey, giraffe, zebra, buffalo, warthog, bushbuck, flamingo (seasonal), over 400 bird species. No lion.",
        "image_slug": "arusha-national-park",
        "gallery_count": 3,
        "image_dir": "destinations",
        "is_featured": False,
    },
    {
        "name": "Mount Kilimanjaro",
        "country": "Tanzania",
        "region": "Northern Tanzania",
        "latitude": -3.0758,
        "longitude": 37.3533,
        "short_description": "Africa's tallest mountain — 5,895 m of standalone volcano, climbable without technical mountaineering experience.",
        "description": (
            "Mount Kilimanjaro is the tallest free-standing mountain on Earth, rising from the Tanzanian plains to 5,895 m "
            "at Uhuru Peak. Unlike the world's other high-altitude challenges, it requires no technical climbing skills — just "
            "stamina, acclimatisation and persistence. Five established routes lead to the summit: Marangu (the only one with "
            "huts), Machame (the most popular), Lemosho (the most scenic), Rongai (the only northern approach) and the "
            "challenging Umbwe. A summit attempt typically takes 6-8 days, ascending through five distinct ecological zones — "
            "cultivated foothills, montane rainforest, heath and moorland, alpine desert, and finally arctic glaciers. The "
            "summit-night push begins around midnight to reach Uhuru Peak at dawn. Success rates vary by route and duration; "
            "8-day Lemosho climbs report the highest summit rates at around 90 percent."
        ),
        "best_time_to_visit": "January - mid-March and June - October (dry seasons). Avoid April-May (long rains).",
        "climate": "Five climate zones from tropical at the base (25°C) to arctic at the summit (below -20°C at night).",
        "wildlife": "Lower slopes: blue monkey, colobus, bushbuck, duiker. Above the forest: largely lifeless alpine zone.",
        "image_slug": "mount-kilimanjaro",
        "gallery_count": 4,
        "image_dir": "destinations",
        "is_featured": True,
    },

    # ===================== TANZANIA — Southern Circuit =====================
    {
        "name": "Selous Game Reserve (Nyerere National Park)",
        "country": "Tanzania",
        "region": "Southern Circuit",
        "latitude": -8.8333,
        "longitude": 37.5833,
        "short_description": "Africa's largest game reserve — 50,000 km² of remote wilderness, boat safaris on the Rufiji River, and walking safaris among elephants.",
        "description": (
            "Officially upgraded in 2019 to Nyerere National Park, the former Selous Game Reserve remains one of Africa's "
            "great wildernesses — 50,000 km² of miombo woodland, open savannah, swamps and the meandering Rufiji River system. "
            "It is roughly four times the size of the Serengeti, with a fraction of the visitors. The park is famous for boat "
            "safaris on the Rufiji (the only major Tanzanian park where this is possible), walking safaris led by armed guides, "
            "and large populations of elephant, buffalo, hippo, crocodile and African wild dog — the latter being among the "
            "best dog-watching destinations on the continent. The terrain is wilder and more challenging than the northern "
            "parks, with sand rivers, hot springs and untouched bush; it appeals to repeat-visitor safari travellers looking "
            "for something less mainstream."
        ),
        "best_time_to_visit": "June - October (dry season). Closed sectors during heavy March-May rains.",
        "climate": "Hot and humid (25-35°C). Wet November-May, dry June-October.",
        "wildlife": "Elephant, buffalo, hippo, crocodile, lion, leopard, African wild dog (excellent), giraffe, zebra, wildebeest, sable antelope, greater kudu, over 440 bird species including African skimmer.",
        "image_slug": "selous-game-reserve",
        "gallery_count": 6,
        "image_dir": "destinations",
        "is_featured": True,
    },
    {
        "name": "Ruaha National Park",
        "country": "Tanzania",
        "region": "Southern Circuit",
        "latitude": -7.6833,
        "longitude": 34.9333,
        "short_description": "Tanzania's largest national park — vast, remote, with East and Southern Africa wildlife overlapping in the same baobab-studded landscape.",
        "description": (
            "Ruaha National Park covers 20,200 km² in central Tanzania — Tanzania's largest national park and one of the "
            "wildest places in East Africa. It sits at a biogeographic crossroads where East African and Southern African "
            "wildlife species meet: greater and lesser kudu, sable and roan antelope appear alongside East African staples "
            "like elephant, giraffe and zebra. Ruaha holds 10 percent of Africa's lion population, including the famous "
            "Mwagusi pride, and is one of the best places anywhere to see large lion prides hunting buffalo. The terrain is "
            "dramatic: ancient baobab forests, granite kopjes, the seasonal Great Ruaha River and rolling miombo woodlands. "
            "Crowds are virtually non-existent."
        ),
        "best_time_to_visit": "June - November (dry season — best big game viewing)",
        "climate": "Hot dry climate (28-35°C in dry season). Wet December-April.",
        "wildlife": "Lion (10% of Africa's population), leopard, cheetah, African wild dog, elephant, greater kudu, lesser kudu, sable antelope, roan antelope, eland, hippo, crocodile, over 570 bird species.",
        "image_slug": "ruaha-national-park",
        "gallery_count": 3,
        "image_dir": "destinations",
        "is_featured": False,
    },
    {
        "name": "Mikumi National Park",
        "country": "Tanzania",
        "region": "Southern Circuit",
        "latitude": -7.4000,
        "longitude": 37.1167,
        "short_description": "The accessible southern park — open Mkata floodplain with elephant, lion and giraffe, just five hours by road from Dar es Salaam.",
        "description": (
            "Mikumi National Park is Tanzania's fourth-largest park at 3,230 km², easily accessed by road from Dar es Salaam "
            "in about five hours. The Mkata Floodplain in the centre of the park is open savannah dotted with acacia and "
            "borassus palms — picture-perfect East African safari country. Wildlife is abundant and easy to see: elephant, "
            "buffalo, lion, giraffe, zebra, wildebeest, eland and hippo are routine. Mikumi shares an ecosystem with the much "
            "larger Selous to its south and is often combined with it as part of a Southern Circuit itinerary, or visited "
            "independently as a 2-3 day safari escape from the coast."
        ),
        "best_time_to_visit": "June - October (dry season)",
        "climate": "Hot tropical (25-32°C). Wet November-May.",
        "wildlife": "Elephant, lion, giraffe (the local Masai giraffe), zebra, wildebeest, buffalo, eland, hippo, crocodile, leopard, sable antelope, over 400 bird species.",
        "image_slug": "mikumi-national-park",
        "gallery_count": 4,
        "image_dir": "destinations",
        "is_featured": False,
    },
    {
        "name": "Saadani National Park",
        "country": "Tanzania",
        "region": "Coast",
        "latitude": -6.0333,
        "longitude": 38.7833,
        "short_description": "The only park in East Africa where the bush meets the beach — game drives in the morning, Indian Ocean swimming in the afternoon.",
        "description": (
            "Saadani National Park is unique in East Africa: a wildlife park that borders the Indian Ocean. Across 1,062 km² "
            "of coastal forest, savannah and mangrove, you can see elephant, buffalo, giraffe, sable antelope and lion "
            "in the morning, then return to your lodge for a swim in the warm sea in the afternoon. The Wami River runs "
            "through the park, supporting hippo, crocodile and excellent birdlife; boat safaris along it are a highlight. "
            "Sea turtles nest on Saadani's beaches between May and October. The park is accessible by road from Dar es Salaam "
            "(about 5 hours), light aircraft from Zanzibar (35 minutes), or as a unique add-on between a Southern Circuit "
            "safari and a coastal beach stay."
        ),
        "best_time_to_visit": "June - February (avoid April-May long rains)",
        "climate": "Hot and humid year-round (24-32°C). Coastal influence.",
        "wildlife": "Elephant, buffalo, giraffe, sable antelope, lion (small population), waterbuck, reedbuck, hippo, crocodile, sea turtle nesting (May-October), dolphin, dugong (rare).",
        "image_slug": "saadani-national-park",
        "gallery_count": 3,
        "image_dir": "destinations",
        "is_featured": False,
    },

    # ===================== TANZANIA — Western & Remote =====================
    {
        "name": "Mahale Mountains National Park",
        "country": "Tanzania",
        "region": "Western Tanzania",
        "latitude": -6.1167,
        "longitude": 29.8500,
        "short_description": "Remote, mountainous, accessible only by boat — and home to about 800 wild chimpanzees, the largest known population on Earth.",
        "description": (
            "Mahale Mountains National Park rises sharply from the shore of Lake Tanganyika on Tanzania's western border with "
            "the DRC, covering 1,613 km² of forested mountains that reach 2,460 m. It is one of two parks in the world (along "
            "with neighbouring Gombe) where you can trek to see wild chimpanzees in their natural forest habitat. About 800 "
            "chimps live in Mahale, including the habituated M-group that researchers have studied since the 1960s. Trekking "
            "to find them is humid, occasionally steep, and unforgettable — once located, you sit just metres from a chimp "
            "group going about its day. The park is accessible only by light aircraft and boat, making it expensive and "
            "exclusive; Greystoke Mahale is the famous beach-camp base."
        ),
        "best_time_to_visit": "July - October (dry season — chimps tend to come lower down the slopes)",
        "climate": "Tropical lakeside (22-30°C). Heavy rains November-April.",
        "wildlife": "Chimpanzee (800 wild, M-group habituated), red colobus monkey, yellow baboon, leopard, otter, over 350 bird species. Lake Tanganyika fish.",
        "image_slug": "mahale-mountains-national-park",
        "gallery_count": 2,
        "image_dir": "destinations",
        "is_featured": False,
    },
    {
        "name": "Gombe Stream National Park",
        "country": "Tanzania",
        "region": "Western Tanzania",
        "latitude": -4.6500,
        "longitude": 29.6333,
        "short_description": "Jane Goodall's research base — tiny, steep, and home to the best-studied chimpanzee community in the world.",
        "description": (
            "Gombe Stream is Tanzania's smallest national park at just 35 km², but it is one of the most famous: this is "
            "where Jane Goodall began her landmark study of chimpanzee behaviour in 1960. The Kasekela community she has "
            "studied for over six decades remains fully habituated, allowing visitors to spend an hour with them on guided "
            "trekking expeditions. The park's steep forested ridges descend to the shore of Lake Tanganyika, where the camps "
            "are beach-fronted. Wildlife beyond chimps includes red colobus and red-tailed monkeys, otters, mongooses and an "
            "abundance of forest birds. Like Mahale, access is by boat from Kigoma; expect a remote, exclusive experience."
        ),
        "best_time_to_visit": "July - October and December - February (drier months)",
        "climate": "Tropical (22-30°C). Heavy rains March-May and November.",
        "wildlife": "Chimpanzee (Kasekela community), red colobus, red-tailed monkey, vervet, olive baboon, bushbuck, otter, mongoose, over 200 bird species.",
        "image_slug": "gombe-stream-national-park",
        "gallery_count": 3,
        "image_dir": "destinations",
        "is_featured": False,
    },
    {
        "name": "Katavi National Park",
        "country": "Tanzania",
        "region": "Western Tanzania",
        "latitude": -6.8500,
        "longitude": 31.1500,
        "short_description": "Untouched, untracked wilderness — Tanzania's third-largest park with virtually no other tourists.",
        "description": (
            "Katavi National Park covers 4,471 km² of remote western Tanzania and sees fewer than a thousand visitors a year. "
            "Its seasonal floodplains — Katisunga, Chada and Katuma — become extraordinary wildlife concentration points in "
            "the dry season (July to October) when buffalo herds of 1,000+, hippo super-pods, large prides of lion and big "
            "elephant groups congregate around the few remaining water sources. The Katuma River shrinks to a series of muddy "
            "pools where hundreds of hippos pile on top of each other in a daily, deafening, prehistoric spectacle. Access "
            "is by light aircraft only; lodges are few and small."
        ),
        "best_time_to_visit": "August - October (peak dry-season concentrations)",
        "climate": "Hot and dry July-October (25-35°C). Wet November-April.",
        "wildlife": "Buffalo (huge herds), hippo (densest concentrations in Africa), lion, leopard, elephant, sable antelope, roan antelope, eland, giraffe, crocodile.",
        "image_slug": "katavi-national-park",
        "gallery_count": 3,
        "image_dir": "destinations",
        "is_featured": False,
    },

    # ===================== TANZANIA — Coast & Islands =====================
    {
        "name": "Zanzibar Stone Town",
        "country": "Tanzania",
        "region": "Zanzibar Archipelago",
        "latitude": -6.1659,
        "longitude": 39.2026,
        "short_description": "A UNESCO World Heritage labyrinth of Swahili, Arab and Indian architecture — the cultural heart of Tanzania's coast.",
        "description": (
            "Stone Town is the old quarter of Zanzibar City, a UNESCO World Heritage site since 2000. Its narrow alleys, "
            "carved wooden doors, coral-stone buildings and bustling markets reflect 1,000 years of Swahili coast trade with "
            "Arabia, Persia, India and Europe. Highlights include the House of Wonders (former Sultan's palace), the Old Fort, "
            "the slave market memorial at the Anglican Cathedral, Forodhani Gardens at sunset (the famous evening food market), "
            "and the spice markets that gave Zanzibar its nickname. Stone Town is the natural cultural counterweight to a "
            "safari — most travellers spend 1-2 nights here before heading to the beaches on the north or east coast."
        ),
        "best_time_to_visit": "June - October and December - February (dry, less humid)",
        "climate": "Tropical (24-32°C). Long rains April-May, short rains November.",
        "wildlife": "N/A — cultural destination. Nearby coral reefs for diving.",
        "image_slug": "zanzibar-stone-town",
        "gallery_count": 4,
        "image_dir": "destinations",
        "is_featured": True,
    },
    {
        "name": "Pemba Island",
        "country": "Tanzania",
        "region": "Zanzibar Archipelago",
        "latitude": -5.0833,
        "longitude": 39.7667,
        "short_description": "Zanzibar's quieter, greener sister island — world-class diving and almost no tourists.",
        "description": (
            "Pemba Island lies 50 km north of Unguja (Zanzibar's main island) and is dramatically different: hillier, greener, "
            "less developed, and home to a deeply traditional Swahili Muslim culture. Pemba is one of the world's premier "
            "scuba diving destinations — the Pemba Channel drops to over 800 metres just offshore, with steep walls, big "
            "pelagics, healthy coral and very few divers. The island's interior is given to clove plantations (it produces "
            "much of the world's supply), mangroves and traditional fishing villages. Accommodation is limited to a handful "
            "of small eco-lodges, which is part of the appeal."
        ),
        "best_time_to_visit": "June - October and December - February",
        "climate": "Tropical (24-32°C). Heavier rainfall than Unguja due to greener interior.",
        "wildlife": "Pemba flying fox (endemic), Pemba scops owl, Pemba white-eye, dugong (rare). Diving: reef sharks, turtles, manta rays, big pelagics.",
        "image_slug": "pemba-island",
        "gallery_count": 2,
        "image_dir": "destinations",
        "is_featured": False,
    },
    {
        "name": "Mafia Island",
        "country": "Tanzania",
        "region": "Coast",
        "latitude": -7.9167,
        "longitude": 39.7500,
        "short_description": "Whale shark season, untouched coral reefs and zero crowds — Tanzania's most under-the-radar island.",
        "description": (
            "Mafia Island lies 160 km south of Zanzibar and is part of the Mafia Archipelago — a chain of small islands "
            "surrounded by Mafia Island Marine Park, one of the largest marine protected areas in the Indian Ocean. From "
            "October to March, large numbers of whale sharks aggregate in shallow waters off the western coast, and snorkelling "
            "with them is the island's most famous offering. Beyond whale sharks, the coral reefs of Chole Bay are spectacular "
            "and unspoiled. The island has fewer than 50,000 residents and a tiny handful of small lodges — it's the "
            "anti-Zanzibar."
        ),
        "best_time_to_visit": "October - March (whale shark season). June - October for diving with cooler water.",
        "climate": "Tropical (24-32°C). Rains April-May.",
        "wildlife": "Whale shark (Oct-Mar), green and hawksbill turtles, dolphins, reef fish, dugong (very rare). Pemba flying fox in mangroves.",
        "image_slug": "mafia-island",
        "gallery_count": 2,
        "image_dir": "destinations",
        "is_featured": False,
    },
    {
        "name": "Bagamoyo",
        "country": "Tanzania",
        "region": "Coast",
        "latitude": -6.4333,
        "longitude": 38.9000,
        "short_description": "Once the largest port in East Africa — a fading 19th-century town of Arab caravan ruins, German colonial buildings and quiet beaches.",
        "description": (
            "Bagamoyo, just 75 km north of Dar es Salaam, was the most important trading port on the East African coast in "
            "the 19th century — the end point for caravans bringing ivory and slaves from the interior. The historic centre, "
            "with its Arab tombs, German colonial-era boma, and the haunting ruins of the old slave market, is being considered "
            "for UNESCO World Heritage status. Today Bagamoyo is a sleepy town with a small but active artist community, "
            "long undeveloped beaches and easy access from Dar — a half-day cultural detour or a weekend escape rather than "
            "a destination in itself."
        ),
        "best_time_to_visit": "June - February (dry months)",
        "climate": "Hot and humid coastal (24-32°C).",
        "wildlife": "N/A — cultural and historical. Coastal birdlife.",
        "image_slug": "bagamoyo",
        "gallery_count": 1,
        "image_dir": "destinations",
        "is_featured": False,
    },

    # ===================== TANZANIA — Lakes & Highlands =====================
    {
        "name": "Lake Victoria",
        "country": "Tanzania",
        "region": "Lake Zone",
        "latitude": -2.3333,
        "longitude": 33.0000,
        "short_description": "Africa's largest lake — sport fishing, fishing villages and the gateway to the western Serengeti.",
        "description": (
            "Lake Victoria is Africa's largest lake (and the world's second-largest freshwater lake by area), shared between "
            "Tanzania, Uganda and Kenya. Tanzania holds the largest share of the shoreline, with the cities of Mwanza (the "
            "'rock city') and Bukoba as gateways. The lake is famous for sport fishing — the Nile perch grows to 200 kg "
            "here — and for the islands and rocky shores that dot its surface, several of which host community-based ecotourism. "
            "Rubondo Island National Park sits in the lake and is home to chimpanzee, sitatunga and over 200 bird species. "
            "Lake Victoria stops are often combined with the western Serengeti corridor or used as the launch point for "
            "Serengeti charter flights."
        ),
        "best_time_to_visit": "June - October (drier, calmer water)",
        "climate": "Warm tropical (22-30°C). Lake-effect storms common.",
        "wildlife": "Hippo, crocodile, sitatunga, otter (lake), bird life prolific. Rubondo Island: chimpanzee, elephant, giraffe, sitatunga.",
        "image_slug": "lake-victoria",
        "gallery_count": 4,
        "image_dir": "destinations",
        "is_featured": False,
    },

    # ===================== KENYA — neighbour stubs (no images yet) =====================
    {
        "name": "Maasai Mara National Reserve",
        "country": "Kenya",
        "region": "Southwest Kenya",
        "latitude": -1.4833,
        "longitude": 35.0833,
        "short_description": "Kenya's most famous reserve — the northern stage of the Great Migration and arguably the densest big-cat viewing on Earth.",
        "description": (
            "The Maasai Mara National Reserve is Kenya's flagship safari destination, the northern leg of the Serengeti-Mara "
            "ecosystem. From July to October, the wildebeest migration crosses the Mara River and grazes the reserve's open "
            "plains in one of the great wildlife spectacles of the natural world. Outside migration months, the Mara is "
            "still extraordinary for big cats — lion prides hunt in the open, leopards are reliably found along the riverine "
            "forest, and cheetah are seen in the eastern conservancies. Tourist numbers are higher than in the Serengeti, "
            "but the conservancies bordering the reserve (Mara North, Olare Motorogi, Naboisho) offer exclusive game viewing "
            "with off-road driving and night drives permitted."
        ),
        "best_time_to_visit": "July - October (migration), or year-round for big cats",
        "climate": "Mild highland (15-28°C). Rains April-May and November.",
        "wildlife": "Wildebeest migration (Jul-Oct), lion (high density), leopard, cheetah, elephant, buffalo, black rhino, giraffe, zebra, hippo, crocodile, hyena.",
        "image_slug": None,
        "gallery_count": 0,
        "image_dir": None,
        "is_featured": False,
    },
    {
        "name": "Amboseli National Park",
        "country": "Kenya",
        "region": "Southern Kenya",
        "latitude": -2.6500,
        "longitude": 37.2667,
        "short_description": "Iconic elephant herds with Mount Kilimanjaro as the backdrop — the postcard view of African safari.",
        "description": (
            "Amboseli National Park covers just 392 km² in southern Kenya, right against the Tanzanian border at the foot "
            "of Mount Kilimanjaro. It is famous for two things: large elephant herds (including some of the largest-tusked "
            "elephants left in Africa) and unobstructed views of Kilimanjaro rising 5,895 m beyond the plains. The park's "
            "marshes — fed by snowmelt from Kilimanjaro through underground aquifers — concentrate wildlife year-round. "
            "Beyond elephants, expect lion, cheetah, hyena, buffalo, giraffe and flamingo on the alkaline lake."
        ),
        "best_time_to_visit": "June - October and January - February (dry, best Kili views)",
        "climate": "Hot semi-arid (15-30°C). Dust storms in dry season.",
        "wildlife": "Elephant (massive herds, large tuskers), lion, cheetah, hyena, buffalo, giraffe, zebra, wildebeest, flamingo (seasonal), over 400 bird species.",
        "image_slug": None,
        "gallery_count": 0,
        "image_dir": None,
        "is_featured": False,
    },

    # ===================== RWANDA =====================
    {
        "name": "Volcanoes National Park",
        "country": "Rwanda",
        "region": "Northern Rwanda",
        "latitude": -1.4667,
        "longitude": 29.5000,
        "short_description": "Mountain gorilla trekking in the Virunga volcanoes — life-list wildlife encounter at $1,500 per permit.",
        "description": (
            "Volcanoes National Park in northwestern Rwanda is part of the Virunga Massif, a chain of dormant volcanoes "
            "shared between Rwanda, Uganda and the DRC. It is home to roughly a third of the world's remaining mountain "
            "gorillas — about 350 individuals — and a one-hour visit with a habituated family is the park's signature "
            "experience. Permits are $1,500 per person per trek and must be booked months in advance. Treks vary from "
            "30 minutes to 5+ hours depending on which gorilla family is being tracked that day. The park also offers golden "
            "monkey tracking, hikes up the volcanoes (Bisoke crater lake is a good day-hike), and visits to the Dian Fossey "
            "research camp where she was murdered in 1985."
        ),
        "best_time_to_visit": "June - September and December - February (drier — less muddy trails)",
        "climate": "Cool montane (10-22°C). Often misty and rainy.",
        "wildlife": "Mountain gorilla, golden monkey, forest elephant, buffalo, bushbuck, over 175 bird species.",
        "image_slug": None,
        "gallery_count": 0,
        "image_dir": None,
        "is_featured": False,
    },

    # ===================== UGANDA =====================
    {
        "name": "Bwindi Impenetrable National Park",
        "country": "Uganda",
        "region": "Southwestern Uganda",
        "latitude": -1.0667,
        "longitude": 29.6667,
        "short_description": "Half the world's mountain gorillas in dense ancient rainforest — and gorilla permits at $800, cheaper than Rwanda.",
        "description": (
            "Bwindi Impenetrable National Park is a UNESCO World Heritage site covering 321 km² of montane and lowland forest "
            "in southwestern Uganda. It harbours roughly half of the world's mountain gorilla population — around 480 "
            "individuals across multiple habituated families. Permits cost $800, significantly less than Rwanda's $1,500. "
            "Trekking is steep, slippery and often very wet (the forest's name is accurate), but the encounter with a gorilla "
            "family is no less profound. Bwindi is often combined with Queen Elizabeth National Park to its north (savannah "
            "wildlife) or with a Rwanda gorilla trek for a two-country itinerary."
        ),
        "best_time_to_visit": "June - August and December - February (drier — though Bwindi is always damp)",
        "climate": "Cool wet montane (10-25°C). Rain possible any day.",
        "wildlife": "Mountain gorilla (~half the world's population), chimpanzee, forest elephant, L'Hoest's monkey, black-and-white colobus, over 350 bird species including 23 Albertine Rift endemics.",
        "image_slug": None,
        "gallery_count": 0,
        "image_dir": None,
        "is_featured": False,
    },
]
