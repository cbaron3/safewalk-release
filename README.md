<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->





<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/cbaron3/safewalk-release">
    <img src="images/bulb-icon.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">SafeWalk London</h3>

  <p align="center">
    An awesome README template to jumpstart your projects!
    <br />
    <a href="https://github.com/cbaron3/safewalk-release"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/cbaron3/safewalk-release">View Demo</a>
    ·
    <a href="https://github.com/cbaron3/safewalk-release/issues">Report Bug</a>
    ·
    <a href="https://github.com/cbaron3/safewalk-release/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://safewalklondon.ca)

Starting as a [hackathon project](https://devpost.com/software/safewalks-io), SafeWalk London gives residents of London, ON, Canada the ability to plan their walk home not only based on time, but also based on some key comfort metrics:
* Streetlight Density - Number of lights per km on any given walking path. Choose your brightness walk home at night.
* Sidewalk Availability -  Percentange of walking path that has sidewalk accessibility. Note, 100% availability means the path is accessible by sidewalk alone one entire side. 
* Road Traffic - Average daily traffic distributed along the walking path. Choose your walk home while remaining as visible to others as possible. 

This project was inspired by stories from people in London of walking home at night, especially students in the downtown area, running into situations that compromised their safety and security. 

### Built With
#### Frontend
* [React](https://reactjs.org/)
* [Redux](https://redux.js.org/)
* [Tailwind CSS](https://tailwindcss.com/)

#### Backend
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [PostgreSQL](https://www.postgresql.org/)

#### APIs
* [Google Maps](https://console.cloud.google.com/google/maps-apis/overview)
* [OpenData London](https://opendata.london.ca/)



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

* npm
```sh
npm install npm@latest -g
```

* python
```
python -m pip install virtualenv
```

### Usage

1. Get a free Google Maps API key at [https://console.cloud.google.com/google/maps-apis/overview](https://console.cloud.google.com/google/maps-apis/overview)

#### Frontend
2. Create an environment file for the frontend
```
cd frontend
touch .env
```
3. Fill in the following environment variables
```
REACT_APP_BACKEND_BASE_URL = 'enter-backend-url-here' // Backend URL. http://localhost:5000 for local development
REACT_APP_FRONTEND_GMAPS_API_KEY = 'enter-map-api-key-here' // Google Maps API Key
REACT_APP_GOOGLE_ANALYTICS_ID = 'enter-analytics-key-here' // Used for Google Analytics in Deployment
REACT_APP_ENV = 'production' // Used for Deployment
```
4. Install NPM packages
```
npm install
```

#### Backend

5. Create an environment file for the backend
```
cd backend
touch .env
```

6. Fill in the following environment variables
```
FLASK_APP_BACKEND_GMAPS_API_KEY = 'enter-map-api-key-here'
FLASK_APP_MAIL_USERNAME = 'enter-gmail-email-here'    // Only required if you want to use email contacting
FLASK_APP_MAIL_PASSWORD = 'enter-gmail-password-here' // Only required if you want to use email contacting
FLASK_APP_DB_URL = 'enter-database-url-here'
```

7. Install python dependencies

##### Windows
```
virtualenv venv
.\venv\Scripts\activate
```

##### Linux/mac
```
virtualenv venv
source venv/Scripts/activate
```

<!-- USAGE EXAMPLES -->
## Usage

### Backend
```
cd backend
python application.py
```

### Frontend
```
cd frontend
npm start
```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the GNU License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact
Carl Baron - carbaro196@gmail.com

Project Link: [https://github.com/cbaron3/safewalk-release](https://github.com/cbaron3/safewalk-release)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Steepless](http://cheeaun.github.io/steepless/)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/cbaron3/safewalk-release.svg?style=flat-square
[contributors-url]: https://github.com/cbaron3/safewalk-release/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/cbaron3/safewalk-release.svg?style=flat-square
[forks-url]: https://github.com/cbaron3/safewalk-release/network/members
[stars-shield]: https://img.shields.io/github/stars/cbaron3/safewalk-release.svg?style=flat-square
[stars-url]: https://github.com/cbaron3/safewalk-release/stargazers
[issues-shield]: https://img.shields.io/github/issues/cbaron3/safewalk-release.svg?style=flat-square
[issues-url]: https://github.com/cbaron3/safewalk-release/issues
[license-shield]: https://img.shields.io/github/license/cbaron3/safewalk-release.svg?style=flat-square
[license-url]: https://github.com/cbaron3/safewalk-release/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/cbaron3
[product-screenshot]: images/screenshot.PNG
