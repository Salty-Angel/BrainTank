# Brain Tank
## Summary
This is a little project to teach programming skills as well as basic AI.
To run it just execute main.py with python.

## Simulation Rules
Every time a trank becomes "idle" it will run the `think()` function associated
with that brain to queue up more commands. 
The tank then executes these, which can take a variable amount of time.
Tanks can also fire shots in the direction they are facing. 
They must turn to aim. 
Turning one facing takes half a second, turning twice takes one second.
The shots move at twice the speed of a tank.

### Tile Rules
  * Crossing __dirt__ will take twice as long as regular tiles.
  * The tank will abort a move if it runs into a blocking tile or other tank.
  * Shots can destroy blocking tiles such as __trees__ or __rocks__.
  * Driving into __water__ will destroy the tank.

## Making a Brain
Copy brains/wander.py to brains/yourname.py and add "yourname" it to config.py.
For now it will only read the first two brains listed.
There is a small guide that describes what this brain does and what is 
available for brains to use in wander.py.

## TODO
  1. Add explosions and other animations.
  2. Make sound effects for actions.
  3. Add GUI elements like victory screen, etc.

## Requirements
  * [Python 2.7+](http://www.python.org/) - does NOT run on Python 3.
  * [Pyglet](http://pyglet.org/)
    * Windows users should use [pip](http://www.pip-installer.org/) to install.
    * OSX users should use [this fork](http://code.google.com/r/evilphillip-cocoa-ctypes/) 
      * If you have pip: `pip install https://github.com/downloads/pysgf/BrainTank/pyglet-evilphillip-cocoa-ctypes.tar.bz2`
    * Ubuntu
      * If you have pip: `pip install pyglet`
  * [AVBin](http://code.google.com/p/avbin/) - For playing music & sounds.
    * Windows users should pull down http://code.google.com/p/avbin/downloads/detail?name=avbin-win32-5.zip.
    * OSX users should use http://code.google.com/p/avbin/downloads/detail?name=avbin-darwin-x86-64-8.zip.
      * After downloading the zip, unzip & run sudo install.sh.
    * Ubuntu
      * `$ sudo apt-get install libavbin-dev`

## Running
```bash
$ python main.py brains/amanda.py brains/phil.py
```

## Licensing
The code is GPLv3, but the art/sound is not.

### Attribution
  * The Planet Cute sprites are from the venerable Danc. Check out his [site](http://www.lostgarden.com).
  * The tank is by Saypen on [Open Game Art](http://opengameart.org/content/american-tank).
  * The Main song is by Mister Electric Demon on [Jamendo](http://www.jamendo.com/en/album/7686).
  * Everything else I've made and is in the public domain.
