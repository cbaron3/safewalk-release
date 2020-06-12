// React imports
import React, {Component} from 'react';

// Main app styling
import '../../main.css';
import '../../tailwind.css';

import PropTypes from 'prop-types';

// Google autocomplete 
import GooglePlacesAutocomplete from 'react-google-places-autocomplete';

import ContactForm from './ContactForm';
import About from './About';

import { connect } from 'react-redux';
import { loadRoutes, getRoutes, setRouteError, setBoundsError, resetContactForm } from '../../actions/routeActions';

import 'react-responsive-modal/styles.css';
import { Modal } from 'react-responsive-modal';
import Geocode from "react-geocode";

Geocode.setApiKey( process.env.REACT_APP_FRONTEND_GMAPS_API_KEY );
Geocode.setLanguage("en");
Geocode.setRegion("ca");

// Form that handles directions input
class RouteForm extends Component {
    constructor(props) {
        super(props);

        this.callMetricsAPI = this.callMetricsAPI.bind(this);
        this.handleFormSubmit = this.handleFormSubmit.bind(this);

        this.onAboutOpenModal = this.onAboutOpenModal.bind(this);
        this.onAboutCloseModal = this.onAboutCloseModal.bind(this);

        this.state = {
            aboutOpen: false,
            contactOpen: false,
            startPoint: '',
            endPoint: '',
        };
    }
    // Handle submission of form
    handleFormSubmit(event) {
        // Prevent default reload action
        event.preventDefault();

        this.props.loadRoutes();

        let validStart = false;
        let validEnd = false;

        Geocode.fromAddress(this.state.startPoint).then(
            response => {
                const result = response.results[0].formatted_address;

                validStart = result.includes("London, ON");
                
                console.log(result, validStart);

                Geocode.fromAddress(this.state.endPoint).then(
                    response => {
                        const result = response.results[0].formatted_address;
        
                        validEnd = result.includes("London, ON");
        
                        console.log(result, validEnd);
        
                        if(validStart && validEnd) {
                            this.callMetricsAPI();
                        } else {
                            this.props.setBoundsError();
                            console.log("Error");
                        }
                    },
                    error => {
                        console.error(error);
                        this.props.setRouteError();
                    }
                );
            },
            error => {
                console.error(error);
                this.props.setRouteError();
            }
        );

        
    }

    callMetricsAPI() {
        const data = {
            'start': this.state.startPoint,
            'end': this.state.endPoint
        };

        this.props.getRoutes(data);
    }

    onAboutOpenModal = () => {
        this.setState({ aboutOpen: true });
    };

    onContactOpenModal = () => {
        this.setState({ contactOpen: true });
    };
     
    onAboutCloseModal = () => {
        this.setState({ aboutOpen: false });
    };

    onContactCloseModal = () => {
        this.setState({ contactOpen: false });

        this.props.resetContactForm();
    };

    // Render form
    render() {
        return (
            <div className="flex items-center justify-center border-b-2 border-gray-300 pt-4 pb-4">
                <form id="input-form" onSubmit={this.handleFormSubmit} className="w-11/12">
                    
                    {/* From label */}
                    <label className="text-gray-500 mt-5">From</label>

                    {/* Autocomplete input for google maps; start point */}
                    <GooglePlacesAutocomplete 
                        required={true}

                        // Only in Canada
                        autocompletionRequest={{
                            componentRestrictions: {
                            country: ['ca'],
                        }}}

                        placeholder='Choose start...'
                        
                        inputClassName={"bg-gray-200 w-full mb-2 text-center text-xs sm:text-base md:text-base lg:text-lg xl:text-lg"}
                        suggestionsClassNames={{ container: 'border-2 border-black', 
                                                 suggestion: "bg-gray-200 text-center border-b-2 border-gray-400 main-suggestions text-xs sm:text-base md:text-base lg:text-lg xl:text-lg", 
                                                 suggestionActive: "main-suggestions" }}

                        onSelect={
                            ({description}) => {
                                this.setState({ startPoint: description });
                            }
                        }
                    />
                    
                    {/* To label */}
                    <label className="text-gray-500">To</label>
                    
                    {/* Autocomplete input for google maps; end point */}
                    <GooglePlacesAutocomplete 
                        required={true}

                        // Only in Canada
                        autocompletionRequest={{
                            componentRestrictions: {
                            country: ['ca'],
                        }}}

                        placeholder='Choose end...'
                        
                        inputClassName={"bg-gray-200 w-full mb-2 text-center text-xs sm:text-base md:text-base lg:text-lg xl:text-lg"}
                        suggestionsClassNames={{ container: 'border-2 border-black', 
                                                 suggestion: "bg-gray-200 text-center border-b-2 border-gray-400 main-suggestions text-xs sm:text-base md:text-base lg:text-lg xl:text-lg", 
                                                 suggestionActive: "main-suggestions" }}


                        onSelect={
                            ({description}) => {
                                this.setState({ endPoint: description }, () => {});
                            }
                        }
                    />

                    {/* Form footer that contains buttons */}
                    <div className="flex items-center justify-center w-full pt-1 pb-2">
                        <button className=" main-go-btn font-bold py-2 px-4 rounded w-full text-xs sm:text-base md:text-base lg:text-base xl:text-base">Go</button>
                    </div>
                    
                    <div className="flex items-center justify-between w-full m-auto">
                        
                        <button id="about-btn" onClick={this.onAboutOpenModal} type="button" className="main-btn font-bold rounded text-xs sm:text-base md:text-base lg:text-base xl:text-base
                                                                                                        w-1/2 h-auto py-1 px-1 mr-1">About</button>
                                                                                                                           
                        <button id="contact-btn" onClick={this.onContactOpenModal} type="button" className="main-btn font-bold rounded text-xs sm:text-base md:text-base lg:text-base xl:text-base
                                                                                                            w-1/2 h-auto py-1 px-1 ml-1">Contact</button>
                    </div>
                </form>

                <Modal open={this.state.aboutOpen} onClose={this.onAboutCloseModal} center>
                    <h2 className="font-bold text-3xl">About</h2>
                    <About />
                </Modal>

                <Modal open={this.state.contactOpen} onClose={this.onContactCloseModal} center>
                    <h2 className="font-bold text-3xl">Contact</h2>
                    <ContactForm />
                </Modal>
            </div>
        )
    }
}

RouteForm.propTypes = {
    getRoutes: PropTypes.func.isRequired,
    setBoundsError: PropTypes.func.isRequired,
    loadRoutes: PropTypes.func.isRequired,
    resetContactForm: PropTypes.func.isRequired,
    setRouteError: PropTypes.func.isRequired
};
  
export default connect(null, { loadRoutes, getRoutes, setRouteError, setBoundsError, resetContactForm })(RouteForm);
