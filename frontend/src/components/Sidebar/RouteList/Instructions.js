import React, { Component } from 'react'

// Main app styling
import '../../../tailwind.css';

export default class Instructions extends Component {
    render() {
        return (
            <div className="flex flex-col items-center pt-5">   
                <div className="fa-3x ">
                    <i className="fas fa-walking"/>
                </div>
                <p className="font-sans text-xs text-center px-2 sm:text-s md:text-base lg:text-xl xl:text-2xl">Begin by entering a start and end location above.</p>
            </div>
        )
    }
}