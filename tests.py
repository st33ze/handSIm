# Simulation test data:
sim_data = [
            # Flush checks. #0
            [ [[0,12],[0,11]],  [[2,12],[2,11]],     [[0,0],[0,4],[0,6],[1,0],[1,5]] ], # Player 1 wins
            [ [[3,2], [1,12]],  [[1,11],[1,10]],     [[1,0],[1,7],[0,5],[1,5],[2,8]] ], # Player 2 wins
            [  [[3,12],[3,8]],  [[3,11],[3,10]],    [[3,0],[2,1],[3,6],[0,11],[3,4]] ], # Player 1 wins
            [ [[2,12],[3,10]],    [[0,7],[0,8]],    [[2,0],[0,9],[2,10],[2,3],[2,9]] ], # Player 1 wins
            [  [[3,9],[2,9]],    [[0,2],[1,11]],    [[0,5],[0,8],[1,2],[0,3],[0,10]] ], # Player 2 wins

            # Poker checks. #4
            [  [[0,12],[0,1]],  [[3,12],[3,11]],     [[0,0],[3,2],[0,3],[3,5],[0,2]] ], # Player 1 wins
            [  [[1,12],[1,9]],  [[3,12],[3,11]],   [[2,10],[2,8],[3,9],[3,10],[3,8]] ], # Player 2 wins
            [   [[2,7],[2,6]],   [[2,2],[1,10]],     [[2,5],[1,6],[2,3],[2,4],[0,7]] ], # Player 1 wins
            [   [[1,6],[2,6]],    [[1,1],[1,0]],     [[1,2],[1,5],[3,0],[1,4],[1,3]] ], # Player 1 wins
            [   [[3,12],[2,12]],  [[0,7],[1,8]],    [[0,5],[0,4],[1,12],[0,8],[0,6]] ], # Player 2 wins

            # Four of a kind checks. #9
            [   [[0,9],[1,9]],   [[3,12],[3,5]],     [[3,3],[3,4],[2,9],[1,0],[3,9]] ], # Player 1 wins
            [ [[2,11],[2,12]],  [[0,12],[0,10]],  [[1,10],[3,3],[2,8],[3,10],[2,10]] ], # Player 2 wins

            # Full house checks. #11
            [   [[1,4],[3,4]],    [[3,6],[3,7]],  [[2,4],[3,12],[3,10],[3,0],[2,10]] ], # Player 1 wins
            [   [[0,0],[1,0]],    [[2,9],[3,8]],     [[0,8],[3,0],[2,8],[1,8],[1,4]] ], # Player 2 wins
            [   [[0,0],[3,0]],  [[1,11],[3,10]], [[0,12],[2,7],[1,12],[2,10],[3,10]] ], # Player 2 wins
            [   [[0,8],[0,9]],   [[3,12],[3,9]],  [[0,11],[2,0],[2,11],[3,11],[3,8]] ], # Player 1 wins

            # Straight checks. #15
            [   [[2,7],[1,5]],   [[0,10],[0,4]],     [[1,4],[3,6],[0,1],[3,0],[3,8]] ], # Player 1 wins
            [ [[0,10],[0,11]],   [[1,12],[0,2]],     [[1,3],[2,5],[3,8],[3,4],[0,6]] ], # Player 2 wins
            [  [[3,12],[3,3]],  [[0,10],[2,10]],     [[1,2],[2,3],[0,0],[1,1],[0,9]] ], # Player 1 wins

            # Three of a kind checks. #18
            [   [[3,3],[1,3]],  [[0,10],[1,10]],     [[1,8],[2,6],[0,0],[3,5],[2,3]] ], # Player 1 wins
            [ [[0,11],[1,12]],  [[3,10],[3,11]],  [[1,12],[2,10],[0,2],[0,5],[0,10]] ], # Player 2 wins 12:9

            # hands_compare tests:

            # High card. #20
            [  [[0,12],[0,6]],    [[1,9],[1,8]],    [[0,0],[2,1],[3,3],[3,4],[2,10]] ],
            [   [[1,6],[2,2]],    [[3,5],[1,7]],  [[0,12],[0,11],[1,10],[1,3],[3,9]] ],
            [   [[1,6],[2,2]],    [[3,5],[1,4]],  [[0,12],[0,11],[1,10],[1,7],[3,9]] ],
            
            # One pair. #23
            [   [[1,4],[2,4]],   [[2,11],[3,9]],    [[0,1],[1,3],[3,11],[2,5],[3,7]] ],
            [   [[0,5],[0,7]],   [[1,5],[2,10]],     [[2,5],[0,9],[3,0],[3,4],[1,8]] ],
            [   [[2,8],[3,5]],    [[1,8],[2,0]],    [[0,12],[3,9],[1,6],[1,2],[0,8]] ],

            # Two pairs. #26
            [   [[0,4],[1,4]],    [[0,8],[3,9]],    [[2,0],[3,0],[1,8],[1,12],[0,9]] ],
            [  [[0,12],[1,0]],    [[3,7],[3,8]],    [[2,3],[1,5],[0,10],[0,5],[1,3]] ],
            [   [[0,8],[1,0]],    [[3,7],[3,8]],    [[2,3],[1,5],[0,10],[0,5],[1,3]] ],
            [  [[0,12],[1,0]],    [[3,7],[3,12]],    [[2,3],[1,5],[0,10],[0,5],[1,3]] ],
            
            # Three of a kind. #30
            [   [[1,5],[3,5]],  [[2,10],[0,10]],   [[1,10],[2,5],[3,8],[3,11],[0,0]] ],
            [ [[3,12],[3,11]],   [[3,4],[0,11]],  [[2,11],[1,2],[3,5],[1,11],[1,10]] ],
            [  [[3,3],[3,11]],   [[3,4],[0,11]],  [[2,11],[1,2],[3,5],[1,11],[1,10]] ],
            [   [[0,7],[1,1]],    [[3,1],[3,5]],  [[1,12],[0,2],[2,12],[0,12],[3,4]] ],

            # Straight. #34
            [    [[0,5],[0,7]],   [[1,7],[3,11]],    [[2,6],[3,9],[1,10],[2,8],[1,5]] ],
            [    [[0,8],[1,3]],    [[2,4],[2,3]],   [[3,12],[3,0],[1,2],[0,1],[1,12]] ],
            [  [[0,12],[1,12]],   [[0,9],[3,10]],     [[0,2],[3,4],[1,5],[1,3],[2,6]] ],
            [  [[0,12],[1,12]],   [[3,12],[3,8]],     [[0,0],[1,3],[3,9],[0,1],[3,2]] ],

            # Flush. #38
            [   [[0,9],[0,10]],  [[0,12],[1,12]],     [[1,3],[0,2],[0,8],[0,6],[0,0]] ],
            [    [[3,9],[0,0]],    [[3,8],[1,8]],   [[2,8],[3,0],[3,5],[3,11],[3,12]] ],
            [   [[0,12],[1,3]],   [[2,12],[1,5]],  [[1,6],[1,8],[1,10],[1,11],[1,12]] ],
            [   [[2,10],[2,5]],    [[2,0],[2,1]],   [[2,3],[2,7],[2,9],[2,11],[2,12]] ],

            # Full house. #42
            [    [[0,5],[1,5]],  [[1,12],[2,11]],   [[3,5],[3,12],[0,0],[1,0],[2,12]] ],
            [    [[1,8],[2,9]],    [[0,6],[1,6]],     [[2,0],[3,8],[3,0],[2,5],[0,0]] ],
            [   [[0,12],[0,8]],  [[3,12],[1,11]],    [[0,5],[1,12],[2,5],[3,9],[3,5]] ],
            [    [[0,5],[1,5]],    [[1,7],[3,7]],     [[3,5],[0,9],[2,9],[2,7],[1,9]] ],

            # Four of a kind. #46
            [    [[0,7],[0,8]],  [[3,12], [1,3]],     [[0,9],[1,9],[2,3],[3,9],[2,9]] ],
            [   [[0,4],[1,10]],    [[3,7],[2,7]],    [[0,3],[3,3],[2,11],[1,3],[2,3]] ],

            # Straight Flush. #48
            [   [[3,4],[0,11]],   [[3,12],[1,5]],     [[3,0],[3,2],[3,1],[2,7],[3,3]] ],
            [   [[0,5],[1,12]],    [[2,7],[3,7]],    [[0,7],[0,9],[0,10],[0,6],[0,8]] ],

]
