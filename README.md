# Jetpack joyride

This is an amazing implementation of a subset of the Jetpack Joyride game. You will most probably enjoy it.

Special thanks to [zubair's mario console](https://github.com/zubairabid/mario-console/) for giving me ideas on how to go about this project, and to [this website](https://www.sounds-resource.com/mobile/jetpackjoyride/sound/6078/) for providing in-game soundtrack mp3 files (which I am yet to implement due to Python venv problems -_-).

## Instructions

1. WASD to move, fire bullets with b, activate shield with Space, activate dragon with y and speed up with t.
2. Firebeam is represented by F, and coins by C

## Assignment related stuff

1. **Polymorphism** - both player and dragon have the `fire_laser` but it behaves differently in both of them, however, it is fired in the same way.
2. **Inheritance** - all frame objects inheit from a generic frame object class gives a common interface for spawn probability, draw, cleanup, exceeds
3. **Encapsulation** - most instance variables are private, the inherited ones are protected, and they have getters and setters (although this is a Java concept which does not exist in Python but TAs wanted us to do so please don't hate me :(
4. **Abstraction** - functions like `check_collision` and `fire_laser` hide underlying implementation and can be used in whatever way since it always works the way you want it to.

**Disclaimer**: This project was only made as a part of IIIT DASS Assingment 1. This project does not endorse the actual game by any means. The developer is NOT liable for ANY and ALL of the waste of your time as a result of playing this addicting implementation.
