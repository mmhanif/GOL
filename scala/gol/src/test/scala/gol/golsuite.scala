package gol

import org.scalatest.FunSuite

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

@RunWith(classOf[JUnitRunner])
class GameOfLifeSuite extends FunSuite {

  /**
   * Import all members of the GameOfLife object.
   */ 
  import GameOfLife._
  

  /**
   * GOL Tests
   */
  test("empty grid stays empty") {
    assert(nextBoard(List()) === List())
  }
  
  test("lonely cell dies") {
    val lonely = (0,0)
    assert(nextBoard(List(lonely)) === List())
  }
  
  test("cells with three neighbors live") {
    val state = List((0,0), (0,1), (1,0), (1,1))
    assert(nextBoard(state) === state)
  }
  
  test("overcrowded cell dies") {
    val overcrowded = (0,0)
    val initial = List(overcrowded, (0,1), (1,0), (0,-1), (-1,0))
    assert(!nextBoard(initial).contains(overcrowded))
  }
  
  test("dead cell with three living neighbors comes alive") {
    val wasDead = (0,0)
    val initial = List((0,1), (0,-1), (-1,0))
    assert(nextBoard(initial).contains(wasDead))
  }
  
}
