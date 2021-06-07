from tkinter import *
from core import *
from tkinter import filedialog
from PIL import Image, ImageTk


class MyInterface:
	fileName = ''
	classP = ImageLoad()
	window = Tk()
	scale_top = object
	scale_bot = object
	dis = True
	photo_frame = object
	photo = object
	var = IntVar()
	var_l = IntVar()
	area_v = object
	line_lengh = object



	def start_ch(self, value): #Обновление картинки при движении ползунка
		self.var.set(1)
		
		self.classP.dark_b = self.scale_bot.get()
		self.classP.light_b = self.scale_top.get()
		self.classP.findCanny()
		img = Image.open('tempimg.jpg')
		img = ImageTk.PhotoImage(img)
		self.photo.destroy()
		self.photo = Label(master = self.photo_frame, image = img)
		self.photo.image = img
		self.photo.pack()
		self.area.delete('1.0', 'end')
		self.line_lengh.delete('1.0', 'end')
		self.ploshad_text.delete('1.0', 'end')
		self.area.insert(1.0, self.classP.area_arr)
		self.ploshad_text.insert(1.0, self.classP.ploshad)
		self.line_lengh.insert(1.0, self.classP.lengh_arr)



	def start(self): #запуск при нажатие на загрузить
		self.var.set(1)
		self.scale_top['state'] = 'active'
		self.scale_bot['state'] = 'active'
		self.fileName = filedialog.askopenfilename()
		if self.fileName == '':
			return 0
		if self.photo != object:
			self.photo.destroy()
		self.classP.auto_canny(self.fileName)
		
		img = Image.open('tempimg.jpg')
		img = ImageTk.PhotoImage(img)
		self.photo = Label(master = self.photo_frame, image = img)
		self.photo.image = img
		self.photo.pack()
		self.scale_top.set(self.classP.light_b)
		self.scale_bot.set(self.classP.dark_b)
		self.dis = False
		self.area.delete('1.0', 'end')
		self.line_lengh.delete('1.0', 'end')
		self.ploshad_text.delete('1.0', 'end')
		self.area.insert(1.0, self.classP.area_arr)
		self.ploshad_text.insert(1.0, self.classP.ploshad)
		self.line_lengh.insert(1.0, self.classP.lengh_arr)
		

	def start_line(self):
		if self.var_l.get() == 0:
			self.classP.Central_line()
			self.start_ch(1)
			img = Image.open('lines.jpg')
			img = ImageTk.PhotoImage(img)
			self.photo.destroy()
			self.photo = Label(master = self.photo_frame, image = img)
			self.photo.image = img
			self.photo.pack()
		else:
			self.change()
		

	def change(self):
		if self.photo != object:
			self.photo.destroy()
		if self.var.get() == 0:
			img = Image.open(self.fileName)
		else:
			if self.var_l.get() == 0:
				img = Image.open('lines.jpg')
			else:
				img = Image.open('tempimg.jpg')
		img = ImageTk.PhotoImage(img)
		self.photo = Label(master = self.photo_frame, image = img)
		self.photo.image = img
		self.photo.pack()


	def __init__(self):
		self.var_l.set(1)
		self.window.title("Программа")
		self.window.attributes('-fullscreen', True)
		top_menu = Frame(master = self.window, bg = 'grey', relief = 'raised', bd = '1')
		top_menu.place(relwidth=1, relheight=0.05)

		exit_button = Button(master = top_menu,text = 'Выход', command = click_exit)
		exit_button.place(relwidth = 0.1, relheight = 0.8, relx = 0.88, rely = 0.1)
		load_button = Button(master = top_menu, text = 'Загрузить', command = self.start)
		load_button.place(relwidth = 0.1, relheight = 0.8, x = 20, rely = 0.1)

		self.photo_frame = Frame(master = self.window)
		self.photo_frame.place(relwidth = 0.7, relheight = 0.95, rely = 0.05)

		parametr_frame = Frame(master = self.window, bg = 'grey')
		parametr_frame.place(relwidth = 0.3, relheight = 0.95, rely = 0.05, relx = 0.7)

		label_top = Label(parametr_frame, text='Верхняя граница')
		label_top.pack(pady=15)
		self.scale_top = Scale(parametr_frame, from_=0, to=255, orient='horizontal',length = 300,command = self.start_ch)
		self.scale_top.pack(side=TOP)

		label_bot = Label(parametr_frame, text='Нижняя граница')
		label_bot.pack(pady = 15)
		self.scale_bot = Scale(parametr_frame, from_=0, to=255, orient='horizontal',length = 300, command = self.start_ch)
		self.scale_bot.pack(side=TOP)
		if self.dis == True:
			self.scale_top['state'] = 'disabled'
			self.scale_bot['state'] = 'disabled'

		radio_orig = Radiobutton(parametr_frame, text='Оригинал', variable = self.var, value = 0, command = self.change)
		radio_change = Radiobutton(parametr_frame, text='Измененная',variable = self.var, value = 1,  command = self.change)
		radio_orig.place(relx=0.13, rely = 0.3)
		radio_change.place(relx=0.35, rely = 0.3)

		check_lines = Checkbutton(parametr_frame, text='Средние линии', variable=self.var_l, onvalue = 0, offvalue = 1, command = self.start_line)
		check_lines.place(relx=0.6, rely = 0.3)

		label_area = Label(parametr_frame, text='Площади', bg='grey')
		label_area.place(x = 3, rely = 0.35)
		self.area = Text(parametr_frame ,width = 50, height = 10)
		self.area.place(x = 3, rely = 0.375)
		label_v = Label(parametr_frame, text='Общая площадь=', bg = 'grey')
		label_v.place(x=3, rely=0.6)
		self.ploshad_text = Text(parametr_frame,width=20, height = 1, bg='grey')
		self.ploshad_text.place(x = 110, rely=0.6)

		label_lines = Label(parametr_frame, text='Длины линий', bg = 'grey')
		label_lines.place(x = 3, rely=0.63)
		self.line_lengh = Text(parametr_frame, width = 50, height = 10)
		self.line_lengh.place(x = 3, rely=0.655)
		


		self.window.mainloop()