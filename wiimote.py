import cwiid, time
import Tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=600, borderwidth=0, highlightthickness=0, bg="black")
canvas.pack()

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)


tk.Canvas.create_circle = _create_circle
posx = 200
posy = 200
curr_size = 20
circle1 = canvas.create_circle(posx, posy, curr_size, fill="SlateBlue4")
circle2 = canvas.create_circle(posx, posy, curr_size, fill="tomato")

root.wm_title("Object Position based on Wiimote")

#Wii Part
print 'Please press buttons 1 + 2 on your Wiimote now ...'
time.sleep(1)

# This code attempts to connect to your Wiimote and if it fails the program quits
try:
  wii=cwiid.Wiimote()
except RuntimeError:
  print "Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!"
  quit()

print 'Wiimote connection established!\n'
print 'Go ahead and press some buttons\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'

time.sleep(3)
wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC  | cwiid.RPT_IR

while True:
	prev_x = posx
	prev_y = posy
	root.wm_title("Object Position based on Wiimote")
	buttons = wii.state['buttons']
	
	valid_src = False
	count = 0;
	for src in wii.state['ir_src']:
		count += 1
		if src:
			valid_src = True
			posx = int(src['pos'][0])			
			posy = int(src['pos'][1])
			change_posx = posx - prev_x
			change_posy = posy - prev_y
			# canvas.move(circle, change_posx, change_posy)

			# x = canvas.canvasx(change_posx)
			# y = canvas.canvasy(change_posy)
			if(count == 1):
				print 'x1:', posx,' y1:', posy
				canvas.move(circle1, change_posx, change_posy)
			elif(count == 2):
				print 'x2:', posx,' y2:', posy
				canvas.move(circle2, change_posx, change_posy)	
			else:
				print(posx, posy)	
			root.update()
		if not valid_src:
			print 'no sources detected'
	# current_position_x = wii.state['acc'][cwiid.X]
	# current_position_y = wii.state['acc'][cwiid.Y]
	# current_position_z = wii.state['acc'][cwiid.Z]
	# print('Acc: x=%d y=%d z=%d' % (current_position_x, current_position_y, current_position_z))
	time.sleep(0.3)
  
	# Detects whether + and - are held down and if they are it quits the program
	if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
		print '\nClosing connection ...'
		# NOTE: This is how you RUMBLE the Wiimote
		wii.rumble = 1
		time.sleep(1)
		wii.rumble = 0
		exit(0)


