# CS50 AI (2020 - 2021) Project Descriptions

This repository is used to store my completed project solutions for the 2020-2021 Harvard CS50 AI course.

[Course homepage](https://cs50.harvard.edu/ai/2020/)

[YouTube demos playlist](https://youtube.com/playlist?list=PL1vywBcTokGQin39SLJf8B43U9yijkugJ)

## [Project 0a - Degrees](0a-degrees)

[YouTube demo](https://youtu.be/YrFb7oPvnBI)

This project is to write a program that determines the degrees of separation between 2 actors. The idea here is to find the shortest path, therefore the search method chosen is breadth wise search, a queue frontier was chosen as opposed to a stack frontier which is used for depth wise search.

*usage ex.* `python 0a-degrees/degrees.py 0a-degrees/large`


## [Project 0b - Tic-tac-toe](0b-tictactoe)

[YouTube demo](https://youtu.be/D_rX45x3-zI)

This project is to write an AI that can play Tic-tac-toe (and never lose), the AI deicides on moved using the Minimax algorithm. whereas for each move it makes, it would first simulate all the possible remaining moves all the way to the end of the game, and then select its next move to minimize the chance of the other player winning. Using this approach, the AI will never lose in Tic-tac-toe (the worst it can do is a tie).

*usage ex.* `python 0b-tictactoe/runner.py`


## [Project 1a - Knights](1a-knights)

[YouTube demo](https://youtu.be/u5jNbUDYmuk)

This project is to write an AI that can solve the Knights and Knaves logic puzzle. It is first given a set of rules and then a set of knowledge (both hardcoded as propositional logic) and determines who is a Knight and who is a Knave based on those.

*usage ex.* `python 1a-knights/puzzle.py`


## [Project 1b - Minesweeper](1b-minesweeper)

[YouTube demo](https://youtu.be/_uG6m4oKQmA)

This project is to write and AI that can play the Minesweeper game. The AI utilizes a knowledge base (containing propositional logic) to determine best possible moves, it also does inference on the knowledge base to generate new propositional logic sentences which aids its decision. Note that the AI cannot solve the game 100% of the time, as if it gets unlucky and runs out of safe moves to make, it will make a random move (which has a chance to be a mine) in an attempt to improve its knowledge, and if it keeps making moves that doesn't add any additional propositional logic sentences to it knowledge base (either directly or through inferencing), then it would have to keep making risky moves to gain knowledge.

*usage ex.* `python 1b-minesweeper/runner.py`


## [Project 2a - PageRank](2a-pagerank)

[YouTube demo](https://youtu.be/baCoqRa3dkY)


This project is to write an algorithm that rank webpages using a simplified version of Google's old PageRank algorithm which determines how important a webpage is based on how many other webpages link to it. This is done with two separate methods, one is using an iterative algorithm which iteratively calculates the page ranking through a PageRank formula. the other approach is through sampling (random surfer model), whereas the webpages are considered to be a part of a Markov chain (where the pages are treated as states, and next states are selected at random from the linked states of the currently selected state), and page ranking is calculated based on how likely a particular page is to be selected.

*usage ex.* `python 2a-pagerank/pagerank.py 2a-pagerank/corpus2`


## [Project 2b - Heredity](2b-heredity)

[YouTube demo](https://youtu.be/njxCPjPDgQ0)

This project is to write an algorithm that predicts the likelihood of a person possessing a particular genetic trait given some info about the genes and/or traits of the parents. Essentially it computes the joint probability of events occurring based on given info. the relationships between the parents/childs genes and traits are modeled as a Bayesian network.

*usage ex.* `python 2b-heredity/heredity.py 2b-heredity/data/family2.csv`


## [Project 3 - Crossword](3-crossword)

[YouTube demo](https://youtu.be/Jgs_Vw_9pZU)

This project is to write an AI that can generate a crossword puzzle when given a puzzle structure and a dictionary of words to choose from. It’s essentially a constraint satisfaction problem where the AI must satisfy the rules of generating the puzzle while maintaining arc and node consistency (i.e. has to have overlapping characters between words, no repeating words, correct word lengths). The solution utilizes backtrack search to try to assign words to the puzzle recursively. The AI must be optimized so that every time it tries to assign a particular word into the puzzle, that word should be the least constraining option (i.e. that word eliminates the least amount of possible words choices for neighboring variables)

*usage ex.* `python 3-crossword/generate.py 3-crossword/data/structure1.txt 3-crossword/data/words2.txt`


## [Project 4a - Shopping](4a-shopping)

[YouTube demo](https://youtu.be/_1wutfuQyzU)

This project is to write an AI that can read data from CSV file containing a labeled dataset of online user shopping behavior data, split the data into training set and testing set to train, test, and benchmark a model with SciKit-learn to predict whether a particular customer will complete a purchase.

*usage ex.* `python 4a-shopping/shopping.py 4a-shopping/shopping.csv`


## [Project 4b - Nim](4b-nim)

[YouTube demo](https://youtu.be/aElj6iGLZWg)

This project is to write an AI that can train itself, through reinforcement learning (Q-learning in this case), to play the Nim game against a human player. While the AI trains itself, the epsilon greedy algorithm is used to control the AI's decision between exploring (take unexplored routes to potentially learn more efficient solutions) vs exploiting (take routes that are known to bring good outcome).

*usage ex.* `python 4b-nim/play.py`


## [Project 5 - Traffic](5-traffic)

[YouTube demo](https://youtu.be/kp6rc1-Jgls)

This project is to train an AI model to recognize and identify traffic signs from given images. TensorFlow was used to build a neural network, the neural network was trained with a labeled dataset of different kinds of road signs. Model was optimized using trial and error of different types / numbers of hidden layers (ex. different number of convolutional layers, sizes and number of pooling layers, number of filters, sizes of dropouts).

*usage ex.* `python 5-traffic/traffic.py 5-traffic/gtsrb`


## [Project 6a - Parser](6a-parser)

[YouTube demo](https://youtu.be/TOhpRWI8-EM)

This project is to write an AI that when given a set of grammar rules (for generating non-terminal symbols) and words (for generating terminal symbols), can parse through sentences, determining the sentence structure, and extract noun phrases.

*usage ex.* `python 6a-parser/parser.py 6a-parser/sentences/10.txt`


## [Project 6b - Questions](6b-questions)

[YouTube demo](https://youtu.be/VIh0d6jheOk)

This project is to write an AI that can answer simple questions based on inverse document frequency. When a query (question) is sent to the AI, it retrieved the most relevant document (basically Wikipedia articles) from its database, selected based on TF-IDF (term frequency * inverse document frequency) and picks the most relevant sentence from that document pertaining to the query, selected based on IDF (inverse document frequency) and query term density (how often words from the query shows up in the sentence).

*usage ex.* `python 6b-questions/questions.py 6b-questions/corpus`