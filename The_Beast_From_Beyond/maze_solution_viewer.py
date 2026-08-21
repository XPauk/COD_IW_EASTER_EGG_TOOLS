#https://mmmrkennedy.com/games/IW/the_beast_from_beyond/the_beast_from_beyond_guide
#https://steamcommunity.com/sharedfiles/filedetails/?id=2998590075

import io
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

try:
    import cairosvg
    from PIL import Image, ImageTk
    SVG_SUPPORT = True
except Exception as e:
    print(f"SVG-Unterstützung deaktiviert: {e}")
    SVG_SUPPORT = False

# ------------------------------------------------------------
# Coordinate system
# ------------------------------------------------------------
# Every field is addressed as (row, column).
# Both values start at 0:
#
#   (0, 0) = top left
#   (0, 5) = top right
#   (5, 0) = bottom left
#   (5, 5) = bottom right
#
# Example:
#   (2, 4) means row 3, column 5.
#
# A wall is stored between two directly adjacent fields:
#   ((0, 0), (0, 1)) = vertical wall between these fields
#   ((0, 0), (1, 0)) = horizontal wall between these fields
#
# The order does not matter. The normalize_edge() function sorts it.
# ------------------------------------------------------------

Cell = Tuple[int, int]
Edge = Tuple[Cell, Cell]


def normalize_edge(a: Cell, b: Cell) -> Edge:
    """Return an edge in a stable order."""
    return tuple(sorted((a, b)))  # type: ignore[return-value]


@dataclass(frozen=True)
class MazeSolution:
    path: List[Cell]
    walls: Set[Edge]
    name: str = ""


def make_walls(*pairs: Tuple[Cell, Cell]) -> Set[Edge]:
    """Convenience function for defining walls."""
    return {normalize_edge(a, b) for a, b in pairs}


# ------------------------------------------------------------
# SOLUTIONS
# ------------------------------------------------------------
# Key:
#   ((start_row, start_column), (end_row, end_column))
#
# Value:
#   MazeSolution(
#       path=[all fields of the route in order],
#       walls=make_walls(all barriers),
#       name="optional description"
#   )
#
# IMPORTANT:
# Consecutive path fields must touch horizontally or vertically.
# Diagonal steps are not allowed.
#
# These are demonstration solutions only. Replace or extend them
# with the real solutions from the game.
# ------------------------------------------------------------

SOLUTIONS: Dict[Tuple[Cell, Cell], MazeSolution] = {
    ((1, 4), (5, 0)): MazeSolution(
            name="Maze 1",
            path=[
                (1, 4), (1, 3), (2, 3), (2, 4), (2, 5),
                (3, 5), (3, 4), (3, 3), (4, 3), (4, 4), (5, 4),
                (5, 3), (5, 2), (5, 1), (5, 0)
            ],
            walls=make_walls(
                ((0, 1), (1, 1)),
                ((0, 2), (1, 2)),
                ((0, 3), (1, 3)),
                ((0, 4), (1, 4)),

                ((1, 2), (1, 3)),
                ((1, 4), (1, 5)),

                ((1, 0), (2, 0)),
                ((1, 1), (2, 1)),
                ((1, 4), (2, 4)),
                ((1, 5), (2, 5)),

                ((2, 1), (2, 2)),
                ((2, 2), (2, 3)),

                ((2, 3), (3, 3)),
                ((2, 4), (3, 4)),

                ((3, 0), (3, 1)),
                ((3, 1), (3, 2)),
                ((3, 2), (3, 3)),

                ((3, 4), (4, 4)),

                ((4, 0), (4, 1)),
                ((4, 2), (4, 3)),
                ((4, 4), (4, 5)),

                ((4, 1), (5, 1)),
                ((4, 2), (5, 2)),
                ((4, 3), (5, 3)),

                ((5, 4), (5, 5)),
            ),
        ),
    ((1, 1), (4, 3)): MazeSolution(
                name="Maze 2",
                path=[
                    (1, 1), (2, 1), (2, 2), (3, 2), (3, 1),
                    (4, 1), (4, 2), (5, 2), (5, 3), (5, 4), (5, 5),
                    (4, 5), (4, 4), (4, 3)
                ],
                walls=make_walls(
                    ((0, 1), (1, 1)),
                    ((0, 3), (1, 3)),
                    ((0, 4), (1, 4)),
    
                    ((1, 0), (1, 1)),
                    ((1, 2), (1, 3)),

                    ((1, 2), (2, 2)),
                    ((1, 3), (2, 3)),
                    ((1, 5), (2, 5)),

                    ((2, 0), (2, 1)),
                    ((2, 2), (2, 3)),
                    ((2, 3), (2, 4)),
                    ((2, 4), (2, 5)),

                    ((2, 1), (3, 1)),

                    ((3, 0), (3, 1)),
                    ((3, 2), (3, 3)),
                    ((3, 3), (3, 4)),

                    ((3, 2), (4, 2)),
                    ((3, 4), (4, 4)),
                    ((3, 5), (4, 5)),

                    ((4, 0), (4, 1)),
                    ((4, 2), (4, 3)),

                    ((4, 1), (5, 1)),
                    ((4, 3), (5, 3)),
                    ((4, 4), (5, 4)),

                    ((5, 1), (5, 2)),
                ),
            ),
    ((3, 1), (0, 4)): MazeSolution(
                    name="Maze 3",
                    path=[
                        (3, 1), (2, 1), (1, 1), (1, 2), (2, 2),
                        (2, 3), (1, 3), (1, 4), (2, 4), (2, 5), (1, 5),
                        (0, 5), (0, 4)
                    ],
                    walls=make_walls(
                        ((0, 1), (1, 1)),
                        ((0, 2), (1, 2)),
                        ((0, 3), (1, 3)),
                        ((0, 4), (1, 4)),
        
                        ((1, 0), (1, 1)),
                        ((1, 2), (1, 3)),
                        ((1, 4), (1, 5)),
    
                        ((2, 0), (2, 1)),
                        ((2, 1), (2, 2)),
                        ((2, 3), (2, 4)),

                        ((2, 0), (3, 0)),
                        ((2, 2), (3, 2)),
                        ((2, 3), (3, 3)),
                        ((2, 4), (3, 4)),

                        ((3, 0), (3, 1)),
                        ((3, 1), (3, 2)),
                        ((3, 3), (3, 4)),
                        ((3, 4), (3, 5)),

                        ((3, 1), (4, 1)),
                        ((3, 2), (4, 2)),

                        ((4, 1), (4, 2)),
                        ((4, 3), (4, 4)),

                        ((4, 0), (5, 0)),
                        ((4, 3), (5, 3)),
                        ((4, 5), (5, 5)),

                        ((5, 2), (5, 3)),
                    ),
                ),
    ((4, 5), (3, 3)): MazeSolution(
                        name="Maze 4",
                        path=[
                            (4, 5), (3, 5), (2, 5), (1, 5), (1, 4),
                            (2, 4), (2, 3), (2, 2), (3, 2), (3, 3)
                        ],
                        walls=make_walls(
                            ((0, 1), (1, 1)),
                            ((0, 4), (1, 4)),
                            ((0, 5), (1, 5)),
            
                            ((1, 1), (1, 2)),
                            ((1, 2), (1, 3)),
                            ((1, 3), (1, 4)),
        
                            ((1, 0), (2, 0)),
                            ((1, 1), (2, 1)),
                            ((1, 3), (2, 3)),
    
                            ((2, 1), (2, 2)),
                            ((2, 4), (2, 5)),

                            ((2, 1), (3, 1)),
                            ((2, 3), (3, 3)),
                            ((2, 4), (3, 4)),

                            ((3, 0), (3, 1)),
                            ((3, 3), (3, 4)),

                            ((3, 1), (4, 1)),
                            ((3, 2), (4, 2)),
                            ((3, 3), (4, 3)),

                            ((4, 0), (4, 1)),
                            ((4, 4), (4, 5)),

                            ((4, 2), (5, 2)),
                            ((4, 3), (5, 3)),
                            ((4, 4), (5, 4)),

                            ((5, 1), (5, 2)),
                        ),
                    ),
    ((3, 2), (4, 1)): MazeSolution(
                            name="Maze 5",
                            path=[
                                (3, 2), (3, 3), (2, 3), (2, 2), (2, 1),
                                (1, 1), (1, 2), (0, 2), (0, 1), (0, 0),
                                (1, 0), (2, 0), (3, 0), (4, 0), (4, 1)
                            ],
                            walls=make_walls(
                                ((0, 2), (0, 3)),
                                ((0, 3), (0, 4)),

                                ((0, 1), (1, 1)),
                                ((0, 4), (1, 4)),

                                ((1, 0), (1, 1)),
                                ((1, 2), (1, 3)),
                                ((1, 4), (1, 5)),

                                ((1, 2), (2, 2)),
                                ((1, 3), (2, 3)),

                                ((2, 0), (2, 1)),
                                ((2, 4), (2, 5)),

                                ((2, 1), (3, 1)),
                                ((2, 2), (3, 2)),
                                ((2, 4), (3, 4)),

                                ((3, 0), (3, 1)),
                                ((3, 3), (3, 4)),

                                ((3, 1), (4, 1)),
                                ((3, 2), (4, 2)),
                                ((3, 3), (4, 3)),
                                ((3, 5), (4, 5)),

                                ((4, 4), (4, 5)),

                                ((4, 1), (5, 1)),
                                ((4, 2), (5, 2)),
                                ((4, 3), (5, 3)),
                                ((4, 4), (5, 4)),
                            ),
                        ),
    ((4, 4), (2, 2)): MazeSolution(
                            name="Maze 6",
                            path=[
                                (4, 4), (4, 3), (5, 3), (5, 2), (5, 1),
                                (5, 0), (4, 0), (3, 0), (2, 0), (2, 1),
                                (2, 2)
                            ],
                            walls=make_walls(
                                ((0, 1), (1, 1)),
                                ((0, 2), (1, 2)),
                                ((0, 3), (1, 3)),
                                ((0, 4), (1, 4)),
                                ((0, 5), (1, 5)),

                                ((1, 0), (1, 1)),

                                ((1, 1), (2, 1)),
                                ((1, 2), (2, 2)),
                                ((1, 3), (2, 3)),
                                ((1, 4), (2, 4)),

                                ((2, 4), (2, 5)),

                                ((2, 1), (3, 1)),
                                ((2, 2), (3, 2)),
                                ((2, 4), (3, 4)),

                                ((3, 0), (3, 1)),
                                ((3, 3), (3, 4)),

                                ((3, 1), (4, 1)),
                                ((3, 2), (4, 2)),
                                ((3, 3), (4, 3)),
                                ((3, 5), (4, 5)),

                                ((4, 2), (4, 3)),
                                ((4, 4), (4, 5)),

                                ((4, 4), (5, 4))
                            ),
                        ),
    ((3, 1), (1, 2)): MazeSolution(
                            name="Maze 7",
                            path=[
                                (3, 1), (4, 1), (4, 2), (5, 2), (5, 3),
                                (4, 3), (4, 4), (3, 4), (3, 5), (2, 5),
                                (2, 4), (2, 3), (3, 3), (3, 2), (2, 2),
                                (2, 1), (1, 1), (1, 2)
                            ],
                            walls=make_walls(
                                ((0, 4), (0, 5)),

                                ((0, 1), (1, 1)),
                                ((0, 2), (1, 2)),
                                ((0, 3), (1, 3)),

                                ((1, 0), (1, 1)),
                                ((1, 4), (1, 5)),

                                ((1, 2), (2, 2)),
                                ((1, 3), (2, 3)),
                                ((1, 4), (2, 4)),

                                ((2, 0), (2, 1)),
                                ((2, 2), (2, 3)),

                                ((2, 1), (3, 1)),
                                ((2, 4), (3, 4)),

                                ((3, 0), (3, 1)),
                                ((3, 1), (3, 2)),
                                ((3, 3), (3, 4)),

                                ((3, 0), (4, 0)),
                                ((3, 2), (4, 2)),
                                ((3, 3), (4, 3)),
                                ((3, 5), (4, 5)),

                                ((4, 2), (4, 3)),
                                ((4, 4), (4, 5)),

                                ((4, 1), (5, 1)),
                                ((4, 4), (5, 4)),

                                ((5, 1), (5, 2)),
                            ),
                        ),
    ((3, 4), (2, 1)): MazeSolution(
                            name="Maze 8",
                            path=[
                                (3, 4), (3, 5), (4, 5), (5, 5), (5, 4),
                                (5, 3), (5, 2), (5, 1), (4, 1), (4, 2),
                                (3, 2), (2, 2), (2, 1)
                            ],
                            walls=make_walls(
                                ((0, 2), (0, 3)),

                                ((0, 0), (1, 0)),
                                ((0, 4), (1, 4)),

                                ((1, 1), (1, 2)),
                                ((1, 2), (1, 3)),
                                ((1, 3), (1, 4)),
                                ((1, 4), (1, 5)),

                                ((1, 2), (2, 2)),
                                ((1, 3), (2, 3)),

                                ((2, 2), (2, 3)),

                                ((2, 1), (3, 1)),
                                ((2, 4), (3, 4)),
                                ((2, 5), (3, 5)),

                                ((3, 1), (3, 2)),
                                ((3, 2), (3, 3)),
                                ((3, 3), (3, 4)),

                                ((3, 1), (4, 1)),
                                ((3, 4), (4, 4)),

                                ((4, 0), (4, 1)),
                                ((4, 2), (4, 3)),

                                ((4, 2), (5, 2)),
                                ((4, 3), (5, 3)),
                                ((4, 4), (5, 4)),

                                ((5, 0), (5, 1))
                            ),
                        ),
    ((1, 2), (5, 3)): MazeSolution(
                            name="Maze 9",
                            path=[
                                (1, 2), (0, 2), (0, 3), (0, 4), (0, 5),
                                (1, 5), (1, 4), (1, 3), (2, 3), (2, 2),
                                (3, 2), (3, 3), (4, 3), (4, 4), (5, 4),
                                (5, 3)
                            ],
                            walls=make_walls(
                                ((0, 1), (1, 1)),
                                ((0, 3), (1, 3)),
                                ((0, 4), (1, 4)),

                                ((1, 0), (1, 1)),
                                ((1, 2), (1, 3)),

                                ((1, 2), (2, 2)),
                                ((1, 4), (2, 4)),
                                ((1, 5), (2, 5)),

                                ((2, 0), (2, 1)),
                                ((2, 1), (2, 2)),
                                ((2, 3), (2, 4)),

                                ((2, 3), (3, 3)),

                                ((3, 0), (3, 1)),
                                ((3, 1), (3, 2)),
                                ((3, 3), (3, 4)),
                                ((3, 4), (3, 5)),

                                ((3, 2), (4, 2)),
                                ((3, 4), (4, 4)),

                                ((4, 0), (4, 1)),
                                ((4, 2), (4, 3)),
                                ((4, 4), (4, 5)),

                                ((4, 0), (5, 0)),
                                ((4, 1), (5, 1)),
                                ((4, 3), (5, 3)),

                                ((5, 2), (5, 3))
                            ),
                        ),
    ((1, 2), (4, 4)): MazeSolution(
                            name="Maze 10",
                            path=[
                                (1, 2), (2, 2), (2, 1), (1, 1), (1, 0),
                                (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                                (1, 4), (1, 5), (2, 5), (3, 5), (4, 5),
                                (4, 4)
                            ],
                            walls=make_walls(
                                ((0, 1), (1, 1)),
                                ((0, 2), (1, 2)),
                                ((0, 3), (1, 3)),
                                ((0, 5), (1, 5)),

                                ((1, 1), (1, 2)),
                                ((1, 3), (1, 4)),

                                ((1, 0), (2, 0)),
                                ((1, 4), (2, 4)),

                                ((2, 0), (2, 1)),
                                ((2, 2), (2, 3)),
                                ((2, 4), (2, 5)),

                                ((2, 1), (3, 1)),
                                ((2, 2), (3, 2)),
                                ((2, 3), (3, 3)),

                                ((3, 4), (3, 5)),

                                ((3, 1), (4, 1)),
                                ((3, 2), (4, 2)),
                                ((3, 3), (4, 3)),
                                ((3, 4), (4, 4)),

                                ((4, 0), (4, 1)),
                                ((4, 3), (4, 4)),

                                ((4, 2), (5, 2)),
                                ((4, 3), (5, 3)),

                                ((5, 1), (5, 2)),
                                ((5, 4), (5, 5))
                            ),
                        ),
    ((2, 0), (2, 3)): MazeSolution(
                            name="Maze 11",
                            path=[
                                (2, 0), (1, 0), (0, 0), (0, 1), (0, 2),
                                (0, 3), (0, 4), (0, 5), (1, 5), (2, 5),
                                (2, 4), (1, 4), (1, 3), (1, 2), (2, 2),
                                (3, 2), (3, 3), (2, 3)
                            ],
                            walls=make_walls(
                                ((0, 1), (1, 1)),
                                ((0, 2), (1, 2)),
                                ((0, 3), (1, 3)),
                                ((0, 4), (1, 4)),

                                ((1, 0), (1, 1)),
                                ((1, 4), (1, 5)),

                                ((1, 1), (2, 1)),
                                ((1, 3), (2, 3)),

                                ((2, 1), (2, 2)),
                                ((2, 2), (2, 3)),
                                ((2, 3), (2, 4)),

                                ((2, 4), (3, 4)),
                                ((2, 5), (3, 5)),

                                ((3, 0), (3, 1)),
                                ((3, 1), (3, 2)),
                                ((3, 4), (3, 5)),

                                ((3, 0), (4, 0)),
                                ((3, 2), (4, 2)),
                                ((3, 3), (4, 3)),

                                ((4, 1), (4, 2)),
                                ((4, 3), (4, 4)),
                                ((4, 4), (4, 5)),

                                ((4, 1), (5, 1)),
                                ((4, 3), (5, 3)),

                                ((5, 2), (5, 3))
                            ),
                        ),
    ((0, 4), (4, 2)): MazeSolution(
                            name="Maze 12",
                            path=[
                                (0, 4), (0, 5), (1, 5), (1, 4), (1, 3),
                                (0, 3), (0, 2), (0, 1), (0, 0), (1, 0),
                                (2, 0), (3, 0), (4, 0), (5, 0), (5, 1),
                                (5, 2), (4, 2)
                            ],
                            walls=make_walls(
                                ((0, 3), (0, 4)),

                                ((0, 1), (1, 1)),
                                ((0, 4), (1, 4)),

                                ((1, 0), (1, 1)),
                                ((1, 2), (1, 3)),

                                ((1, 2), (2, 2)),
                                ((1, 3), (2, 3)),
                                ((1, 4), (2, 4)),
                                ((1, 5), (2, 5)),

                                ((2, 0), (2, 1)),
                                ((2, 2), (2, 3)),

                                ((2, 1), (3, 1)),
                                ((2, 4), (3, 4)),

                                ((3, 0), (3, 1)),
                                ((3, 1), (3, 2)),
                                ((3, 4), (3, 5)),

                                ((3, 2), (4, 2)),
                                ((3, 3), (4, 3)),
                                ((3, 4), (4, 4)),

                                ((4, 0), (4, 1)),
                                ((4, 2), (4, 3)),
                                ((4, 4), (4, 5)),

                                ((4, 1), (5, 1)),
                                ((4, 4), (5, 4)),

                                ((5, 2), (5, 3))
                            ),
                        ),
    ((0, 5), (3, 4)): MazeSolution(
                            name="Maze 13",
                            path=[
                                (0, 5), (0, 4), (1, 4), (1, 5), (2, 5),
                                (3, 5), (4, 5), (5, 5), (5, 4), (5, 3),
                                (5, 2), (5, 1), (4, 1), (4, 2), (4, 3),
                                (3, 3), (3, 4)
                            ],
                            walls=make_walls(
                                ((0, 2), (0, 3)),

                                ((0, 1), (1, 1)),
                                ((0, 5), (1, 5)),

                                ((1, 0), (1, 1)),
                                ((1, 2), (1, 3)),
                                ((1, 3), (1, 4)),

                                ((1, 2), (2, 2)),
                                ((1, 4), (2, 4)),

                                ((2, 0), (2, 1)),
                                ((2, 1), (2, 2)),
                                ((2, 4), (2, 5)),

                                ((2, 3), (3, 3)),
                                ((2, 4), (3, 4)),

                                ((3, 0), (3, 1)),
                                ((3, 2), (3, 3)),
                                ((3, 4), (3, 5)),

                                ((3, 1), (4, 1)),
                                ((3, 2), (4, 2)),
                                ((3, 4), (4, 4)),

                                ((4, 0), (4, 1)),
                                ((4, 3), (4, 4)),

                                ((4, 2), (5, 2)),
                                ((4, 3), (5, 3)),
                                ((4, 4), (5, 4)),

                                ((5, 0), (5, 1)),
                            ),
                        ),
    ((0, 5), (4, 0)): MazeSolution(
                            name="Maze 14",
                            path=[
                                (0, 5), (0, 4), (1, 4), (1, 3), (1, 2),
                                (0, 2), (0, 1), (1, 1), (2, 1), (2, 2),
                                (2, 3), (3, 3), (4, 3), (4, 2), (4, 1),
                                (4, 0)
                            ],
                            walls=make_walls(
                                ((0, 0), (0, 1)),
                                ((0, 3), (0, 4)),

                                ((0, 3), (1, 3)),

                                ((1, 0), (1, 1)),
                                ((1, 1), (1, 2)),
                                ((1, 4), (1, 5)),

                                ((1, 2), (2, 2)),
                                ((1, 3), (2, 3)),
                                ((1, 4), (2, 4)),

                                ((2, 0), (2, 1)),
                                ((2, 3), (2, 4)),

                                ((2, 1), (3, 1)),
                                ((2, 2), (3, 2)),
                                ((2, 5), (3, 5)),

                                ((3, 2), (3, 3)),
                                ((3, 3), (3, 4)),
                                ((3, 4), (3, 5)),

                                ((3, 1), (4, 1)),
                                ((3, 2), (4, 2)),
                                ((3, 4), (4, 4)),

                                ((4, 3), (4, 4)),

                                ((4, 1), (5, 1)),
                                ((4, 2), (5, 2)),
                                ((4, 3), (5, 3)),

                                ((5, 4), (5, 5))
                            ),
                        ),
    ((0, 1), (5, 3)): MazeSolution(
                            name="Maze 15",
                            path=[
                                (0, 1), (0, 0), (1, 0), (1, 1), (2, 1),
                                (3, 1), (3, 2), (2, 2), (2, 3), (3, 3),
                                (4, 3), (5, 3)
                            ],
                            walls=make_walls(
                                ((0, 2), (0, 3)),

                                ((0, 1), (1, 1)),
                                ((0, 4), (1, 4)),

                                ((1, 1), (1, 2)),
                                ((1, 2), (1, 3)),
                                ((1, 3), (1, 4)),

                                ((1, 0), (2, 0)),
                                ((1, 2), (2, 2)),
                                ((1, 3), (2, 3)),
                                ((1, 5), (2, 5)),

                                ((2, 0), (2, 1)),
                                ((2, 1), (2, 2)),
                                ((2, 3), (2, 4)),

                                ((2, 4), (3, 4)),

                                ((3, 0), (3, 1)),
                                ((3, 2), (3, 3)),
                                ((3, 3), (3, 4)),

                                ((3, 1), (4, 1)),
                                ((3, 2), (4, 2)),

                                ((4, 2), (4, 3)),
                                ((4, 3), (4, 4)),

                                ((4, 2), (5, 2)),

                                ((5, 0), (5, 1))
                            ),
                        ),
    # ((1, 3), (4, 4)): MazeSolution(
    #                         name="Maze 16",
    #                         path=[
    #                             (1, 3), (0, 0), (1, 0), (1, 1), (2, 1),
    #                             (3, 1), (3, 2), (2, 2), (2, 3), (3, 3),
    #                             (4, 3), (5, 3)
    #                         ],
    #                         walls=make_walls(
    #                             ((0, 2), (0, 3)),


    #                         ),
    #                     ),
}


class MazeApp:
    GRID_SIZE = 6
    CELL_SIZE = 82
    MARGIN = 28

    BACKGROUND = "#16181d"
    GRID_COLOR = "#737984"
    WALL_COLOR = "#f2f2f2"
    PATH_COLOR = "#34c6eb"
    START_COLOR = "#50d890"
    END_COLOR = "#ff6262"
    CELL_COLOR = "#252932"
    TEXT_COLOR = "#f5f5f5"
    MUTED_TEXT = "#b6bbc5"

    # Put these four files in the same folder as this Python file.
    DIRECTION_SVG_FILES = {
        "left": "d-left.svg",
        "up": "d-up.svg",
        "right": "d-right.svg",
        "down": "d-down.svg",
    }

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Maze Solution Viewer")
        self.root.configure(bg=self.BACKGROUND)
        self.root.resizable(False, False)

        self.start: Optional[Cell] = None
        self.end: Optional[Cell] = None
        self.selection_mode = tk.StringVar(value="start")
        self.show_coordinates = tk.BooleanVar(value=True)
        self.direction_images: Dict[str, object] = {}

        self._build_ui()
        self._load_direction_images()
        self._validate_all_solutions()
        self.draw()

    def _build_ui(self) -> None:
        header = tk.Frame(self.root, bg=self.BACKGROUND)
        header.pack(fill="x", padx=18, pady=(16, 8))

        tk.Label(
            header,
            text="Maze Solution Viewer",
            font=("Segoe UI", 18, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BACKGROUND,
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Choose Start or End, then click a field.",
            font=("Segoe UI", 10),
            fg=self.MUTED_TEXT,
            bg=self.BACKGROUND,
        ).pack(anchor="w", pady=(2, 0))

        controls = tk.Frame(self.root, bg=self.BACKGROUND)
        controls.pack(fill="x", padx=18, pady=(0, 10))

        tk.Radiobutton(
            controls,
            text="Place start",
            variable=self.selection_mode,
            value="start",
            font=("Segoe UI", 10),
            fg=self.TEXT_COLOR,
            bg=self.BACKGROUND,
            activebackground=self.BACKGROUND,
            activeforeground=self.TEXT_COLOR,
            selectcolor="#303641",
        ).pack(side="left")

        tk.Radiobutton(
            controls,
            text="Place end",
            variable=self.selection_mode,
            value="end",
            font=("Segoe UI", 10),
            fg=self.TEXT_COLOR,
            bg=self.BACKGROUND,
            activebackground=self.BACKGROUND,
            activeforeground=self.TEXT_COLOR,
            selectcolor="#303641",
        ).pack(side="left", padx=(14, 0))

        tk.Checkbutton(
            controls,
            text="Show coordinates",
            variable=self.show_coordinates,
            command=self.draw,
            font=("Segoe UI", 10),
            fg=self.TEXT_COLOR,
            bg=self.BACKGROUND,
            activebackground=self.BACKGROUND,
            activeforeground=self.TEXT_COLOR,
            selectcolor="#303641",
        ).pack(side="left", padx=(18, 0))

        tk.Button(
            controls,
            text="Reset",
            command=self.reset,
            font=("Segoe UI", 10),
            padx=12,
        ).pack(side="right")

        canvas_size = self.MARGIN * 2 + self.CELL_SIZE * self.GRID_SIZE
        self.canvas = tk.Canvas(
            self.root,
            width=canvas_size,
            height=canvas_size,
            bg=self.BACKGROUND,
            highlightthickness=0,
        )
        self.canvas.pack(padx=18)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.steps_title = tk.Label(
            self.root,
            text="Button sequence",
            font=("Segoe UI", 11, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BACKGROUND,
        )

        self.steps_frame = tk.Frame(
            self.root,
            bg=self.BACKGROUND,
        )

        self.status = tk.Label(
            self.root,
            text="Select a start and an end field.",
            font=("Segoe UI", 10),
            fg=self.MUTED_TEXT,
            bg=self.BACKGROUND,
            anchor="w",
        )
        self.status.pack(fill="x", padx=20, pady=(8, 16))

    def on_canvas_click(self, event: tk.Event) -> None:
        column = (event.x - self.MARGIN) // self.CELL_SIZE
        row = (event.y - self.MARGIN) // self.CELL_SIZE

        if not (0 <= row < self.GRID_SIZE and 0 <= column < self.GRID_SIZE):
            return

        cell = (int(row), int(column))

        if self.selection_mode.get() == "start":
            self.start = cell
            if self.end == cell:
                self.end = None
            self.selection_mode.set("end")
        else:
            self.end = cell
            if self.start == cell:
                self.start = None
            self.selection_mode.set("start")

        self.draw()

    def reset(self) -> None:
        self.start = None
        self.end = None
        self.selection_mode.set("start")
        self.draw()

    def get_solution(self) -> Optional[MazeSolution]:
        if self.start is None or self.end is None:
            return None

        return SOLUTIONS.get((self.start, self.end))

    def draw(self) -> None:
        self.canvas.delete("all")

        solution = self.get_solution()
        path = solution.path if solution else []
        walls = solution.walls if solution else set()

        self._draw_cells(path)
        self._draw_path(path)
        self._draw_grid()
        self._draw_walls(walls)
        self._draw_markers()
        self._draw_button_sequence(path)

        if self.start is None or self.end is None:
            self.status.config(text="Select a start and an end field.")
        elif solution:
            label = f"Solution found: {solution.name}" if solution.name else "Solution found."
            self.status.config(
                text=f"{label}  |  Start: {self.pretty_cell(self.start)}  "
                     f"End: {self.pretty_cell(self.end)}  |  "
                     f"Steps: {max(0, len(solution.path) - 1)}"
            )
        else:
            self.status.config(
                text=(
                    f"No stored solution for Start {self.pretty_cell(self.start)} "
                    f"and End {self.pretty_cell(self.end)}."
                )
            )

    def _load_direction_images(self) -> None:
        """Load and convert the four SVG files, when SVG support is installed."""
        if not SVG_SUPPORT:
            return

        script_folder = Path(__file__).resolve().parent

        for direction, filename in self.DIRECTION_SVG_FILES.items():
            svg_path = script_folder / filename
            if not svg_path.exists():
                continue

            try:
                png_data = cairosvg.svg2png(
                    url=str(svg_path),
                    output_width=46,
                    output_height=46,
                )
                image = Image.open(io.BytesIO(png_data)).convert("RGBA")
                self.direction_images[direction] = ImageTk.PhotoImage(image)
            except Exception:
                # A broken or unsupported SVG should not stop the program.
                continue

    def _path_to_directions(self, path: List[Cell]) -> List[str]:
        """Convert consecutive path cells into left/up/right/down."""
        directions: List[str] = []

        for current, following in zip(path, path[1:]):
            row_change = following[0] - current[0]
            column_change = following[1] - current[1]

            if row_change == 0 and column_change == -1:
                directions.append("left")
            elif row_change == -1 and column_change == 0:
                directions.append("up")
            elif row_change == 0 and column_change == 1:
                directions.append("right")
            elif row_change == 1 and column_change == 0:
                directions.append("down")

        return directions

    def _draw_button_sequence(self, path: List[Cell]) -> None:
        """Show the required direction buttons below the maze."""
        for widget in self.steps_frame.winfo_children():
            widget.destroy()

        directions = self._path_to_directions(path)

        if not directions:
            self.steps_title.pack_forget()
            self.steps_frame.pack_forget()
            return

        self.steps_title.pack(anchor="w", padx=20, pady=(10, 4))
        self.steps_frame.pack(fill="x", padx=20)

        symbols = {
            "left": "←",
            "up": "↑",
            "right": "→",
            "down": "↓",
        }

        # Wrap the sequence after eight symbols so long routes stay readable.
        for index, direction in enumerate(directions):
            row = index // 8
            column = index % 8

            image = self.direction_images.get(direction)

            if image is not None:
                label = tk.Label(
                    self.steps_frame,
                    image=image,
                    bg=self.BACKGROUND,
                    bd=0,
                )
            else:
                label = tk.Label(
                    self.steps_frame,
                    text=symbols[direction],
                    font=("Segoe UI Symbol", 24, "bold"),
                    width=2,
                    fg=self.TEXT_COLOR,
                    bg="#303641",
                    relief="ridge",
                    bd=2,
                )

            label.grid(
                row=row,
                column=column,
                padx=4,
                pady=4,
            )

    def _draw_cells(self, path: List[Cell]) -> None:
        path_set = set(path)

        for row in range(self.GRID_SIZE):
            for column in range(self.GRID_SIZE):
                x1, y1, x2, y2 = self.cell_rect((row, column))
                fill = "#21414b" if (row, column) in path_set else self.CELL_COLOR

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill,
                    outline="",
                )

                if self.show_coordinates.get():
                    self.canvas.create_text(
                        x1 + 8,
                        y1 + 8,
                        text=f"{row},{column}",
                        #text=f"{row + 1},{column + 1}",
                        anchor="nw",
                        fill="#8c929d",
                        font=("Consolas", 8),
                    )

    def _draw_grid(self) -> None:
        left = self.MARGIN
        top = self.MARGIN
        right = left + self.GRID_SIZE * self.CELL_SIZE
        bottom = top + self.GRID_SIZE * self.CELL_SIZE

        for index in range(self.GRID_SIZE + 1):
            x = left + index * self.CELL_SIZE
            y = top + index * self.CELL_SIZE

            self.canvas.create_line(
                x, top, x, bottom,
                fill=self.GRID_COLOR,
                width=1,
            )
            self.canvas.create_line(
                left, y, right, y,
                fill=self.GRID_COLOR,
                width=1,
            )

    def _draw_path(self, path: List[Cell]) -> None:
        if len(path) < 2:
            return

        points = []
        for cell in path:
            points.extend(self.cell_center(cell))

        self.canvas.create_line(
            *points,
            fill=self.PATH_COLOR,
            width=10,
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND,
        )

        for index, cell in enumerate(path):
            x, y = self.cell_center(cell)
            radius = 12
            self.canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=self.PATH_COLOR,
                outline=self.BACKGROUND,
                width=2,
            )
            self.canvas.create_text(
                x,
                y,
                text=str(index + 1),
                fill="#071418",
                font=("Segoe UI", 8, "bold"),
            )

    def _draw_walls(self, walls: Set[Edge]) -> None:
        # Outer border
        left = self.MARGIN
        top = self.MARGIN
        right = left + self.GRID_SIZE * self.CELL_SIZE
        bottom = top + self.GRID_SIZE * self.CELL_SIZE

        self.canvas.create_rectangle(
            left, top, right, bottom,
            outline=self.WALL_COLOR,
            width=5,
        )

        for a, b in walls:
            row_a, col_a = a
            row_b, col_b = b

            if abs(row_a - row_b) + abs(col_a - col_b) != 1:
                continue

            if row_a == row_b:
                # Cells are next to each other horizontally:
                # draw a vertical wall.
                boundary_col = max(col_a, col_b)
                x = self.MARGIN + boundary_col * self.CELL_SIZE
                y1 = self.MARGIN + row_a * self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                self.canvas.create_line(
                    x, y1, x, y2,
                    fill=self.WALL_COLOR,
                    width=7,
                    capstyle=tk.ROUND,
                )
            else:
                # Cells are above/below each other:
                # draw a horizontal wall.
                boundary_row = max(row_a, row_b)
                y = self.MARGIN + boundary_row * self.CELL_SIZE
                x1 = self.MARGIN + col_a * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                self.canvas.create_line(
                    x1, y, x2, y,
                    fill=self.WALL_COLOR,
                    width=7,
                    capstyle=tk.ROUND,
                )

    def _draw_markers(self) -> None:
        if self.start is not None:
            x,y=self.cell_center(self.start)
            s=24
            self.canvas.create_rectangle(x-s,y-s,x+s,y+s,fill="#FFD83D",outline=self.BACKGROUND,width=4)

        if self.end is not None:
            x,y=self.cell_center(self.end)
            r=30
            self.canvas.create_polygon([x,y-r,x+r,y,x,y+r,x-r,y],fill="#3F8CFF",outline=self.BACKGROUND,width=4)

    def cell_rect(self, cell: Cell) -> Tuple[int, int, int, int]:
        row, column = cell
        x1 = self.MARGIN + column * self.CELL_SIZE
        y1 = self.MARGIN + row * self.CELL_SIZE
        return x1, y1, x1 + self.CELL_SIZE, y1 + self.CELL_SIZE

    def cell_center(self, cell: Cell) -> Tuple[int, int]:
        x1, y1, x2, y2 = self.cell_rect(cell)
        return (x1 + x2) // 2, (y1 + y2) // 2

    @staticmethod
    def pretty_cell(cell: Cell) -> str:
        row, column = cell
        return f"({row + 1},{column + 1})"

    def _validate_all_solutions(self) -> None:
        errors = []

        for (start, end), solution in SOLUTIONS.items():
            if not solution.path:
                errors.append(f"{start} -> {end}: path is empty.")
                continue

            if solution.path[0] != start:
                errors.append(
                    f"{start} -> {end}: first path field must be the start."
                )

            if solution.path[-1] != end:
                errors.append(
                    f"{start} -> {end}: last path field must be the end."
                )

            for cell in solution.path:
                if not self._valid_cell(cell):
                    errors.append(
                        f"{start} -> {end}: invalid path field {cell}."
                    )

            for a, b in zip(solution.path, solution.path[1:]):
                distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
                if distance != 1:
                    errors.append(
                        f"{start} -> {end}: path fields {a} and {b} "
                        f"are not directly adjacent."
                    )

            for a, b in solution.walls:
                if not self._valid_cell(a) or not self._valid_cell(b):
                    errors.append(
                        f"{start} -> {end}: invalid wall {a} <-> {b}."
                    )
                    continue

                distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
                if distance != 1:
                    errors.append(
                        f"{start} -> {end}: wall fields {a} and {b} "
                        f"are not directly adjacent."
                    )

        if errors:
            messagebox.showerror(
                "Invalid solution data",
                "\n".join(errors[:20]),
            )

    def _valid_cell(self, cell: Cell) -> bool:
        row, column = cell
        return (
            0 <= row < self.GRID_SIZE
            and 0 <= column < self.GRID_SIZE
        )


def main() -> None:
    root = tk.Tk()
    MazeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
