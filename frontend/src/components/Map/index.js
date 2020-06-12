// React imports
import React, { Component } from 'react';

// Google maps
import { withScriptjs, withGoogleMap, GoogleMap, Polyline, Marker } from "react-google-maps"

// App stlying
import '../../tailwind.css';

// Component styling
import { inactivePolylineStyle, activePolylineStyle } from '../../styles';

// Define component props based on Redux
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

// Used to decode encoded polyline string into waypooints
import decodePolyline from 'decode-google-map-polyline'

// Markers for start/stop of polylines
import startIcon from '../../assets/blue-dot.png';
import stopIcon from '../../assets/red-dot.png';

// Google map styling
const mapStyle = require('./googleMapStyles.json');

// Google from window elements
const google = window.google;

/**
 * Function to create polyline components only for inactive routes
 */
function getInactiveRoutes(routes, activeRoute) {
    let inactives = [];
    routes.forEach(route => {
        if(route.polyline !== activeRoute) {
            inactives.push(
                <Polyline 
                    path={decodePolyline(route.polyline)}
                    options={inactivePolylineStyle}
                />
            )
        }
    })

    return inactives;
}

// Map component
const MyMapComponent = withScriptjs(withGoogleMap((props) =>
    <GoogleMap

        defaultZoom={14}
        
        center={{ lat: props.center.lat(), lng: props.center.lng()}}
    
        defaultOptions={{
            disableDefaultUI: true, // disable default map UI
            draggable: true, // make map draggable
            keyboardShortcuts: false, // disable keyboard shortcuts
            scaleControl: true, // allow scale controle
            scrollwheel: true, // allow scroll wheel
            styles: mapStyle // change default map styles
        }}>
        
        {/* Render active route on map if it exists*/}
        {props.inactiveRoutes}
        {props.activeRoute}

        {/* Render markers */}
        {props.startMarker}
        {props.endMarker}

    </GoogleMap>
))

// The map container and map itself
class MapContainer extends Component {
    constructor() {
        super();

        let center = new google.maps.LatLngBounds();
        center.extend({ lat: 42.9849, lng: -81.2453 });
        this.default_center = center.getCenter();
    }

    render() {
        
        // Determine route polylines that are not active
        const inactives = getInactiveRoutes(this.props.routes, this.props.activeRoute)
        
        // Determine active route polyline
        const active = <Polyline 
                            path={decodePolyline(this.props.activeRoute)}
                            options={activePolylineStyle}
                        />

        // Get start and stop markers
        const waypoints = decodePolyline(this.props.activeRoute);
        const start = <Marker position={ waypoints[0] } icon={startIcon}/>
        const end = <Marker position={ waypoints[waypoints.length - 1] } icon={stopIcon} />
        
        // Calculate center based on active route
        let bounds = new google.maps.LatLngBounds();
        for (var i = 0; i < waypoints.length; i++) {
            bounds.extend(waypoints[i]);
        }

        const center = bounds.getCenter();
        
        return (
         <div className="w-2/3 h-full">
            <MyMapComponent
                // Map render and props
                inactiveRoutes={inactives}

                activeRoute={active}

                startMarker={start}

                endMarker={end}

                center = {
                    // Use calculate center if waypoint length is greater than 0; meaning a non-null active route exists
                    waypoints.length > 0 ? center : this.default_center
                }

                googleMapURL={ 'https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=' + process.env.REACT_APP_FRONTEND_GMAPS_API_KEY }

                loadingElement={<div style={{ position: 'relative', height: '100%' }} />}

                containerElement={<div style={{ position: 'relative', height: '100%' }} />}
                
                mapElement={<div style={{ position: 'relative', height: '100%' }} />}
            />
        </div>
      )
    }
}

// Define the required props
MapContainer.propTypes = {
    routes: PropTypes.array.isRequired,
    activeRoute: PropTypes.string.isRequired,
};

// Convert the required parts of the redux store state to usable props
const mapStateToProps = state => ({
    routes: state.routes.availableRoutes,
    activeRoute: state.routes.activeRoute,
});

// Connect component prop to app state
export default connect(mapStateToProps, { })(MapContainer);