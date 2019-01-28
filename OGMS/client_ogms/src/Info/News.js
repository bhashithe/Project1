import _ from 'lodash';

import React from 'react';


class info extends React.Component{
  constructor() {
    super();
    this.state = {info:null};
    this.handleScroll = this.handleScroll.bind(this);
  }

  componentDidMount() {
    this.loadMoreinfo();
    this.loadMoreinfo = _.debounce(this.loadMoreinfo, 1000);
    window.addEventListener('scroll', this.handleScroll);
  }

  handleScroll() {
    let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
    if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
      console.log('Loading more info');
      this.loadMoreinfo();
    }
  }

  loadMoreinfo() {
    let request = new Request('http://localhost:8080/info', {
      method: 'GET',
      headers: {
        'Authorization': 'bearer ' + Auth.getToken(),
      },
      cache: false});


    fetch(request)
      .then((res) => res.json())
      .then((info) => {
        this.setState({
          info: this.state.info? this.state.info.concat(info) : info,
        });
      });
  }

  renderinfo() {
    let info_list = this.state.info.map(function(info) {
      return(
        <a className='list-group-item' href="#">
          <infoCard info={info} />
        </a>
      );
    });

    return(
      <div className="container-fluid">
        <div className='list-group'>
          {info_list}
        </div>
      </div>
    );
  }

  render() {
    if (this.state.info) {
        return(
          <div>
            {this.renderinfo()}
          </div>
        );
    } else {
      return(
        <div>
          <div id='msg-app-loading'>
            Loading
          </div>
        </div>
      );
    }
  }
}

export default info;
