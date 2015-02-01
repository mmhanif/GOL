package gol

import org.scalatest.FunSuite

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

@RunWith(classOf[JUnitRunner])
class GameOfLife2Suite extends FunSuite {

  /**
   * Import all members of the GameOfLife object.
   */ 
  import GameOfLife2._
  

  /**
   * GOL Tests
   */
  test("empty grid stays empty") {
    assert(nextBoard(Set()) === Set())
  }
  
  test("lonely cell dies") {
    val lonely = (0,0)
    assert(nextBoard(Set(lonely)) === Set())
  }
  
  test("cells with three neighbors live") {
    val state = Set((0,0), (0,1), (1,0), (1,1))
    assert(nextBoard(state) === state)
  }
  
  test("overcrowded cell dies") {
    val overcrowded = (0,0)
    val initial = Set(overcrowded, (0,1), (1,0), (0,-1), (-1,0))
    assert(!nextBoard(initial)(overcrowded))
  }
  
  test("dead cell with three living neighbors comes alive") {
    val wasDead = (0,0)
    val initial = Set((0,1), (0,-1), (-1,0))
    assert(nextBoard(initial)(wasDead))
  }
  
}
