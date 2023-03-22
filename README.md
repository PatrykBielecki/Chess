###Chess with Reinforcement Learning
This project is an implementation of the game of Chess using Reinforcement Learning techniques. The goal of the project is to develop an AI agent that can learn to play Chess at a competitive level using only self-play and reinforcement learning.

##Overview
The project is divided into two main components:

The Chess Engine - This is a traditional chess engine that implements the rules of the game and provides the interface for the Reinforcement Learning agent to interact with.

The Reinforcement Learning Agent - This is the AI agent that learns to play Chess by playing against itself and using reinforcement learning techniques to improve its play.

The Reinforcement Learning agent is implemented using a variant of the Deep Q-Network (DQN) algorithm.

##Requirements
The following are the requirements for running the project:

Python 3.6+
TensorFlow 2.0+
Keras 2.0+
Numpy
Matplotlib

##Installation
To install the project, follow these steps:

Clone the repository from Github.

Install the required dependencies by running pip install -r requirements.txt.

Run the Chess Engine by running python chess_engine.py.

##Usage
To train the Reinforcement Learning agent, run python train.py. The agent will play against itself and learn from its mistakes using the DQN algorithm.

To watch the Reinforcement Learning agent play against a traditional Chess engine, run python play.py. The Reinforcement Learning agent will play as the black pieces and the traditional Chess engine will play as the white pieces.

##Results
The project is still under development and results will be added as they become available.
