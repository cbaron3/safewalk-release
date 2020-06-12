import React, { Component } from 'react'

// Main app styling
import '../../../main.css';

export default class LoadingIcon extends Component {
    render() {
        return (
            // Using font awesome for loading icon
            <div className="flex flex-col items-center pt-5">
                <div className="fa-3x ">
                    <i className="fas fa-circle-notch fa-spin" />
                </div>
                <p className="font-sans text-xs text-center px-2 sm:text-s md:text-base lg:text-xl xl:text-2xl">Retrieving routes...</p>
            </div>
        )
    }
}
