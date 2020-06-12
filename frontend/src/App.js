import React, {Component} from 'react';

// Provider to connect store to redux
import { Provider } from 'react-redux';

// Redux global data store
import store from './store';

// Container that contains the sidebar elements
import Sidebar from './components/Sidebar'

// Container that contains the map elements
import Map from './components/Map'

import GA from './utility/analytics'

import { BrowserRouter, Switch, Route } from 'react-router-dom'

import './main.css';

class App extends Component {
  // Render app
  render() {
    return (
        <Provider store={store}>
          <BrowserRouter>
            { GA.init() && <GA.RouteTracker /> }
            <div className="font-sans h-full w-full flex">
                <Sidebar />
                <Map />
            </div>
          </BrowserRouter>
        </Provider>
    )
  }
}

export default App;
