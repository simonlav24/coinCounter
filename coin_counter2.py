#import math
import random
import pygame
from pygame import gfxdraw
import colorsys
import cv2
from math import pi, cos, sin, fabs
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 12)

dim = (853, 480)
image = pygame.image.load("coins.jpg")
image = pygame.transform.scale(image, dim)
image_org = image.copy()
# image = pygame.transform.threshold(image, surf, search_color, threshold=(0,0,0,0), set_color=(0,0,0,0))
#pygame.Surface.get_at #get color value on signel circle

#image = pygame.transform.laplacian(image)

win_width = dim[0]
win_height = dim[1]
win = pygame.display.set_mode((win_width,win_height))

def rgb2hsv(color):
	ans = colorsys.rgb_to_hsv(color[0], color[1], color[2])
	return (int(ans[0]*100), int(ans[1]*100), int((ans[2]/255)*100))
	
def hsv2rgb(h,s,v):
	h/=100
	s/=100
	v/=100
	return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def draw_circle(pos,rad,col):
	pygame.gfxdraw.aacircle(win, int(pos[0]), int(pos[1]), rad, col)
	pygame.gfxdraw.filled_circle(win, int(pos[0]), int(pos[1]), rad, col)

def write_on(pos, text, col):
	color_sur = myfont.render(text, False, col)
	win.blit(color_sur, pos)

def fill(surf, point, color, t1, t2):
	arr = pygame.surfarray.array3d(surf)    # copy array from surface
	swapPoint = (point[1], point[0])        # swap X and Y
	cv2.floodFill(arr, None, swapPoint, color, (t1,t1,t1,t1), (t2,t2,t2,t2))
	pygame.surfarray.blit_array(surf, arr)
	return surf
	
def image_procces(surf):
	arr = pygame.surfarray.array3d(surf)
	corner_colors_rgb = (surf.get_at((1,1)), surf.get_at((dim[0]-1,1)), surf.get_at((1,dim[1]-1)), surf.get_at((dim[0]-1,dim[1]-1)))
	corner_colors_hsv = (rgb2hsv(corner_colors_rgb[0]), rgb2hsv(corner_colors_rgb[1]), rgb2hsv(corner_colors_rgb[2]), rgb2hsv(corner_colors_rgb[3]))
	print(corner_colors_hsv)
	steps = 50
	thresh = 50
	for i in range(steps):
		x,y = random.randint(1,dim[0]-1), random.randint(1,dim[1]-1)
		color_at_place = rgb2hsv(surf.get_at((x,y)))
		count = 0
		for corner in corner_colors_hsv:
			if fabs(color_at_place[0] - corner[0]) <= thresh:
				count += 1
			if fabs(color_at_place[1] - corner[1]) <= thresh:
				count += 1
			if fabs(color_at_place[2] - corner[2]) <= thresh:
				count += 1
		print(count)
		
		
		
	
	
	
def threshold(surf, amount):
	pygame.transform.threshold(surf, surf, (0,0,0), (amount, amount, amount, amount), (255,0,0,255))
	return surf
	




################################################################################ Setup:
circles_found = []
radius_border = 5
def show_mouse_color():
	color = rgb2hsv(image.get_at(pygame.mouse.get_pos()))
	color_str = str(color)
	color_sur = myfont.render(color_str, False, (255, 0, 0))
	win.blit(color_sur, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+25))
	
def show_mouse_stat():
	pos = pygame.mouse.get_pos()
	color_str = "d1= " + str(d1) + "      d2= " + str(d2)
	color_sur = myfont.render(color_str, False, (255, 0, 0))
	win.blit(color_sur, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+25))
	
def show_mouse_result():
	pos = pygame.mouse.get_pos()
	color_str = "Total circles: " + str(len(circles_found))
	color_sur = myfont.render(color_str, False, (255, 0, 0))
	win.blit(color_sur, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+25))

def is_in_circle(pos):
	for circle in circles_found:
		if ((pos[0] - circle[0])**2 + (pos[1] - circle[1])**2 ) < (circle[2] + radius_border)**2:
			return True

def find_first_point():
	win.blit(image, (0,0))#visual
	if len(circles_found) > 0:
		last_pos = (circles_found[-1][0], circles_found[-1][1]-circles_found[-1][2])
	else:
		last_pos = (0,0)
	for y in range(last_pos[1], dim[1]):
		for x in range(dim[0]):
			if is_in_circle((x,y)):
				continue
			#get pixel color:
			color = image.get_at((x,y))
			#if not background return upper part
			if color != (0,255,0):
				root = (x,y)
				d = 0
				while True:
					# win.fill((0,0,0), ((x,y+d), (1, 1)))#visual
					# pygame.display.update()#visual
					# pygame.time.wait(10)#visual
					col = image.get_at((x,y + d))
					if col == (0,255,0):
						height = d
						break
					d += 1
				y_center = int(y + height/2)
				d = 1
				while True:
					# win.fill((0,0,0), ((x+d,y_center), (1, 1)))#visual
					# pygame.display.update()#visual
					# pygame.time.wait(10)#visual
					col_right = image.get_at((x + d,y_center))
					if col_right == (0,255,0):
						right = d
						break
					d += 1
				d = 1
				while True:
					# win.fill((0,0,0), ((x-d,y_center), (1, 1)))#visual
					# pygame.display.update()#visual
					# pygame.time.wait(10)#visual
					col_left = image.get_at((x - d,y_center))
					if col_left == (0,255,0):
						left = d
						break
					d += 1
				x_center = int((x-left) + (left+right)/2)
				#ready to return:
				rad = int((left+right)/2)
				if rad > 20:
					return (x_center, y_center, int((left+right)/2))
			#draw_circle((x,y),1,(255,0,0))#visual
			#pygame.display.update()#visual
	return [-1,0,0]
			
def check_for_circles():
	while True:
		point = find_first_point()
		if point[0] == -1:
			break
		circles_found.append([point[0], point[1], point[2]])

#pygame.time.delay(10)

# fill(image, (0,0), (0,255,0), 15, 100)
# win.blit(image, (0,0))
# check_for_circles()

image_procces(image)

d1 = 0
d2 = 0
process_fin = False

################################################################################ Main Loop:
run = True
while run:
	#pygame.time.delay(1)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False
	if keys[pygame.K_q]:
		if d1 < 255:
			d1 += 1
	if keys[pygame.K_e]:
		if d1 > 0:
			d1 -= 1
	if keys[pygame.K_a]:
		d2 += 1
	if keys[pygame.K_d]:
		d2 -= 1
	
	#background:
	# win.blit(image_org, (0,0))
	win.blit(image, (0,0))
	
	#step:
	
	# image_2 = image_org.copy()
	# image_2 = threshold(image_2,d1)
	# image_2 = fill(image_2, (0,0), (255,0,0), d1, d2)
	# win.blit(image_2, (0,0))
	
	show_mouse_color()
	#show_mouse_stat()
	#show_mouse_result()
	
	for circle in circles_found:
		#draw_circle(circle, circle[2], (255,0,0,100))
		write_on((circle[0],circle[1]), str(circles_found.index(circle)+1), (0,0,255))
	
	
	
	pygame.display.update()
pygame.quit()














