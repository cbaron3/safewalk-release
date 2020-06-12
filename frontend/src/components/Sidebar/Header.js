// React imports
import React, {Component} from 'react';

// Bulb icon for header
import bulb_icon from '../../assets/bulb-icon.png';

// App styling
import '../../tailwind.css';


// Misc styling
class Header extends Component {
    render() {
        return(
            <div className="main-bg-blue flex items-center justify-center 
                            h-8 
                            sm:h-12 
                            md:h-16 
                            lg:h-16 
                            xl:h-20">

                <img src={bulb_icon} alt="Light Bulb Icon" className="  ml-0 h-5
                                                                        sm:ml-4 sm:h-10
                                                                        md:ml-6 md:h-12
                                                                        lg:ml-8 lg:h-14
                                                                        xl:ml-10 xl:h-16"></img>

                <h1 className=" font-sans text-yellow-200 
                                text-l ml-1 mr-1
                                sm:text-3xl 
                                md:text-4xl 
                                lg:text-5xl 
                                xl:text-5xl ">SafeWalk</h1>

                
                <img src={bulb_icon} alt="Light Bulb Icon" className="  mr-0 h-5
                                                                        sm:mr-4 sm:h-10
                                                                        md:mr-6 md:h-12
                                                                        lg:mr-8 lg:h-14
                                                                        xl:mr-10 xl:h-16"></img>
            </div>
        )
    }
}

export default Header;