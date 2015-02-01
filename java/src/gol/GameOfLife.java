package gol;

import java.util.*;

public class GameOfLife {
    private Set<Cell> cells;

    public void next() {
        Set<Cell> nextCells = new HashSet<Cell>();

        for (Cell cell : neighborhood()) {
            if (willLive(cell)) {
                nextCells.add(cell);
            }
        }

        cells = nextCells;
    }

    private Set<Cell> neighborhood() {
        Set<Cell> theHood = new HashSet<Cell>(cells);
        for (Cell cell : cells) {
            theHood.addAll(cell.neighbors());
        }
        return theHood;
    }

    private boolean willLive(Cell aCell) {
        int n = numLivingNeighbors(aCell);

        return (  ((n == 2) && isAlive(aCell))
                || (n == 3));
    }

    private int numLivingNeighbors(Cell aCell) {
        int nLivingNeighbors = 0;
        for (Cell neighbor : aCell.neighbors()) {
            if (isAlive(neighbor)) {
                nLivingNeighbors += 1;
            }
        }
        return nLivingNeighbors;
    }

    public int numLivingCells() {
        return cells.size();
    }

    public boolean isAlive(Cell aCell) {
        return cells.contains(aCell);
    }

    public GameOfLife(Set<Cell> cells) {
        this.cells = cells;
    }

}