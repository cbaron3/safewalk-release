// Route form state
export const ROUTE_STATE = {
    API_LOADING:        'API_LOADING',  // Form has been submitted
    API_LOADED:         'API_LOADED',   // Form has returned data
    API_ERROR:          'API_ERROR',    // Form has produced an error
    API_OUT_OF_BOUNDS:  'API_OUT_OF_BOUNDS', // Form inputs are out of London bounds
    INITIAL:            'INITIAL',      // Form initial state
};

// Contact form state
export const CONTACT_STATE = {
    LOADING: 'API_LOADING',     // Contact form is submitted
    LOADED:  'API_LOADED',      // Contact form has returned message
    ERROR:   'API_ERROR',       // Contact form has produced error
    INITIAL: 'INITIAL',         // Contact form initial state
}