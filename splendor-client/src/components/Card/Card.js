import React, { Component } from 'react';

import './Card.css';

class Card extends Component {
  constructor() {
    super();
    this.handleReservation = this.handleReservation.bind(this);
    this.handlePurchase = this.handlePurchase.bind(this);
    this.showAction = this.showAction.bind(this);
    this.state = {
      showAction: false,
    }
  }

  showAction() {
    this.setState((prevState) => {
      return {showAction: !prevState.showAction}
    })  }

  handleReservation() {
    this.props.handleAction(this.props.reserve.option);
  }

  handlePurchase() {
    this.props.handleAction(this.props.purchase.option);
  }

  render() {
    return (
      <div className={this.props.purchase? "purchasable DevCard": "DevCard"} onClick={this.showAction}>
        <div className="cardHeader">
          <h4 className="cardPoints">{this.props.points}</h4>
          <p className="gemType">{this.props.gem_type}</p>
        </div>
        {this.state.showAction? <div>
          {this.props.reserve? <button onClick={this.handleReservation}>
            Reserve
          </button>: ''}
          {this.props.purchase? <button onClick={this.handlePurchase}>
            Purchase
          </button>: ''}
        </div>: <div className="cardBody">
          {this.props.red > 0? <div className="gem red">{this.props.red}</div>: ''}
          {this.props.blue > 0? <div className="gem blue">{this.props.blue}</div>: ''}
          {this.props.green > 0? <div className="gem green">{this.props.green}</div>: ''}
          {this.props.white > 0? <div className="gem white">{this.props.white}</div>: ''}
          {this.props.black > 0? <div className="gem black">{this.props.black}</div>: ''}
        </div>}
      </div>
    );
  }
}

Card.defaultProps = {
  tier: 1,
  gem_type: '',
  points: 0,
  red: 0,
  blue: 0,
  green: 0,
  white: 0,
  black: 0,
  reserve: undefined,
  purchase: undefined,
}

export default Card;
