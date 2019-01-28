import React, { Component } from 'react';
import logo from './logo.jpg';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} alt="logo" />
          <p>
            Welcome to access CSC department information!
          </p>
          <a
            className="App-link"
            href="/students"
            target="_blank"
            rel="noopener noreferrer"
          >
            All students
          </a>
          <a
            className="App-link"
            href="/courses"
            target="_blank"
            rel="noopener noreferrer"
          >
            All courses
          </a>
          <a
            className="App-link"
            href="/enrollment"
            target="_blank" 
            rel="noopener noreferrer"
          >
            All enrollment
          </a>
          <a
            className="App-link"
            href="/students"
            target="_blank"
            rel="noopener noreferrer"
          >
            All assistantship
          </a>
          <a
            className="App-link"
            href="/students"
            target="_blank"
            rel="noopener noreferrer"
          >
            Level statistics
          </a>
        </header>
      </div>
    );
  }
}

export default App;
