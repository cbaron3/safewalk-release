// Action types
import { ROUTE_FORM_BOUNDS_ERROR, 
         ROUTE_FORM_RETURNED, 
         ROUTE_CARD_ACTIVE, 
         ROUTE_FORM_SUBMITTED, 
         ROUTE_FORM_ERROR, 
         CONTACT_FORM_SUBMITTED, 
         CONTACT_FORM_RETURNED, 
         CONTACT_FORM_ERROR,
         CONTACT_FORM_CLOSED } from './types';

// Used for API call
import axios from 'axios'
import encodeurl from 'encodeurl'

/**
 * Redux action to initiate loading icon in route list
 */
export const loadRoutes = () => dispatch => {
    dispatch({
        type: ROUTE_FORM_SUBMITTED
    });
}

/**
 * Redux action that grabs routes based on form data
 */
export const getRoutes = (postData) => dispatch => {
    const URL = encodeurl(process.env.REACT_APP_BACKEND_BASE_URL + '/api/calc_rating')
    // Post request to get routes
    axios.post(URL, {
        'start': postData.start,
        'end': postData.end
    }).then((response) => {
        console.log(response);

        // Dispatch API response when valid
        dispatch({
            type: ROUTE_FORM_RETURNED,
            payload: response.data.data
        });

    }, (error) => {
        console.log(error);

        // Dispatch empty result when API error
        dispatch({
            type: ROUTE_FORM_ERROR,
            payload: []
        });
    });

    // TODO: Store requests here
};

/**
 * Redux action that dispatches data to store when a route card is clicked
 */
export const setActiveCard = (clickData) => dispatch => {
    
    // Dispatch card data on click
    dispatch({
        type: ROUTE_CARD_ACTIVE,
        payload: clickData
    })
};

/**
 * Redux action that dispatches data to handle when the route form has locations outside London, ON
 */
export const setBoundsError = () => dispatch => {
    dispatch({
        type: ROUTE_FORM_BOUNDS_ERROR,
        payload: []
    })
}

/**
 * Redux action that dispatches a route form error action, initiating an error message
 */
export const setRouteError = () => dispatch => {
    dispatch({
        type: ROUTE_FORM_ERROR,
        payload: []
    })
}

/**
 * Redux action that dispatches a route form closed action, allowing for the contact form to have its state reset
 */
export const resetContactForm = () => dispatch => {
    dispatch({
        type: CONTACT_FORM_CLOSED,
        payload: []
    })
}

/**
 * Redux action that sends email via backend when contact form is submitted
 */
export const sendEmail = (contactData) => dispatch => {

    const URL = encodeurl(process.env.REACT_APP_BACKEND_BASE_URL + '/api/email')
    
    // Form is submitted
    dispatch({
        type: CONTACT_FORM_SUBMITTED
    });

    // POST
    axios.post(URL, {
        'name': contactData.name,
        'subject': contactData.subject,
        'email': contactData.email,
        'message': contactData.message,
    }).then((response) => {
        console.log(response);

        // Dispatch API response when valid
        dispatch({
            type: CONTACT_FORM_RETURNED,
        });

    }, (error) => {
        console.log(error);

        // Dispatch empty result when API error
        dispatch({
            type: CONTACT_FORM_ERROR,
        });
    });
}