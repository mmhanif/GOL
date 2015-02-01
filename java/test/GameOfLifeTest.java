package gol;

import org.junit.*;
import static org.junit.Assert.*;
import static org.hamcrest.CoreMatchers.*;
import java.util.*;

public class GameOfLifeTest {

    @Test
    public void emptyGridStaysEmpty() {
        Set<Cell> cells = new HashSet<Cell>();
        GameOfLife game = new GameOfLife(cells);
        game.next();
        assertThat(game.numLivingCells(), equalTo(0));
    }

    @Test
    public void cellWithNoNeighborsDies() {
        Cell singleCell = new Cell(0,0);
        Set<Cell> cells = new HashSet<Cell>();
        cells.add(singleCell);

        GameOfLife game = new GameOfLife(cells);
        game.next();

        assertFalse(game.isAlive(singleCell));
    }

    @Test
    public void cellWithOneNeighborDies() {
        Cell first = new Cell(0,0);
        Cell second = new Cell(0,1);
        Set<Cell> cells = new HashSet<Cell>();
        cells.add(first);
        cells.add(second);

        GameOfLife game = new GameOfLife(cells);
        game.next();

        assertFalse(game.isAlive(first));
        assertFalse(game.isAlive(second));
    }

    @Test
    public void cellWithTwoOrThreeNeighborsLives() {
        // x x x       x x
        // x       ->  x
        Cell firstWith2N = new Cell(0,0);
        Cell secondWith2N = new Cell(1,0);
        Cell thirdWith3N = new Cell(0,1);
        Cell fourthWith1N = new Cell(0,2);
        Set<Cell> cells = new HashSet<Cell>();
        cells.add(firstWith2N);
        cells.add(secondWith2N);
        cells.add(thirdWith3N);
        cells.add(fourthWith1N);

        GameOfLife game = new GameOfLife(cells);
        game.next();

        assertTrue(game.isAlive(firstWith2N));
        assertTrue(game.isAlive(secondWith2N));
        assertTrue(game.isAlive(thirdWith3N));
        assertFalse(game.isAlive(fourthWith1N));
    }

    @Test
    public void deadCellWithExactlyThreeLivingNeighborsLives() {
        // x x         x x
        // x       ->  x X
        Cell first = new Cell(0,0);
        Cell second = new Cell(1,0);
        Cell third = new Cell(0,1);
        Cell lazarus = new Cell(1,1);
        Set<Cell> cells = new HashSet<Cell>();
        cells.add(first);
        cells.add(second);
        cells.add(third);

        GameOfLife game = new GameOfLife(cells);
        game.next();

        assertTrue(game.isAlive(lazarus));
    }

}