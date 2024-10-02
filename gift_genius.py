import gi
import json
import urllib.request
from io import BytesIO
import tkinter as tk
from tkinter import filedialog

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class ItemViewer(Gtk.Window):
	def __init__(self, json_data):
		Gtk.Window.__init__(self, title="Item Viewer")

		self.set_default_size(800, 600)

		self.scrolled_window = Gtk.ScrolledWindow()
		self.add(self.scrolled_window)

		self.grid = Gtk.Grid()
		self.scrolled_window.add(self.grid)

		self.load_items_from_json(json_data)

	def load_items_from_json(self, json_data):
		try:
			data = json.loads(json_data)
			for i, item in enumerate(data):
				self.add_item(item, i)
		except json.JSONDecodeError:
			print("Invalid JSON data.")

	def add_item(self, item, row):
		name = item.get('name')
		url = item.get('URL')
		image_url = item.get('image')

		if name and url and image_url:
			label = Gtk.Label(label=name)
			self.grid.attach(label, 0, row, 1, 1)

			image = Gtk.Image()
			self.load_image(image, image_url, 250, 250)
			self.grid.attach(image, 1, row, 1, 1)

			url_entry = Gtk.Entry()
			url_entry.set_text(url)
			url_entry.set_editable(False)
			self.grid.attach(url_entry, 2, row, 1, 1)

	def load_image(self, image, image_url, width, height):
		try:
			response = urllib.request.urlopen(image_url)
			data = response.read()
			loader = GdkPixbuf.PixbufLoader()
			loader.write(data)
			loader.close()
			pixbuf = loader.get_pixbuf()
			scaled_pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
			image.set_from_pixbuf(scaled_pixbuf)
		except Exception as e:
			print(f"Error loading image: {e}")

def load_json_file():
	root = tk.Tk()
	root.withdraw()

	file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])

	if file_path:
		try:
			with open(file_path, 'r') as file:
				data = json.load(file)
				return json.dumps(data)
		except FileNotFoundError:
			print("JSON file not found.")
		except json.JSONDecodeError:
			print("Invalid JSON file.")
	else:
		print("No file selected.")

	return None

if __name__ == "__main__":
	json_data = load_json_file()
	if json_data:
		win = ItemViewer(json_data)
		win.connect("destroy", Gtk.main_quit)
		win.show_all()
		Gtk.main()