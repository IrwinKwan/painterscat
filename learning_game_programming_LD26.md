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

__2013-04-27	10:33:36__	Trying to add in a "painted line". I'm now getting "invalid destination for blit" after adding in some code to try to expand the vertical height of the Surface image.

__2013-04-27	11:00:03__	Some success - the surface now grows properly and draws the lines moving up toward the top of the screen!

__2013-04-27	11:12:40__	Next step: to try to rotate the Cat to keep its feet on the "floor", because if this works, then I'd want to always start the painting at the bottomright of the Cat rect.

__2013-04-27	11:21:02__	Success: I had to reassign the surface after the transformation.

__2013-04-27	11:22:03__	I'd like to make it so that the cat faces the direction of the mouse cursor, but I think I'll work on the "shooting" mechanic first and try to get the core gameplay working at this point.

__2013-04-27	11:23:05__	Also: the rect doesn't seem to be rotated with the Surface, I probably have to rotate that too if I want the painting to start always from the cat's lower right side.

__2013-04-27	11:26:42__	This might work in the future, but the problem is that the rect is clamped and it appears that I can't just arbitrarily move that around too much. I will simply hardcode the cases for now, maybe seeing relative transforms is going to be more useful in other engines.

__2013-04-27	11:31:43__	Paint correctly grows from all directions now. I probably need to check at some point if they keep growing past the edges of the screen and lead to a crash though.

__2013-04-27	11:32:09__	I need to add something for the Paint to collide with before I can do collision detection. I will create some random painted Mondrian-style colours.

__2013-04-27	12:16:20__	The square successfully grows in size and kind of caps off around the screen edges. Good enough. Time to do square-based collision detection between the Paint and the Square.

__2013-04-27	12:16:46__	The ideal behaviour, eventually is that the paint will "overwrite" the square and actually cut it such that the half with the least area will disappear (after the line's crossed the square). Theoretically I should also stop the growing of the square as well when the paint contacts the square.

__2013-04-27	12:42:06__	I added in some collision detection and I magically seemed to have gotten a bunch of stuff for free, like the items are destroyed and a new square spawns. Technically if I started keeping score and added a win or lose condition I have an initial game!

__2013-04-27	13:50:50__	What am I going to do now.... the player death works. May be a good time to list some "summary statistics" for when the game is over.

__2013-04-27	14:41:19__	So even after 8 hours of working with PyGame, I still don't seem to truly understand surfaces, as I can't get my image title screen to load up yet.

__2013-04-27	14:57:11__	Apparently, PyGame doesn't like sprites with alpha transparencies. I have to do some extra processing to ensure that those load up properly. I'm going to try to replace the load_one_image with an alpha version before exporting my images again.

__2013-04-27	15:38:18__	Okay I am trying to get some "artistic noises" going on here. If only the firing sounds actually synced up with the collision sounds, I could probably calculate 120 bpm and ensure that sounds fire only on the beats

__2013-04-27	16:20:20__	I've finished both the scoreboard and the title screen. It's time to work on the most important part of the game.... gameplay. Specifically, the collision detection needs work, and then I can begin to implement some intended behaviours like the "painting over" of squares.

__2013-04-27	16:21:14__	Start Collision Detection Fixes now.

__2013-04-27	18:19:26__ This took me the better part of the last two hours to figure out collision detection. I ran into many barriers.

- When I was using my image, the top-left corner was masked to be transparent. **This was the biggest problem I had.** I did not realise this and this was making it seem like the collisions were occurring even though the entire thing was "white" i.e. transparent. LIES

- I learned a little bit about masks in the meantime. I think I'm going to need to use this if I want to do the collision of the paint line and the squares if the square contacts the "back" of a line. But I don't think I'll be able to get that implemented in time. I wasn't able to get the Pixel Perfect drag-and-drop working and I haven't yet tried to work with masking. Still, it seems like it's really easy overall as long as I get my graphics shit together.

- I eventually learned how to do the scale transform correctly. By default, it is locked on the top-left corner and grows to the right and down. You need to do a "rect.move_ip(posx - self.size/2, posy - self.size/2)" to shift the square back so it looks like it's in center.

__2013-04-27	18:23:24__	Moving on to other things... converting the square to different shades of Mondrian colors. Also, different colour squares need to grow at different rates.

__2013-04-27	19:01:34__	Stopping for dinner.

__2013-04-27	19:41:43__	Programming in the car!

__2013-04-27	19:42:00__	I want to work on the "cut" behavior of the lines on the squares.

__2013-04-27	22:26:04__	Okay I skipped the Cut behavior for now. The cat now animates.

    self.frame = pygame.time.get_ticks()
    self.image = self.images[self.frame//self.animation_cycle % 2]

where "2" is the number of frames available. Probably would be better to use "len(self.images)".

__2013-04-27	23:07:32__	Added code to ensure that the cat animates properly on all four sides of the grid. This was a lot of manual checks for conditions.

In general though I just had to remember that the cat only has two facing sides: left, and right, and depending on where the mouse moved and what wall he was on, the cat would face left or right (and the rotation would take care of the rest).

So for example, if he's on the LEFT wall, then moving up = "direction left" and down is "direction right". So you just have to set the LEFT image to the second two images in the images array, and the RIGHT image to the first two images in the images array.

Having a library for these kinds of 2D transformations would help me save a lot of time in a later version of game dev.

__2013-04-28	07:33:22__	I did a lot of work last night (until about 1 AM) trying to do the square splitting code. There are eight cases I'm going to have to work with and I don't know enough about computational geometry to make this work easily in PyGame. I suspect the secret would deal with matrix work and transforms, OpenGL style.

__2013-04-28	07:34:49__	For now, move onto something more pertinent, and also important: not having things spawn on top of each other. This could be REALLY slow code though if I'm writing it from scratch.

__2013-04-28	10:06:42__	Did music and new sound effects in OGG format. It's very rudimentary and not creative music. Orchestral, especially minimalist orchestral, isn't really my thing. True minimalism might have been a little more eccentric likely... but who knows.

__2013-04-28	14:13:25__	I've spent the last three to four hours coming up with the computations for cutting the geometry. A lot of it was spent coming up with a test bed to ensure the cuts worked fine, and then I fine-tuned the pixels so there's no whitespace between the lines and the squares.

__2013-04-28	14:14:11__	Some remaining things to do:

- Align the cat's paint to be dependent on where s/he's facing
- Identify where the audio pops are coming from

- Try to make the game more "fun"?


__2013-04-28	16:03:41__	Changing the cat's paint was easy.

__2013-04-28	16:03:46__	I ended up keeping score of "bounded boxes" and it's much more interesting now. However, there are still one-pixel off errors. I also want to make the lines that bound the boxes immutable like the immutable boxes are, so that when you're done you have a Mondrian-like painting.

__2013-04-28	17:08:36__	After spending a lot of time with rects and inflate.... inflate increases by an OFFSET. So inflate and inflate_ip increase or decrease with that value.... it's not a NEW width or height as in transform. :( This is a lesson learned from bad API documentation where statements are vague or depend on other areas.

__2013-04-28	17:46:55__	Figured out that game wasn't loading a sound file. No exception thrown, just a pop. So I added the file in.

__2013-04-28	17:47:12__	Need to compile a binary... this might be tight.

__2013-04-28	18:51:56__	Links to py2app:

Really good link here

http://stackoverflow.com/questions/5201133/py2app-built-app-displays-error-pygame-macosx-import-failed-on-other-machines

OK but less useful

http://stackoverflow.com/questions/5607121/how-do-i-use-py2app


__2013-04-28	21:38:46__	It was all submitted a few hours ago. Time to commit the last-minute changes I had to make in order to package it. I'll write up some instructions for py2exe as well as I work on that portion.

__2013-04-28	22:27:56__	Windows Python Executable:

1. Go to the [Installing Windows for Python page.](http://docs.python-guide.org/en/latest/starting/install/win/).

2. Download and install the Python 2.7 MSI (I didn't use the x64 version).

3. Ensure that you set up the Powershell variables

4. Get the ```python-distribute.py``` script.

	* Download it to your folder (ex. C:\Users\Kwan\Administrator\Downloads):
	* Run Powershell (go to Start Menu and in the search box type "powershell")
	* Type:
	
    cd ~/Downloads
    python python-distribute.py
    easy_install pip

5. Go to the [py2exe homepage](http://www.py2exe.org/). On the link to SourceForge, download the appropriate version of py2exe, which is likely the [Python 2.7 win32 version](http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/py2exe-0.6.9.win32-py2.7.exe/download).

6. 


__2013-04-28	23:15:51__	Maybe get binaries from a site like (http://www.lfd.uci.edu/~gohlke/pythonlibs/)? There seems to be an issue with pip install.

Seems you need a compiler for Windows. the GNU alternative is [here] (http://www.mingw.org/) which you should be able to [download here](http://sourceforge.net/projects/mingw/files/latest/download?source=files).


__2013-04-28	23:56:25__	You should use the official pygame installer from the pygame web site for Windows. Also, py2exe doesn't appear to have the same issue with import pygame._view that py2app has. Unfortunately the game seems to crash when you get to the score screen on Windows.

__2013-04-29	08:44:47__	After spending about three or four hours at this, I have finally managed to make PyGame/Python with data compile into Windows. Here's the brief rundown.

1. Use PyInstaller. It's more reliable at making Windows EXEs. (I haven't figured out how to make it work in Mac yet).

2. Include these secret lines of code around every file name:

	def resource_path(relative):
	    if hasattr(sys, "_MEIPASS"):
	        return os.path.join(sys._MEIPASS, relative)
	    return os.path.join(relative)
		
Example:

	filename = 'freesansbold.ttf'
	myfontfile = resource_path(os.path.join(data_dir, filename)

3. Include the font file! Don't use ```None``` in the code.

4. When you run pyinstaller, first create the .spec file by running it normally with the --onefile option. Then, go into the spec file, and modify the EXE section to add the following line:

	Tree('C:\\Users\\Administrator\\Documents\\painterscat\\data', prefix='\\data')
	
The result should look something like this:

	exe = EXE(pyz,
	          a.scripts,
	          a.binaries,
	          a.zipfiles,
	          a.datas,
	          Tree('C:\\Users\\Administrator\\Documents\\painterscat\\data', prefix='\\data'),
	          name=os.path.join('dist', 'painterscat.exe'),
	          debug=False,
	          strip=None,
	          upx=True,
	          console=True )

5. Run pyinstaller again. Give the spec file as the argument (ex: ```python C:\pyinstaller\pyinstaller.py --onefile painterscat.spec```)

6. You should have an .EXE in your dist folder ready to go.
	