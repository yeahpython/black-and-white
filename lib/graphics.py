bw = 30
bh = 30

world_tw = 0
world_th = 0
world_w = "lmfao"
world_h = "chrchr"
world_size = (world_w, world_h)

def load(file_in):
	file_descriptor = open(file_in)
	lines = file_descriptor.readlines()
	extract_dimensions(lines)
	file_descriptor.close()

def extract_dimensions(lines):
	global world_th, world_tw, world_w, world_h, world_size
	world_th = len(lines)-1
	world_tw = len(lines[-1])
	world_w = world_tw * bw
	world_h = world_th * bh
	world_size = (world_w, world_h)

#world_w = world_tw * bw
#world_h = world_th * bh
#world_size = (world_w, world_h)

screen_w = 1920
screen_h = 1080
screen_size = (screen_w, screen_h)

border_thickness = 0
rightborder_thickness = 600

top_space = border_thickness

disp_w = screen_w - 2*(border_thickness) - rightborder_thickness
disp_h = screen_h - top_space - border_thickness
disp_size = (disp_w, disp_h)


#background = [0,0,50]#(80, 128, 75)
#foreground = [100, 120, 150]
#outline = [80,255,100]

skin = 4

#Note that player currently uses the fact that only
# background is black to check if the feet are supported
#boring but functional
background = [0,0,0]
foreground = [30, 30, 30]
outline = [255,255,255]
creature = [100,0,100]

if skin == 1:
	#sunny day with clouds
	background = [12,122,247]
	foreground = [255, 255, 255]
	outline = [50,200,255]
	creature = [0, 0, 0]

elif skin == 2:
	#sunny day with trees
	background = [12,122,247]
	foreground = [97, 145, 19]
	outline = [255, 255, 255]

elif skin == 3:
	#morning-suitable view
	background = [255,255,255]
	foreground = [12,122,247]
	outline = [0,0,0]

elif skin == 4:
	background = [0,0,0]
	foreground = [200, 200, 200]
	outline = [0,0,0]
	creature = [0,255,0]

CLEAR_SCREEN = 0
REDRAW_ROOM = 0

colorcycle = [(0, 0, 255), (0, 255, 255), (0, 255, 0), (255, 0, 0), (255, 0, 255),]
colorcycle2 = [(255,55,155)]#[(100, 230, 230)]

