````markdown
# Find The Place (Geolocation OSINT)

### Step1 (Understanding the challenge):
> ##### We are given a photo taken at a well-known public location. Our goal is to determine the **exact latitude and longitude** of where the photo was taken. The flag format is `CSCC{latitude_longitude}`.

### Step2 (Analyzing the image):
> ###### We start by examining the image for visual clues:
> - **Landmarks** — buildings, monuments, signs, or distinctive structures
> - **Text** — any visible text, street signs, or store names
> - **Vegetation & terrain** — climate indicators that narrow down the region
> - **Architecture style** — helps identify the country or region
>
> ###### We also check the image metadata using `exiftool` for any GPS data that might be embedded:
> ```bash
> exiftool "Find The Place.jpeg"
> ```

### Step3 (Geolocating the photo):
> ###### Using the visual clues identified in the image, we perform a reverse image search or use **Google Maps / Google Earth** to pinpoint the location. Matching the landmarks and surroundings narrows it down to the exact coordinates.
> ###### The location is found at coordinates **36.67, 4.52**.

**Flag:**
```
CSCC{36.67_4.52}
```
````
