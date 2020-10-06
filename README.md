# Live GPS Tracking Dashboard and other web pages.

**The URL to this application is not posted due to outstanding issues, it will be posted once I resolve these issues and register a domain.**

This project uses Flask to serve a variety of web pages, including a live GPS Tracking Dashboard, water quality Leaflet map, and will be built out to contain other web pages.

Currently this Flask application is hosted on an AWS Elastic Beanstalk Free-Tier instance and can be publically accessed, but sensitive data/webpages are secured using HTTP Authenication. The instance does not yet have a registered domain name and uses the generic address provided by AWS.

Web pages are dynamic and pull their data from a Postgres/PostGIS AWS RDS backend that is interacted with using Python and SQLAlchemy ORM.

## GPS Tracking Dashboard - Backend
This web page displays the GPS location, battery life, and coordinates of my phone in near realtime when I'm recording my location. 

The dashboard also displays activity information, nearest road and distance to road, and nearest trail if doing an off-road activity.   

### GPS Logging and processing

The open source mobile app **[GPS Logger for Android](https://gpslogger.app/)** is used to log location and other phone data, note that this app is Android only. 
When logging begins the appropriate profile name is selected, which is used to control query and display logic.  
Logging is set to use cell tower information or GPS if available, usually only when a GPS-dependant app like Strava is already collecting data, however the mobile app can also be set to obtain only GPS data at the cost of battery life.   

Data and authentication credentials (basic auth, admin) are sent via the Custom URL setting to the Flask API URL in a HTTP POST message with the following settings:

HTTP Headers:
Content-Type: application/json

HTTP Body:
{
   "Longitude":"%LON",
   "Latitude":"%LAT",
   "Satellites":"%SAT",
   "Altitude":"%ALT",
   "Speed":"%SPD",
   "Accuracy":"%ACC",
   "Direction":"%DIR",
   "Provider":"%PROV",
   "Timestamp":"%TIMESTAMP",
   "Time_UTC":"%TIME",
   "Date":"%DATE",
   "Start_timestamp":"%STARTTIMESTAMP",
   "Battery":"%BATT",
   "Android_ID":"%AID",
   "Serial":"%SER",
   "Profile":"%PROFILE",
   "hdop":"%HDOP",
   "vdop":"%VDOP",
   "pdop":"%PDOP",
   "Dist_Travelled":"%DIST",
   "Activity":"%ACT"
}

### Handling Data with Flask
First the script checks if movement has occurred between the incoming point and the most recent previous point.

If movement has occurred, based on two different thresholds for GPS or cell tower location, a track is created between the two points.

Next the incoming point is intersected against the area of interest PostGIS table and the nearest road and distance to it are queried. 

If the activity type is a outdoor activity (based on logging profile name), such as MTB, running, hiking, etc, then the nearest trail/path and distance are queried.

Finally these point and line data are committed to the Postgres database.

## GPS Tracking Dashboard - Frontend

Located at /liveviewer and requires viewer authenication to view. 

The GPS Tracking Dashboard is dynamic and automatically updates to display data in near realtime.

Flask renders the HTML template, the Javascript Leaflet library is used to display a map and the GPS point location, and CSS Grid is used to layout the page.

In order to ensure realtime data access and updates, two APIs were built in Flask to provide geojson data, one to provide the most recent location and phone data and another to provide GPS tracks for that day. Both these APIs require viewer level authentication to load properly.

The Leaflet Javascript plugin **[Leaflet Realtime](https://github.com/perliedman/leaflet-realtime)** polls the GPS location and GPS track APIs at a set interval for changes.

When a change is detected the location marker is moved to the new location and new tracks are loaded and displayed. An event listener detects when an "update" event occurs on the GPS location realtime function and Javascript is used to update dashboard text and icons with the new information. These details are defaulted to "loading" and loading icons until the initial run of Leaflet Realtime can occur and overwrite the default state. If no or invalid credientials are given then these will display their default loading state indefinitely. The map bounds will also automatically pan to the new location. 

# Santa Barbara Water Quality Reports

The Santa Barbara County Health Department posts Ocean Water Test results to their Ocean Water Monitoring Program webpage:
https://www.countyofsb.org/phd/oceanwatermonitoring

The results are posted as a PDF to the link:
https://www.countyofsb.org/uploadedFiles/phd/PROGRAMS/EHS/Ocean%20Water%20Weekly%20Results.pdf

This PDF has a static name and download link with dynamic content that is updated at least weekly.

My script located in this [repo](https://github.com/gavleavitt/Water_Quality_PDF_Parsing) processes the PDF and sends the data to the Postgres AWS RDS. This script currently runs on a schedule on my local machine.

## Santa Barbara Water Quality Leaflet - Frontend
Located at /SBCOceanWaterQuality

Displays a Leaflet map with the Santa Barbara County beaches mapped out. The beach icons reflect the most recently reported status of the beach and popups contain  test report data. 
On page load Flask queries the postgres AWS RDS (populated by the previously mentioned script) to find the most recent water quality report for each beach and passes this information as a geojson feature collection to the HTML document. 

#TODO:

Register a domain to make a friendly domain name to share website publically and to enable HTTPS. 

Integrate PDF parsing script into this Flask application using the APScheduler library. 

Build a GIS/mapping portfolio page to display and describe projects, also include an About section

Build a script to use the Strava API to download new activities, including spatial data, and add to database 

Build a Leafet and data dashboard page to allow a user to dynamically filter stored Strava and/or GPS Logger data.


 
