package gol

object GameOfLife {
  
  type Cell = (Int, Int)
  
  type Board = List[Cell]
  
  type CellStatus = (Cell, Boolean, Int)
  
  type BoardStatus = List[CellStatus]

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
  
  def neighbors(cell: Cell): List[Cell] = {
    (for {
      xd <- (-1 to 1)
      yd <- (-1 to 1)
      x = cell._1 + xd
      y = cell._2 + yd
      if (x,y) != cell
    } yield (x, y)).toList
  }
  
  def isAlive(cell: Cell, board: Board): Boolean = board.contains(cell)
    
  def allCellsWithNeighborStatus(board: Board): List[(Cell, Cell, Boolean)] = {
    for {
      cell <- board
      nbr <- neighbors(cell)
      nbrIsAlive = isAlive(nbr, board)
    } yield (cell, nbr, nbrIsAlive)
  }
  
  def countLiveNeighbors(cellNbrFlags: List[(Cell, Cell, Boolean)]): BoardStatus = {
    
	  def updateCellStatus(boardStatus: BoardStatus, ACell: Cell, alive: Boolean): BoardStatus = boardStatus match {
	    case Nil                        => List((ACell, alive, 1))
	    case (ACell, flag, count) :: xs => (ACell, flag, count+1) :: xs
	    case x :: xs                    => x :: updateCellStatus(xs, ACell, alive)
	  }
	  
	  def updateBoardStatus(boardStatus: BoardStatus, cellNbrFlag: (Cell, Cell, Boolean)): BoardStatus = cellNbrFlag match {
	    case (cell, _, true) => updateCellStatus(boardStatus, cell, true)
	    case (_, nbr, false) => updateCellStatus(boardStatus, nbr, false)
	  }
      
    val initCount: List[CellStatus] = List()
    cellNbrFlags.foldLeft(initCount){ (boardStatus, cellNbrFlag) => updateBoardStatus(boardStatus, cellNbrFlag) }
  }
  
  def cellsAndNeighborsWithCounts(board: Board): BoardStatus = countLiveNeighbors(allCellsWithNeighborStatus(board))
     
  def nextBoard(initialBoard: Board): Board = {
    for {
      (cell, alive, count) <- cellsAndNeighborsWithCounts(initialBoard)
      if shouldLive(count, alive)
    } yield (cell)
  }
  
}
