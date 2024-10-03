import React, { useState, useEffect } from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import fetchFunc from './scripts/FetchFunc';


const App = () => {
  const [enemies, setEnemies] = useState({array: []})
  const [player, setPlayer] = useState({isloaded: false})
  const [selectedMove, setSelectedMove] = useState(-1)
//enemy object



useEffect( () => {
  const getUser = async () => {
    if(!player.isloaded){
    const response = await fetchFunc('/json', "GET")
    console.log(response)
    response.isloaded = true
    setPlayer(response)
  }
  }
  getUser()
  
}, [])


const getEnemies = async () => {
  const response = await fetchFunc('/json', "POST", {player:player, task:'getEnemies'})
  console.log(response)
  setEnemies(response)
}

const takeTurn = async (targetIndex) => {
  if(selectedMove === -1){

  }else{
    const response = await fetchFunc('/json', "POST", {player:player, task:'turn', enemies:enemies, moveIndex: selectedMove, targetIndex: targetIndex })
    console.log(response)
    console.log
    setEnemies({array: response.enemies})
    setPlayer(response.player)
    setSelectedMove(-1)
  }
  
}
console.log(player.status)
let statusEffects = <div>{player.status}</div>
/**
if(player.status.length > 0){
  statusEffects = <Col> <ul>
{player.status.map((effect, index) => {
  return (<li key={index}>{effect}</li>)
})}
</ul></Col>
}
 */


let enemyRow = <Row>
                  <Col></Col>
                </Row>
console.log(enemies.array.length)
if(enemies.array.length === 0){
  enemyRow = <Row>
    <Col></Col>
    <Col>
    <div>|you are alone|</div>
    </Col>
    <Col><button onClick={(e) => {getEnemies()}}>find enemies</button></Col>
  </Row>
}else{
enemyRow = <Row>
  {enemies.array.map((enemy, index) => {
    return ( 
    <Col key={index}>
      <div>{enemy.name}</div>
      <div>{enemy.hp}</div>
      <button onClick={(e) => takeTurn(index)}>select</button>
    </Col>)
  })}
</Row>

}
let playLog = <div></div>
let playerRow = <div></div>

const showMove = () => {
  if(selectedMove == -1){
    return 'none'
  }else{
    return player.moves[selectedMove].name
  }
}
if(player.isloaded){
  console.log(player.xp, player.level)
   playerRow = <Row>

    <Col>
    <div>selected move: {showMove()}</div>
    <div id='playerlevel'>level: {player.level}</div>
    <div id='playerxp'>XP: {player.xp}</div>
    <div>xp to next level: {player.level * 10}</div>
    <div id='playerHp'>HP: {player.hp}</div>
    <div id='playerAmmo'>Ammo: {player.ammo}</div>
    </Col>
    
    {player.moves.map((move, index) => {
      return (
        <Col key={index}>
          <div className='moveName' id={index + 'move'}>{move.name}</div>
          <div className='moveDesc'>{move.description}</div>
          <button onClick={(e) => setSelectedMove(index)}>Use</button>
          </Col>)
    })}
    {statusEffects}

  </Row>
playLog =  <ul>
{player.logs.map((log, index) => {
  return (<li key={index}>{log}</li>)
})}
</ul>
}else{
  playerRow = <div>{toString(player)}</div>
}









  return (
      <Container>
          {enemyRow}
          {playerRow}
          <Row>
          <Col>
       {playLog}
    </Col>
          </Row>
      </Container>
  );
}

export default App;