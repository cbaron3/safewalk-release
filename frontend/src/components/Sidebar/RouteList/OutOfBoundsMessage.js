import React, { Component } from 'react'

// Main app styling
import '../../../main.css';

export default class OutOfBoundsMessage extends Component {
    render() {
        return (
            <div className="flex flex-col items-center pt-5">
                <div className="fa-3x ">
                    <i className="fas fa-exclamation-circle" />
                </div>
                <p className="font-sans text-xs text-center px-2 sm:text-s md:text-base lg:text-xl xl:text-2xl">Sorry, this service works only for addresses in London, Ontario, Canada</p>
            </div>
        )
    }
}
