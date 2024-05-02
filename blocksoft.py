import numpy as np
import os
import glob
#import matplotlib.pyplot as plt
from solid import *
from solid.utils import * 
from subprocess import run
from subprocess import Popen
import subprocess

import pydicom as dicom

#import beamDicomParser as dp

from tkinter import Tk as tk_Tk
from tkinter import Frame as tk_Frame
from tkinter import Label as tk_Label
from tkinter import Entry as tk_Entry
from tkinter import StringVar as tk_StringVar
from tkinter import DoubleVar as tk_DoubleVar
from tkinter import Button as tk_Button
from tkinter import ttk
from tkinter import IntVar as tk_IntVar
from tkinter import Radiobutton as tk_Radiobutton
from tkinter import Checkbutton as tk_Checkbutton
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

import tkinter as tk

import vtkplotlib as vpl
from stl.mesh import Mesh

cm = 1/2.54

setting_file = 'setting.ini'
test_str = 'C:/Apps/blocksoft_en/openscad/openscad.exe'
with open(setting_file, 'r') as setfile:
        for line in setfile:
                if 'blocksoft' in line[:12]:
                        conf = line.replace('blocksoft','',1)
                        block_path = ''
                        for i,char in enumerate(conf):
                                if char not in [' ','=']:
                                        block_path = conf[i:-1]
                                        break
                        #print('blocksoftpath: ',block_path)
                if 'python' in line[:12]:
                        conf = line.replace('python','',1)
                        python_path = ''
                        for i,char in enumerate(conf):
                                if char not in [' ','=']:
                                        python_path = conf[i:-1]
                                        break
                        #print('pythonpath: ',python_path)
                if 'openscad' in line[:12]:
                        conf = line.replace('openscad','',1)
                        openscad_path = ''
                        for i,char in enumerate(conf):
                                if char not in [' ','=']:
                                        openscad_path = conf[i:-1]
                                        break
                        #print('openscadpath: ',openscad_path)
                if 'stl_def' in line[:12]:
                        conf = line.replace('stl_def','',1)
                        stl_path = ''
                        for i,char in enumerate(conf):
                                if char not in [' ','=']:
                                        stl_path = conf[i:-1]
                                        break
                        #print('STLpath: ',stl_path)
                if 'dcm_def' in line[:12]:
                        conf = line.replace('dcm_def','',1)
                        dcm_path = ''
                        for i,char in enumerate(conf):
                                if char not in [' ','=']:
                                        dcm_path = conf[i:]
                                        break
                        #print('DCMpath: ',dcm_path)

def del_folder_content(path):
	files = glob.glob(path)
	for f in files:
		os.remove(f)



def _vec2d_dist(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2


def _vec2d_sub(p1, p2):
    return (p1[0]-p2[0], p1[1]-p2[1])


def _vec2d_mult(p1, p2):
    return p1[0]*p2[0] + p1[1]*p2[1]

def smooth_data(line, dist):
    if len(line) < 3:
        return line

    (begin, end) = (line[0], line[-1]) if line[0] != line[-1] else (line[0], line[-2])

    distSq = []
    for curr in line[1:-1]:
        tmp = (
            _vec2d_dist(begin, curr) - _vec2d_mult(_vec2d_sub(end, begin), _vec2d_sub(curr, begin)) ** 2 / _vec2d_dist(begin, end))
        distSq.append(tmp)

    maxdist = max(distSq)
    if maxdist < dist ** 2:
        return [begin, end]

    pos = distSq.index(maxdist)
    return (smooth_data(line[:pos + 2], dist) + 
            smooth_data(line[pos + 1:], dist)[1:])

class OpenButton():
	def __init__(self,name,masterframe,path,block_id,data,data_s=0):
		self.frame = masterframe
		self.path = path
		#self.id = button_id
		self.name = name
		self.block_id = block_id
		self.data = data
		self.data_s = data_s

		self.button3d = tk_Button(masterframe, text='3D', fg="black",command=self.open_stl_ext,font='Verdana 10 bold')
		#self.button.pack(side='top',pady=10)
		self.button3d.grid(row=block_id, column=1,padx=10)

		self.button2d = tk_Button(masterframe, text='2D', fg="black",command=self.open_data_ext,font='Verdana 10 bold')
		#self.button.pack(side='top',pady=10)
		self.button2d.grid(row=block_id, column=2,padx=10)

	def open_stl(self):

		# Read the STL using numpy-stl
		mesh = Mesh.from_file(self.path)

		# Plot the mesh
		vpl.mesh_plot(mesh)

		# Show Text with beam- and block-name
		vpl.text(self.name,fontsize=14, color='black')

		# Show the figure
		vpl.show()

	def open_stl_ext(self):
		# Open plot with external script in the background
		Popen([python_path, block_path+"open_stl.py",  self.path, self.name])

	def open_data_ext(self):
		if self.data_s == 0:
			path_data_s = 0
		else:
			path_data_s = './temp/'+self.name + '_s.npy'
			np.save(path_data_s,self.data_s)
		path_data = './temp/'+self.name + '.npy'
		np.save(path_data,self.data)
		
		# Open plot with external script in the background
		Popen([python_path, block_path+"open_data.py",  path_data, path_data_s,self.name])




class BlockCheck():
	def __init__(self, masterframe):
		self.masterframe = masterframe
		self.pack = 0
		self.dataset = 0
		self.stl_folder = stl_path
		self.dicom_folder = dcm_path

	def select_dicom(self):
		filetypes = (('DICOM', '*.dcm'),('All Files','*.*'))
		filename = askopenfilename(title = 'Open DICOM file', initialdir = self.dicom_folder, filetypes=filetypes)
		#print(filename)
		dicom_path.set(filename)

		index = filename.rfind('/')

		self.dicom_folder = filename[:index]

		dataset = dicom.dcmread(filename)
		self.dataset = dataset

		beams = dataset.BeamSequence

		

		if self.pack == 0:
			self.frame = tk_Frame(master=self.masterframe)
			self.frame.pack(side='top',fill='both',pady=10)
			self.pack=1
		else:
			self.frame.pack_forget()
			self.frame.destroy()

			self.frame = tk_Frame(master=self.masterframe)
			self.frame.pack(side='top',fill='both',pady=10)

		self.header = tk.Label(self.frame,text = 'Shieldings and appertures:',font = "Verdana 12 bold",anchor='w')
		self.header.pack(side='top',fill='both')
		beam_labels = []
		beam_frames = []
		block_boxes = []
		self.block_checks = []
		check_id = 0

		for i, beam in enumerate(beams):
			block_boxes.append([])
			beam_labels.append(tk.Label(self.frame,text = '-'+beam.BeamName,font = "Verdana 11 bold",anchor='w'))
			beam_frames.append(tk_Frame(master=self.frame))
			if hasattr(beam,'BlockSequence'):
				beam_labels[i].pack(side='top',fill='both')
				beam_frames[i].pack(side='top',fill='both')
				for j, block in enumerate(beam.BlockSequence):
					self.block_checks.append([i,j,tk_IntVar(value=1)])
					block_boxes[i].append(tk_Checkbutton(beam_frames[i], text=block.BlockType+' '+str(j), variable=self.block_checks[check_id][2],font = "Verdana 11", onvalue=1, offvalue=0))
					block_boxes[i][j].grid(row=j, column=0,padx=10)
					check_id += 1
		self.block_boxes = block_boxes
		self.beam_frames = beam_frames

	def save_stl(self):
		folder = askdirectory(title = 'Choose STL folder', initialdir = self.stl_folder)
		#print(filename)
		stl_save.set(folder)
		self.stl_folder = folder

	def render(self):
		if self.dataset != 0:
			del_folder_content('./temp/*.npy')
			#print(self.dataset)
			stl_objects = []
			for check in self.block_checks:
				print(check[0],',',check[1],',',check[2].get())
				if check[2].get() == 1:
					beam = self.dataset.BeamSequence[check[0]]
					beam_name = beam.BeamName
					block = self.dataset.BeamSequence[check[0]].BlockSequence[check[1]]

					#print(block)

					data_l = list(zip(block.BlockData[::2], block.BlockData[1::2]))
					#print('BLOCKDATA ROH:')
					#print(data_l)
					if smooth_check.get() == 1:
						data_r = data_l
						#data_l = list(zip(*ramerdouglas(item["blockXY"],reductionDistance)))
						#data_l = list(zip(*smooth_data(data_l, smooth_num.get())))
						data_l = smooth_data(data_l, smooth_num.get())
						#print('BLOCKDATA RED:')
						#print(data_l)
						

					maxi_data = np.amax(np.absolute(data_l))
					maxi_data = maxi_data*(2**(1/2))
					block_type = block.BlockType
					block_id = check[1]
					special = special_check.get()

					file_save = self.stl_folder + '/' + beam_name + '_'+ block_type+ '_' +str(block_id)
					if block_type == 'SHIELDING':
						ssd_u = 670
						h = 80
					else:
						ssd_u = 950
						h = 12

					if special == 1:
						ssd_u = special_num.get()
						u = ssd_u-1000
						scale_fac = ssd_u/1000.
						h= 80

						poly = polygon(points=data_l)
						extr = linear_extrude(height=u, center=False, convexity=10,slices=20,scale=scale_fac)(poly)
						extr_m = mirror([0,0,1])(extr)
						extr_mt = translate([0,0,u])(extr_m)
						cube_o_v = cube(size = [maxi_data*2*scale_fac,maxi_data*2*scale_fac,ssd_u], center =True)
						cube_o = translate([0,0,ssd_u/2+h])(cube_o_v)
						obj = difference()(extr_mt,cube_o)
					else:
						u = 1000-ssd_u
						poly = polygon(points=data_l)
						extr = linear_extrude(height=1000, center=False, convexity=10,slices=20,scale=0.0)(poly)
						cube_u = cube(size = [maxi_data*2,maxi_data*2,2*u], center =True)
						cube_o_v = cube(size = [maxi_data*2,maxi_data*2,ssd_u], center =True)
						cube_o = translate([0,0,ssd_u/2+u+h])(cube_o_v)
						obj = difference()(extr,cube_u,cube_o)

					scad_render_to_file(obj, file_save+'.scad')
					#scad_render_to_file(extr, 'test_file.scad')
					print('OPENSCAD:',openscad_path)
					run([openscad_path, "-o",  file_save+".stl", file_save+".scad"])
					print(file_save+'.scad')
					os.remove(file_save+".scad")
					#run(["rm", file_save+".scad"])
					if smooth_check.get() == 1:
						stl_objects.append(OpenButton(name = beam_name + '_'+ block_type+ '_' +str(block_id),masterframe=self.beam_frames[check[0]],path=file_save+'.stl',block_id=check[1],data=data_r,data_s=data_l))
					else:
						stl_objects.append(OpenButton(name = beam_name + '_'+ block_type+ '_' +str(block_id),masterframe=self.beam_frames[check[0]],path=file_save+'.stl',block_id=check[1],data=data_l))



	def open_folder(self):
		stl_folder_os = self.stl_folder
		os.startfile(stl_folder_os)


root = tk.Tk()
root.title('BlockSoft')

#add and pack master frame
frame_master = tk.Frame(master=root)
frame_master.pack(side='top', padx='5', pady='5')


#add header and text to masterframe
header1 = tk.Label(frame_master,text = 'Instruction:',font = "Verdana 12 bold",anchor='w')
header1.pack(side='top',fill='both')
text1 = tk.Label(frame_master,text = '- Select DCMRT_Plan file of the desired treatment plan.', font = 'Verdana 9',anchor='w')
text1.pack(side='top',fill='both')
text2 = tk.Label(frame_master,text = '- Specify STL-storage location.', font = 'Verdana 9',anchor='w')
text2.pack(side='top',fill='both')
text3 = tk.Label(frame_master,text = '- Select shieldings and appertures for rendering.', font = 'Verdana 9',anchor='w')
text3.pack(side='top',fill='both')
text4 = tk.Label(frame_master,text = '- If necessary, select point reduction and enter reduction radius.', font = 'Verdana 9',anchor='w')
text4.pack(side='top',fill='both')
text5 = tk.Label(frame_master,text = '- Optionally select special SSD for SSD over 1000mm. Default SSD=1000mm.', font = 'Verdana 9',anchor='w')
text5.pack(side='top',fill='both')
text6 = tk.Label(frame_master,text = '- Press RENDER to create the STL files.', font = 'Verdana 9',anchor='w')
text6.pack(side='top',fill='both')
text7 = tk.Label(frame_master,text = '- A 2D and 3D preview is now available for the rendered files.', font = 'Verdana 9',anchor='w')
text7.pack(side='top',fill='both')

#CHECKBOXES#
check_box = BlockCheck(frame_master)

##INPUT##

#INPUT1#
frame_input_1 = tk_Frame(master=frame_master)
frame_input_1.pack(side='top',fill='both',pady=10)


#path input
label_path = tk_Label(frame_input_1, text='DICOM-Path:',anchor='w',font='Verdana 10 bold')
label_path.grid(row=0, column=0,padx=10)

dicom_path = tk_StringVar(root, value=dcm_path)

entry_path = tk_Entry(frame_input_1, textvariable=dicom_path)
#entry_path.bind("<Return>",calculate_i)
entry_path.grid(row=0, column=1)

button_path = ttk.Button(frame_input_1,text='open',command=check_box.select_dicom)
button_path.grid(row=0, column=2)


#INPUT2#
# frame_input_2 = tk_Frame(master=frame_master)
# frame_input_2.pack(side='top',fill='both',pady=10)

#path input
label_save = tk_Label(frame_input_1, text='STL-Folder:',anchor='w',font='Verdana 10 bold')
label_save.grid(row=1, column=0,padx=10)

stl_save = tk_StringVar(root, value=stl_path)

entry_save = tk_Entry(frame_input_1, textvariable=stl_save)
#entry_path.bind("<Return>",calculate_i)
entry_save.grid(row=1, column=1)

button_save = ttk.Button(frame_input_1,text='save',command=check_box.save_stl)
button_save.grid(row=1, column=2)

#INPUT3#
label_smooth = tk_Label(frame_input_1, text='Point-reduction',anchor='w',font='Verdana 10 bold')
label_smooth.grid(row=2, column=0,padx=10)

smooth_num = tk_DoubleVar(root, value=0.5)

entry_smooth = tk_Entry(frame_input_1, textvariable=smooth_num)
entry_smooth.grid(row=2, column=1)

smooth_check = tk_IntVar(root, value=1)

check_smooth = tk_Checkbutton(frame_input_1, variable=smooth_check,font = "Verdana 11", onvalue=1, offvalue=0)
check_smooth.grid(row=2, column=2)

#INPUT4#
label_special = tk_Label(frame_input_1, text='Special SSD > 1m [mm]',anchor='w',font='Verdana 10 bold')
label_special.grid(row=3, column=0,padx=10)

special_num = tk_DoubleVar(root, value=1715)

entry_special = tk_Entry(frame_input_1, textvariable=special_num)
entry_special.grid(row=3, column=1)

special_check = tk_IntVar(root, value=0)

check_special = tk_Checkbutton(frame_input_1, variable=special_check,font = "Verdana 11", onvalue=1, offvalue=0)
check_special.grid(row=3, column=2)


frame_button = tk_Frame(master=frame_master)
frame_button.pack(side='top',pady=10)

render_button = tk_Button(frame_button, text="RENDER", fg="black",command=check_box.render,font='Verdana 10 bold')
render_button.pack(side='left',pady=10,padx=10)

open_button = tk_Button(frame_button, text="Open folder", fg="black",command=check_box.open_folder,font='Verdana 10 bold')
open_button.pack(side='right',pady=10,padx=10)


root.mainloop()