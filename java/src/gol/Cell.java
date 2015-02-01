package gol;

import java.util.*;
/**
 * Created by mhanif on 1/31/15.
 */
public class Cell {
    public final int x;
    public final int y;

    public Set<Cell> neighbors() {
        Set<Cell> nbors = new HashSet<Cell>();
        int [] offsets = {-1, 0, 1};
        for (int a : offsets) {
            for (int b: offsets) {
                if (!((a == 0) && (b == 0))) {
                    nbors.add(new Cell(x+a, y+b));
                }
            }
        }
        return nbors;
    }

    public boolean equals(Object other) {
        if (other == null)
            return false;
        if (this == other)
            return true;
        Cell otherCell = (Cell)other;
        return ((otherCell.x == x) && (otherCell.y == y));
    }

    public int hashCode() {
        return 31 * ((31 * x) + y);
    }

    public String toString() {
        return "(" + x + "'" + y + ")";
    }

    public Cell(int x, int y) {
        this.x = x;
        this.y = y;
    }
}
