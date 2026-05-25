"""
Accommodation seed data — real Tanzanian properties matched to images in
core/seed_data/images/accommodations/ by `image_slug`. Price bands reflect
2025-2026 high-season USD rack rates (operators will overwrite with their
actual negotiated rates per booking).

`destination_slug` resolves to a Destination FK at seed time. Latitude /
longitude are approximate (within a few km of the property's real location).
"""

ACCOMMODATIONS = [
    # ============================== SERENGETI ==============================
    # ---------- Ultra-luxury ----------
    {
        "name": "Singita Sasakwa Lodge",
        "destination_slug": "serengeti-national-park",
        "type": "lodge",
        "stars": 5,
        "price_min": 2200, "price_max": 3800,
        "lat": -2.0833, "lng": 34.1500,
        "image_slug": "sasakwa-lodge",
        "short": "Edwardian manor-style lodge on the Singita Grumeti reserve — Out-of-Africa elegance, polo field, private game viewing.",
        "description": (
            "Singita Sasakwa Lodge sits on a hilltop in the private Grumeti Reserve, overlooking 350,000 acres of Serengeti "
            "wilderness. Nine cottages and a manor suite are decorated in Edwardian colonial style with private pools, "
            "antique furnishings and panoramic plains views. The reserve is private — game viewing happens with no other "
            "vehicles in sight. Additional facilities include a polo field, stable, spa, wine cellar, gym and clay-pigeon range."
        ),
        "amenities": "Private pool,Spa,Gym,Wine cellar,Polo field,Stable,WiFi,Laundry,Butler service",
        "is_featured": True,
    },
    {
        "name": "Singita Mara River Tented Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 1800, "price_max": 2800,
        "lat": -1.4500, "lng": 35.0000,
        "image_slug": "singita-mara-river-tented-camp",
        "short": "Six luxury tents on a private bend of the Mara River — the most exclusive crossing-season camp.",
        "description": (
            "Singita's intimate Mara River Camp consists of just six luxury tents on a private stretch of the Mara River in "
            "the northern Serengeti. Tents are built from canvas, recycled glass and reclaimed wood, designed to disappear into "
            "the riverine forest. From July to October the wildebeest migration crosses directly in front of camp; the rest "
            "of the year, resident wildlife along the river is exceptional."
        ),
        "amenities": "Plunge pool,Spa,WiFi,All-inclusive dining,Wine cellar,Library,River views",
        "is_featured": True,
    },
    {
        "name": "andBeyond Klein's Camp",
        "destination_slug": "serengeti-national-park",
        "type": "lodge",
        "stars": 5,
        "price_min": 1100, "price_max": 1800,
        "lat": -1.9500, "lng": 35.1167,
        "image_slug": "andbeyond-kleins-camp",
        "short": "Ten thatched stone cottages on a private concession adjoining the northern Serengeti — game viewing off-road.",
        "description": (
            "Klein's Camp sits on the private 25,000-acre Klein's concession adjoining the northern Serengeti, on the edge of "
            "the Mara River corridor. Ten thatched stone cottages have hand-carved furniture, private verandahs and views over "
            "the Kuka Hills. Because it is a private concession, off-road driving and night drives are permitted — game "
            "experiences impossible inside the national park."
        ),
        "amenities": "Pool,Spa,WiFi,All-inclusive,Off-road driving,Night drives,Walking safari",
        "is_featured": True,
    },
    {
        "name": "Four Seasons Safari Lodge Serengeti",
        "destination_slug": "serengeti-national-park",
        "type": "lodge",
        "stars": 5,
        "price_min": 1200, "price_max": 2200,
        "lat": -2.4333, "lng": 34.8333,
        "image_slug": "four-seasons-serengeti-lodge",
        "short": "Five-star resort-style lodge in central Serengeti — infinity pool overlooking an elephant-frequented watering hole.",
        "description": (
            "Four Seasons Safari Lodge brings full resort-style amenities to the heart of the central Serengeti. Rooms, suites "
            "and villas overlook a year-round watering hole that draws elephant, buffalo and antelope to within metres of the "
            "infinity pool. Facilities include a spa, gym, kids' programme and a wildlife discovery centre — making it one "
            "of the few truly family-friendly luxury options in the park."
        ),
        "amenities": "Infinity pool,Spa,Gym,Kids' club,WiFi,Discovery centre,Family rooms,Multiple restaurants",
        "is_featured": True,
    },
    {
        "name": "Serengeti Bushtops Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 1300, "price_max": 1900,
        "lat": -1.7500, "lng": 35.0833,
        "image_slug": "serengeti-bushtops-camp",
        "short": "Twelve tents in the northern Serengeti with private hot tubs, butler service and migration crossings on the doorstep.",
        "description": (
            "Bushtops Serengeti is set on a remote hillside in the Lamai Wedge in the far north of the Serengeti, directly "
            "above the Mara River corridor. Twelve tented suites each have a private deck with a wood-fired hot tub overlooking "
            "the plains. The location puts you at the heart of the migration river crossings from July to October."
        ),
        "amenities": "Private hot tub,Spa,Butler service,WiFi,All-inclusive,River views,Walking safari",
        "is_featured": True,
    },
    {
        "name": "Lamai Serengeti",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 900, "price_max": 1400,
        "lat": -1.4833, "lng": 34.9333,
        "image_slug": "lamai-serengeti",
        "short": "Architecturally striking lodge built into the Kogakuria kopje — front-row seats on the Lamai Wedge crossings.",
        "description": (
            "Lamai Serengeti tucks into the slopes of the Kogakuria kopje in the far north Lamai Wedge — possibly the most "
            "exclusive sector of the entire ecosystem during crossing season. Twelve rooms across two camps (North and South) "
            "are built around natural granite boulders, with infinity pool and main areas all framing 360° plains views."
        ),
        "amenities": "Pool,Spa,WiFi,All-inclusive,River views,Walking safari",
        "is_featured": True,
    },
    {
        "name": "Sayari Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 1100, "price_max": 1700,
        "lat": -1.4833, "lng": 34.8833,
        "image_slug": "sayari-camp",
        "short": "Asilia's flagship Mara River camp — fifteen tents with stone bath tubs, walking distance to the crossing points.",
        "description": (
            "Sayari is Asilia's flagship property in the northern Serengeti, fifteen luxurious permanent tents perched above "
            "the rolling Mara grasslands. Each tent has a freestanding stone bath and a private verandah. From July to October "
            "the camp's location offers some of the best Mara River crossing access of any operator in the park."
        ),
        "amenities": "Plunge pool,Spa treatments,WiFi,All-inclusive,Stone bath,River access,Walking safari",
        "is_featured": True,
    },
    {
        "name": "Namiri Plains",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 1100, "price_max": 1600,
        "lat": -2.4833, "lng": 35.1667,
        "image_slug": "namiri-plains-serengeti",
        "short": "Closed for 20 years to protect cheetah — Namiri reopened as ten tents on the eastern plains, best big-cat density anywhere.",
        "description": (
            "Namiri Plains sits on the eastern Serengeti's Soit Le Motonyi plains, a sector that was closed to tourism for "
            "20 years to protect breeding cheetah. The reopened camp has just ten tents and a 95 percent cheetah-sighting "
            "record. Lion and leopard density is also exceptional. Open year-round, with the calving herds passing through "
            "in February."
        ),
        "amenities": "WiFi,Pool,Library,All-inclusive,Walking safari,Stargazing",
        "is_featured": False,
    },
    # ---------- Luxury (medium) ----------
    {
        "name": "Dunia Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 850, "price_max": 1300,
        "lat": -2.4833, "lng": 34.7833,
        "image_slug": "dunia-camp",
        "short": "Asilia's central Serengeti camp — Africa's first all-female-staffed safari camp, in the heart of the Moru Kopjes.",
        "description": (
            "Dunia is set in the picturesque Moru Kopjes area of the central Serengeti — granite outcrops rising from open "
            "plains — within easy reach of the resident lion prides and rhino sanctuary. Asilia's choice to staff the camp "
            "entirely with women makes it a leader in the African safari industry. Eight tents, friendly atmosphere, year-round operation."
        ),
        "amenities": "WiFi,All-inclusive,Library,Walking safari,Cultural visits",
        "is_featured": False,
    },
    {
        "name": "Ubuntu Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 4,
        "price_min": 700, "price_max": 1050,
        "lat": -2.0000, "lng": 34.8500,
        "image_slug": "ubuntu-camp",
        "short": "Asilia's mobile migration camp — moves twice yearly to stay with the herds, six tents, intimate atmosphere.",
        "description": (
            "Ubuntu is a mobile camp that relocates twice a year to follow the wildebeest migration: north to the Mara from "
            "June-October, south to the Ndutu calving plains from December-March. Six classic-style tents with bucket showers "
            "and en-suite bathrooms; rustic but well-appointed. Intimate atmosphere, communal meals."
        ),
        "amenities": "Bucket shower,All-inclusive,Library,Walking safari",
        "is_featured": False,
    },
    {
        "name": "Lemala Kuria Hills Lodge",
        "destination_slug": "serengeti-national-park",
        "type": "lodge",
        "stars": 5,
        "price_min": 900, "price_max": 1400,
        "lat": -1.5333, "lng": 34.9167,
        "image_slug": "lemala-kuria-hills-lodge",
        "short": "Contemporary 15-suite lodge in the northern Wogakuria area — heated plunge pools, panoramic plains views.",
        "description": (
            "Kuria Hills sits in the Wogakuria area of the northern Serengeti, ideal for migration crossings July-October. "
            "Fifteen contemporary canvas-and-stone suites each have a private deck with heated plunge pool. Striking modern "
            "design within the bush — different aesthetic from the more traditional safari lodges."
        ),
        "amenities": "Heated plunge pool,Spa,WiFi,All-inclusive,Boutique",
        "is_featured": True,
    },
    {
        "name": "Nimali Central Serengeti",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 850, "price_max": 1250,
        "lat": -2.4333, "lng": 34.8167,
        "image_slug": "nimali-central-serengeti-camp",
        "short": "Eight luxury tents on the Grumeti River in central Serengeti — peaceful, intimate, exceptional service.",
        "description": (
            "Nimali Central is eight luxury tents along the Grumeti River in central Serengeti — slightly off the main game "
            "routes for a quieter feel. Tents feature copper bath tubs and large private verandahs. Hot-air balloon launches "
            "are nearby; great year-round wildlife on the doorstep."
        ),
        "amenities": "Pool,Copper bath,WiFi,All-inclusive,River views",
        "is_featured": False,
    },
    {
        "name": "Faru Faru Lodge",
        "destination_slug": "serengeti-national-park",
        "type": "lodge",
        "stars": 5,
        "price_min": 1200, "price_max": 1900,
        "lat": -2.0833, "lng": 34.2833,
        "image_slug": "faru-faru-lodge",
        "short": "Singita's mid-sized Grumeti property — nine tented suites by the river, family-friendly within the luxury bracket.",
        "description": (
            "Faru Faru is one of three Singita lodges on the private Grumeti Reserve. Nine tented suites are spread along "
            "the Grumeti River with rim-flow pools, designer interiors and the same wildlife access as Sasakwa. The slightly "
            "smaller scale and family-friendly setup makes it popular with multigenerational groups."
        ),
        "amenities": "Pool,Spa,WiFi,All-inclusive,Family-friendly,Stargazing",
        "is_featured": True,
    },
    {
        "name": "Sabora Tented Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 1300, "price_max": 2000,
        "lat": -2.1833, "lng": 34.2167,
        "image_slug": "sabora-tented-camp",
        "short": "Singita's tented camp on the Grumeti plains — Edwardian explorer aesthetic, six tents only.",
        "description": (
            "Sabora is Singita's third Grumeti property — a tented camp evoking the great Edwardian-era exploration camps, "
            "with six elegant guest tents set across an open plain. Antique furnishings, leather armchairs, an open-air "
            "library and a tennis court keep the colonial-explorer aesthetic complete."
        ),
        "amenities": "Pool,Tennis court,Spa,WiFi,All-inclusive,Antique decor,Library",
        "is_featured": False,
    },
    {
        "name": "Grumeti Migration Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 4,
        "price_min": 600, "price_max": 900,
        "lat": -2.0500, "lng": 34.0500,
        "image_slug": "grumeti-migration-camp",
        "short": "Classic mobile-style migration camp in the western Serengeti — eight tents, follows the herds.",
        "description": (
            "Grumeti Migration Camp moves to track the wildebeest migration through the western corridor (May-July river "
            "crossings) and central Serengeti. Eight comfortable canvas tents with bucket showers, hosted meals, and a "
            "back-to-basics safari atmosphere at a moderate price."
        ),
        "amenities": "Bucket shower,All-inclusive,Walking safari,Library",
        "is_featured": False,
    },
    {
        "name": "Serengeti Migration Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 950, "price_max": 1400,
        "lat": -2.0167, "lng": 35.1500,
        "image_slug": "serengeti-migration-camp",
        "short": "Elewana's flagship northern Serengeti camp — twenty raised stilted tents above the Grumeti River.",
        "description": (
            "Elewana's Serengeti Migration Camp has twenty large tented suites raised on stilts above a tributary of the "
            "Grumeti River in the northern Serengeti. Classic East African safari styling, large viewing decks, infinity "
            "pool and a strong reputation for service. Great year-round position."
        ),
        "amenities": "Pool,Spa,WiFi,All-inclusive,River views,Stargazing",
        "is_featured": False,
    },
    {
        "name": "Elewana Serengeti Pioneer Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 4,
        "price_min": 700, "price_max": 1100,
        "lat": -2.5500, "lng": 34.5333,
        "image_slug": "elewana-serengeti-pioneer-camp",
        "short": "Twelve tents in the southern Serengeti, designed in 1930s safari style — antique trunks, brass fittings.",
        "description": (
            "Pioneer Camp is set on a wooded ridge in southern central Serengeti, designed in the romantic 1930s safari style "
            "with traditional Persian rugs, brass fittings, and antique steamer trunks. Twelve tents, an open mess, and "
            "excellent year-round game-viewing in a quieter sector of the park."
        ),
        "amenities": "Pool,WiFi,All-inclusive,Heritage design,Library",
        "is_featured": False,
    },
    {
        "name": "Mwiba Lodge",
        "destination_slug": "serengeti-national-park",
        "type": "lodge",
        "stars": 5,
        "price_min": 1400, "price_max": 2200,
        "lat": -3.1167, "lng": 34.7333,
        "image_slug": "mwiba-lodge",
        "short": "Spectacular cliff-edge lodge on a private 130,000-acre concession south of the Serengeti — walking safaris, night drives, hot-air balloon.",
        "description": (
            "Mwiba is built into a granite gorge on a vast private concession in the southern Serengeti ecosystem, with eight "
            "tented suites cantilevered out from the cliff edge. Because it is on a private concession, walking safaris, "
            "night drives and off-road driving are permitted year-round, and the Lake Eyasi Hadzabe bushmen are nearby."
        ),
        "amenities": "Pool,Spa,WiFi,All-inclusive,Walking safari,Night drives,Cultural visits",
        "is_featured": True,
    },
    # ---------- Mid-range ----------
    {
        "name": "Serengeti Serena Safari Lodge",
        "destination_slug": "serengeti-national-park",
        "type": "lodge",
        "stars": 4,
        "price_min": 340, "price_max": 520,
        "lat": -2.5167, "lng": 34.8333,
        "image_slug": "serengeti-serena-safari-lodge",
        "short": "Mid-range chain lodge in central Serengeti — 66 rooms, pool, Maasai-architecture design, good value.",
        "description": (
            "Serena's flagship Serengeti property has 66 rooms designed as East African villages with conical Maasai-inspired "
            "roofs. Set high on a hill in the central Seronera valley, the lodge offers excellent views, two pools, multiple "
            "restaurants and reliable family-friendly facilities at a much lower price point than the boutique camps."
        ),
        "amenities": "Pool,Spa,WiFi,Multiple restaurants,Kids' menu,Family rooms",
        "is_featured": False,
    },
    {
        "name": "Serengeti Sopa Lodge",
        "destination_slug": "serengeti-national-park",
        "type": "lodge",
        "stars": 4,
        "price_min": 280, "price_max": 450,
        "lat": -2.4167, "lng": 34.6000,
        "image_slug": "serengeti-sopa-lodge",
        "short": "79-room mid-range lodge in central Serengeti — pool, expansive grounds, great for families and groups.",
        "description": (
            "Sopa Lodge sits at the head of a valley in the western Seronera area, offering large two-room suites suitable "
            "for families. Facilities include a 50-metre pool, multiple bars and restaurants, and a soft-pricing structure "
            "that makes it one of the best-value 4-star properties inside the park."
        ),
        "amenities": "Large pool,WiFi,Multiple restaurants,Family suites,Kids' menu",
        "is_featured": False,
    },
    {
        "name": "Mbuzi Mawe Serena Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 4,
        "price_min": 380, "price_max": 580,
        "lat": -2.2167, "lng": 34.8500,
        "image_slug": "mbuzi-mawe-serena-camp",
        "short": "Serena's tented camp in the eastern Seronera valley — 16 tents around a granite kopje frequented by klipspringer.",
        "description": (
            "Mbuzi Mawe (Swahili for 'rocky goat', after the klipspringer antelopes that live here) is Serena's smaller, "
            "more tented sister to Serengeti Serena Safari Lodge. Sixteen large tents are clustered around a granite kopje "
            "in eastern Seronera, perfect big-cat country."
        ),
        "amenities": "Pool,WiFi,Restaurant,Klipspringer viewing",
        "is_featured": False,
    },
    {
        "name": "Kirawira Serena Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 580, "price_max": 880,
        "lat": -2.1500, "lng": 33.9667,
        "image_slug": "kirawira-serena-camp",
        "short": "Serena's premium tented camp in the western Serengeti — 25 grand tents with Victorian colonial decor.",
        "description": (
            "Kirawira sits on a hilltop in the western Serengeti, overlooking the Grumeti River. Twenty-five tents are "
            "decorated in lavish Victorian style with antique furniture, four-poster beds, and silver-service dining. The "
            "western corridor catches the herds in May-July."
        ),
        "amenities": "Pool,WiFi,Antique decor,Silver service,Stargazing,River views",
        "is_featured": False,
    },
    # ---------- Budget / Tented ----------
    {
        "name": "Kati Kati Tented Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 3,
        "price_min": 220, "price_max": 340,
        "lat": -2.4500, "lng": 34.8333,
        "image_slug": "kati-kati-tented-camp",
        "short": "Affordable mobile tented camp in central Serengeti — comfortable canvas tents, en-suite bathrooms, hot bucket showers.",
        "description": (
            "Kati Kati ('in the middle') is a budget-friendly seasonal tented camp in central Serengeti — twelve standard "
            "canvas tents with en-suite bathrooms and bucket showers, hosted communal meals. A great option for travellers "
            "who want the authentic tented experience without the boutique price tag."
        ),
        "amenities": "Bucket shower,En-suite bathroom,Hosted meals",
        "is_featured": False,
    },
    {
        "name": "Mara Kati Kati Tented Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 3,
        "price_min": 240, "price_max": 360,
        "lat": -1.5000, "lng": 34.9667,
        "image_slug": "mara-kati-kati-tented-camp",
        "short": "Northern Serengeti seasonal version of Kati Kati — open Jul-Oct for migration crossings, value pricing.",
        "description": (
            "Mara Kati Kati operates seasonally (July to October) in the Kogatende area of the northern Serengeti to catch "
            "the migration crossings. Twelve simple but comfortable canvas tents, hosted meals, and the same value pricing "
            "as the central Kati Kati."
        ),
        "amenities": "Bucket shower,En-suite,Migration access,Seasonal",
        "is_featured": False,
    },
    {
        "name": "Kubu Kubu Tented Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 4,
        "price_min": 320, "price_max": 480,
        "lat": -2.3833, "lng": 34.9500,
        "image_slug": "kubu-kubu-tented-camp",
        "short": "Tortilis's elevated tented camp in central Serengeti — 25 tents on a ridge with views over the Moru Kopjes.",
        "description": (
            "Kubu Kubu (Swahili for 'baby hippo') sits on a ridge in central Serengeti with sweeping views toward the Moru "
            "Kopjes. Twenty-five tents on raised platforms, infinity pool, and excellent service make this one of the best "
            "mid-range options in the central park."
        ),
        "amenities": "Infinity pool,WiFi,All-inclusive,Stargazing,Family rooms",
        "is_featured": False,
    },
    {
        "name": "Lemala Ewanjan Tented Camp",
        "destination_slug": "serengeti-national-park",
        "type": "camp",
        "stars": 4,
        "price_min": 480, "price_max": 720,
        "lat": -2.4000, "lng": 34.8333,
        "image_slug": "lemala-ewanjan-tented-camp",
        "short": "Twelve secluded tents in the central Seronera valley — quiet location off the main routes, good for predators.",
        "description": (
            "Ewanjan is Lemala's central Serengeti tented camp, tucked into a quiet acacia grove off the main Seronera tourist "
            "routes. Twelve tents, hot-bucket showers, hosted meals — classic African safari aesthetic with surprising "
            "comfort. Year-round operation."
        ),
        "amenities": "Bucket shower,All-inclusive,Quiet location,Walking safari",
        "is_featured": False,
    },

    # ============================== NGORONGORO ==============================
    {
        "name": "andBeyond Ngorongoro Crater Lodge",
        "destination_slug": "ngorongoro-crater",
        "type": "lodge",
        "stars": 5,
        "price_min": 1800, "price_max": 2800,
        "lat": -3.2333, "lng": 35.5500,
        "image_slug": "andbeyond-ngorongoro-crater-lodge",
        "short": "Theatrical baroque suites on the crater rim — gold-leaf ceilings, chandeliers, Maasai-warrior butlers.",
        "description": (
            "Crater Lodge is Africa's most theatrical luxury lodge — thirty suites with gold-leaf domed ceilings, crystal "
            "chandeliers and antique furniture, perched on the rim of the Ngorongoro Crater. Each suite has a private "
            "butler in traditional Maasai dress, a private deck overlooking the crater floor, and complimentary champagne."
        ),
        "amenities": "Butler service,Spa,WiFi,All-inclusive,Champagne breakfast,Antique decor",
        "is_featured": True,
    },
    {
        "name": "The Highlands by Asilia",
        "destination_slug": "ngorongoro-crater",
        "type": "lodge",
        "stars": 5,
        "price_min": 950, "price_max": 1400,
        "lat": -3.0833, "lng": 35.5167,
        "image_slug": "lemala-nanyukie",  # placeholder image
        "short": "Eight geodesic-dome suites high on the Olmoti volcano — striking modern architecture, walking and cultural access.",
        "description": (
            "Set on the slopes of Olmoti volcano above the crater, the Highlands is Asilia's most architecturally unusual "
            "property — eight glass-and-steel geodesic domes with wood-burning stoves, sheepskin rugs and crater views. "
            "Walking safaris, Maasai cultural visits and the rarely-visited Olmoti crater are all on the doorstep."
        ),
        "amenities": "Wood stove,Spa,WiFi,All-inclusive,Walking,Cultural visits",
        "is_featured": False,
    },
    {
        "name": "Lion's Paw Camp Ngorongoro",
        "destination_slug": "ngorongoro-crater",
        "type": "camp",
        "stars": 4,
        "price_min": 480, "price_max": 720,
        "lat": -3.2000, "lng": 35.5667,
        "image_slug": "lions-paw-camp-ngorongoro",
        "short": "Ten tents on the crater rim — closest camp to the descent road, simple but well-located.",
        "description": (
            "Lion's Paw is a tented camp set right on the eastern rim of the Ngorongoro Crater, the closest property to "
            "the main descent road into the crater floor. Ten standard tents with hot-bucket showers — simple compared to "
            "the rim's luxury lodges, but unbeatable location for the first dawn descent."
        ),
        "amenities": "Bucket shower,En-suite,Crater views,Quiet location",
        "is_featured": False,
    },
    {
        "name": "Ngorongoro Serena Safari Lodge",
        "destination_slug": "ngorongoro-crater",
        "type": "lodge",
        "stars": 4,
        "price_min": 380, "price_max": 580,
        "lat": -3.2000, "lng": 35.5333,
        "image_slug": "ngorongoro-serena-safari-lodge",
        "short": "Stone-and-thatch chain lodge on the crater rim — 75 rooms, pool, panoramic views from every room.",
        "description": (
            "Serena's Ngorongoro property is built into the rim itself, with stone-and-thatch architecture blending into the "
            "landscape. Seventy-five rooms each have private balconies with direct crater views; multiple restaurants and "
            "an outdoor pool make it family-friendly. A reliable mid-range option."
        ),
        "amenities": "Pool,WiFi,Multiple restaurants,Crater views,Family rooms",
        "is_featured": False,
    },
    {
        "name": "Ngorongoro Sopa Lodge",
        "destination_slug": "ngorongoro-crater",
        "type": "lodge",
        "stars": 4,
        "price_min": 320, "price_max": 480,
        "lat": -3.1667, "lng": 35.6167,
        "image_slug": "ngorongoro-sopa-lodge",
        "short": "Eastern-rim chain lodge — 92 large suites, private descent road, more affordable than rim peers.",
        "description": (
            "Sopa Lodge sits on the eastern rim of the crater, with 92 suite-style rooms and its own private descent road "
            "into the crater (avoiding queues at the main gate). Large rooms, expansive grounds, and pricing that beats "
            "most rim competitors — a popular family choice."
        ),
        "amenities": "Pool,Private crater access,Large suites,WiFi,Family-friendly",
        "is_featured": False,
    },
    {
        "name": "Lemala Ngorongoro Tented Camp",
        "destination_slug": "ngorongoro-crater",
        "type": "camp",
        "stars": 4,
        "price_min": 580, "price_max": 880,
        "lat": -3.1833, "lng": 35.5667,
        "image_slug": "lemala-ngorongoro-tented-camp",
        "short": "Nine tents in a clearing on the descent road side of the crater — wake-up to elephants passing the tents.",
        "description": (
            "Lemala Ngorongoro is the only camp inside the conservation area but BELOW the rim, set in an acacia grove on "
            "the road down to the crater floor. Nine tents, woodstoves for warmth, and a genuine chance of bushbuck and "
            "elephant walking through camp at night."
        ),
        "amenities": "Wood stove,Hot bucket shower,All-inclusive,Wildlife in camp",
        "is_featured": False,
    },
    {
        "name": "Melia Ngorongoro Lodge",
        "destination_slug": "ngorongoro-crater",
        "type": "lodge",
        "stars": 4,
        "price_min": 280, "price_max": 440,
        "lat": -3.2000, "lng": 35.4833,
        "image_slug": "melia-ngorongoro-lodge",
        "short": "International chain on the southwestern rim — modern rooms, pool, good value with crater access.",
        "description": (
            "Meliá's Ngorongoro property is a modern 88-room lodge on the southwestern rim, offering more contemporary "
            "rooms and facilities than the older chain lodges. Pool, gym, spa, and a competitive price point for the "
            "rim location."
        ),
        "amenities": "Pool,Spa,Gym,WiFi,Modern rooms",
        "is_featured": False,
    },

    # ============================== TARANGIRE ==============================
    {
        "name": "Sanctuary Swala",
        "destination_slug": "tarangire-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 850, "price_max": 1300,
        "lat": -4.0833, "lng": 35.7833,
        "image_slug": "sanctuary-swala",
        "short": "Twelve tents in southwestern Tarangire — secluded acacia grove, frequented by elephant and resident lions.",
        "description": (
            "Swala (Swahili for 'antelope') sits in a remote acacia grove in the southwestern corner of Tarangire National "
            "Park, far from the day-tripper routes. Twelve tents with copper bath tubs and verandahs overlooking a busy "
            "watering hole. Elephant herds drink within metres of the public deck. Excellent year-round."
        ),
        "amenities": "Pool,Spa,WiFi,All-inclusive,Walking safari,Wildlife in camp",
        "is_featured": True,
    },
    {
        "name": "Chem Chem Lodge",
        "destination_slug": "tarangire-national-park",
        "type": "lodge",
        "stars": 5,
        "price_min": 1100, "price_max": 1700,
        "lat": -3.7833, "lng": 35.9000,
        "image_slug": "chem-chem-lodge",
        "short": "Eight large suites on a private corridor between Tarangire and Lake Manyara — walking and night drives.",
        "description": (
            "Chem Chem sits on a private corridor connecting Tarangire and Lake Manyara, an area free of vehicle traffic. "
            "Eight enormous tented suites blend safari classicism with contemporary design. Walking safari, night drives and "
            "off-road driving are all available — game experiences not permitted inside the national parks."
        ),
        "amenities": "Pool,Spa,WiFi,All-inclusive,Walking,Night drives,Private concession",
        "is_featured": True,
    },
    {
        "name": "Elewana Tarangire Treetops",
        "destination_slug": "tarangire-national-park",
        "type": "lodge",
        "stars": 5,
        "price_min": 750, "price_max": 1150,
        "lat": -3.7000, "lng": 36.0167,
        "image_slug": "elewana-tarangire-treetops",
        "short": "Twenty huge stilted treehouse suites in ancient baobab trees — Tarangire's most unique sleep.",
        "description": (
            "Treetops is a unique lodge with twenty suites built into the canopy of ancient baobab and marula trees just "
            "outside Tarangire's eastern boundary. Each suite is enormous — the largest rooms in northern Tanzania — with "
            "panoramic windows overlooking a watering hole that draws elephant herds reliably."
        ),
        "amenities": "Pool,Spa,WiFi,All-inclusive,Treehouse rooms,Wildlife views,Walking",
        "is_featured": True,
    },
    {
        "name": "Oliver's Camp",
        "destination_slug": "tarangire-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 850, "price_max": 1300,
        "lat": -4.1500, "lng": 36.0167,
        "image_slug": "olivers-camp-tarangire",
        "short": "Asilia's classic mobile-style camp in southern Tarangire — ten tents, walking safari and night drives in private concession.",
        "description": (
            "Oliver's Camp pioneered walking safari in Tarangire and remains one of the best for it. Ten classic tents in "
            "a private concession in the wild southern part of the park; nights are quiet apart from the lion and hyena. "
            "Walking and night drives are this camp's signature."
        ),
        "amenities": "Walking safari,Night drives,All-inclusive,Library",
        "is_featured": False,
    },
    {
        "name": "Tarangire Safari Lodge",
        "destination_slug": "tarangire-national-park",
        "type": "lodge",
        "stars": 4,
        "price_min": 280, "price_max": 420,
        "lat": -3.9500, "lng": 36.0000,
        "image_slug": "tarangire-safari-lodge",
        "short": "Classic 1980s safari lodge on a cliff above the Tarangire River — 35 tents/bungalows, excellent value, prime location.",
        "description": (
            "Tarangire Safari Lodge has the best location of any property inside the park — perched on a cliff above the "
            "Tarangire River, with panoramic views of the elephant-frequented river bend. 35 tents and bungalows on a "
            "shady site dotted with baobabs. Excellent value within the park."
        ),
        "amenities": "Pool,WiFi,Restaurant,Elephant views,Cliff location",
        "is_featured": True,
    },
    {
        "name": "Tarangire Sopa Lodge",
        "destination_slug": "tarangire-national-park",
        "type": "lodge",
        "stars": 4,
        "price_min": 260, "price_max": 400,
        "lat": -3.8833, "lng": 36.0167,
        "image_slug": "tarangire-sopa-lodge",
        "short": "75-room mid-range lodge in central Tarangire — pool, restaurant, suite-sized rooms, family-friendly.",
        "description": (
            "Sopa's Tarangire property has 75 rooms in stone bungalows scattered across landscaped grounds in the heart of "
            "the park. Large two-room suites suit families, pool and multiple dining options round out the resort feel. "
            "Reliable mid-range pick."
        ),
        "amenities": "Pool,Family suites,Multiple restaurants,WiFi",
        "is_featured": False,
    },
    {
        "name": "Maramboi Tented Camp",
        "destination_slug": "tarangire-national-park",
        "type": "camp",
        "stars": 3,
        "price_min": 220, "price_max": 340,
        "lat": -3.8500, "lng": 35.8000,
        "image_slug": "maramboi-tented-camp",
        "short": "Forty tents between Tarangire and Lake Manyara — open plains location, often visited by zebra and wildebeest.",
        "description": (
            "Maramboi sits on the open plains between Tarangire and Lake Manyara — outside both parks but in a wildlife "
            "corridor crossed daily by zebra and wildebeest. Forty large tents, two pools, and a hosted-dinner format. "
            "Walking safari is permitted here."
        ),
        "amenities": "Two pools,Walking safari,Wildlife in camp,Mid-range pricing",
        "is_featured": False,
    },

    # ============================== LAKE MANYARA ==============================
    {
        "name": "andBeyond Lake Manyara Tree Lodge",
        "destination_slug": "lake-manyara-national-park",
        "type": "lodge",
        "stars": 5,
        "price_min": 1300, "price_max": 1900,
        "lat": -3.6000, "lng": 35.8500,
        "image_slug": "andbeyond-lake-manyara-tree-lodge",
        "short": "Ten elevated treehouse suites in mahogany forest inside the park — the only lodge inside Manyara.",
        "description": (
            "Lake Manyara Tree Lodge is the only accommodation INSIDE Lake Manyara National Park — ten luxury treehouse "
            "suites built on stilts in a centuries-old mahogany forest. Tree-climbing lion territory is on the doorstep, "
            "and the lake's flamingo flocks are 15 minutes' drive away."
        ),
        "amenities": "Pool,Spa,WiFi,All-inclusive,Forest setting,Tree house design,Walking safari",
        "is_featured": True,
    },
    {
        "name": "Lake Manyara Serena Safari Lodge",
        "destination_slug": "lake-manyara-national-park",
        "type": "lodge",
        "stars": 4,
        "price_min": 340, "price_max": 520,
        "lat": -3.5667, "lng": 35.8833,
        "image_slug": "lake-manyara-serena-safari-lodge",
        "short": "Cliff-top chain lodge above Lake Manyara — 67 rooms, panoramic views over the lake and rift valley.",
        "description": (
            "Serena's Manyara lodge perches on top of the rift escarpment, with sweeping views down across the lake and "
            "out to the rift valley floor. 67 rooms, pool, multiple restaurants. Lake Manyara is small enough that a half-day "
            "game drive suffices, making this a comfortable mid-route stop."
        ),
        "amenities": "Pool,Spa,WiFi,Cliff views,Family rooms",
        "is_featured": False,
    },
    {
        "name": "Escarpment Luxury Lodge",
        "destination_slug": "lake-manyara-national-park",
        "type": "lodge",
        "stars": 5,
        "price_min": 580, "price_max": 880,
        "lat": -3.5500, "lng": 35.8333,
        "image_slug": "escarpment-luxury-lodge-manyara",
        "short": "Sixteen suites on the rift escarpment — spectacular views, infinity pool, walking distance to crater ascent.",
        "description": (
            "Escarpment Lodge is built into the edge of the rift escarpment above Manyara, offering some of the most dramatic "
            "views in northern Tanzania. Sixteen large suites, infinity pool overlooking the rift valley, and easy onward "
            "access to Ngorongoro and Tarangire."
        ),
        "amenities": "Infinity pool,Spa,WiFi,All-inclusive,Cliff views",
        "is_featured": False,
    },
    {
        "name": "Kirurumu Manyara Lodge",
        "destination_slug": "lake-manyara-national-park",
        "type": "lodge",
        "stars": 4,
        "price_min": 280, "price_max": 440,
        "lat": -3.5500, "lng": 35.8500,
        "image_slug": "kirurumu-manyara-lodge",
        "short": "27 tented rooms on the rift escarpment — sundowner views over the lake, mid-range pricing.",
        "description": (
            "Kirurumu sits on the rift escarpment with great views over Lake Manyara below. Twenty-seven tented rooms with "
            "private decks, a swimming pool, and a quieter atmosphere than the larger chain lodges. Strong value."
        ),
        "amenities": "Pool,Lake views,WiFi,Tented rooms",
        "is_featured": False,
    },

    # ============================== ARUSHA ==============================
    {
        "name": "Legendary Lodge",
        "destination_slug": "arusha-national-park",
        "type": "lodge",
        "stars": 5,
        "price_min": 480, "price_max": 720,
        "lat": -3.3833, "lng": 36.8167,
        "image_slug": "legendary-lodge-arusha",
        "short": "Eight cottages on a coffee farm at the foot of Mount Meru — Singita-quality finishes, ideal arrival/departure stop.",
        "description": (
            "Legendary Lodge is Elewana's Arusha boutique lodge — eight private cottages set in a working coffee plantation "
            "at the base of Mount Meru, twenty minutes from Kilimanjaro International Airport. Spacious cottages, a pool, "
            "spa, and excellent farm-to-table dining make it the natural overnight before flying out to safari camps."
        ),
        "amenities": "Pool,Spa,WiFi,Restaurant,Coffee tour,Garden",
        "is_featured": True,
    },
    {
        "name": "Arusha Coffee Lodge",
        "destination_slug": "arusha-national-park",
        "type": "lodge",
        "stars": 4,
        "price_min": 280, "price_max": 440,
        "lat": -3.3833, "lng": 36.7000,
        "image_slug": "arusha-coffee-lodge",
        "short": "Plantation lodge on the outskirts of Arusha — 30 chalets in coffee fields, close to KIA airport.",
        "description": (
            "Arusha Coffee Lodge sits on a working 70-acre coffee plantation 25 minutes from the airport. Thirty large "
            "garden suites in colonial-style chalets, an outdoor pool, three restaurants, and the chance to walk into "
            "the coffee fields with the plantation manager."
        ),
        "amenities": "Pool,Spa,WiFi,Restaurant,Coffee plantation,Airport transfer",
        "is_featured": False,
    },
    {
        "name": "Arusha Serena Hotel",
        "destination_slug": "arusha-national-park",
        "type": "hotel",
        "stars": 4,
        "price_min": 220, "price_max": 360,
        "lat": -3.3833, "lng": 36.7167,
        "image_slug": "arusha-serena-hotel",
        "short": "Lake Duluti Serena property — 51 rooms in colonial gardens, swimming, lakeside walks.",
        "description": (
            "Serena's Arusha property is set in gardens overlooking the crater lake at Duluti, a small extinct volcano "
            "lake. 51 rooms in two colonial buildings, pool, lake walks, and proximity to the airport make this a reliable "
            "stopover hotel."
        ),
        "amenities": "Pool,Spa,Lake walks,Restaurant,Airport transfer",
        "is_featured": False,
    },
    {
        "name": "Gran Meliá Arusha",
        "destination_slug": "arusha-national-park",
        "type": "hotel",
        "stars": 5,
        "price_min": 380, "price_max": 580,
        "lat": -3.3833, "lng": 36.6833,
        "image_slug": "gran-melia-arusha",
        "short": "Arusha's newest 5-star — full-service business hotel with safari concierge, large pool and spa.",
        "description": (
            "Gran Meliá Arusha opened in 2022 and is the city's most contemporary luxury hotel — 165 rooms and suites, "
            "large outdoor pool, full spa, gym, multiple dining options. Suited to either pre-safari business stays or "
            "transit nights for travellers who prefer a city hotel over a garden lodge."
        ),
        "amenities": "Pool,Spa,Gym,Multiple restaurants,WiFi,Conference facilities",
        "is_featured": True,
    },
    {
        "name": "Rivertrees Country Inn",
        "destination_slug": "arusha-national-park",
        "type": "boutique",
        "stars": 4,
        "price_min": 240, "price_max": 380,
        "lat": -3.3500, "lng": 36.9333,
        "image_slug": "rivertrees-country-inn",
        "short": "Family-run boutique inn 20 minutes from KIA — country-house atmosphere in coffee-and-banana gardens.",
        "description": (
            "Rivertrees has been hosting travellers for decades and feels like a country home — twenty-five rooms across a "
            "main house, garden chalets and river cottages in a tropical garden on the river. Genuinely warm hosts, "
            "excellent farm-style food, and pure tranquility before or after safari."
        ),
        "amenities": "Pool,Garden,WiFi,Restaurant,River walks,Family-run",
        "is_featured": True,
    },
    {
        "name": "Onsea House",
        "destination_slug": "arusha-national-park",
        "type": "boutique",
        "stars": 4,
        "price_min": 280, "price_max": 440,
        "lat": -3.4000, "lng": 36.6500,
        "image_slug": "onsea-house",
        "short": "Belgian-run boutique guesthouse — eight rooms, internationally-acclaimed restaurant, hillside garden views.",
        "description": (
            "Onsea House is a small, Belgian-run boutique with eight rooms on a hillside in suburban Arusha. Its restaurant "
            "is the highest-rated in northern Tanzania, with a frequently-rotating tasting menu. Genuinely small, intimate, "
            "and very different from chain hotels."
        ),
        "amenities": "Pool,Garden,Acclaimed restaurant,WiFi,Boutique",
        "is_featured": False,
    },
    {
        "name": "Mount Meru Hotel",
        "destination_slug": "arusha-national-park",
        "type": "hotel",
        "stars": 4,
        "price_min": 180, "price_max": 290,
        "lat": -3.3667, "lng": 36.6833,
        "image_slug": "mount-meru-hotel",
        "short": "168-room city-centre business hotel — pool, gym, conference facilities, reliable mid-range value.",
        "description": (
            "Mount Meru Hotel is Arusha's largest international-standard hotel — 168 rooms, two pools, a gym, conference "
            "facilities, casino, and multiple restaurants. Suited to business travellers and large groups; central "
            "location with easy onward transfers to safari."
        ),
        "amenities": "Two pools,Gym,Casino,Conference centre,Multiple restaurants,WiFi",
        "is_featured": False,
    },
    {
        "name": "The African Tulip",
        "destination_slug": "arusha-national-park",
        "type": "boutique",
        "stars": 4,
        "price_min": 200, "price_max": 320,
        "lat": -3.3833, "lng": 36.6833,
        "image_slug": "the-african-tulip",
        "short": "Boutique central-Arusha hotel — 29 rooms, walking distance to restaurants and the clock tower.",
        "description": (
            "The African Tulip is a stylish 29-room boutique hotel in central Arusha, walking distance to the clock tower "
            "and the city's better restaurants. Pool, spa, and one of the better in-house restaurants in town. Good choice "
            "for travellers who want to be in the city itself."
        ),
        "amenities": "Pool,Spa,Restaurant,WiFi,Central location,Boutique",
        "is_featured": False,
    },
    {
        "name": "Kibo Palace Hotel",
        "destination_slug": "arusha-national-park",
        "type": "hotel",
        "stars": 4,
        "price_min": 140, "price_max": 230,
        "lat": -3.3833, "lng": 36.6833,
        "image_slug": "kibo-palace-hotel",
        "short": "Mid-range business hotel in Arusha city centre — 51 rooms, pool, good value transit stay.",
        "description": (
            "Kibo Palace is a reliable mid-range business hotel in central Arusha with 51 modern rooms, an outdoor pool, "
            "gym and conference facilities. Walking distance to the city's main commercial area and the bus station. "
            "Strong value for transit nights."
        ),
        "amenities": "Pool,Gym,Conference,Restaurant,WiFi",
        "is_featured": False,
    },
    {
        "name": "Planet Lodge Arusha",
        "destination_slug": "arusha-national-park",
        "type": "lodge",
        "stars": 3,
        "price_min": 90, "price_max": 150,
        "lat": -3.3833, "lng": 36.7000,
        "image_slug": "planet-lodge-arusha",
        "short": "Budget garden lodge on the outskirts of Arusha — 25 rooms in tropical gardens, value pricing.",
        "description": (
            "Planet Lodge is a budget-friendly garden lodge on the outskirts of Arusha, with 25 rooms in stone-and-thatch "
            "chalets across landscaped gardens. Pool, restaurant, transfer service. Great for backpacker/budget safari "
            "operators and overland travellers."
        ),
        "amenities": "Pool,Garden,WiFi,Restaurant,Budget pricing",
        "is_featured": False,
    },

    # ============================== KILIMANJARO ==============================
    {
        "name": "Kaliwa Lodge",
        "destination_slug": "mount-kilimanjaro",
        "type": "lodge",
        "stars": 4,
        "price_min": 220, "price_max": 360,
        "lat": -3.2333, "lng": 37.2333,
        "image_slug": "kaliwa-lodge",
        "short": "Boutique lodge on Kilimanjaro's lower slopes — 14 stone cottages, the natural pre/post-climb stay.",
        "description": (
            "Kaliwa Lodge sits in the foothills of Kilimanjaro near Moshi, a 30-minute drive from the Machame and Marangu "
            "gates. Fourteen stone cottages with private gardens, a pool, and direct views of the mountain on clear days. "
            "Used by most quality climbing operators as the briefing and post-summit lodge."
        ),
        "amenities": "Pool,Spa,WiFi,Restaurant,Mountain views,Pre-climb briefing",
        "is_featured": True,
    },
    {
        "name": "Weru Weru River Lodge",
        "destination_slug": "mount-kilimanjaro",
        "type": "lodge",
        "stars": 4,
        "price_min": 160, "price_max": 260,
        "lat": -3.3000, "lng": 37.3000,
        "image_slug": "weru-weru-river-lodge",
        "short": "Garden lodge on a river in the Kilimanjaro foothills — 22 rooms, jungle gym, pre/post-climb favourite.",
        "description": (
            "Weru Weru sits on the banks of a small river in the Kili foothills near Moshi. Twenty-two garden rooms, pool, "
            "and a calm jungle-edge atmosphere ideal for unwinding before or after a climb. Free transfers from Moshi airport."
        ),
        "amenities": "Pool,Garden,WiFi,Restaurant,River walks",
        "is_featured": False,
    },
    {
        "name": "Kilimanjaro Luxury Tented Camp",
        "destination_slug": "mount-kilimanjaro",
        "type": "camp",
        "stars": 5,
        "price_min": 320, "price_max": 480,
        "lat": -3.2333, "lng": 37.2667,
        "image_slug": "kilimanjaro-luxury-tented-camp",
        "short": "Boutique tented camp on Kilimanjaro's lower slopes — combines safari aesthetic with mountain views.",
        "description": (
            "Kilimanjaro Luxury Tented Camp offers eight permanent tents on the lower slopes of Kilimanjaro, blending the "
            "safari-tent aesthetic with mountain views unique to this region. Pool, fire pit, mountain-view dining deck."
        ),
        "amenities": "Pool,WiFi,All-inclusive,Mountain views,Fire pit",
        "is_featured": False,
    },

    # ============================== SELOUS / NYERERE ==============================
    {
        "name": "Sand Rivers Selous",
        "destination_slug": "selous-game-reserve-nyerere-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 950, "price_max": 1500,
        "lat": -8.0000, "lng": 36.9833,
        "image_slug": "roho-ya-selous",  # closest available image
        "short": "Nomad Tanzania's flagship Selous property — eight stone-and-canvas rooms on the Rufiji River.",
        "description": (
            "Sand Rivers is Nomad Tanzania's flagship Selous lodge — eight open-fronted stone-and-canvas rooms perched "
            "above a quiet bend of the Rufiji River. Boat safaris, walking safaris and fly camping are all on offer in "
            "what is arguably Tanzania's wildest park."
        ),
        "amenities": "Pool,All-inclusive,Boat safari,Walking safari,Fly camping,River views",
        "is_featured": True,
    },
    {
        "name": "Selous Serena Camp",
        "destination_slug": "selous-game-reserve-nyerere-national-park",
        "type": "camp",
        "stars": 4,
        "price_min": 480, "price_max": 720,
        "lat": -7.8333, "lng": 38.1667,
        "image_slug": "selous-serena-camp",
        "short": "Twelve tented suites on Lake Nzerakera — boat safari on the lake, walking and game drives in the reserve.",
        "description": (
            "Serena's Selous property is twelve tented suites on a deck overlooking Lake Nzerakera, a tributary lake of "
            "the Rufiji system. Daily boat safaris on the lake, walking safari in the surrounding bush, and game drives "
            "into the wider reserve."
        ),
        "amenities": "Pool,Boat safari,Walking safari,All-inclusive,Lake views",
        "is_featured": False,
    },
    {
        "name": "Rufiji River Camp",
        "destination_slug": "selous-game-reserve-nyerere-national-park",
        "type": "camp",
        "stars": 4,
        "price_min": 380, "price_max": 580,
        "lat": -7.9667, "lng": 37.7833,
        "image_slug": "rufiji-river-camp",
        "short": "Twenty tents on the Rufiji River — classic Selous experience at mid-range pricing, boat safari focus.",
        "description": (
            "Rufiji River Camp has been a Selous staple since the 1980s — twenty large tents along the river bank, with "
            "boat safari as the centerpiece of the experience. Excellent value for the experience in Nyerere National Park."
        ),
        "amenities": "Pool,Boat safari,Walking,All-inclusive,River views",
        "is_featured": False,
    },
    {
        "name": "Roho Ya Selous",
        "destination_slug": "selous-game-reserve-nyerere-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 700, "price_max": 1050,
        "lat": -8.0833, "lng": 37.3167,
        "image_slug": "roho-ya-selous",
        "short": "Asilia's central Selous camp — eight tents on Lake Manze, prime African wild dog territory.",
        "description": (
            "Roho ya Selous ('Heart of the Selous') is Asilia's eight-tent camp on the edge of Lake Manze, prime African "
            "wild dog territory in the heart of the reserve. Excellent year-round, with boat safaris on the lake and game "
            "drives in surrounding bush."
        ),
        "amenities": "Pool,Boat safari,All-inclusive,Wild dog viewing,Walking",
        "is_featured": True,
    },
    {
        "name": "Lemala Mpingo Ridge Lodge",
        "destination_slug": "selous-game-reserve-nyerere-national-park",
        "type": "lodge",
        "stars": 5,
        "price_min": 580, "price_max": 880,
        "lat": -7.8500, "lng": 38.1833,
        "image_slug": "lemala-mpingo-ridge-lodge",
        "short": "Twelve stone suites on a ridge above the Rufiji — open vista, eco-friendly design, fly camping option.",
        "description": (
            "Mpingo Ridge sits on a high ridge overlooking the Rufiji floodplain, with twelve eco-built stone suites and "
            "panoramic views. Solar-powered, low-impact design, with the full range of Selous activities (boat, walking, "
            "drives, fly camping)."
        ),
        "amenities": "Pool,Solar,All-inclusive,Boat safari,Fly camping,Ridge views",
        "is_featured": False,
    },

    # ============================== ZANZIBAR (BEACH) ==============================
    {
        "name": "andBeyond Mnemba Island",
        "destination_slug": "pemba-island",  # Mnemba is technically off NE Unguja but in image set under pemba
        "type": "resort",
        "stars": 5,
        "price_min": 2200, "price_max": 3500,
        "lat": -5.8167, "lng": 39.3833,
        "image_slug": "andbeyond-mnemba-island",
        "short": "Twelve thatched beach bandas on a private island — one of Africa's most exclusive beach hideouts.",
        "description": (
            "Mnemba is a tiny private island in a coral atoll off the northeast tip of Unguja. Twelve thatched palm-roofed "
            "bandas open onto a single uninterrupted beach. Diving and snorkelling on house reefs, kitesurfing, dhow trips. "
            "All-inclusive at the top end of African luxury."
        ),
        "amenities": "Private island,All-inclusive,Snorkelling,Diving,Kitesurf,Spa",
        "is_featured": True,
    },
    {
        "name": "Park Hyatt Zanzibar",
        "destination_slug": "zanzibar-stone-town",
        "type": "hotel",
        "stars": 5,
        "price_min": 480, "price_max": 780,
        "lat": -6.1583, "lng": 39.1917,
        "image_slug": "park-hyatt-zanzibar",
        "short": "67-room urban-meets-beach 5-star — Stone Town location with a private beach and pool, white-glove service.",
        "description": (
            "Park Hyatt Zanzibar combines a Stone Town heritage building with a contemporary wing, all opening onto a "
            "private beach. 67 rooms, pool, spa, gym, multiple restaurants — the best 5-star hotel actually inside Stone "
            "Town itself."
        ),
        "amenities": "Pool,Spa,Gym,Beach,WiFi,Multiple restaurants",
        "is_featured": True,
    },
    {
        "name": "Zuri Zanzibar",
        "destination_slug": "zanzibar-stone-town",
        "type": "resort",
        "stars": 5,
        "price_min": 580, "price_max": 980,
        "lat": -5.7500, "lng": 39.3000,
        "image_slug": "zuri-zanzibar",
        "short": "55-villa boutique resort on Kendwa beach — designer interiors, eco-luxury aesthetic, pristine sand.",
        "description": (
            "Zuri sits on the powdery Kendwa beach in northern Zanzibar — 55 boutique villas and suites in a hand-painted "
            "eco-luxury style, two pools, full spa, multiple restaurants. One of the best beach resorts on the island."
        ),
        "amenities": "Pools,Spa,Beach,WiFi,Multiple restaurants,Villas",
        "is_featured": True,
    },
    {
        "name": "The Residence Zanzibar",
        "destination_slug": "zanzibar-stone-town",
        "type": "resort",
        "stars": 5,
        "price_min": 580, "price_max": 980,
        "lat": -6.2500, "lng": 39.3000,
        "image_slug": "the-residence-zanzibar",
        "short": "66 private villas on the southwest coast — most with private pool, lush garden setting, beach access.",
        "description": (
            "The Residence on Zanzibar's southwest coast has 66 villas (most with private plunge pools) in a 32-hectare "
            "coastal estate with mature gardens, restaurants and a long private beach. One of the more spacious resorts "
            "on the island."
        ),
        "amenities": "Private pool villas,Spa,Beach,WiFi,Multiple restaurants,Gardens",
        "is_featured": True,
    },
    {
        "name": "Baraza Resort & Spa",
        "destination_slug": "zanzibar-stone-town",
        "type": "resort",
        "stars": 5,
        "price_min": 520, "price_max": 880,
        "lat": -6.2333, "lng": 39.5500,
        "image_slug": "baraza-resort-and-spa-zanzibar",
        "short": "30 all-suite villas on Bwejuu beach — Persian-Arab-Indian design, all-inclusive, adults-only-leaning.",
        "description": (
            "Baraza is a small all-suite resort on the southeastern Bwejuu beach with strong Arab-Persian-Indian decor "
            "throughout. Thirty suites with private plunge pools, beach access, spa, multiple restaurants. All-inclusive "
            "rate structure with a calm adults-focused atmosphere."
        ),
        "amenities": "Private plunge pools,All-inclusive,Spa,Beach,Multiple restaurants",
        "is_featured": False,
    },
    {
        "name": "Melia Zanzibar",
        "destination_slug": "zanzibar-stone-town",
        "type": "resort",
        "stars": 5,
        "price_min": 380, "price_max": 620,
        "lat": -5.9500, "lng": 39.3500,
        "image_slug": "melia-zanzibar",
        "short": "162-room beach resort on Kiwengwa — multiple pools, restaurants, kids' club, family-friendly all-inclusive.",
        "description": (
            "Meliá's Zanzibar property has 162 rooms across spacious tropical gardens on the eastern Kiwengwa beach. "
            "Multiple pools, six restaurants, kids' club, spa — a full-service family-friendly resort with all-inclusive "
            "rate options."
        ),
        "amenities": "Multiple pools,Kids' club,Spa,All-inclusive,Six restaurants,Beach",
        "is_featured": False,
    },
    {
        "name": "Essque Zalu Zanzibar",
        "destination_slug": "zanzibar-stone-town",
        "type": "resort",
        "stars": 5,
        "price_min": 420, "price_max": 720,
        "lat": -5.7333, "lng": 39.3333,
        "image_slug": "essque-zalu-zanzibar",
        "short": "Cliff-top boutique resort near Nungwi — 38 suites, dramatic jetty restaurant, infinity pool.",
        "description": (
            "Essque Zalu sits on a clifftop overlooking the Indian Ocean near Nungwi on the northern tip of Zanzibar. "
            "Thirty-eight suites, infinity pool, spa, and a famous jetty restaurant suspended over the water at sunset. "
            "More adult-oriented than the family resorts."
        ),
        "amenities": "Infinity pool,Cliff views,Jetty restaurant,Spa,WiFi",
        "is_featured": False,
    },
    {
        "name": "Konokono Beach Resort",
        "destination_slug": "zanzibar-stone-town",
        "type": "resort",
        "stars": 5,
        "price_min": 350, "price_max": 580,
        "lat": -6.2833, "lng": 39.5833,
        "image_slug": "konokono-beach-resort",
        "short": "21 stone-and-thatch villas on Michamvi beach — eco-conscious design, all-suite, intimate.",
        "description": (
            "Konokono is a small adults-oriented eco-luxury resort on Michamvi beach in southeastern Zanzibar. Twenty-one "
            "villas in coral-stone and palm-thatch, with private plunge pools. Long private beach, snorkelling on the "
            "house reef."
        ),
        "amenities": "Private plunge pools,Eco-design,Beach,Snorkelling,All-inclusive",
        "is_featured": False,
    },
    {
        "name": "Zanzibar Serena Hotel",
        "destination_slug": "zanzibar-stone-town",
        "type": "hotel",
        "stars": 4,
        "price_min": 220, "price_max": 360,
        "lat": -6.1583, "lng": 39.1917,
        "image_slug": "zanzibar-serena-hotel",
        "short": "51-room heritage Stone Town hotel — restored 19th-century buildings on the seafront, pool.",
        "description": (
            "Serena's Stone Town hotel is housed in two restored 19th-century buildings on the seafront, opposite Forodhani "
            "Gardens. Fifty-one rooms, swimming pool, restaurant, and walking distance to all of Stone Town's main sights. "
            "Strong cultural value for travellers who want to actually be IN Stone Town."
        ),
        "amenities": "Pool,Restaurant,Seafront,WiFi,Heritage building",
        "is_featured": False,
    },
    {
        "name": "Dhow Palace Hotel",
        "destination_slug": "zanzibar-stone-town",
        "type": "boutique",
        "stars": 4,
        "price_min": 110, "price_max": 180,
        "lat": -6.1633, "lng": 39.1867,
        "image_slug": "dhow-palace-hotel",
        "short": "Atmospheric small hotel in a restored Stone Town mansion — antique Zanzibari decor, rooftop pool.",
        "description": (
            "Dhow Palace is a small heritage hotel in a 19th-century Indian merchant's mansion in the heart of Stone Town. "
            "Twenty-six rooms with carved Zanzibari beds and antique furniture, courtyard restaurant and a rooftop pool. "
            "Genuine Stone Town atmosphere at affordable pricing."
        ),
        "amenities": "Rooftop pool,Heritage building,Restaurant,WiFi,Antique decor",
        "is_featured": False,
    },
    {
        "name": "Jafferji House & Spa",
        "destination_slug": "zanzibar-stone-town",
        "type": "boutique",
        "stars": 4,
        "price_min": 140, "price_max": 220,
        "lat": -6.1633, "lng": 39.1917,
        "image_slug": "jafferji-house-and-spa",
        "short": "Small heritage boutique in Stone Town — themed suites celebrating the island's history, rooftop dining.",
        "description": (
            "Jafferji House is a tiny boutique guesthouse in Stone Town with each of its eight suites themed around a "
            "different chapter of Zanzibari history — Princess Salme, Livingstone, the Sultan's harem, etc. Rooftop "
            "restaurant and a spa make it a Stone Town favourite."
        ),
        "amenities": "Rooftop dining,Spa,Themed suites,Heritage,WiFi",
        "is_featured": False,
    },
    {
        "name": "Hotel The Zanzibari",
        "destination_slug": "zanzibar-stone-town",
        "type": "boutique",
        "stars": 4,
        "price_min": 180, "price_max": 280,
        "lat": -5.7167, "lng": 39.2833,
        "image_slug": "hotel-the-zanzibari",
        "short": "Boutique adults-only hotel in Nungwi — 28 suites, ocean-front pool, intimate setting.",
        "description": (
            "The Zanzibari is a small adults-only boutique on the northern tip of Zanzibar at Nungwi. Twenty-eight suites "
            "with private balconies, an ocean-front infinity pool, full spa and a calm, romantic atmosphere — popular with "
            "honeymooners."
        ),
        "amenities": "Adults only,Infinity pool,Spa,Ocean view,WiFi,Honeymoon",
        "is_featured": False,
    },
    {
        "name": "Ras Nungwi Beach Hotel",
        "destination_slug": "zanzibar-stone-town",
        "type": "resort",
        "stars": 4,
        "price_min": 220, "price_max": 360,
        "lat": -5.7167, "lng": 39.3000,
        "image_slug": "ras-nungwi-beach-hotel",
        "short": "Long-established Nungwi resort — 32 cottages, dive centre, traditional beach-resort feel.",
        "description": (
            "Ras Nungwi has been on the northern tip of Zanzibar for decades — 32 thatched cottages along a quiet stretch "
            "of beach, with a strong on-site PADI dive centre. Traditional resort feel, family-friendly, and one of the "
            "best beaches on the island."
        ),
        "amenities": "Beach,Dive centre,Pool,Restaurant,Family-friendly",
        "is_featured": False,
    },
    {
        "name": "Karafuu Hotel Beach Resort",
        "destination_slug": "zanzibar-stone-town",
        "type": "resort",
        "stars": 4,
        "price_min": 180, "price_max": 320,
        "lat": -6.0167, "lng": 39.5500,
        "image_slug": "karafuu-hotel-beach-resort",
        "short": "Long-established all-inclusive on Pingwe beach — 144 rooms, multiple pools, kids' club.",
        "description": (
            "Karafuu is one of Zanzibar's oldest all-inclusive resorts on the southeastern Pingwe beach. 144 rooms in "
            "garden-set cottages, three pools, kids' club, full all-inclusive food and beverage. Strong family value."
        ),
        "amenities": "All-inclusive,Three pools,Kids' club,Beach,Multiple restaurants",
        "is_featured": False,
    },
    {
        "name": "Riu Palace Zanzibar",
        "destination_slug": "zanzibar-stone-town",
        "type": "resort",
        "stars": 5,
        "price_min": 320, "price_max": 520,
        "lat": -5.7000, "lng": 39.3000,
        "image_slug": "hotel-riu-palace-zanzibar",
        "short": "Large all-inclusive resort on Nungwi beach — 388 rooms, six pools, mass-market appeal.",
        "description": (
            "Riu Palace Zanzibar is the island's largest all-inclusive resort with 388 rooms on the Nungwi beach. Six pools, "
            "five restaurants, multiple bars, full evening entertainment programme — a mainstream beach holiday experience "
            "at a competitive price."
        ),
        "amenities": "All-inclusive,Six pools,Five restaurants,Entertainment,Beach",
        "is_featured": False,
    },
    {
        "name": "Chumbe Island Coral Park",
        "destination_slug": "zanzibar-stone-town",
        "type": "boutique",
        "stars": 4,
        "price_min": 280, "price_max": 420,
        "lat": -6.2833, "lng": 39.1833,
        "image_slug": "chumbe-island",
        "short": "Seven eco-bungalows on a private 22ha marine reserve island — pioneering conservation tourism in Zanzibar.",
        "description": (
            "Chumbe Island is a tiny private 22-hectare marine reserve south of Zanzibar town, with just seven "
            "solar-powered eco-bungalows, no internet, and a no-shoes-required ethos. The surrounding reef is one of the "
            "best-preserved in East Africa. All-inclusive of meals, snorkel guides and marine education programmes."
        ),
        "amenities": "Eco-luxury,All-inclusive,Marine reserve,Snorkelling,Solar power,No WiFi",
        "is_featured": True,
    },
    {
        "name": "Smiles Beach Hotel",
        "destination_slug": "zanzibar-stone-town",
        "type": "hotel",
        "stars": 3,
        "price_min": 90, "price_max": 150,
        "lat": -5.7167, "lng": 39.2917,
        "image_slug": "smiles-beach-hotel",
        "short": "Budget-friendly small hotel in Nungwi — 22 rooms, pool, beach access, family-run.",
        "description": (
            "Smiles is a small family-run hotel in Nungwi village, a budget-friendly alternative to the big beach resorts. "
            "Twenty-two simple rooms, pool, easy beach access. Good value for backpackers and budget travellers."
        ),
        "amenities": "Pool,Beach,WiFi,Budget,Family-run",
        "is_featured": False,
    },

    # ============================== MAFIA ==============================
    {
        "name": "Pole Pole Bungalow Resort",
        "destination_slug": "mafia-island",
        "type": "boutique",
        "stars": 4,
        "price_min": 380, "price_max": 580,
        "lat": -7.9167, "lng": 39.7333,
        "image_slug": "butiama-beach-lodge",  # placeholder
        "short": "Seven thatched bungalows on Mafia's main island — whale shark season focal point, intimate eco-luxury.",
        "description": (
            "Pole Pole (Swahili for 'slowly slowly') is a tiny seven-bungalow resort on Mafia Island's western coast. "
            "Open-fronted thatched bungalows, all-inclusive dining, and a focus on whale-shark season (Oct-Mar) and "
            "Chole Bay diving."
        ),
        "amenities": "All-inclusive,Beach,Whale shark season,Diving,Eco-design",
        "is_featured": False,
    },
    {
        "name": "Butiama Beach Lodge",
        "destination_slug": "mafia-island",
        "type": "boutique",
        "stars": 3,
        "price_min": 180, "price_max": 280,
        "lat": -7.9333, "lng": 39.7500,
        "image_slug": "butiama-beach-lodge",
        "short": "12 simple beach bungalows on Mafia — budget-friendly base for whale sharks and diving.",
        "description": (
            "Butiama is a small simple beach lodge on Mafia Island, with twelve thatched bungalows directly on the beach. "
            "Half-board dining, dive operation, and good prices for travellers who don't need 5-star and just want access "
            "to Mafia's marine wildlife."
        ),
        "amenities": "Half-board,Beach,Diving,WiFi,Budget option",
        "is_featured": False,
    },

    # ============================== LAKE NATRON & WESTERN =============================
    {
        "name": "Africa Safari Lake Natron",
        "destination_slug": "serengeti-national-park",  # geographically closer to Serengeti via Lake Natron extension
        "type": "camp",
        "stars": 4,
        "price_min": 280, "price_max": 440,
        "lat": -2.4167, "lng": 36.0000,
        "image_slug": "africa-safari-lake-natron",
        "short": "Twenty tented bungalows by alkaline Lake Natron — climb Ol Doinyo Lengai, flamingo flocks at the shore.",
        "description": (
            "On the shore of the soda Lake Natron in the remote Rift Valley between the Serengeti and Mt Kilimanjaro, this "
            "camp offers access to Ol Doinyo Lengai (the only active soda-carbonatite volcano in the world), the Engare Sero "
            "footprints (1.2 million years old), and flamingo viewing at the lake. A truly remote stop."
        ),
        "amenities": "Pool,Lake views,WiFi,Volcano hikes,Cultural visits,Remote",
        "is_featured": False,
    },
    {
        "name": "Greystoke Mahale",
        "destination_slug": "mahale-mountains-national-park",
        "type": "camp",
        "stars": 5,
        "price_min": 1400, "price_max": 2200,
        "lat": -6.1167, "lng": 29.8500,
        "image_slug": "mahale-mountains-national-park-2",
        "short": "Six bandas on a remote Lake Tanganyika beach — chimp tracking by morning, kayaking by afternoon.",
        "description": (
            "Greystoke Mahale, operated by Nomad Tanzania, is one of Africa's most romantic and remote camps — six "
            "open-fronted wooden bandas on a white-sand Lake Tanganyika beach, with chimpanzee forest rising directly "
            "behind. Activities include chimp trekking (the M-group), kayaking, snorkelling and forest hiking."
        ),
        "amenities": "All-inclusive,Beach,Lake Tanganyika,Chimp trekking,Kayak,Boat",
        "is_featured": True,
    },
]
