from .general import *

class List ():

	def __init__ (self, entry : list = []) -> None:

		self.value : list = entry
		self.default_value : list = self.value

	def set_to (self, entry : Union[list, None] = None) -> None:

		self.value = entry if (entry != None) else self.default_value

	def value (self) -> list:

		return (self.value)

	def set_at (self, entry : Any, index : int = 0) -> None:

		self.value[index] = entry

	def value_at (self, index : int = 0) -> Any:

		return (self.value[index])

	def length (self) -> int:

		return (len (self.value))

	def has (self, entry : Any) -> bool:

		return (entry in self.value)

	def is_empty (self) -> bool:

		return (len (self.value) == 0)

	def is_not_empty (self) -> bool:

		return (len (self.value) > 0)

	def is_equal_to (self, entry : Union[list, None] = None) -> bool:

		return (self.value == entry) if (entry != None) else (self.value == self.default_value)

	def is_not_equal_to (self, entry : Union[list, None] = None) -> bool:

		return (self.value != entry) if (entry != None) else (self.value != self.default_value)

	def append (self, entry : Any) -> None:

		self.value.append (entry)

class Ext_List (List):

	def __repr__ (self) -> str:

		return (f"List : {self.value}")
	
	def __iadd__ (self, entry : Any) -> None:

		self.value.append (entry)

	def __setitem__ (self, entry : Any, index : int = 0) -> None:

		self.value[index] = entry

	def __getitem__ (self, index : int = 0) -> Any:

		return (self.value[index])