<p align="center">
  <img src="AImbidextro.png" alt="AImbidextro Logo" width="300"/>
</p>

***

`AImbidextro` is an attempt to develop an agent that autonomously plays the game [Ambidextro](https://www.majorariatto.com/es/ambidextro), made by spanish indie dev `Alva Majo`.

The project is in an early stage, so any changes are welcome.

Currently, a level can be hardcoded to be played by the agent using a series of keyboard presses. e.g:
```python
keys_yellow = [
    's',  # key s is pressed 'delay'=0.2 seconds
    {'keys': 'd', 'delay': 0.6}, # key d is pressed 'delay'=0.6 seconds
    {'keys': ('d', 'w'), 'delay': 0.5}, # keys d, w are pressed 'delay'=0.5 seconds
]
```
Yellow and purple wizards can be found at each time step using `cv2.matchTemplate`.

## Level 0 Example
[Level 0](https://github.com/user-attachments/assets/f5514826-3519-4f00-8dd2-ef3b8e347b5a)

## Future steps
These are the two main directions I want to follow:
1. Implementing a `Genetic Algorithm (GA)` that learns the best combination of key presses to beat a level. This is easier to implement, but needs to be trained for each level.

2. Using `Reinforcement Learning (RL)` sparse rewards to make a learning agent that is able to play unseen levels. This is a more generalizable approach, but way harder to implement
