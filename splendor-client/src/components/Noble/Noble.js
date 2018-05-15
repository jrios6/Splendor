import React, { Component } from 'react';

import './Noble.css';

class Noble extends Component {
  render() {
    return (
      <div className="NobleCard">
        {this.props.red > 0? <div className="gem red">{this.props.red}</div>: ''}
        {this.props.blue > 0? <div className="gem blue">{this.props.blue}</div>: ''}
        {this.props.green > 0? <div className="gem green">{this.props.green}</div>: ''}
        {this.props.white > 0? <div className="gem white">{this.props.white}</div>: ''}
        {this.props.black > 0? <div className="gem black">{this.props.black}</div>: ''}
      </div>
    );
  }
}

Noble.defaultProps = {
  type: '',
  red: 0,
  blue: 0,
  green: 0,
  white: 0,
  black: 0,
}

export default Noble;
