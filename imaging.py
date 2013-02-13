#!/usr/bin/python
import Image, ImageTk
import Tkinter
from sys import argv
import numpy
import random
import math, random, time
from os import path

OUTPUT_FILE = "output.png"

#Ruido sal y pimienta, aplicando pixeles negros y blancos al azar
#Parametro
#-im Objeto de la clase PIL con la pix a aplicar el ruido
#-intensidad Porcentaje de pixeles sobre el total que seran sal y pimienta.
#-pol Rango de polarizacion que determina que tan blancos o que tan negros
#		 son los puntos.
def sal_y_pimienta(im, intensidad, pol):
	w, h = im.size
	pix = im.load()
	n = w*h
	n = int(intensidad*(n/100))
	i = 0
	if im.mode == "RGB":
		while i != n:
			x, y = random.randint(0, w - 1), random.randint(0, h - 1)
			det = random.randint(0, 1)
			if det == 1:
				sal = random.randint(255-pol, 255)
				pix[x, y] = (sal, sal, sal)
			else:
				pim = random.randint(0, pol)
				pix[x, y] = (pim, pim, pim)
			i += 1

	if im.mode == "L":
		while i != n:
			x, y = random.randint(0, w - 1), random.randint(0, h - 1)
			det = random.randint(0, 1)
			if det == 1:
				sal = random.randint(255-pol, 255)
				pix[x, y] = sal
			else:
				pim = random.randint(0, pol)
				pix[x, y] = pim
			i += 1

	im.save("output.png", "png")
	return im

#Eliminacion del ruido sal y pimienta, usando una combinacion entre promedio y umbrales
#Parametros
#-im Objeto de la libreria PIL con la pix a la cual se eliminara el ruido.
#-umb Umbral que determinara en que rangos de pixeles se aplicara la eliminacion de ruido.
def des_sal_y_pimienta(im, umb):
	w, h = im.size
	pix = im.load()
	salypimienta = []
	for i in range(umb):
		salypimienta.append((i, i, i))
		salypimienta.append((i))
	for i in range(255-umb, 255):
		salypimienta.append((i, i, i))
		salypimienta.append((i))
	if im.mode == "RGB":
		for i in range(w):
			for j in range(h):
				prom = []
				if pix[i, j] in salypimienta:
					if i > 0: prom.append(list(pix[i-1, j]))
					if i < w-1: prom.append(list(pix[i+1, j]))
					if j < h-1: prom.append(list(pix[i, j+1]))
					if j > 0: prom.append(list(pix[i, j-1]))
					col_totals = [ sum(x) for x in zip(*prom) ]
					pix[i, j] = col_totals[0]/len(prom), col_totals[1]/len(prom), col_totals[2]/len(prom)
		im.save(OUTPUT_FILE, "png")
	elif im.mode == "L":
		output = Image.new("L", (w, h))
		out_pix = output.load()
		for i in range(w):
			for j in range(h):
				prom = []
				if pix[i, j] in salypimienta:
					if i > 0: prom.append(pix[i-1, j])
					if i < w-1: prom.append(pix[i+1, j])
					if j < h-1: prom.append(pix[i, j+1])
					if j > 0: prom.append(pix[i, j-1])
					pix[i, j] = sum(prom)/len(prom)
		im.save(OUTPUT_FILE, "png")
	return im

#Convertir a grayscale
#Parametros
#image Objeto de la libreria PIL con la pix a convertir.
#filt Filtro a usar("prom" para promedio, "max" para mayor", "min" para menor)
def to_grayscale(image, filt):
	w, h = image.size
	pix = image.load()
	output = Image.new("RGB", (w, h))
	out_pix = output.load()
	for i in range(w):
		for j in range(h):
			curr = pix[i, j]
			if filt == "prom":
				prom = (curr[0] + curr[1] + curr[2]) / 3
				out_pix[i, j] = prom, prom, prom
			if filt == "max":
				max_ = max(curr)
				out_pix[i, j] = max_, max_, max_
			if filt == "min":
				min_ = min(curr)
				out_pix[i, j] = min_, min_, min_
	output.save(OUTPUT_FILE, 'PNG')
	return output

#Conversion a pix binarizada
#Parametros
#image Objeto de la libreria PIL con la pix a convertir
#umb Umbral de decision para convertir a 0 o 255
def to_binary(image, umb):
	w, h = image.size
	pix = image.load() 
	output = Image.new("RGB", (w, h))
	out_pix = output.load()
	for i in range(w):
		for j in range(h):
			if image.mode == "RGB":
				if max(pix[i, j]) >= umb: out_pix[i, j] = (255, 255, 255)
				else: out_pix[i, j] = (0, 0, 0)
			elif image.mode == "L":
				if pix[i, j] >= umb: out_pix[i, j] = 255
				else: out_pix[i, j] = 0
	output.save(OUTPUT_FILE, 'PNG')
	return output

#Aplicacion de blur ("borrosidad") a una pix
#Parametro
#image Objeto de la libreria PIL con la pix a la que se aplicara blur
#n Numero de veces que se le aplicara el efecto
def blur(image, n):
	w, h = image.size
	pix = image.load() 
	output = Image.new("RGB", (w, h))
	out_pix = output.load()
	for k in range(n):
		for i in range(w):
			for j in range(h):
				prom = []
		 		prom.append(list(pix[i, j]))
				if i > 0: prom.append(list(pix[i-1, j]))
				if i < w-1: prom.append(list(pix[i+1, j]))
				if j < h-1: prom.append(list(pix[i, j+1]))
	 			if j > 0: prom.append(list(pix[i, j-1]))
				col_totals = [ sum(x) for x in zip(*prom) ]
	 			out_pix[i, j] = col_totals[0]/len(prom), col_totals[1]/len(prom), col_totals[2]/len(prom)
	output.save(OUTPUT_FILE, "png")
	return output

#Normalizacion de la pix para fijar los pixeles dentro de un rango
#entre el pixel mayor y menor.
#Parametros
#-im Objeto de la libreria PIL con la pix a normalizar
def normalize(im):
	w, h = im.size
	pix1 = im.load()
	im2 = Image.new("RGB", (w, h))
	pix2 = im2.load()
	max_ = 0
	min_ = 256
	for i in range(w):
		for j in range(h):
			if pix1[i, j][0] > max_:
				max_ = pix1[i, j][0]
			if pix1[i, j][0] < min_:
				min_ = pix1[i, j][0]
	#print max_, min_
	prop = 256.0/(max_ - min_);
	for i in range(w):
		for j in range(h):
			curr = int(math.floor((pix1[i, j][0] - min_)*prop))
			pix2[i, j] = curr, curr, curr
	im2.save(OUTPUT_FILE, "png") 
	return im2 

#Diferencia entre dos pixes, restando los pixeles de una a otra.
#Parametros
#-im1 pix original a la cual se restaran pixeles.
#-im2 pix que se restara a la original.
def contornos(im1, im2):
	pix1 = im1.load()
	pix2 = im2.load()
	w, h = im1.size
	im3 = Image.new('RGB', im1.size)
	pix3 = im3.load()
	for i in range(w):
		for j in range(h):
			pix3[i, j] = (pix1[i, j][0] - pix2[i, j][0], \
										pix1[i, j][1] - pix2[i, j][1], \
										pix1[i, j][2] - pix2[i, j][2])
	im3.save(OUTPUT_FILE, 'png')
	return im3

def zeros(n, m):
	matrix = []
	for i in range(n):
		curr = []
		for j in range(m):
			curr.append(0)
		matrix.append(curr)
	return matrix

def convolucion(im, g):
	w, h = im.size
	pix = im.load()
	out_im = Image.new("RGB", (w, h))
	out = out_im.load()
	for i in xrange(w):
		for j in xrange(h):
			suma = 0
			for n in xrange(i-1, i+2):
				for m in xrange(j-1, j+2):
						if n >= 0 and m >= 0 and n < w and m < h:
							suma += g[n - (i - 1)][ m - (j - 1)] * pix[n, m][1]
			out[i, j] = suma, suma, suma
	out_im.save("output.png", "png")
	return out_im


def bfs(im, origen, color):
	cola = []
	cola.append(origen)
	pix = im.load()
	original = pix[origen]
	w, h = im.size
	n = 0
	xs = []
	ys = []
	while len(cola) > 0:
		(x, y) = cola.pop(0)
		#print 'pop'
		actual = pix[x, y]
		if actual == original or actual == color:
			#print x, y
			for dx in [-1, 0, 1]:
				for dy in [-1, 0, 1]:
					candidato = (x + dy, y + dx)
					if candidato[0] >= 0 and candidato[0] < w and \
									candidato[1] >= 0 and candidato[1] < h:
						contenido = pix[candidato[0], candidato[1]]
						if contenido == original:
							pix[candidato[0], candidato[1]] = color
							xs.append(candidato[0])
							ys.append(candidato[1])
							n += 1
							cola.append(candidato)
	im.save(OUTPUT_FILE, 'png')
	return n, xs, ys

def find_max(array):
	maxim = 0.0
	max_id = 0
	for i in range(len(array)):
		if array[i][0] > maxim:
			maxim = array[i][0]
			max_id = i
	return max_id

def classify_forms(im):
	w, h = im.size
	#im = to_binary(im, 127)
	total = w*h
	porcentajes = []
	centroids = []
	cont = 0
	pix = im.load()
	for i in range(w):
		for j in range(h):
			if pix[i, j] == (0, 0, 0):
				r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
				n, x, y = bfs(im, (i, j), (r, g, b))
				centroids.append((sum(x) / len(x), sum(y) / len(y)))
				porcentajes.append([float(n)/float(total), (r, g, b)])
				print "Pintando figura %s"%cont
				cont += 1
	fondo_id = find_max(porcentajes)
	max_color = porcentajes[fondo_id][1]
	print "Pintando fondo"
	for i in range(w):
		for j in range(h):
			if pix[i, j] == max_color:
				pix[i, j] = (150, 150, 150)
	print "Pintando centros de masa"
	for i in range(len(centroids)):
		if i == fondo_id:
			pix[centroids[i]] = (255, 0, 0)
		else:
			pix[centroids[i]] = (0, 0, 0)
	im.save(OUTPUT_FILE, 'png')
	cont = 0
	for p in porcentajes:
		print "Porcentaje de la figura ID %s: %.2f"%(cont, p[0]*100.0)
		cont += 1
	return im, centroids

def callback_classify():
	global WORKING_IMAGE
	WORKING_IMAGE, centroids = classify_forms(WORKING_IMAGE)
	w, h = WORKING_IMAGE.size
	canvas.config(width = w, height = h)
	photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
	label.config(image = photo)
	label.image = photo
	i = 0
	for center in centroids:
		dx, dy = center[0], center[1]
		Tkinter.Label(canvas, text = 'Objeto %d'%i).place(x = dx, y = dy)
		i += 1

def callback_blur():
	print "flip"
	global WORKING_IMAGE
	WORKING_IMAGE = blur(WORKING_IMAGE, 10)
	w, h = WORKING_IMAGE.size
	canvas.config(width = w, height = h)
	photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
	label.config(image = photo)
	label.image = photo

def callback_grayscale():
	global WORKING_IMAGE
	WORKING_IMAGE = to_grayscale(WORKING_IMAGE, "prom")
	w, h = WORKING_IMAGE.size
	canvas.config(width = w, height = h)
	photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
	label.config(image = photo)
	label.image = photo

def callback_binary():
	global WORKING_IMAGE
	WORKING_IMAGE = to_binary( WORKING_IMAGE, 127)
	w, h = WORKING_IMAGE.size
	canvas.config(width = w, height = h)
	photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
	label.config(image = photo)
	label.image = photo

def callback_sal():
	w, h = image.size
	global	WORKING_IMAGE
	WORKING_IMAGE = sal_y_pimienta(WORKING_IMAGE, 0.5, 30)
	canvas.config(width = w, height = h)
	photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
	label.config(image = photo)
	label.image = photo

def callback_des_sal():
	w, h = image.size
	global	WORKING_IMAGE
	WORKING_IMAGE = des_sal_y_pimienta(WORKING_IMAGE, 30)
	canvas.config(width = w, height = h)
	photo = ImageTk.PhotoImage(file = OUTPUT_FILE)
	label.config(image = photo)
	label.image = photo

def callback_reset():
	w, h = image.size
	global	WORKING_IMAGE
	WORKING_IMAGE = image
	canvas.config(width = w, height = h)
	photo = ImageTk.PhotoImage(file = argv[1])
	label.config(image = photo)
	label.image = photo


if __name__ == "__main__":
	assert(path.isfile(argv[1]))
	im = Image.open(argv[1]).convert('RGB')
	#im = to_grayscale(im, 'prom')
	#h = [[ -1, -1, -1],
	#			[-1, 8, -1],
	#			[-1, -1, -1]]						
	#im = convolucion(im, h)
	#im = blur(im, 10)
	#im = classify_forms(im)
	#im = to_binary(im, 30)
	#im = classify_forms(im)
	
	root = Tkinter.Tk()
	root.title("Vision Computacional")
	image = Image.open(argv[1]).convert('RGB')

	global WORKING_IMAGE 
	WORKING_IMAGE = image
	photo = ImageTk.PhotoImage(file = argv[1])
	w, h = image.size

	canvas = Tkinter.Canvas(root, width = w, height = h)
	label = Tkinter.Label(canvas, image = photo)
	label.image = photo
	label.pack()

	button_content = { 'Grayscale' : lambda:callback_grayscale, 'Binary' : lambda:callback_binary(),
										'MedianBlur' : lambda:callback_blur(), 'SalyPimienta' : lambda:callback_sal(),
										'DeshacerSyP': lambda:callback_des_sal(), 'Reset' : lambda:callback_reset(),
										'Clasificar' : lambda:callback_classify()
									  }
	second_canvas = Tkinter.Canvas(root, width = w, height = h+50)
	i = 1
	for item in button_content:
		button = Tkinter.Button(second_canvas, text = item, command = button_content[item], width = 30)
		button_window = second_canvas.create_window(10, 30*i, anchor='nw', window=button)
		i += 1


	canvas.pack(side = "left")
	second_canvas.pack(side = "right")
	root.mainloop()
