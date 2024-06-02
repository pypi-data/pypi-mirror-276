from .general import *

class Str ():

	def __init__ (self, entry : str = "") -> None:

		self.value : str = entry
		self.default_value : str = self.value

	def set_to (self, entry : Union[str, None] = None) -> None:

		self.value = entry if (entry != None) else self.default_value

	def value (self) -> str:

		return (self.value)

	def concatenate (self, entry : str = "", separator : str = "") -> str:

		return (f"{self.value}{separator}{entry}")

	def length (self) -> int:

		return (len (self.value))

	def set_concatenate (self, entry : str = "", separator : str = "") -> None:

		self.value = f"{self.value}{separator}{entry}"

	def has (self, entry : str) -> bool:

		return (entry in self.value)
	
	def is_equal_to (self, entry : Union[str, None] = None) -> bool:

		return (self.value == entry) if (entry != None) else (self.value == self.default_value)

	def is_not_equal_to (self, entry : Union[str, None] = None) -> bool:

		return (self.value != entry)if (entry != None) else (self.value != self.default_value)

class Ext_Str (Str):

	def __repr__ (self) -> str:

		return (f"Str : {self.value}")
	
	def __setitem__ (self, entry : str, index : Union[int, None] = None) -> None:

		if (index == None):

			self.value = f"{self.value}{entry}"

		else:

			self.value[index] = entry

	def __getitem__ (self, index : int = 0) -> str:

		return (self.value[index])