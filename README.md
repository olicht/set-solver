# Set Solver

Using OpenCV to identify cards in an image and solve for valid sets in a game of [Set](https://www.wikiwand.com/en/Set_(game)). 

## Demo
![sets](http://i.imgur.com/uS3xILw.jpg)

Sets found:

```
1 RED DIAMOND EMPTY
1 GREEN DIAMOND STRIPED
1 PURPLE DIAMOND SOLID
---
3 GREEN DIAMOND STRIPED
2 GREEN DIAMOND STRIPED
1 GREEN DIAMOND STRIPED
---
2 GREEN DIAMOND STRIPED
2 PURPLE DIAMOND STRIPED
2 RED DIAMOND STRIPED
---
1 PURPLE OBLONG SOLID
3 PURPLE SQUIGGLE EMPTY
2 PURPLE DIAMOND STRIPED
---
1 GREEN DIAMOND STRIPED
3 PURPLE DIAMOND STRIPED
2 RED DIAMOND STRIPED
---
1 GREEN DIAMOND STRIPED
2 RED SQUIGGLE STRIPED
3 PURPLE OBLONG STRIPED
---
```


## Installation

you will need OpenCV installation on your machine.

```
# install requirements
pip install -r requirements.txt
```

## Run tests

For examples on how to use code, check out `tests.py`. Run it to see the card detection and solving in action:

```
python
>>> import tests 
>>> tests.main() #to run basic tests
>>> tests.play_game(<path/to/image>) #to find sets in image
```

## Known issues
* Has issues detecting card properties when shadowed
* Inaccurate detection with low-res image
