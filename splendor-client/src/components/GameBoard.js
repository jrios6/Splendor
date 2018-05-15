import React, { Component } from 'react';
import logo from '../logo.svg';
import Card from './Card/Card';
import Treasury from './Treasury/Treasury';
import Player from './Player/Player';
import Action from './Action/Action';
import Noble from './Noble/Noble';
import Deck from './Deck/Deck';

import '../App.css';
import './Player/Player.css';

class GameBoard extends Component {
  constructor() {
    super();
    this.updateState = this.updateState.bind(this);
    this.handleAction = this.handleAction.bind(this);
    this.state = {}
  }

  cardsAreEqual(c1, c2) {
    return c1.tier == c2.tier && c1.red == c2.red && c1.blue == c2.blue
      && c1.green == c2.green && c1.black == c2.black && c1.white == c2.white
      && c1.points == c2.points && c1.gem_type == c2.gem_type
  }

  updateState(myJson) {
    let board = JSON.parse(myJson[0]);
    let actions = JSON.parse(myJson[1]);
    let dev_cards = board['open_tier_1'].concat(board['open_tier_2'], board['open_tier_3']);
    let remaining_actions = [];
    let players = board['players'];
    let current_player = players[board['current_player']];
    let deck_1 = {tier: 1, cards: 40};
    let deck_2 = {tier: 2, cards: 40};
    let deck_3 = {tier: 3, cards: 40};

    // Add action into cards
    actions.map((action) => {
      if (action.type === "reserve_open_development") {
        for (let i=0; i < dev_cards.length; i++) {
          if (this.cardsAreEqual(dev_cards[i], action.card)) {
            dev_cards[i].reserve = action
          }
        }
      } else if (action.type === "purchase_development") {
        for (let i=0; i < dev_cards.length; i++) {
          if (this.cardsAreEqual(dev_cards[i], action.card)) {
            dev_cards[i].purchase = action;
          }
        }
        for (let i=0; i < current_player.board_reservations.length; i++) {
          if (this.cardsAreEqual(current_player.board_reservations[i], action.card)) {
            current_player.board_reservations[i].purchase = action;
          }
        }

        for (let i=0; i < current_player.deck_reservations.length; i++) {
          if (this.cardsAreEqual(current_player.deck_reservations[i], action.card)) {
            current_player.deck_reservations[i].purchase = action;
          }
        }
      } else if (action.type === "reserve_from_deck") {
        switch (action.deck_num) {
          case 0:
            deck_1.reserve = action;
            break;
          case 1:
            deck_2.reserve = action;
            break;
          case 2:
            deck_3.reserve = action;
            break;
        }
      } else {
        remaining_actions.push(action);
      }
    })

    this.setState({
      handlingAction: false,
      treasury: board['treasury'],
      leaderboard: board['leaderboard'],
      round: board['round'],
      current_player: board['current_player'],
      should_discard_coin: board['should_discard_coin'],
      nobles: board['nobles'],
      players: board['players'],
      dev_cards: dev_cards,
      actions: remaining_actions,
      deck_1: deck_1,
      deck_2: deck_2,
      deck_3: deck_3,
    })
  }

  handleAction(option) {
    if (!this.state.handlingAction) {
      this.setState({ handlingAction: true })
      fetch(`http://localhost:5000/game/${option}`, {
        method: 'GET',
      }).then((response) => response.json())
      .then((myJson) => this.updateState(myJson));
    } else {
      console.log("Please wait for server to respond")
    }
  }


  render() {
    return (
      <div className="GameBoard">
        <div className="Column1">
          <h2>Round {this.state.round}</h2>
            <h4>Nobles</h4>
          <div className="Nobles">
            {this.state.nobles? this.state.nobles.map((noble) => {
              return <div><Noble {...noble} /></div>
            }): ''}
          </div>
          {this.state.treasury? <Treasury {...this.state.treasury}/> : ''}
          <h4>Collect Coins</h4>
          <div className="Actions">
            {this.state.actions ? this.state.actions.map((action) => {
              return <tr><Action {...action} handleAction={this.handleAction}/></tr>}) : ''}
          </div>
        </div>
        <div className="players">
          {this.state.players? <div>
            <Player active={this.state.current_player == 1} {...this.state.players[1]}
              handleAction={this.handleAction} />
          </div>: ''}
          {this.state.players? <div className="board-row3">
            <Player active={this.state.current_player == 2} {...this.state.players[2]}
              handleAction={this.handleAction} />
          </div>: ''}
          {this.state.players? <div>
            <Player active={this.state.current_player == 3} {...this.state.players[3]}
              handleAction={this.handleAction} />
          </div> : ''}
        </div>
        <div className="board">
          <div className="board-row2">
            <table>
              <tr>
                <td><Deck {...this.state.deck_1} handleAction={this.handleAction}/></td>
                {this.state.dev_cards? this.state.dev_cards.map((card) => {
                  if (card.tier === 1) {
                    return <td><Card {...card} handleAction={this.handleAction}/></td>
                  }
                }): ''}
              </tr>
              <tr>
                <td><Deck {...this.state.deck_2} handleAction={this.handleAction}/></td>
                {this.state.dev_cards? this.state.dev_cards.map((card) => {
                  if (card.tier === 2) {
                    return <td><Card {...card} handleAction={this.handleAction}/></td>
                  }
                }): ''}
              </tr>
              <tr>
                <td><Deck {...this.state.deck_3} handleAction={this.handleAction}/></td>
                {this.state.dev_cards? this.state.dev_cards.map((card) => {
                  if (card.tier === 3) {
                    return <td><Card {...card} handleAction={this.handleAction}/></td>
                  }
                }): ''}
              </tr>
            </table>

          </div>
          {this.state.players? <div>
            <Player active={this.state.current_player == 0} {...this.state.players[0]}
              handleAction={this.handleAction} />
          </div>: ''}
        </div>
      </div>
    );
  }
}

export default GameBoard;
