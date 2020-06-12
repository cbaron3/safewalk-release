// React imports
import React, {Component} from 'react';

import streetlight from '../../../assets/streetlight.png';
import sidewalk from '../../../assets/sidewalk.png';
import traffic from '../../../assets/traffic.png';


import '../../../tailwind.css';

// Define component props based on Redux
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import {generateMapURL} from '../../../utility'

// Card redux action
import { setActiveCard } from '../../../actions/routeActions';

import { Modal } from 'react-responsive-modal';

import decodePolyline from 'decode-google-map-polyline'

/**
 * Convert google api seconds value into hr-mins string
 */
function secondsToHrMins(seconds) {

    var d = Number(seconds);

    var h = Math.floor(d / 3600);
    var m = Math.floor(d % 3600 / 60);

    var hDisplay = h > 0 ? h + (h === 1 ? " hr, " : " hrs, ") : "";
    var mDisplay = m > 0 ? m + (m === 1 ? " min" : " mins") : "";

    return hDisplay + mDisplay; 
}

function metresToKms(metres) {
    // TODO: Make it work with VALUE
    return metres + "";
}

/** 
 * Component that encapsulates the reusable img-text pair on the route card
 */
class CardText extends Component {
    render() {
        return (
            <div className="flex py-2 px-2">
                <img src={this.props.img} alt={this.props.alt} className="h-6 w-6 
                                                                               sm:h-6 sm:w-6
                                                                               md:h-6 md:w-6
                                                                               lg:h-10 lg:w-10
                                                                               xl:h-10 xl:w-10"></img>
                <p className="ml-1 text-xs xl:text-lg">{this.props.metric}{this.props.metric_type}</p>

            </div>
        )
    }
}

class RouteCard extends Component {
    constructor() {
        super();

        this.onClick = this.onClick.bind(this);
        this.onRedirect = this.onRedirect.bind(this);
        this.onOpenModal = this.onOpenModal.bind(this);
        this.onCloseModal = this.onCloseModal.bind(this);

        this.state = {
            modalOpen: false,
        };
    }
    
    // On click of this route card, make it active
    onClick() {
        this.props.setActiveCard(this.props.polyline);   
    }

    // Open directions modal
    onOpenModal() {
        this.setState({ modalOpen: true });
    }

    // Close directions modal
    onCloseModal() {
        this.setState({ modalOpen: false });
    }

    // Redirect to google maps on click of modal button
    onRedirect() {
        // 8 is arbitray; seems to work the best
        const url = generateMapURL(decodePolyline(this.props.polyline), 8)
        window.open(url);
        this.setState({ modalOpen: false });
    }

    render() {
        return (
            <div>
                <div className="border-b-2 border-gray-300 p-2 mt-1">
                    <div onClick={this.onClick} className={this.props.active ? "flex flex-col items-center lg:flex-row xl:flex-row w-full m-auto" : "flex flex-col items-center lg:flex-row xl:flex-row opacity-50 w-full m-auto"}>
            
                            <div className={"lg:w-1/2 xl:w-1/2 flex flex-col items-center justify-start lg:ml-5 xl:ml-5"}>
                                <div className="flex flex-col justify-start">
                                    <CardText alt={"Streetlight"} img={streetlight} metric={this.props.lights} metric_type={" Lights per km"} />
                                    <CardText alt={"Sidewalk"} img={sidewalk} metric={this.props.sidewalks} metric_type={"% Sidewalk coverage"} />
                                    <CardText alt={"Streetlight"} img={traffic} metric={this.props.traffic} metric_type={" Cars per day"} />
                                </div>

                            </div>
                    

                            <div className="lg:w-1/2 xl:w-1/2 lg:h-40 xl:h-40 main-card-height flex flex-col justify-center items-center lg:items-end xl:items-end lg:justify-between xl:justify-between xl:mr-5 lg:mr-5">
                                <p className="text-center">{secondsToHrMins(this.props.time)} - {metresToKms(this.props.distance)} km</p>
                                {this.props.active && <button id="go-btn" 
                                        onClick={this.onOpenModal} 
                                        type="button" 
                                        className="w-full sm:w-full md:w-full lg:w-auto xl:w-auto bg-green-300 hover:bg-green-500 font-bold rounded text-xs mt-1 sm:text-s md:text-s lg:text-s xl:text-lg py-2 px-2 ">START</button> }
                            </div>
                            

                            
                    </div>
                </div>

                <Modal open={this.state.modalOpen} onClose={this.onCloseModal} center>
                    <h2 className="font-bold text-3xl">Directions</h2>
                    <p className="my-2">You will be redirected to Google Maps for live directions, is that ok?</p>

                   
                    <div className="flex items-center justify-between w-full my-2 pt-2">
                        
                        <button id="about-btn" onClick={this.onRedirect} type="button" className="main-btn font-bold rounded text-xs sm:text-base md:text-base lg:text-base xl:text-base
                                                                                                        w-1/2 h-auto py-1 px-1 mr-1">Ok</button>
                        

                        <button id="contact-btn" onClick={this.onCloseModal} type="button" className="main-btn font-bold rounded text-xs sm:text-base md:text-base lg:text-base xl:text-base
                                                                                                            w-1/2 h-auto py-1 px-1 ml-1">Close</button>
                    </div>
                </Modal>
            </div>
        )
    }
}

// Define the required props
RouteCard.propTypes = {
    setActiveCard: PropTypes.func.isRequired
};

// Connect redux action to app state
export default connect(null, { setActiveCard })(RouteCard);