import React, { Component } from 'react'

// Main app styling
import '../../tailwind.css';
import 'react-responsive-modal/styles.css';

import streetlight from '../../assets/streetlight.png';
import sidewalk from '../../assets/sidewalk.png';
import traffic from '../../assets/traffic.png';

export default class About extends Component {
    render() {
        return (
            <div className="font-sans">
                <br></br>

                <p>Plan your walk home with safety in mind.</p>
                
                <br></br>

                <p>Select your start and end point. Each walking route is then analyzed for:</p>

                <br></br>
                
                <div className="overflow-hidden w-auto display-inline flex flex-col items-center justify-center">
                    <div className="flex flex-col items-start justify-start">
                        <div className="flex flex-row my-2">
                            <img src={streetlight} alt={"Streetlight icon"} className="h-6 w-6 pr-2
                                                                                       sm:h-10 sm:w-10
                                                                                       md:h-10 md:w-10
                                                                                       lg:h-10 lg:w-10
                                                                                       xl:h-10 xl:w-10"></img>
                            <p className="m-auto">Street Light Density</p>
                        </div>
                        
                        <div className="flex flex-row my-2">
                            <img src={sidewalk} alt={"Sidewalk icon"} className="h-6 w-6 pr-2
                                                                                 sm:h-10 sm:w-10
                                                                                 md:h-10 md:w-10
                                                                                 lg:h-10 lg:w-10
                                                                                 xl:h-10 xl:w-10"></img>
                            <p className="m-auto">Sidewalk Availabilty</p>
                        </div>

                        <div className="flex flex-row my-2">
                            <img src={traffic} alt={"Car icon"} className="h-6 w-6 pr-2
                                                                           sm:h-10 sm:w-10
                                                                           md:h-10 md:w-10
                                                                           lg:h-10 lg:w-10
                                                                           xl:h-10 xl:w-10"></img>
                            <p className="m-auto">Road Traffic</p>
                        </div>
                    </div>
                </div>
            
                <br></br>
                <p><b>* Functional only in London, Ontario, Canada.</b></p>

                <br></br>
                <div>Icons made by: <a href="https://www.flaticon.com/authors/roundicons" title="Roundicons">Roundicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> <a href="https://www.vexels.com/">and Vexel</a> from <a href="https://www.vexels.com/" title="Flaticon">www.vexels.com</a></div>
            </div>
        )
    }
}
