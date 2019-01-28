import React from 'react';
import PropTypes from 'prop-types';

import './App.css';

const App = ({ children }) => (
  <div>
    <header>
      <div className="container">
        <a href="#" data-activates="nav-mobile" className="button-collapse top-nav full hide-on-large-only">
          <i className="material-icons">Menu</i>
        </a>
      </div>
      <ul className="side-nav fixed sideNavStyle">
        <li className="logo">
          <a id="logo-container" href="http://www.linawheretogo.com/" className="brand-logo">
            {/*<object id="front-page-logo" type="image/svg+xml" data="../../logo.png"></object>*/}
            Project1 Website
          </a>
        </li>
        <li className="bold"><a href="/news" className="waves-effect waves-teal">News Management</a></li>
        <li className="bold"><a href="/friends" className="waves-effect waves-teal">Friends Management</a></li>
        <li className="bold"><a href="/reviews" className="waves-effect waves-teal">Reviews Management</a></li>
        <li className="bold"><a href="" className="waves-effect waves-teal">Account Setting</a></li>
      </ul>
    </header>
    <main className="main-with-padding">{children}</main>   
  </div>
);

App.propTypes = {
  children: PropTypes.object.isRequired
};

export default App;

