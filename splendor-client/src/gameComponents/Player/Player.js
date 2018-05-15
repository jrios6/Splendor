import React, { Component } from 'react';
import Card from '../Card/Card';
import Noble from '../Noble/Noble';

import '../Card//Card.css';
import '../game.css';
import './Player.css';

class Player extends Component {
  constructor() {
    super();
    this.handleShowDevelopments = this.handleShowDevelopments.bind(this);
    this.handleShowNobles = this.handleShowNobles.bind(this);
    this.state = {
      showDevelopments: false,
      showNobles: false,
      active: false,
    }
  }

  handleShowDevelopments() {
    this.setState((prevState) => {
      return {showDevelopments: !prevState.showDevelopments}
    })
  }

  handleShowNobles() {
    this.setState((prevState) => {
      return {showNobles: !prevState.showNobles}
    })
  }

  render() {
    return (
      <div>
        <table>
          <tr>
            <h4>{this.props.name}: {this.props.points} points</h4>
          </tr>
          <tr>
            <td>
              <h4>Gems</h4>
              <div className="FlexContainer">
                {this.props.gems[0] > 0? <div className="gem red">{this.props.gems[0]}</div>: ''}
                {this.props.gems[1] > 0? <div className="gem blue">{this.props.gems[1]}</div>: ''}
                {this.props.gems[2] > 0? <div className="gem green">{this.props.gems[2]}</div>: ''}
                {this.props.gems[3] > 0? <div className="gem white">{this.props.gems[3]}</div>: ''}
                {this.props.gems[4] > 0? <div className="gem black">{this.props.gems[4]}</div>: ''}
              </div>
            </td>
            <td>
              <h4>Coins ({this.props.red + this.props.blue + this.props.green +
                this.props.white + this.props.black + this.props.gold})</h4>
                <div className="FlexContainer">
                  {this.props.red > 0? <div className="gem red">{this.props.red}</div>: ''}
                  {this.props.blue > 0? <div className="gem blue">{this.props.blue}</div>: ''}
                  {this.props.green > 0? <div className="gem green">{this.props.green}</div>: ''}
                  {this.props.white > 0? <div className="gem white">{this.props.white}</div>: ''}
                  {this.props.black > 0? <div className="gem black">{this.props.black}</div>: ''}
                  {this.props.gold > 0? <div className="gem gold">{this.props.gold}</div>: ''}
                </div>
            </td>
          </tr>
          <tr>
            <td>
              <h4>Nobles
                <button onClick={this.handleShowNobles}>
                  {this.state.handleShowNobles? 'hide' : 'show'}
                </button>
              </h4>
            </td>
            <td>
              <h4>Developments
                <button onClick={this.handleShowDevelopments}>
                  {this.state.showDevelopments? 'hide' : 'show'}
                </button>
              </h4>
            </td>
          </tr>
          <tr>
            <td>
              {this.state.showNobles? <tr>
                {this.props.nobles.map((noble) => {
                  return <td><Noble {...noble} /></td>
                })}
              </tr> : ''}
            </td>
            <td>
              {this.state.showDevelopments? <tr>
                {this.props.developments.map((card) => {
                  return <td><Card {...card} handleAction={this.props.handleAction} /></td>
                })}
              </tr> : ''}
            </td>
          </tr>
          <tr><h4>Reserved Developments</h4></tr>
          <tr>
            {this.props.board_reservations.map((card) => {
              return <td><Card {...card} handleAction={this.props.handleAction} /></td>
            })}
            {this.props.deck_reservations.map((card) => {
              return <td><Card {...card} handleAction={this.props.handleAction} /></td>
            })}
          </tr>
        </table>
      </div>
    );
  }
}

Player.defaultProps = {
  name: 'Player',
  points: 0,
  gems: [0, 0, 0, 0, 0],
  developments: [],
  board_reservations: [],
  deck_reservations: [],
  nobles: [],
  red: 0,
  blue: 0,
  green: 0,
  white: 0,
  black: 0,
  gold: 0,
}

export default Player;
