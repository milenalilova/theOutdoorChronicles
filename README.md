# The Outdoor Chronicles

## Description
The Outdoor Chronicles is a comprehensive guide for nature enthusiasts, focusing on connecting people with wildlife in their natural habitats. The platform offers a detailed database of hiking trails and animal profiles, highlighting which animals are commonly found on specific trails and where particular trails lead to unique wildlife encounters.

Designed for those who love exploring nature, the site helps users plan their outdoor adventures by providing essential information about the animals they can expect to encounter. The platform also caters to wildlife photographers by pointing them toward ideal locations for capturing animals in their natural surroundings.

In addition to browsing the curated content, users can log their own trail experiences, record animal sightings, and upload photos, creating a personalized journey log. The Outdoor Chronicles is the ultimate companion for anyone eager to discover and learn more about the fascinating connection between wildlife and trails.

## Project set up
- **Clone the repo**
  ` https://github.com/milenalilova/theOutdoorChronicles.git `
- **Install dependencies**
  ` pip install -r requirements.txt `
- **Settings** - for environment variables please use the Google Docs file provided with the survey
- **Read comments** in the caller.py file, at manage.py level

- **Run** caller.py file to create database records, or create your own. Running this file is not essential for strting the project. It is a help tool to provide initial data.

## Features
- **Explore Trails**: Explore detailed profiles of hiking trails and the wildlife associated with them, together with recorded user experiences, statistics, and photographs.
  
- **Animal Search**: Find out detailed descriptions of animals and which trails are their home.
  
- **User Logs**: Record personal experiences, animal sightings, and upload photos to create a digital diary.
  
- **Interactive Database**: Contribute to the growing repository of trails and wildlife information.
  
- **Photography Support**: Discover trails ideal for wildlife photography enthusiasts.
  
- **Map**: Integrated world map.

## User Flow:
- **Homepage**: Users land on the homepage, where they can see an overview of the available trails and wildlife content. Unregistered users can only see limited details with an invitation to register or login, Register/Login page and About page. Registered users see random trails and wildlife content based on their location, if such is provided.
  
- **Create an Account/Log In**: Users need to create an account or log in to see and contribute content, record sightings, and upload photos.
  
- **Create Trails and Animals Profiles**: This can only be done by a staffuser with permissions, or a superuser.
  
- **Explore Trails**: Registered users can search for trails based on name or location. A detailed description of the trail is provided, together with an option to log their own experience, upload photos, and see all other users' content related to the trail.
  
- **Explore Animals**: Similar to trails, registered users can search for species with detailed information about their habitat, an option to find a trail and record their own experience, upload photos, and see other users' content related to that specific animal.
  
- **Search Functionality**: Users can search for specific animals or trails using filters or a search bar. This helps them find the best trails for spotting particular animals or vice versa.
  
- **Log Experiences**: Once logged in, users can start logging their personal experiences by adding entries about the trails they've hiked, the animals they've spotted, and any photos they've taken. This option is available on a trail details page.
  
- **View Personal Log**: Users can view and edit their own logs, keeping track of their journeys and animal sightings, adding photos. Logs are also grouped by specific trail or specific animal, thus helping keep track of personal statistics and achievements.

## Technologies Used:
- Python
- Django Framework
- PostgreSQL
- Django Template Language
- CSS
- HTML
- Pillow
- CSS
- HTML
- Pillow
- JavaScript
- Leaflet

