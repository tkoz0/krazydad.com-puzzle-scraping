# krazydad.com-puzzle-scraping
Project to parse puzzle data from pdfs on krazydad.com

Below is a list of the data files and a description of their format.

### `krazydad-sudoku-20220604.csv.bz2`

Standard 9x9 sudoku puzzles. Each row has the difficulty, volume (1-20), book
(1-100) and puzzle number within the book (1-8). Finally, the puzzle is
described as 81 digits with `0` indicating empty cells. The difficulties in
ascending order are EZ (easy), NO (novice), IM (intermediate), CH (challenging),
TF (tough), ST (super tough), IN (insane).

All are verified as having exactly 1 solution with the solver code in the
parsing program. These were verified before a fix was added to make the solver
work much faster.

### `krazydad-hexsudoku-20220605.csv.bz2`

Standard 16x16 sudoku puzzles. Specified like the 9x9 sudoku, but there are 7
volumes instead of 20. Puzzles are described as 256 characters with `.` being
the empty cell since 0-9 and a-f are used as the 16 symbols for the puzzles.
The 4 difficulties in ascending order are IM (intermediate), CH (challenging),
TF (tough), ST (super tough).

All are verified as having exactly 1 solution with the solver code in the
parsing program. This took about 12 hours on a Xeon X5570.
