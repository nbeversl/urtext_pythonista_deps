import ui
from objc_util import *
from thefuzz import fuzz

class AutoCompleter:
	""" AutoCompleteter Base Class """

	def __init__(self, view_width, view_height, layout, theme):
		self.view_height = view_height
		self.search = ui.TextField()
		self.search.hidden = True
		self.search.delegate = SearchFieldDelegate()
		self.search.delegate.textfield_did_change = self.textfield_did_change
		self.dropDown = ui.TableView()
		self.dropDown.delegate = SearchFieldDelegate()
		self.dropDown.delegate.tableview_did_select = self.tableview_did_select
		self.dropDown.hidden = True
		self.size_fields(view_width, view_height, layout)
		self.dropDown.data_source = ui.ListDataSource([])

	def textfield_did_change(self, textfield):
		entry = textfield.text.lower()
		fuzzy_options = sorted(
			self.items,
			key = lambda option: fuzz.ratio(
				entry,
				self.items_comparision[option]), 
			reverse=True)
		self.dropDown.data_source.items=fuzzy_options[:30]

	def hide(self):		
		self.dropDown.hidden = True
		self.search.hidden = True
		self.reset()

	def reset(self):
		self.search.text=''
		self.items = []

	def tableview_did_select(self, tableview, section, row):
		self.search.text = self.dropDown.data_source.items[row]
		return self.action(self.dropDown.data_source.items[row])
		self.hide()

	def set_items(self, items):
		if isinstance(items, dict):
			self.items = list(items.keys())
		if isinstance(items, list):
			self.items = items
		if self.items:
			self.items_comparision = {}
			for item in items:
				self.items_comparision[item] = item.lower()
			self.dropDown.data_source.items = self.items
			max_items_showing = ( 
				self.view_height - self.search.height 
				) / len(self.items)
			if len(self.dropDown.data_source.items) > max_items_showing:
				self.dropDown.height = self.view_height
			else:
				self.dropDown.height = self.search.height * len(self.items)

	def show(self):
		self.search.hidden = False
		self.search.bring_to_front()
		self.search.text=''
		self.dropDown.hidden = False
		self.dropDown.bring_to_front()
		self.dropDown.data_source.background_color = '#e5dddc'
		self.dropDown.x = self.search.x
		self.dropDown.y = self.search.y + self.search.height
		self.dropDown.width = self.search.width
		self.dropDown.row_height = self.search.height
		self.search.begin_editing()

	def set_action(self, action):
		self.action = action

	def size_fields(self, view_width, view_height, layout):
		self.search.height = layout['search_box_height']
		self.search.width = view_width * 0.8
		self.search.x = view_width / 10
		self.search.y = layout['text_view_distance_from_top'] + layout['padding']['md']
		self.search.border_width = layout['button_border_width']
		self.dropDown.height = view_height

class SearchFieldDelegate:
	
	def __init__(self):
		pass