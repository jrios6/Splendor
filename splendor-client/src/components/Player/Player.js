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
    this.handleShow = this.handleShow.bind(this);
    this.state = {
      showDevelopments: false,
      show: false,
      active: false,
    }
  }

  handleShowDevelopments() {
    this.setState((prevState) => {
      return {showDevelopments: !prevState.showDevelopments}
    })
  }

  handleShow() {
    this.setState((prevState) => {
      return {show: !prevState.show}
    })
  }

  render() {
    return (
      <div className={this.props.active? "ActivePlayer" : "Player"}>
        <table>
          <tr>
            <h4>{this.props.name}: {this.props.points} points</h4>
            {this.props.active? '': <button onClick={this.handleShow}>
              {this.state.handleShow? 'hide' : 'show'}
            </button>}
          </tr>
          {this.state.show || this.props.active? <div>
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
              <td>
                <h4>Nobles</h4>
                {this.props.nobles.map((noble) => {
                  return <td><Noble {...noble} /></td>
                })}
              </td>
            </tr>
            <tr className="Developments">
              <td>
                <h4>Developments
                  <button onClick={this.handleShowDevelopments}>
                    {this.state.showDevelopments? 'hide' : 'show'}
                  </button>
                </h4>
                {this.state.showDevelopments? <tr>
                  {this.props.developments.map((card) => {
                    return <td><Card {...card} handleAction={this.props.handleAction} /></td>
                  })}
                </tr> : ''}
              </td>
              <td>
                <h4>Reserved Developments</h4>
                {this.props.board_reservations.map((card) => {
                  return <td><Card {...card} handleAction={this.props.handleAction} /></td>
                })}
                {this.props.deck_reservations.map((card) => {
                  return <td><Card {...card} handleAction={this.props.handleAction} /></td>
                })}
              </td>
            </tr>
          </div>: ''}
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
