import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="AI Virtual Tour Guide", page_icon="🌍")

st.title("🌍 AI Virtual Tour Guide")
st.write("Search route, traffic, stays & rentals (100% FREE)")

# ---------- IMAGE FETCH (WIKIMEDIA – FREE) ----------
def get_place_image(name):
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": name,
        "gsrlimit": 1,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    try:
        r = requests.get(url, params=params).json()
        pages = r.get("query", {}).get("pages", {})
        for p in pages.values():
            return p["imageinfo"][0]["url"]
    except:
        pass
    return "https://via.placeholder.com/400x250?text=No+Image"

# ---------- PLACE SEARCH (OPENSTREETMAP – FREE) ----------
def search_places(query):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "extratags": 1,
        "limit": 5
    }
    headers = {"User-Agent": "AI-Virtual-Tour-Guide"}
    return requests.get(url, params=params, headers=headers).json()

# ---------- USER INPUT ----------
start_place = st.text_input("🚩 Start Location (eg: Salem)")
destination_place = st.text_input("🎯 Destination (eg: Ooty)")

if st.button("Search & Show Everything"):
    if not start_place or not destination_place:
        st.warning("Please enter both locations")
    else:
        # ---------- GOOGLE MAPS FREE ROUTE ----------
        s = urllib.parse.quote(start_place)
        d = urllib.parse.quote(destination_place)

        maps_url = (
            f"https://www.google.com/maps/dir/?api=1"
            f"&origin={s}&destination={d}&travelmode=driving"
        )

        st.subheader("🗺️ Route with Live Traffic")
        st.markdown(f"[👉 Open Google Maps Route]({maps_url})")
        st.info("Shows live traffic, travel time & alternate routes (FREE)")

        # ---------- HOTELS ----------
        st.subheader("🏨 Room Stays / Hotels")
        hotels = search_places(f"hotels in {destination_place}")

        for h in hotels:
            image = get_place_image(h["display_name"])
            phone = h.get("extratags", {}).get("phone", "Not available")
            website = h.get("extratags", {}).get("website", "Not available")
            map_link = f"https://www.openstreetmap.org/{h['osm_type']}/{h['osm_id']}"

            st.image(image, use_column_width=True)
            st.markdown(f"### 🏨 {h['display_name'].split(',')[0]}")
            st.write("📝 Comfortable stay with basic amenities.")
            st.write(f"📞 Contact: {phone}")
            if website != "Not available":
                st.markdown(f"🌐 Website: {website}")
            st.markdown(f"📍 [View Location]({map_link})")
            st.divider()

        # ---------- CAR RENTALS ----------
        st.subheader("🚗 Car Rentals")
        cars = search_places(f"car rental in {destination_place}")

        for c in cars:
            image = get_place_image(c["display_name"])
            phone = c.get("extratags", {}).get("phone", "Not available")
            website = c.get("extratags", {}).get("website", "Not available")
            map_link = f"https://www.openstreetmap.org/{c['osm_type']}/{c['osm_id']}"

            st.image(image, use_column_width=True)
            st.markdown(f"### 🚗 {c['display_name'].split(',')[0]}")
            st.write("📝 Reliable car rental service.")
            st.write(f"📞 Contact: {phone}")
            if website != "Not available":
                st.markdown(f"🌐 Website: {website}")
            st.markdown(f"📍 [View Location]({map_link})")
            st.divider()

        # ---------- BIKE RENTALS ----------
        st.subheader("🏍️ Bike Rentals")
        bikes = search_places(f"bike rental in {destination_place}")

        for b in bikes:
            image = get_place_image(b["display_name"])
            phone = b.get("extratags", {}).get("phone", "Not available")
            website = b.get("extratags", {}).get("website", "Not available")
            map_link = f"https://www.openstreetmap.org/{b['osm_type']}/{b['osm_id']}"

            st.image(image, use_column_width=True)
            st.markdown(f"### 🏍️ {b['display_name'].split(',')[0]}")
            st.write("📝 Affordable bikes for city & tourist travel.")
            st.write(f"📞 Contact: {phone}")
            if website != "Not available":
                st.markdown(f"🌐 Website: {website}")
            st.markdown(f"📍 [View Location]({map_link})")
            st.divider()

        # ---------- AI ASSISTANT ----------
        st.success(
            f"🤖 I found route, traffic, stays and rentals for {destination_place}. "
            "Use map links to contact and navigate easily."
      )
