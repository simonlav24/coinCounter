#import math
import random
import pygame
from pygame import gfxdraw
import colorsys
import cv2
from math import pi, cos, sin
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
	return (ans[0], ans[1], int((ans[2]/255)*100))
	
def hsv2rgb(h,s,v):
	h/=100
	s/=100
	v/=100
	return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def draw_circle(pos,rad,col):
	pygame.gfxdraw.aacircle(win, int(pos[0]), int(pos[1]), rad, col)
	pygame.gfxdraw.filled_circle(win, int(pos[0]), int(pos[1]), rad, col)

def fill(Surf, Point, Color, t1, t2):
	arr = pygame.surfarray.array3d(Surf)    # copy array from surface
	swapPoint = (Point[1], Point[0])        # swap X and Y
	cv2.floodFill(arr, None, swapPoint, Color, (t1,t1,t1,t1), (t2,t2,t2,t2))
	pygame.surfarray.blit_array(Surf, arr)




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
	# if is_in_circle(pos):
		# color_str = "true"
		# color_sur = myfont.render(color_str, False, (255, 0, 0))
		# win.blit(color_sur, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+25))
	color_str = "d1= " + str(d1) + "      d2= " + str(d2)
	color_sur = myfont.render(color_str, False, (255, 0, 0))
	win.blit(color_sur, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+25))

def is_in_circle(pos):
	for circle in circles_found:
		if ((pos[0] - circle[0])**2 + (pos[1] - circle[1])**2 ) < (circle[2] + radius_border)**2:
			return True

def find_first_point():
	#win.blit(image, (0,0))#visual
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
				return [x,y,0]
			#draw_circle((x,y),1,(255,0,0))#visual
			#pygame.display.update()#visual
			
	return [-1,0,0]
			
def check_by_radius(pos, radius):
	d_start = pi/2
	d_end = 2.5*pi
	dx = 0.1
	d = d_start
	list = []
	diff = 90
	while d < d_end:
		d += dx
		pos_check = (int(radius * cos(d) + pos[0]), int(radius * sin(d) + pos[1] + radius))
		pygame.draw.circle(win, (255,0,0), pos_check, 5)#visual
		pygame.display.update()#visual
		color = image.get_at(pos_check)
		list.append(color)
	large_pixels = sum(map(lambda x : x == (0,255,0), list))
	small_pixels = sum(map(lambda x : x != (0,255,0), list))
	if large_pixels > small_pixels:
		return True
	return False

def check_for_circle(pos, radius_min, radius_max):
	for radius in range(radius_min, radius_max):
		if check_by_radius(pos, radius):
			return radius
			
def check_for_circles():
	while True:
		point = find_first_point()
		if point[0] == -1:
			break
		rad = check_for_circle(point, 20, 100)
		point[2] = rad
		circles_found.append([point[0], point[1] + point[2], point[2]])

pygame.time.delay(10)

# pygame.display.update()
# first_point = find_first_point()
# rad = check_for_circle(first_point, 1, 50)
# first_point[2] = rad

# circles_found.append([first_point[0], first_point[1]+first_point[2], first_point[2]])
# print(circles_found)

# win.blit(image, (0,0))
# draw_circle((first_point[0], first_point[1]+first_point[2]), first_point[2], (255,0,0,100))
# pygame.display.update()

# second_point = find_first_point()
# rad = check_for_circle(second_point, 1, 50)
# second_point[2] = rad
# circles_found.append([second_point[0], second_point[1]+second_point[2], second_point[2]])

# print(circles_found)

fill(image, (0,0), (0,255,0), 15, 100)
win.blit(image, (0,0))
check_for_circles()
print(circles_found)


#print(rad)
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
		d1 += 1
	if keys[pygame.K_e]:
		d1 -= 1
	if keys[pygame.K_a]:
		d2 += 1
	if keys[pygame.K_d]:
		d2 -= 1
	
	#background:
	win.blit(image_org, (0,0))
	
	#step:
	
	#image_2 = image.copy()
	#fill(image_2, (0,0), (255,255,255), 15, 100)
	#win.blit(image_2, (0,0))
	
	show_mouse_color()
	#show_mouse_stat()
	
	for circle in circles_found:
		draw_circle(circle, circle[2], (255,0,0,100))
	# draw_circle((first_point[0], first_point[1]+first_point[2]), first_point[2], (255,0,0,100))
	# draw_circle((first_point[0], first_point[1]+first_point[2]), first_point[2]+20, (255,0,0,100))
	
	
	
	pygame.display.update()
pygame.quit()














