// Evaluate any actions that were submitted
import { ROUTE_FORM_RETURNED, 
         ROUTE_FORM_SUBMITTED, 
         ROUTE_FORM_ERROR, 
         ROUTE_CARD_ACTIVE, 
         CONTACT_FORM_ERROR, 
         CONTACT_FORM_SUBMITTED, 
         CONTACT_FORM_RETURNED,
         CONTACT_FORM_CLOSED, 
         ROUTE_FORM_BOUNDS_ERROR } from '../actions/types';

import { ROUTE_STATE, 
         CONTACT_STATE } from "../state";

// Initial store state
const initialStore = {
    availableRoutes: [],    // Initially, no routes
    activeRoute: "",        // Initially, active route polyline is blank
    routeState: ROUTE_STATE.INITIAL,
    contactState: CONTACT_STATE.INITIAL
}

// Evaluates state
export default function(state=initialStore, action) {
    switch (action.type) {
        
        case ROUTE_FORM_SUBMITTED:
            // Start loading animation when form is submitted
            return {
                ...state,
                routeState: ROUTE_STATE.API_LOADING,
            }

        case ROUTE_FORM_RETURNED:
            // Update available routes when new payload is received. Update app state
            return {
                ...state,
                availableRoutes: action.payload,
                routeState: ROUTE_STATE.API_LOADED,
            }
        
        case ROUTE_FORM_BOUNDS_ERROR:
            // Change state of route form to out of bounds
            return {
                ...state,
                routeState: ROUTE_STATE.API_OUT_OF_BOUNDS,
            }

        case ROUTE_FORM_ERROR:
            // Change state of route form to error when api gets an error
            return {
                ...state,
                routeState: ROUTE_STATE.API_ERROR,
            }

        case CONTACT_FORM_SUBMITTED:
            // Contact form submitted, wait for result
            return {
                ...state,
                contactState: CONTACT_STATE.LOADING,
            }

        case CONTACT_FORM_RETURNED:
            // Contact form submission was succesful
            return {
                ...state,
                contactState: CONTACT_STATE.LOADED,
            }

        case CONTACT_FORM_ERROR:
            // Contact form submission failed
            return {
                ...state,
                contactState: CONTACT_STATE.ERROR,
            }

        case CONTACT_FORM_CLOSED:
            // Contact form closed, reset state
            return {
                ...state, 
                contactState: CONTACT_STATE.INITIAL,
            }

        case ROUTE_CARD_ACTIVE:
            // Route card was selected; active. Modify active route
            return {
                ...state,
                activeRoute: action.payload,
            }

        default:
            return state;
    }
}