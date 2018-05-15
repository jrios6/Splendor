import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import GameBoard from './components/GameBoard.js';

class App extends Component {
  constructor() {
    super();
    this.handleSubmit = this.handleSubmit.bind(this);
    this.state = {
      player1: 'player1',
      player2: 'player2',
      player3: 'player3',
      player4: 'player4',
    }
  }

  handleSubmit(event) {
    event.preventDefault();

    let payload = {
      'player1': this.state.player1,
      'player2': this.state.player2,
      'player3': this.state.player3,
      'player4': this.state.player4,
    };

    let data = new FormData();
    data.append( "json", JSON.stringify( payload ) );

    fetch('http://localhost:5000/start', {
      method: 'POST',
      body: data,
    }).then((response) => response.json())
    .then((myJson) => this.refs.board.updateState(myJson));
  }

  onChange = (e) => {
        const state = this.state
        state[e.target.name] = e.target.value;
        this.setState(state);
      }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Welcome to Splendor</h1>
          <form onSubmit={this.handleSubmit}>
            <input type="text" name="player1" value={this.state.player1} onChange={this.onChange} />
            <input type="text" name="player2" value={this.state.player2} onChange={this.onChange} />
            <input type="text" name="player3" value={this.state.player3} onChange={this.onChange} />
            <input type="text" name="player4" value={this.state.player4} onChange={this.onChange} />
            <input type="submit" value="Start" />
          </form>
        </header>
        <GameBoard ref="board" />
      </div>
    );
  }
}

export default App;
