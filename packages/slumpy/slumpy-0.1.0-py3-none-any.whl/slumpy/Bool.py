from .general import *

class Bool ():
	
	def __init__ (self, entry : bool = False) -> None:

		self.value : bool = entry
		self.default_value : bool = self.value

	def set_to (self, entry : Union[bool, None] = None) -> None:

		self.value = entry if (entry != None) else self.default_value

	def value (self) -> bool:

		return (self.value)

	def opposite (self) -> bool:

		return (not self.value)
	
	def is_true (self, entry : Union[bool, None] = None) -> bool:

		return (self.value == entry) if (entry != None) else (self.value == self.default_value)

	def is_not_true (self, entry : Union[bool, None] = None) -> bool:

		return (self.value != entry) if (entry != None) else (self.value != self.default_value)

class Ext_Bool (Bool):

	def __repr__ (self) -> str:

		return (f"Bool : {self.value}")