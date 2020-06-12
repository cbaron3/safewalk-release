import React from 'react';
import { connect } from 'react-redux';
import { sendEmail } from '../../actions/routeActions';
import { useForm } from 'react-hook-form';
import { CONTACT_STATE } from '../../state';

// Using functional component for react-hook-form
export const ContactForm = ({ contactState, sendEmail }) => {
    const { register, handleSubmit, errors } = useForm();
    
    // Handle form submission
    const onSubmit = data => {
        // Send to backend for email handling
        const contactData = {
            'name': data.name,
            'subject': data.subject,
            'email': data.email,
            'message': data.message,
        };

        sendEmail(contactData);
    };

    return (
        <div className="font-sans contact-form">
            <form onSubmit={handleSubmit(onSubmit)} id="usrform">
                
                <div>
                    <label htmlFor="name">Name *</label>
                    <input type="text" name="name" ref={register({
                        required: true,
                        maxLength: 60,
                    })}/>
                </div>
                {errors.name && <p className="font-bold text-red-600">Please enter a name</p>}

                <div>
                    <label htmlFor="email">Email *</label>
                    <input type="text" name="email" ref={register({
                        required: true,
                        maxLength: 80,
                        pattern: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
                    })}/>
                </div>
                {errors.email && <p className="font-bold text-red-600">Please enter a valid email</p>}

                <div>
                    <label htmlFor="subject">Subject</label>
                    <input type="text" name="subject" ref={register({
                        required: false,
                        maxLength: 80,
                    })}/>
                </div>

                <div>
                    <label htmlFor="message">Message *</label>
                    <textarea rows="2" type="text" name="message" ref={register({
                        required: true,
                        maxLength: 400,
                    })}/>
                </div>
                {errors.message && <p className="font-bold text-red-600 mb-2">Please enter a message</p>}
                
                <div>
                    <button className={contactState === CONTACT_STATE.ERROR ? "main-contact-error-btn" : "main-contact-btn"}>
                        {
                           (() => {
                            switch (contactState) {
                                case CONTACT_STATE.LOADING:   return <div><i className="fas fa-circle-notch fa-spin" /><p>Sending...</p></div>;
                                case CONTACT_STATE.LOADED :   return <div><i className="fas fa-check" /><p>Sent!</p></div>;
                                case CONTACT_STATE.ERROR:     return <div><i className="fas fa-exclamation-circle"/><p>Error</p></div>;
                                default: return <p>Send Message</p>
                            }
                            })() 
                        }
                    </button>
                </div>
            </form>
        </div>
    );
  }

const mapStateToProps = state => ({
    contactState: state.routes.contactState
});
  

export default connect(mapStateToProps, { sendEmail })(ContactForm);
