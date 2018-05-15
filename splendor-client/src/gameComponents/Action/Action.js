import React, { Component } from 'react';
import Card from '../Card/Card';

import '../Card/Card.css';
import './Action.css';

class Action extends Component {
  constructor() {
    super();
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit() {
    console.log(this.props.option)
    this.props.handleAction(this.props.option)
  }

  render() {
    return (
      <div className="Action" onClick={this.handleSubmit}>
        {this.props.type == 'collect_coins' || this.props.type == 'discard_coins' ?
        <div>
          <h4 className="Title">{this.props.type == 'collect_coins'? '' : 'Discard'}</h4>
          <div className="CoinsContainer">
            {this.props.red > 0? <div className="gem red">{this.props.red}</div>: ''}
            {this.props.blue > 0? <div className="gem blue">{this.props.blue}</div>: ''}
            {this.props.green > 0? <div className="gem green">{this.props.green}</div>: ''}
            {this.props.white > 0? <div className="gem white">{this.props.white}</div>: ''}
            {this.props.black > 0? <div className="gem black">{this.props.black}</div>: ''}
            {this.props.gold > 0? <div className="gem gold">{this.props.gold}</div>: ''}
          </div>
        </div> : ''}
        {/* {this.props.type == 'purchase_development' || this.props.type == 'reserve_open_development' ?
        <div>
          <h4 className="Title">{this.props.type == 'purchase_development'? 'Purchase' : 'Reserve'}</h4>
          <Card {...this.props.card} />
        </div> : ''}
        {this.props.type == 'reserve_from_deck' ?
        <div>
          <h4 className="Title">Reserve</h4>
          <div className="DevCard">
            <div className="cardHeader">
              <h4>{this.props.deck_num}</h4>
            </div>
          </div>
        </div>
         : ''} */}

      </div>
    );
  }
}

Action.defaultProps = {
  type: '',
  option: '',
  card: undefined,
  deck_num: undefined,
  red: undefined,
  blue: undefined,
  green: undefined,
  white: undefined,
  black: undefined,
  gold: undefined,
}

export default Action;
