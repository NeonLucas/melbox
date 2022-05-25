import tkinter as tk
import time
import random

"""
MECHANICS
1. You are the black box. you can move yourself using the wasd keys
2. The blue boxes are als called the "obstacles". They refresh after a set time... their rate of  refreshing changes
the longer you play. If you are inside one of these blue bars by the end of the refresh time it will be game 
over for you!
3. The small red boxes are points... your score increases when you collect one of these. To collect them simply
move over one of them.. every time you collect a point your score increases
4. the slightly larger green box is a time powerup. when you collect one of these the rate at which the blue bars
appear is extended so they appear slower
5. the yellow circle is the score power up. when you collect one of these the score increase everytimeyou pick up a point is doubled
permanently
6.the longer you spend in game the faster it gets
7.the game runs at 20 fps
8.in the beginning the bars refresh at a rate of once every 5 seconds and decrements exponentially
9.the goal of the game is to have the highest score(its supposed to be played by multiple people arcade style)
10.The game is easy.. as long as you identify the secret invisible obstacle waay more dangerous the blue bars
you can get a theoretically infinite score.. if the third obstacle the strongest of all dosent catch up to you
the third obstacle is mine to deal with while i have given you guys the first and second to deal with
"""


"""
1. positions can be made better identifiable...(done)
2. powerups(done)
3. balancing(needs to be tested)
4. bad powerups?(not a great idea)
5. time based events(1 done)
6. permanent highscore counter and a gui possibly??????
7. music??????????????????????????????????(need ideas)
8. more obstacles?(might be too hard for humans to proccess)(not needed)
9. ACTUALLY CONSIDER A FEVER SYSTEM
"""

def position():# updates position
	global pos
	pos = cnv.coords(plyr)

# graphics
def create_y():# create the horizontal bar
	global y_rect, y
	y = random.randint(0,10)*60
	y_rect = cnv.create_rectangle(0, y, 900, y + 60, fill = "blue", outline = "blue")

def create_x():# create the vertical bar
	global x_rect, x
	x = random.randint(0,14)*60
	x_rect = cnv.create_rectangle(x, 0, x + 60, 660, fill = "blue", outline = "blue") 

def breakboxes():# breaks old obstacle boxes
	cnv.delete(y_rect)
	cnv.delete(x_rect)


def scorebox():# creates scorebox (greed system)
	global point_box, x_scorebox, y_scorebox
	y_scorebox = random.randint(0,10)*60 + 15
	x_scorebox = random.randint(0,14)*60 + 15
	point_box = cnv.create_rectangle(x_scorebox, y_scorebox, x_scorebox + 30, y_scorebox + 30, fill = "red")


def create_cycle_powerbox():# creates the cycletime += 1 powerup
	global cycle_powerbox, x_cycle_powerbox, y_cycle_powerbox
	y_cycle_powerbox = random.randint(0,10)*60 + 10
	x_cycle_powerbox = random.randint(0,14)*60 + 10
	cycle_powerbox = cnv.create_rectangle(x_cycle_powerbox, y_cycle_powerbox, x_cycle_powerbox + 40, y_cycle_powerbox + 40, fill = "green")

def create_score_powerbox():# doubles the score you get for picking up a scorebox
	global score_powerbox, x_score_powerbox, y_score_powerbox
	y_score_powerbox = random.randint(0,10)*60 + 10
	x_score_powerbox = random.randint(0,14)*60 + 10
	score_powerbox = cnv.create_oval(x_score_powerbox, y_score_powerbox, x_score_powerbox + 40, y_score_powerbox + 40, fill = "yellow")


# systems
def scoresystem():# keeps track and checks if score is obtained
	global score

	if pos[1] == y_scorebox - 15 and pos[0] == x_scorebox - 15:
		score += scoremult
		cnv.delete(point_box)
		scorebox()
		l1.configure(text = "SCORE = " + str(score))


def cpower_check(): # does everything related to the  properties of cycletime powerup
	global cycletime, cpower_exist, cycle_power_time

	if cycle_power_time >= 3:
		cnv.delete(cycle_powerbox)
		cpower_exist = False

	if pos[1] == y_cycle_powerbox - 10 and pos[0] == x_cycle_powerbox - 10:
		cycletime += 1
		cnv.delete(cycle_powerbox)
		cycle_power_time = 0
		cpower_exist = False

def spower_check(): # does everything related to the properties of score powerup
	global scoremult, spower_exist, score_power_time

	if score_power_time >= 3.5:
		cnv.delete(score_powerbox)
		spower_exist = False

	if pos[1] == y_score_powerbox - 10 and pos[0] == x_score_powerbox - 10:
		scoremult = scoremult*2
		cnv.delete(score_powerbox)
		score_power_time = 0
		spower_exist = False


def highscore_sys():# displays highscore and does necessary global calls to use the highscore variable in other places
	global highscore

	highscore_file = open("highscore.txt", "r")
	highscore = int(highscore_file.read())
	highscore_file.close()

	l2.configure(text = "HIGHSCORE = "+str(highscore))

def death():# test death check system
	
	if pos[1] == y or pos[0] == x:
		l1.configure(text = "game over")
		win.update()

		if score > highscore:
			highscore_file = open("highscore.txt", "w")
			highscore_file.write(str(score))
			highscore_file.close()

		time.sleep(2.0)
		win.destroy()
	
	win.update()


def movement(event):# core movement system
	pos = cnv.coords(plyr)

	if event.char == "w" and pos[1] > 0:
		cnv.move(plyr, 0, -60)
	elif event.char == "s" and pos[3] < 660:
		cnv.move(plyr, 0, 60)
	elif event.char == "a" and pos[0] > 0:
		cnv.move(plyr, -60, 0)
	elif event.char == "d" and pos[2] < 900:
		cnv.move(plyr, 60, 0)
	elif event.char == "p":
		end = True
		pass
	
	win.update()


# window creation
win = tk.Tk()

# widget creation
cnv = tk.Canvas(win, height = 660, width = 900)
l1 = tk.Label(win, text = "SCORE = 0")
l2 = tk.Label(win, text = "")

l1.pack()
l2.pack()
cnv.pack()

# player
plyr = cnv.create_rectangle(420, 300, 480, 360, fill = "black")

# event binding
win.bind("<Key>", movement)

# game intitialization
cpower_exist = False # does cycle powerbox exist
spower_exist = False # does score powerbox exist 

highscore = 0
score = 0
t = 0
runtime = 0
cycletime = 5
scoremult = 1

cycle_power_time = 0
cycle_power_check_time = random.randint(0,5) + 60

score_power_time = 0
score_power_check_time = random.randint(0,10) + 10

highscore_sys()
position()
create_y()
create_x()
scorebox()

# game mainloop
while True:
	time.sleep(0.05)
	t += 0.05
	cycle_power_time += 0.05
	score_power_time += 0.05
	runtime += 0.05
	position()
	scoresystem()

	#time based event
	if runtime >= 360 and cycletime >= 2:
		cycletime = 2
	elif runtime >= 250 and cycletime >= 3:
		cycletime = 3
	elif runtime >= 180 and cycletime >= 4:
		cycletime = 4


	if cpower_exist:
		cpower_check()

	if spower_exist:
		spower_check()

	if score_power_time >= score_power_check_time and cycletime <= 3:
		create_score_powerbox()
		score_power_time = 0
		spower_exist = True
		cycle_power_check_time = random.randint(0,6) + 40

	if cycle_power_time >= cycle_power_check_time:
		create_cycle_powerbox()
		cycle_power_time = 0
		cpower_exist = True
		cycle_power_check_time = random.randint(0,5) + 20
	
	if t >= cycletime: # death checking and obstacle cycle
		death()
		breakboxes()
		create_y()
		create_x()
		t = 0
		cycletime -= 0.05

	win.update()
