import requests
import pandas as pd

SPARQL_URL = "https://query.wikidata.org/sparql"

QUERY = """
SELECT DISTINCT ?iata WHERE {
  ?airline wdt:P31 wd:Q46970 .
  ?airline rdfs:label "InterGlobe Aviation"@en .
  ?route wdt:P31 wd:Q3249551 ;
         wdt:P112 ?airline ;
         wdt:P1192 ?airport .
  ?airport wdt:P238 ?iata .
}
"""

HEADERS = {
    "Accept": "application/sparql+json",
    "User-Agent": "FlightScraper/1.0 (educational project)"
}

response = requests.post(
    SPARQL_URL,
    data={"query": QUERY},
    headers=HEADERS,
    timeout=30
)

# 🔍 DEBUG SAFETY
if response.status_code != 200:
    print("❌ HTTP ERROR:", response.status_code)
    print(response.text[:500])
    exit()

try:
    data = response.json()
except Exception:
    print("❌ Response is not JSON")
    print(response.text[:500])
    exit()

destinations = set()

for item in data["results"]["bindings"]:
    iata = item.get("iata", {}).get("value")
    if iata and len(iata) == 3:
        destinations.add(iata.upper())

df = pd.DataFrame(sorted(destinations), columns=["iata"])
df.to_csv("routes/indigo_destinations.csv", index=False)

print(f"✅ Extracted {len(df)} IndiGo destinations")
