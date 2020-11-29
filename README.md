# Website and Projects

This repo contains all the source code for my Flask based website, found at [leavittmapping.com](https://leavittmapping.com).

All the code for my personal projects, which use open source resources, are included within this repo. Long form descriptions of these projects can be found on my [projects page](https://leavittmapping.com/#goto-proj). My professional GIS projects are not included within this repo, however brief descriptions are available on my website.

I started these projects as a means to expand my client and server side coding knowledge and to get some experience in GIS web development techniques. Most of my coding skills are self taught through research and trial and error. I have tried my best to code cleanly and document clearly (for myself), but I am still very much a beginner at web and GIS development and code may not be efficient or bug free. Feel free to fork my project or open a pull request! If you have any questions or comments you can find visit the [contact page](https://leavittmapping.com/contact) on my website.

## Strava Activities Dashboard
I am currently actively working on this personal project to develop features and add functionality. This project can be found within this repo in its [folder](https://github.com/gavleavitt/Flask_Website_Project/tree/master/Flask_Application/application/projects/strava_activities). You can find a work-in-progress version of this map on my website [here](https://leavittmapping.com/stravamap), but note that it has not been thoroughly tested and is prone to drastic changes. I do not yet have a long form description written for this project.

#### Summary
This personal project displays my up-to-date Strava activity information on a interactive data dashboard using Leaflet to display geographical data and Chart.JS to display graphical information. Data can be filtered and explored by using buttons, date selections, searches, and by selecting geographical data.

Underlining Strava data were initially pulled from the Strava API and processed using Python, then a webhook subscription was created to update my server when new activities are available for processing. Strava activity data are processed in Python using PostGIS functions to remove private areas and to simplify geometries to reduce file sizes at the cost of spatial accuracy. Data are pre-calculated and served to the Leaflet map in the TopoJSON format to further reduce file sizes and server response times.

## Santa Barbara County Ocean Water Quality Map
The map can be found on my website [here](https://leavittmapping.com/maps/sbcoceanwaterquality) and a long form description can be found [here](https://leavittmapping.com/projects/sbcoceanquality). This project can be found within this repo in its [folder](https://github.com/gavleavitt/Flask_Website_Project/tree/master/Flask_Application/application/projects/water_quality).

#### Summary

This is a personal project which uses a Leaflet map to display ocean water test results provided by the Santa Barbara County Public Health Department’s Ocean Water Monitoring Program. The county tests beaches at least weekly and may issue warnings or close beaches if targeted bacterial counts exceed state standards. If a beach exceeds the standards, warnings will be posted or the beach will be closed then re-sampled at intervals until it is within acceptable standards and restrictions can be lifted.

Water quality reports are posted as PDFs to the Ocean Water Monitoring page. Test result data are not otherwise accessible on the internet. I saw this as an opportunity to expand my Python, database management, and web design skills. I designed a workflow and web map to display these data in an easily usable and mobile friendly format. Report PDFs are downloaded, test result details are extracted, and data are inserted into a Postgres database. These data are then served to a Leaflet map which displays the most recent test results.

## Live GPS Tracking Dashboard
This project can be found within this repo in its [folder](https://github.com/gavleavitt/Flask_Website_Project/tree/master/Flask_Application/application/projects/location_tracker). A long form description can be found on my website [here](https://leavittmapping.com/projects/livetrackingdashboard).

#### Summary
This dashboard displays real-time mobile phone location information collected by the open source mobile application GPSLogger for Android as well other mobile phone details. This project was developed as a personal project to expand my web development and database management skills.

The mobile application logs location and other phone details through HTTP POST requests to a personal Flask web server. Upon receiving these requests, the server's python scripts parse the incoming information and perform spatial queries against a Amazon Relation Database Service (RDS) PostgresSQL/PostGIS database to determine nearby features before inserting the data into the database.

These results are updated in near real-time on the dashboard as data are inserted into the database. This is accomplished using by JavaScript functions to poll a Flask API connected to the database for changes, when changes are detected details on the page are automatically updated without requiring a page refresh.

This workflow only works for Android, as the mobile application is Android only, and currently only tracks one user, myself.
