package gol

/* 
 * Solution inspired-by/copied-from http://www.luigip.com/?p=133
 */

object GameOfLife2 {
  
  type Cell = (Int, Int)
  
  type Board = Set[Cell]
  
  /*************************************************************************
   * Game of life rules:

        1. If cell is alive and has less than 2 living neighbors it dies
        2. If cell is alive and has more than 3 living neighbors it dies
        3. If cell is alive and has either 2 or 3 living neighbors it lives
        4. If cell is dead and has exactly 3 living neighbors it lives

        This translates to:
        num living neighbors = <2 => Dead
                                2 => Alive if already Alive else Dead
                                3 => Alive
                               >3 => Dead
   *************************************************************************/
  
  def shouldLive(livingNeighborCount: Int, isAlive: Boolean): Boolean = livingNeighborCount match {
    case 3 => true
    case 2 => isAlive
    case n => false
  }
  
  def neighbors(cell: Cell): Set[Cell] = for {
      xd <- Set(-1, 0, 1)
      yd <- Set(-1, 0, 1)
      if (xd,yd) != (0,0)
    } yield (cell._1 + xd, cell._2 + yd)
  
  def nextBoard(board: Board): Board = {
    board flatMap neighbors filter { cell => 
      val livingNeighborCount = neighbors(cell) count board
      shouldLive(livingNeighborCount, board(cell))
    }
  }
  
}
