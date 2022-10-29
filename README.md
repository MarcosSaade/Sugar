# Sugar
A pygame implementation of the board game Sugar.


Summary of the rules:

There are two players. Each has 6 sugar packages (red and blue squares). They take turns placing them untill they both finish. Then, they take turn moving untill one of them can't move (because all otehr pieces are on top, or because there are no legal moves remaining)
 
* Pieces can move up, down, left, or right, but not diagonally.
* A piece can move from one stack unto anotehr only if the end stack has equal or less height than the starting stack.
* In the placing phase, there is a maximum of three copying moves (putting your piece on top of a piece that was put inmediately before you)

The game features human vs human play, as well as an AI that uses minimax and alpha-beta pruning

The program is not finished, as the static evaluation function can still be made better, and game settings can only be changed directly from the code.
