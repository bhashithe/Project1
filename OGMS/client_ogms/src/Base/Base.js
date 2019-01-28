import 'materialize-css/dist/css/materialize.min.css';
import 'materialize-css/dist/js/materialize.min.js';

import React from 'react';
import PropTypes from 'prop-types';
import './Base.css';


const Base = ({ title, children }) => (
  <div className="section-no-padding">
    <nav className="nav-bar dark-primary-color topBarStyle">
      <div className="container">
        <div className="nav-wrapper"><a className = "pageTitleStyle">{title}</a></div>
      </div>
    </nav>
    <div className="container">{children}</div>
  </div>
);

Base.propTypes = {
  children: PropTypes.object.isRequired,
  title: PropTypes.string
};

export default Base;
