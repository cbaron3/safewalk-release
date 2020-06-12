// React imports
import React, {Component} from 'react';

// Using tailwind for styling
import '../../tailwind.css';


// Side bar components
import Header from './Header';
import RouteForm from './RouteForm';
import RouteList from './RouteList';

class Sidebar extends Component {
    // Sidebar container with header, form, and list
    render() {
        return (
            <div id="sidebar-container" className="h-full   w-1/2 
                                                            sm:w-1/3
                                                            md:w-1/3
                                                            lg:w-1/3
                                                            xl:w-1/3">
                <Header />
                <RouteForm />
                <RouteList />
            </div>
        )
    }
}

export default Sidebar;