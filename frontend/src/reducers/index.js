// Index file so can be imported as reducers
import { combineReducers } from 'redux';

import routeReducer from './routeReducer';

// Combine available reducers
export default combineReducers({
    routes: routeReducer
});