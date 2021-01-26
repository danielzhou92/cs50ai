# CS50 AI (2020 - 2021) Projects Descriptions

## Project Demos:
[YouTube](https://youtube.com/playlist?list=PL1vywBcTokGQin39SLJf8B43U9yijkugJ)

## Project 0a - Degrees: 

This project is to write a program that determines the degrees of seperation between 2 actors, the idea here is to find the shortest path, therefore the search method chosen is breadth wise search and a queue frontiere was chose as oposed to a stack frontiere which is used for deapth wise search.


## Project 0b - TicTacToe:

This project is to write an AI that can play tic tac toe (and never lose), the AI desicides on moved using the Minimax algorithom. wheres for each move it makes, it would first simulates all the possible moves all the way to the end of the game, and selects its move to minimize the chance of the other player winning. Using this approach, the AI will never lose in TicTacTie, the worst it can do is a tie.


## Project 1a - Knights:

This project is to write an AI that can solve Knights and Knaves logic puzzle. It is first given a set of rules and then a set of knowledge (both hard coded as propositional logic) and determines who is a Knight and who is a Knave.


## Project 1b - Minesweeper:

This project is to write and AI that can play mine sweeper, the AI utilizes a knowledge base (containing propositional logic) to determine best possible moves, it also does inferencing on the knowledge base to generate new propositional logic sentences which aids it's decision. Note that the AI can not solve the gome 100% of the time, as if it gets unlucky and keeps making moves that doesn't add any additional propositional logic sentences to it knowledge base (either directly or through inferencing), than it would have to make risky moves to gain knowledge.


## Project 2a - Pagerank:

This project is write an algorithom that rank webpages using a simplified version of Google's old pagerank algorithom which determines how important a webpage is based on how many other webpages link to it. This is done with 2 seperate methods, one is using an iterative algorithom for page rank which iteratively calculates the page ranking through a page rank formula. the other approach is through sampling (ramdon surfer model), wheres the webpages are considered to be a part of a markov chain (where the pages are treated as states and the states are selected at random to a linked state), and page rank is calculated based on how likely a particular page is to be selected.


## Project 2b - Heredity

This project is to write an algorithom that predicts the likelyhood of a person posessing a particular genetic trait given some info about the genes and/or traits of the parents, essentially it computes the joint probability of events occuring based on given info. the relationships between the parents/childs genes/traits are modeled as a baysian network.


## Project 3 - Crossword

This project is to write an AI that can generate a crossword puzzle when given a puzzle structure and a dictionary of words to choose from. Its essentially a constraint satisfaction problem where the AI must satisfy the rules of generating the puzzle while maintaining arc and node consistency (ie. over lapping characters between words, no repeating words, fixed word lengths). The solution utilizes backtrack serch to try to assign words to the puzzle recursively. The AI must be optimized so that as it tries to assign a particular word into the puzzle, that word should be the least constraining option (ie. that word elimates the least amount of possible words choices for neighboring variables)


## Project 4a - Shopping

This project is to write an AI that can read data from CSV file containing a labeled dataset of onling user shopping behavior data, split the data into training set and testing set, train, test, and benchmark a model with Scikit-learn to predict wheather a particular customer will complete a purchase.


## Project 4b - Nim

This project is to write an AI that can train it self, through reinforcament learning (Q-learning in this case), to play the Nim game against a human player. While the AI trains itself, the epsilon greedy algorithm is used to control the AI's decision between exploring(take unexplored routes to discover more efficient solutions) vs exploiting(take rounts that are known to bring good outcome).


## Project 5 - Traffic

This project is to train an AI model to recognize and identyfy traffic signs given an image. Use TensorFlow to build a neural network, the neural network was trained with a labeled dataset of different kinds of road signs, model was optimized using trial and error of different types/amount of hidden layers (ex. adjusting number of convolutional layers, sizes and number of pooling layers, number of filters, different dropout sizes).


## Project 6a - Parser

This project is to write an AI that when given a set of grammer rules ( for generating none terminal symbles) and words (for generating terminal symbols), can parse through sentences, determining the sentence structure, and extract none phrases.


## Project 6b - Questions

This project is to write an AI that can answer simple questions based on inverse document frequency. When a query (question) is sent to the AI, it retrieved the most relavent document (basically wikipedia articles) from it's database, selected based on TF-IDF (term frequency * inverse document frequency) and picks the most relavent sentence from that document pertaining to the query, selected based on IDF (inverse document frequency) and query term density (how ofter words from the query shows up in the sentence).