// React imports
import React, {Component} from 'react';

import { connect } from 'react-redux';

import {ROUTE_STATE} from '../../../state'

import PropTypes from 'prop-types';

// Main app styling
import '../../../tailwind.css';

// Message prompts
import LoadingIcon from './LoadingIcon';
import Instructions from './Instructions';
import ErrorMessage from './ErrorMessage';
import RouteCard from './RouteCard';
import OutOfBoundsMessage from './OutOfBoundsMessage';

// Card redux action
import { setActiveCard } from '../../../actions/routeActions';

/**
 * Create route card based on json from API
 */
function createCard(routeJson, active) {
    return <RouteCard 
                active={active}
                polyline={routeJson.polyline} 
                lights={routeJson.lights.toFixed(0)} 
                sidewalks={(routeJson.sidewalks*100).toFixed(0)} 
                traffic={routeJson.traffic.toFixed(0)}
                time={routeJson.duration}
                distance={routeJson.distance}
            /> 
}

class RouteList extends Component {

    /**
     * Determine list content based on global app states
     */
    contentFromState() {
        let contentToRender;

        switch(this.props.routeState) {

            case ROUTE_STATE.INITIAL:
                // USED FOR DEBUGGING
                // let cards = [];
                // cards.push(<RouteCard active={true}/>)
                // cards.push(<RouteCard />)
                // cards.push(<RouteCard />)
                // contentToRender = cards
                
                contentToRender = <Instructions />
                break;

            case ROUTE_STATE.API_LOADING:
                contentToRender = <LoadingIcon />
                break;

            case ROUTE_STATE.API_LOADED:
                let cards = [];
                this.props.routes.forEach( route => {
                    if(route.polyline === this.props.activeRoute) {
                        cards.push( createCard(route, true) )
                    } else {
                        cards.push( createCard(route, false) )
                    }
                })

                // If there is no active route yet, treat the first route as the active one
                if(this.props.activeRoute === "" && cards.length > 0) {
                    cards[0] = createCard(this.props.routes[0], true)
                    this.props.setActiveCard(this.props.routes[0].polyline); 
                }
                
                contentToRender = cards
                break;

            case ROUTE_STATE.API_ERROR:
                contentToRender = <ErrorMessage />
                break;

            case ROUTE_STATE.API_OUT_OF_BOUNDS:
                contentToRender = <OutOfBoundsMessage />
                break;

            default:
                contentToRender = <Instructions />
                break;
         }

         return contentToRender
    }

    render() {
        return (
            <div>
                { this.contentFromState() }
            </div>
        )
    }
}

RouteList.propTypes = {
    routeState: PropTypes.object.isRequired,
    routes: PropTypes.array.isRequired,
    activeRoute: PropTypes.string.isRequired,
    setActiveCard: PropTypes.func.isRequired
};
  
const mapStateToProps = state => ({
    routeState: state.routes.routeState,
    routes: state.routes.availableRoutes,
    activeRoute: state.routes.activeRoute,
    setActiveCard: PropTypes.func.isRequired
});

export default connect(mapStateToProps, { setActiveCard })(RouteList);