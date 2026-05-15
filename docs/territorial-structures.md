# Territorial Structures Reference

Research into the full territorial/administrative structures of countries with complex overseas or associated territories. Includes notes on Natural Earth shapefile coverage, which is the data source for this project.

---

## Natural Earth Coverage Summary

Before diving per-country, it helps to know how Natural Earth represents these entities:

- **Separate admin-0 polygon (110m):** Greenland (DK), Falkland Islands (GB, Disputed), Puerto Rico (US), New Caledonia (FR), French Southern & Antarctic Lands (FR), Taiwan (TWN — separate from CHN)
- **Admin-1 polygon under parent ISO (10m) but no admin-0:** French overseas departments (under FR), Caribbean Netherlands/BES islands (under NL), Svalbard and Bouvet Island (under NO), Chatham Islands and sub-Antarctic islands (under NZ), Ashmore & Cartier Islands and Jervis Bay (under AU), DC (under US), Hong Kong districts (under HKG)
- **Not in Natural Earth at any scale:** UK Crown Dependencies, most British Overseas Territories, French overseas collectivities, Netherlands constituent countries (Aruba/Curaçao/Sint Maarten), Faroe Islands, Cook Islands, Niue, Tokelau, most US territories, Macau (single junk record in admin-1)

---

## United Kingdom

### Constituent Countries (4)
*They collectively are the United Kingdom. Full EU (pre-Brexit), British citizens. No separate Natural Earth polygons.*

Not separate admin-0 entities in Natural Earth. In the 10m admin-1 shapefile, all subdivisions fall under `adm0_a3 = GBR`. The `region` field gives English statistical regions (North West, South East, etc.) and "Northern Ireland" — but not "England", "Scotland", or "Wales" as explicit values. Scotland and Wales must be inferred by dissolving their admin-1 subdivisions.

| Nation | Devolved body | Subdivision structure |
|--------|--------------|----------------------|
| England | Parliament (Westminster, with English Votes for English Laws) | Mix of Administrative Counties, Unitary Authorities, Metropolitan Boroughs, London Boroughs. 9 statistical regions exist but have no elected government. |
| Scotland | Scottish Parliament (Holyrood) | 32 Unitary Districts (council areas) since 1996 |
| Wales | Senedd (Welsh Parliament) | 22 Unitary Authorities |
| Northern Ireland | Northern Ireland Assembly (Stormont) | 11 councils since 2015 (shapefile still shows old 26 districts) |

### Crown Dependencies (3)
*Possessions of the Crown — not part of the UK, not represented in Parliament. Extensive self-governance (own parliaments, courts, taxation). British citizens. Not in Natural Earth at all.*

| Territory | Notes |
|-----------|-------|
| Bailiwick of Jersey | Largest Crown Dependency |
| Bailiwick of Guernsey | Contains three distinct sub-jurisdictions: Guernsey proper (including Herm, Jethou, Lihou), Alderney (own parliament), and Sark (including Brecqhou). Each has its own assembly. |
| Isle of Man | Tynwald is the world's oldest continuously operating parliament |

### British Overseas Territories (14)
*Under UK sovereignty but not part of the UK. Most inhabited BOTs grant full British citizenship (since British Overseas Territories Act 2002). Outside EU. Only the Falkland Islands has its own admin-0 polygon in Natural Earth (marked Disputed).*

| Territory | Inhabited | Notes |
|-----------|-----------|-------|
| Anguilla | Yes (~15k) | Elected premier |
| Bermuda | Yes (~63k) | Oldest BOT (1609); elected premier |
| British Antarctic Territory | No (research only) | Overlaps Argentine/Chilean claims; Antarctic Treaty limits |
| British Indian Ocean Territory (BIOT) | No permanent civilian pop | Diego Garcia military base; sovereignty transfer to Mauritius under 2025 treaty (currently suspended) |
| British Virgin Islands | Yes (~32k) | Elected premier |
| Cayman Islands | Yes (~79k) | No direct taxation; major financial centre |
| Falkland Islands | Yes (~3.4k) | **Separate admin-0 polygon** (Disputed); claimed by Argentina |
| Gibraltar | Yes (~34k) | Claimed by Spain; voted 98.5% to remain British in 2002 |
| Montserrat | Yes (~5k) | Southern half uninhabitable since Soufrière Hills eruption |
| Pitcairn Islands | Yes (~35) | Smallest inhabited BOT; descendants of Bounty mutineers |
| Saint Helena, Ascension & Tristan da Cunha | Yes (~5.6k combined) | Three island groups in one BOT |
| South Georgia & South Sandwich Islands | No permanent | Research only; claimed by Argentina |
| Turks and Caicos Islands | Yes (~38k) | |
| Akrotiri and Dhekelia | Yes (~7.7k Cypriot civilians) | Sovereign Base Areas on Cyprus — NOT standard BOTs. Use Euro. Cypriot civilian residents do not get full British citizenship (BOTC only, need visa for UK). |

---

## France

France has the most complex territorial structure of any country covered here, with five distinct legal categories.

### Metropolitan France
*Integral part of the French Republic. Full EU member, Schengen Area. French/EU citizens.*

13 regions (since 2016 reform), subdivided into 96 metropolitan departments. Shown in Natural Earth admin-1 under `FR`.

Corsica has special "Collectivité de Corse" status (unified territorial collectivity since 2018, merging the two former Corsican departments) — the shapefile still shows the old 2-department structure.

### Overseas Departments and Regions — DROM (5)
*Integral parts of the French Republic. Full EU outermost regions (Article 349 TFEU). Full French and EU citizenship. Shown in Natural Earth admin-1 under `FR`.*

| Territory | Location | Notes |
|-----------|----------|-------|
| Guadeloupe | Caribbean | Archipelago; Saint-Barthélemy and Saint-Martin split off in 2007 |
| Martinique | Caribbean | Single territorial collectivity (combined region+department) since 2015 |
| French Guiana (Guyane) | South America | Only French territory on mainland South America; borders Brazil |
| Réunion | Indian Ocean | Largest overseas department by population |
| Mayotte | Indian Ocean | Became department in 2011; EU outermost region since 2014; special immigration regime |

### Overseas Collectivities — COM (5)
*Part of the French Republic but with their own laws distinct from metropolitan France. Mostly EU Overseas Countries and Territories (OCT) — EU law does not automatically apply. Full French citizenship. Not in Natural Earth.*

| Territory | Location | Notes |
|-----------|----------|-------|
| Saint-Pierre-et-Miquelon | North Atlantic (near Newfoundland) | Only remnant of French North America; OCT not outermost region |
| Saint-Barthélemy | Caribbean | Split from Guadeloupe in 2007; left EU territory in 2012 (now OCT); duty-free luxury tourism |
| Saint-Martin (French part) | Caribbean | Split from Guadeloupe in 2007; shares island with Dutch Sint Maarten; still in EU territory |
| Wallis and Futuna | South Pacific | Three traditional kingdoms (Uvea, Sigave, Alo) with customary law alongside French governance |
| French Polynesia | South Pacific | Also designated "pays d'outre-mer" (overseas country) — highest autonomy of any COM; 121 islands |

### Sui Generis Collectivity — New Caledonia
*Constitutionally enshrined in its own chapter of the French Constitution. Part of France. EU OCT. French nationals plus own "New Caledonian citizenship" for local elections. **Has its own admin-0 polygon in Natural Earth.***

Three independence referendums: 2018 (56.7% stay), 2020 (53.4% stay), 2021 (96% stay, boycotted by independence movement). As of 2025–2026, negotiating enhanced autonomy as "État de Nouvelle-Calédonie."

### Overseas Territory — TAAF
*French Southern and Antarctic Lands. Part of France. Uninhabited research/conservation territory. **Has its own admin-0 polygon in Natural Earth.***

Components: Kerguelen Islands, Crozet Islands, Amsterdam and Saint-Paul Islands, Scattered Islands (around Madagascar), Adélie Land (Antarctic claim).

### State Private Property
| Territory | Notes |
|-----------|-------|
| Clipperton Island | Uninhabited atoll in the Pacific; administered directly by the French Ministry of Overseas; no EU status |

---

## Netherlands

The Kingdom of the Netherlands is a constitutional monarchy with four constituent countries — not a federation; the countries are equal partners. Each has its own parliament and government; the Netherlands handles joint affairs (defense, foreign policy, nationality law).

### Constituent Country: Netherlands (European)
*Full EU member, Schengen Area. Dutch/EU citizens.*

12 provinces: Drenthe, Flevoland, Friesland, Gelderland, Groningen, Limburg, Noord-Brabant, Noord-Holland, Overijssel, Utrecht, Zeeland, Zuid-Holland. Shown in Natural Earth admin-1 under `NL`, along with the BES islands.

### Constituent Countries — Caribbean (3)
*Equal constitutional partners in the Kingdom. EU Overseas Countries and Territories (OCT) — outside EU and Schengen. Residents are Kingdom of the Netherlands citizens and can move freely to the Netherlands and access EU as Dutch nationals. No separate admin-0 polygons in Natural Earth.*

| Territory | Notes |
|-----------|-------|
| Aruba | Left the Netherlands Antilles in 1986; own Aruban florin currency |
| Curaçao | Gained country status when Netherlands Antilles dissolved in 2010 |
| Sint Maarten (Dutch part) | Southern half of the island; shares with French Saint-Martin |

### Special Municipalities / Caribbean Netherlands — BES Islands (3)
*Legally part of the Netherlands constituent country, administered directly by the national government. EU OCT — EU law does not automatically apply. Dutch citizens. Shown in Natural Earth admin-1 under `NL`.*

These are technically not municipalities (*gemeenten*) — they are public bodies (*openbare lichamen*) with island councils.

| Territory | Notes |
|-----------|-------|
| Bonaire | Largest BES island; UNESCO-protected reef |
| Sint Eustatius | Central government took over direct control in 2018 due to governance failures |
| Saba | Smallest; no flat land; tiny population |

---

## Norway

### Counties (Fylker)
*Full part of Norway. Norwegian citizens. Full EU (EEA), Schengen.*

15 counties as of January 1, 2024, after the reversal of 2020 mergers. Natural Earth still shows the pre-2020 structure (19 counties). Oslo has unique dual status as both a county and a municipality.

### Svalbard
*Full part of the Kingdom of Norway since the 1925 Svalbard Act. Shown in Natural Earth admin-1 under `NO`.*

The 1920 Svalbard Treaty grants all 46 signatory nations equal rights to commercial activities on the islands. Norway cannot militarise beyond defensive purposes. Not part of Schengen, the Nordic Passport Union, or the EEA — so visa rules differ from mainland Norway despite being Norwegian territory. Administered by the Governor of Svalbard; Longyearbyen has a community council with municipality-like powers.

### Jan Mayen
*Full part of the Kingdom of Norway. No permanent population (18–35 non-permanent military/meteorological personnel). Administered by the County Governor of Nordland since 1995. Shown in Natural Earth admin-1 under `NO`.*

### Dependencies — Biland (3)
*NOT part of the Kingdom of Norway. Under Norwegian sovereignty but can be ceded without a constitutional amendment. All uninhabited.*

| Territory | Location | Notes |
|-----------|----------|-------|
| Bouvet Island | South Atlantic | World's most remote island; research station only; ISO code BV. Shown in Natural Earth admin-1 under `NO`. |
| Peter I Island | Antarctic | Norwegian sovereignty claimed; limited by Antarctic Treaty |
| Queen Maud Land | Antarctica | Norway's Antarctic territorial claim; between 20°W and 45°E; Antarctic Treaty applies |

---

## Australia

### States (6)
*Constitutional status, partial sovereignty. Australian citizens. Full EU equivalent (N/A — Australia is independent).*

New South Wales, Victoria, Queensland, Western Australia, South Australia, Tasmania. All shown in Natural Earth admin-1 under `AU`.

### Internal Self-Governing Territories (2)
*Part of Australia but with less constitutional entrenchment than states — the federal Parliament can override their legislatures. Australian citizens. Shown in Natural Earth admin-1 under `AU`.*

| Territory | Notes |
|-----------|-------|
| Australian Capital Territory (ACT) | Contains Canberra; own legislature since 1989; Senate representation |
| Northern Territory (NT) | Own legislature since 1978; failed statehood referendum in 1998 |

### Jervis Bay Territory
*Part of Australia. No elected council — administered by a federal department; ACT laws apply. Exists to give landlocked Canberra port access. Shown in Natural Earth admin-1 under `AU`.*

### External Territories — Inhabited (3)
*Constitutionally part of Australia. Australian citizens.*

| Territory | Population | Governance | Natural Earth | Notes |
|-----------|-----------|------------|---------------|-------|
| Christmas Island | ~1,938 | Shire of Christmas Island; ACT laws apply; federal administration | Not shown separately | Former British colony; ceded to Australia 1958 |
| Cocos (Keeling) Islands | ~547 | Shire of Cocos (Keeling) Islands; voted for integration with Australia 1984 | Not shown separately | Two atolls; WA laws apply |
| Norfolk Island | ~2,601 | Norfolk Island Regional Council (advisory only since 2015) | Not shown separately | Self-governing 1979–2015; autonomy abolished controversially; some residents assert non-Australian identity; appeal to UN pending |

### External Territories — Uninhabited/Research (5)
*Part of Australia. No permanent populations.*

Coral Sea Islands Territory, Ashmore and Cartier Islands (shown in Natural Earth admin-1 under `AU`), Heard Island and McDonald Islands, Australian Antarctic Territory.

---

## United States

### States (50) + Federal District
*Full constitutional status. US citizens voting in all elections.*

All 50 states and DC shown in Natural Earth admin-1 under `US`. The District of Columbia is a Federal District — residents vote in presidential elections (since the 23rd Amendment, 1961) but have no Senate representation and only a non-voting House delegate.

### Inhabited Organized Unincorporated Territories (4)
*Under US sovereignty. US citizens by birth (by statute). Constitution applies only partially — the "Insular Cases" doctrine (1901–1905) holds that only "fundamental rights" apply; other constitutional provisions do not. Non-voting House delegates; cannot vote in the presidential general election.*

Puerto Rico has its own admin-0 polygon in Natural Earth. The others do not.

| Territory | ISO | Population | Notes |
|-----------|-----|-----------|-------|
| Puerto Rico | PR | ~3.3M | Commonwealth; Spanish-speaking; active statehood and independence movements |
| Guam | GU | ~153k | Major US military hub in the Pacific |
| US Virgin Islands | VI | ~87k | Purchased from Denmark in 1917 |
| Northern Mariana Islands (CNMI) | MP | ~47k | Commonwealth; former UN trusteeship ended 1986 |

### Inhabited Unorganized Unincorporated Territory (1)
*The only US territory in this unique category. Residents are US nationals but NOT citizens by birth — must naturalize for full citizenship. Own immigration system.*

| Territory | ISO | Population | Notes |
|-----------|-----|-----------|-------|
| American Samoa | AS | ~49k | Significant Samoan cultural preservation; own immigration controls |

### Incorporated Unorganized Territory (1)
*The only remaining incorporated territory — the full US Constitution applies (unlike all other territories). Full US citizens.*

| Territory | Notes |
|-----------|-------|
| Palmyra Atoll | Became the only incorporated territory after Hawaii gained statehood in 1959; ~4–20 research personnel; managed by the Nature Conservancy |

### Uninhabited Minor Outlying Islands (8)
Baker Island, Howland Island, Jarvis Island, Johnston Atoll, Kingman Reef, Midway Atoll (~40 personnel), Navassa Island (disputed by Haiti), Wake Island (~100 military/civilian; claimed by Marshall Islands).

---

## New Zealand

### Regions (16)
*Part of New Zealand. New Zealand citizens. Full self-governance.*

11 Regional Councils and 5 Unitary Authorities. Natural Earth admin-1 shows all 16 under `NZ`, along with uninhabited sub-Antarctic island groups (Kermadec, Three Kings, Antipodes, Auckland Islands, Campbell Islands, Snares) and the Chatham Islands Territory.

**Chatham Islands Territory** — part of New Zealand proper but administered by its own Island Territory authority. Shown in Natural Earth admin-1 as "Special Island Authority."

### Realm of New Zealand — Free Association States (2)
*Not part of New Zealand. Self-governing states associated with New Zealand. Full internal self-governance; New Zealand handles defense/foreign affairs only with their consent — they can and do conduct independent foreign policy. Residents are New Zealand citizens by statute.*

Cook Islands and Niue are not UN members but participate in UN specialized agencies. The US (2023) and Germany (2026) have recently recognised both as sovereign states. 90%+ of residents from each territory live in New Zealand.

| Territory | ISO | Population | Notes |
|-----------|-----|-----------|-------|
| Cook Islands | CK | ~15k | Maintains foreign relations with 52+ countries independently |
| Niue | NU | ~1.7k | Smallest self-governing territory in the world |

### Realm of New Zealand — Dependent Territory (1)
*Not part of New Zealand. Tokelauans hold New Zealand citizenship. New Zealand Administrator can override local parliament. UN lists as a non-self-governing territory. Failed independence referendums in 2006 and 2007 (fell short of required two-thirds).*

| Territory | Population | Notes |
|-----------|-----------|-------|
| Tokelau | ~1,500 | Three atolls; no land above 5m elevation; extreme climate change vulnerability |

### Antarctic Dependency
Ross Dependency — New Zealand's Antarctic territorial claim. Uninhabited except research stations. Recognized by only some countries.

---

## Denmark

The Danish Realm (*Rigsfællesskabet*) is constitutionally a unitary sovereign state — not a federation — though its three parts have very different governance arrangements.

### Denmark Proper
*Full EU member, Schengen Area. Danish/EU citizens.*

5 regions since 2007 reform: Hovedstaden, Midtjylland, Nordjylland, Sjælland, Syddanmark. Shown in Natural Earth admin-1 under `DK`.

### Faroe Islands
*Constituent part of the Danish Realm. Danish nationals. 2 seats in the Danish Folketing. Not in Natural Earth admin-1 under `DK`; no separate admin-0 polygon.*

Never joined the EU — voted against membership in 1973. Not in Schengen, but in the Nordic Passport Union (free movement from Nordic countries). Home rule since 1948; recognised as an "equal partner" in self-government since 2005. The Løgting (parliament) controls nearly all domestic affairs; Denmark retains defense, foreign affairs, and monetary policy (Danish krone).

### Greenland
*Constituent part of the Danish Realm. Danish nationals; Greenlanders recognised as a distinct "people" with self-determination rights under the 2009 Self-Rule Act. 2 seats in the Danish Folketing. **Has its own admin-0 polygon in Natural Earth.***

Was in the EU when Denmark joined in 1973; voted to leave in 1982 after gaining home rule — the only territory ever to leave the EU. Now an EU OCT. Not in Schengen. Self-Rule (Selvstyre) since 2009: Inatsisartut (parliament) controls judicial affairs, police, natural resources, and immigration. Denmark retains defense and foreign affairs. The 2009 Act explicitly acknowledges the right to full independence.

---

## Finland

### Regions (18)
*Full part of Finland. Finnish/EU citizens. Full EU member, Schengen Area.*

18 mainland regions shown in Natural Earth admin-1 under `FI`. Regional councils are indirect democracies composed of municipal delegates. Since 2022, wellbeing services counties (hyvinvointialueet) have taken over health and social care, following the same regional borders.

### Åland Islands
*Constitutionally part of Finland. Finnish citizens. EU member (joined separately with special protocol in 1995). **Not shown in Natural Earth admin-1 under `FI`; maps under its own ISO code `AX`.***

Åland's special status is among the most layered of any autonomous territory:

- **Demilitarised** since the 1856 Treaty of Paris (after the Crimean War). The only Finns exempt from military conscription.
- **Language:** Swedish is the *only* official language. Finnish has no official status in Åland — constitutionally protected.
- **EU VAT:** Outside the EU VAT area, enabling duty-free sales on ferries between mainland Finland/Sweden and Åland.
- **Domicile right (hembygdsrätt):** Finnish citizens in Åland must separately acquire "domicile right" (regional citizenship) to vote in local elections and own rural property — distinct from Finnish citizenship.
- **Self-governance:** Own parliament (Lagting), own government (Lantråd), own police, own postal system, own flag. The 1991 Act on the Autonomy of Åland is constitutional in nature.

---

## China

China has 34 province-level divisions across four distinct types, plus disputed territories and a complex cross-strait situation with Taiwan.

### Provinces (22)
*Standard first-level divisions. Full PRC citizens. No special autonomy provisions.*

Anhui, Fujian, Gansu, Guangdong, Guizhou, Hainan, Hebei, Heilongjiang, Henan, Hubei, Hunan, Jiangsu, Jiangxi, Jilin, Liaoning, Qinghai, Shaanxi, Shandong, Shanxi, Sichuan, Yunnan, Zhejiang.

All shown in Natural Earth admin-1 under `CHN`, grouped into macro-regions via the `region` field (see below).

### Direct-Controlled Municipalities (4)
*Major urban centres administered directly by the central government. Politically higher status than provinces. Full PRC citizens.*

Beijing, Tianjin, Shanghai, Chongqing. Shown in Natural Earth admin-1 under `CHN`.

### Autonomous Regions (5)
*Established for ethnic minority populations. Equivalent legal status to provinces but with theoretically enhanced self-governance rights — autonomous regions can formulate their own self-government and separate regulations, and their chairman must be from the designated ethnic minority. In practice, the Communist Party's First Secretary position has never been held by an ethnic member of the designated minority in any autonomous region.*

| Region | Minority | Notes |
|--------|----------|-------|
| Tibet Autonomous Region (Xizang) | Tibetan | 7 prefecture-level divisions; heavily restricted autonomy in practice |
| Xinjiang Uyghur AR | Uyghur | 13 prefecture-level divisions including 5 autonomous prefectures; subject of major international human rights scrutiny |
| Inner Mongolia AR | Mongolian | 13 prefecture-level divisions; shares long border with Mongolia |
| Guangxi Zhuang AR | Zhuang | 14 prefecture-level divisions; 110 county-level divisions |
| Ningxia Hui AR | Hui | Smallest AR; 5 prefecture-level cities |

All shown in Natural Earth admin-1 under `CHN`.

### Special Administrative Regions — SARs (2)
*Governed under "One Country, Two Systems." Part of China but with separate legal systems, currencies, borders, and governance. SAR residents hold separate HKSAR/Macau SAR travel documents in addition to Chinese nationality.*

#### Hong Kong (HKG)
*Constitutional basis: Basic Law implementing the 1984 Sino-British Joint Declaration. One Country Two Systems expires July 1, 2047 (50 years from handover). **Has its own admin-1 polygons in Natural Earth under `HKG`; no separate admin-0 polygon at 110m.***

Key autonomy retained:
- Separate currency (HKD, pegged to USD); no mainland exchange controls
- Independent common law courts with final appeal authority
- Separate immigration controls — mainland Chinese require entry permits; HK residents need separate documents for mainland
- Own passport (HKSAR passport, 174 visa-free destinations)
- Separate customs territory

**18 districts** across 3 areas: Hong Kong Island (4 districts), Kowloon (5 districts), New Territories (9 districts). Shown in Natural Earth admin-1 under `HKG`, grouped into these 3 areas via the `region` field — making HKG one of the newly promoted two-level countries under the updated detection logic.

#### Macau (MAC)
*Constitutional basis: Macau Basic Law. Returned from Portuguese sovereignty in 1999. One Country Two Systems expires December 20, 2049. **Not meaningfully represented in Natural Earth — appears only as a single junk record (`MAC+00?`) in admin-1.***

Key autonomy retained:
- Separate currency (Macanese Pataca, MOP)
- Hybrid legal system (Portuguese civil law tradition + Chinese elements)
- Independent courts with final appeal authority
- Own financial and monetary policy

**7 civil parishes (freguesias)** — historical Portuguese administrative divisions retained for cultural and statistical purposes. Municipality government was formally abolished in 2001; parish services now handled by the Municipal Affairs Bureau.

### Macro-Regions (Natural Earth `region` field groupings)
China's provinces are grouped in the Natural Earth admin-1 `region` field into 6 macro-regions. These correspond to the National Bureau of Statistics' official geographic classifications:

| Region | Provinces/Municipalities |
|--------|--------------------------|
| North China | Beijing, Tianjin, Hebei, Shanxi, Inner Mongolia |
| Northeast China | Liaoning, Jilin, Heilongjiang |
| East China | Shanghai, Jiangsu, Zhejiang, Anhui, Fujian, Jiangxi, Shandong |
| South Central China | Henan, Hubei, Hunan, Guangdong, Guangxi, Hainan |
| Southwest China | Chongqing, Sichuan, Guizhou, Yunnan, Tibet |
| Northwest China | Shaanxi, Gansu, Qinghai, Ningxia, Xinjiang |

These groupings are used by China's NBS for census and economic statistics. They are the basis for the level-1 / level-2 two-level structure of China in this app (CHN is one of the previously detected two-level countries).

### Taiwan
*Natural Earth treats Taiwan as a fully separate admin-0 entity with its own polygon (`TWN`). The PRC claims Taiwan as a province; Taiwan is administered by the Republic of China (ROC) government with full de facto independence.*

The PRC's official position is that Taiwan is a province under the One-China policy. The ROC maintains itself as a sovereign state with formal diplomatic relations with 12 UN member states and unofficial relations with most others. ~74% of UN member states endorse the PRC position.

**Taiwan's 22 subnational divisions** (provinces were formally abolished in 2018):
- 6 special municipalities: Taipei, New Taipei, Taoyuan, Taichung, Tainan, Kaohsiung
- 3 cities: Keelung, Hsinchu, Chiayi
- 13 counties: Hsinchu, Miaoli, Changhua, Nantou, Yunlin, Chiayi, Pingtung, Yilan, Hualien, Taitung, Penghu, Kinmen, Lienchiang

Shown in Natural Earth admin-1 under `TWN`, grouped into 3 regions via the `region` field (Fujian Province, Special Municipalities, Taiwan Province) — making TWN one of the newly promoted two-level countries.

### Disputed Territories — South China Sea
China administers several contested island groups through **Sansha City** (established 2012), a prefecture-level city under Hainan Province claiming ~2 million km² of sea but only ~20 km² of actual land.

| District | Islands administered | Other claimants |
|----------|---------------------|-----------------|
| Xisha District | Paracel Islands (occupied by China since 1974), Macclesfield Bank | Vietnam, Taiwan |
| Nansha District | Spratly Islands (China controls 7 outposts; Vietnam controls the most islands/reefs overall) | Vietnam, Philippines, Malaysia, Brunei, Taiwan |

China built ~5 sq miles of artificial islands in the Spratlys between 2013–2015, constructing ports, airstrips, and military installations. Not represented in Natural Earth.

---

## Countries to Consider Adding

The following countries have territorial structures complex enough to be relevant to this project but are not yet documented here:

### Spain
Full EU member. All territories are integral parts of Spain with full Spanish/EU citizenship.
- **17 autonomous communities** on mainland + Balearic Islands
- **Canary Islands** — autonomous community located off the coast of West Africa; EU outermost region
- **Ceuta and Melilla** — two autonomous cities on the African mainland, geographically within Morocco; full Spanish territory; EU outermost regions; significant immigration flashpoint
- **Plazas de soberanía** — small uninhabited rocky islets and promontories off the Moroccan coast

### Portugal
Full EU member. All territories are integral parts of Portugal with full Portuguese/EU citizenship.
- **18 mainland districts** (being replaced by intermunicipal communities)
- **Azores** — autonomous region in the mid-Atlantic; EU outermost region; own regional government and assembly
- **Madeira** — autonomous region off the African coast; EU outermost region; own regional government and assembly

---

## Key Patterns for Schema Design

1. **"Part of the sovereign state" is a spectrum, not binary.** At minimum, you need: integral constituent part → dependent territory → associated state in free association → dependency that is not part of the state at all (e.g. Norwegian Biland).

2. **Citizenship is independent of territory status.** Cook/Niue residents are NZ citizens but those territories are not part of NZ. American Samoans are US nationals but not citizens. Åland residents are Finnish citizens but need a separate domicile right. These distinctions are probably too granular for this app.

3. **Natural Earth admin-1 uses the parent country's ISO code** for territories — French overseas departments appear under `FR` (not `GP`/`MQ`/`GF`/`RE`/`YT`), Caribbean Netherlands under `NL` (not `BQ`). Worth tracking both the NE code the shapefile uses and the territory's own ISO 3166-1 code.

4. **Some entities exist in admin-1 but not admin-0** (Svalbard, French DROMs, BES islands), some in neither (Crown Dependencies, French COMs, Faroe Islands), and a few in both (Greenland, New Caledonia, Falklands, Puerto Rico).

5. **The "realm" concept** (Realm of New Zealand, Danish Realm, Kingdom of the Netherlands) means the sovereign entity is larger than a single ISO country, but Natural Earth uses the metropolitan country's ISO code as the primary unit.

6. **Three-level dependency structures exist** — the Bailiwick of Guernsey contains Alderney and Sark as distinct sub-jurisdictions within the dependency. Worth noting if the schema ever needs to represent dependency-within-dependency.
