_______
#### Summary

This project uses genetic AI and Neural Networks to learn to play a variation of the Flappy Bird game, where players have to control the ship to cross pipes. It is now able to train agents to cross pipes with gaps as low as 350 pixels (although it may take a few tries). Use '''python main.py''' to run the code; it may need a few runs to achieve good results. I'm currently working on making the program more usable and generalized, and thinking of next steps with the project.

______
#### Example

![350-pixel gap](example_gap350.gif)
Work in progress.

_______
#### Process

The first part of the project is to build the game itself. In the game, the player simply controls the ship to go up or down, and let it fly through the pipes without colliding. The ship dies if it collides with the pipes. The player generates score as long as the ship is alive. I wrote the game on pygame which allows me to directly take the game info and score into the AI as input.

The AI is a genetic algorithm that generates many weights and biases for the neural network system, then choose the best performing sets of weights and biases to continue with. For the neural network, I chose to feed it 4 inputs: the player's y position (1 input), and the x and y positions of the nearest pair of pipes (3 inputs). If the output of the neural network is positive, the brain the commands the ship to fly upwards, and if the output is negative, the brain commands the ship to fly downwards. I figured that since the output is only going to be positive or negative, and that determines the action of the AI, there's no need to do logistic regression in the last layer. Whether or not this works remains to be seen.

Our AI is now ready to play the game. I quickly noticed that while some iterations of the brain will commmand the ship to go up or down as new information on the pipes come in, most iterations will only command the ship to go either up or down, with no change in direction. For some of these iterations, while the output of the neural network changes, it is not enough to change the sign of the output (positive or negative), and therefore the ship does not change its direction. This causes the vast majority of brains to not be able to survive even the first pair of pipes.

To solve this problem, I need to get rid of these brains that do not change the ship's direction. For those brains that do change the ship's direction, I assign a higher score than brains that do not change direction, so that the brains that change direction will be selected to test in the next generation. This way, I can identify weights and biases that are useful, even though almost every brain cannot pass even the first pair of pipes at this stage.

After fixing bugs in the code and tweaking values, the program is now able to train agents to play the game. The training is basically finding the right weights for the ship to be able to cross pipes without getting hit.

_______
##### Updates

September 27 update:
Mutation working now, preparing for the model to generate new generations. Fixed bugs from mutation and generating descendants. Need to figure out a way to deal with situations where the number of qualified brains is too low. Can do it directly by editing create_new_gen() or simply increase the number of starting brains.

September 10 update:
Reorganized code to make it more generalized and usable.
Bug fixed: when pygame is run, the first iteration of the game has delayed times for pipe entries, which causes the first iteration to always have a higher score.