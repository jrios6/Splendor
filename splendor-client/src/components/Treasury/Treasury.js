import React, { Component } from 'react';

import '../Card/Card.css';
import '../game.css';

class Treasury extends Component {
  render() {
    return (
      <div className="Treasury">
        <h3>Treasury</h3>
        <div className="CoinsContainer">
          <div className="gem red">{this.props.red}</div>
          <div className="gem blue">{this.props.blue}</div>
          <div className="gem green">{this.props.green}</div>
          <div className="gem white">{this.props.white}</div>
          <div className="gem black">{this.props.black}</div>
          <div className="gem gold">{this.props.gold}</div>
        </div>
      </div>
    );
  }
}

Treasury.defaultProps = {
  red: 7,
  blue: 7,
  green: 7,
  white: 7,
  black: 7,
  gold: 5,
}

export default Treasury;
