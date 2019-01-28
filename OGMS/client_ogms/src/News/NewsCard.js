import './NewCard.css';

import React from 'react';

class NewsCard extends React.Component{
  render() {
    return(
      <div className="news-container">
        <div className='row'>
          <div className='col s4 fill'>
            <img src={this.props.news.urlToImage} alt='news'/>
          </div>
          <div className="col s8">
              <div className="news-details">
                <p>{this.props.news.title}</p>
                <p>{this.props.news.description}</p>
                <p>{this.props.news.url}</p>
                <p>{this.props.news.date}</p>
              </div>
          </div>
        </div>
      </div>
    );
  }
}

export default NewsCard;
