Ludum Dare 26
=============

# Before the Competition
__2013-04-26	07:41:46__	I'm going to use Python as my programming language of choice. I have programmed a few dozen lines of Python in the last few months, after all.

__2013-04-26	07:42:17__	Installing Panda3D and pygame. I don't think I'll go 3D, it seems much too complicated and I do not know how to create 3D artwork assets. Besides, 2D games are fun.

__2013-04-26	07:56:54__	The first PyGame tutorial is a ball that moves around the screen and bounces off of the screen borders. This is code similar to what I've seen in "The Nature of Code" (Daniel Shiffman). Great book, by the way. I still have to finish reading it.

__2013-04-26	07:59:25__	Used ImageMagick Convert to change some assets from GIF to BMP.

__2013-04-26	07:59:36__	Running.... it runs but holy the frame rate is shitty.

__2013-04-26	08:27:09__	I reinstalled PyGame to use the PyGame for Lion Mac OSX. Now it runs, but it only runs if I'm moving the mouse in the window. That's odd.

__2013-04-26	08:27:31__	I downloaded Adobe Air and Pickle, a sprite editor. If you export as PNG, it gives you sprite pages. I don't know how to work with sprite pages though - tutorial time.

__2013-04-26	08:42:30__	Things you learn through compiler errors: images are their own thing, to get the actual "game" object you have to get a rect. Presumably there are ellipses and triangles in PyGame as well.

__2013-04-26	08:43:05__	The guy who wrote the example code for the [SpriteSheet on the Wiki](http://www.pygame.org/wiki/Spritesheet) didn't test his code. There's a problem with the spritesheet New call, and he didn't put the coordinates for image_at in a list.

__2013-04-26	08:45:20__	If you update the image of the rect, it seems to mess things up somehow. Not sure why yet.

__2013-04-26	08:45:59__	There's apparently an [animated sprite class](http://shinylittlething.com/2009/07/21/pygame-and-animated-sprites/).

__2013-04-26	08:48:32__	Before I learn to do animated sprites I probably should learn how to use ordinary sprites, since it appears to depend on them. It's probably a composition of Image and Rect.

__2013-04-26	08:48:55__	Time to go to work.

__2013-04-26	09:14:32__	Things I have to learn this weekend, probably in roughly priority order:

- Loading, using, and moving a sprite object
- Controlling an object with the keyboard
- Controlling an object with the mouse
- Learning the pygame real-time event model
- Background music
- Sprite animation
- Sound effects
- Collision detection
- Loading background images
- Loading levels/tile sets for levels


__2013-04-26	19:17:37__	The "chimp" example, as well as the "How do I move an image?" tutorials in the PyGame tutorials are really useful to get you understanding the fundamentals of how graphics and events work. Required reading for anyone doing PyGame without any knowledge of 2D graphics.

__2013-04-26	19:18:32__	I liked especially how chimp was pretty good OO design as well.

__2013-04-26	20:00:14__	Going up against organization and module issues in Python. Should have done everything in one code file. Especially can't figure out how to do class variables/class methods.

__2013-04-26	20:00:45__	Also forgot to turn on the timer, I have been programming now for about 50 minutes, so the total programming time will be whatever is on my timer + 50m.

__2013-04-26	20:10:09__	Things to remember in Python

To declare class variables/class methods:

    class C(object):
        i = os.path.join('hi','data') # This is a class variable

        @classmethod
        def do_stuff(cls):
          path_desc = "Hard drive: " + C.i
          return path_desc

    C.i
    C.do_stuff()

__2013-04-26	20:12:26__	Don't forget to check the types of your arguments if you get weird stack trace errors, they propagate down and down, kind of like missing semicolons in C.

__2013-04-26	21:36:22__	I was trying to find a way to get a text string on the screen that updates as you move the mouse, but I couldn't get it to blit properly and gave up for now.

__2013-04-26	21:36:55__	I need a vector class unless I want to do this stuff manually. So far it looks like Python doesn't have a handy vector class around.

__2013-04-26	22:10:23__	Borrowed a vector class from PyProcessing, basically the same vector that's used in Processing and in the Nature of Code. I should probably ensure that I always have this around.

__2013-04-26	22:10:49__	Also... curse you, tabs!

__2013-04-26	22:13:09__	And I learned some basic geometry again from here. http://answers.unity3d.com/questions/317648/angle-between-two-vectors.html Yeah I don't like math.

__2013-04-26	22:33:42__	Next challenge: How to make a tiled "map". Looking at http://sheep.art.pl/Tiled%20Map%20in%20PyGame for some information.

__2013-04-26	23:03:51__	That wasn't that useful. All I really want is a repeating graphic background. It seems like PyGame has good examples though. Darn it. I am thinking I should have just left everything in one file, in one class or something.

__2013-04-26	23:45:21__	Small victory: drew the backgrounds some hours ago now.

__2013-04-26	23:45:27__	Another small victory: found out about a "clamp" method that may be promising for making sure input doesn't leave a bounding box

__2013-04-27	07:38:16__	Last night I stopped around 12:30 midnight, today I resume. First lesson is to identify how to make the main character "shoot" a graphic laser that paints on the screen and looks like a brush stroke. Except Piet Mondrian's lines don't look like brush strokes, so I might actually be okay with hard edges.

__2013-04-27	07:43:19__	Decision: hard edges first, brush strokes later.

__2013-04-27	08:07:04__	I was going to work on shooting, but the bad mouse movement really bugged me. The solution? To divide the square into eights rather than to use quarters, and to use topleft, topright, bottomleft, bottomright to avoid clipping with the wall.

__2013-04-27	08:10:57__	Okay, that didn't fix the problem. I'm going to need something more fine-tuned.

__2013-04-27	08:13:30__	Solution to the mouse problem: clamp AFTER the mouse movement is assigned. I don't know now if some of the code above is function-less code. I think it might be but I'll leave it in since it seems to work. I'll do some runtime testing after the compo if I want to figure out if it actually helps. See characters.py:Cat.move()

__2013-04-27	08:14:26__	Now, back to FIRING MY LASERS

__2013-04-27	08:57:45__	Stop for breakfast

__2013-04-27	09:09:12__	Resume trying to figure out why my sprite won't draw anymore

__2013-04-27	09:13:53__	HA I figured it out. In your sprite class, you need to pass a self.containers argument to the superclass constructor to get the containers and the render of updates working.