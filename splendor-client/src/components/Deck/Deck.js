import React, { Component } from 'react';

import './Deck.css';

class Deck extends Component {
  constructor() {
    super();
    this.handleReservation = this.handleReservation.bind(this);
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

  render() {
    return (
      <div className="Deck" onClick={this.showAction}>
        <h4>Deck {this.props.tier}</h4>
        <p>{this.props.cards} cards</p>
        {this.state.showAction? <div>
          {this.props.reserve? <button onClick={this.handleReservation}>
            Reserve
          </button>: ''}
        </div>: ''}
      </div>
    );
  }
}

Deck.defaultProps = {
  tier: 1,
  cards: 0,
  reserve: undefined,
}

export default Deck;
