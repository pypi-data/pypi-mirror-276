from .general import *

class Dict ():

	def __init__ (self, entry : dict = {}) -> None:

		self.value : dict = entry
		self.default_value : dict = self.value

	def set_to (self, entry : Union[dict, None] = None) -> None:

		self.value = entry if (entry != None) else self.default_value

	def value (self) -> dict:

		return (self.value)

	def set_at (self, entry : Any, key : Any) -> None:

		self.value[key] = entry

	def value_at (self, key : Any) -> Any:

		return (self.value[key])
	
	def has (self, entry : Any) -> bool:

		return (entry in self.value)

	def is_equal_to (self, entry : Union[dict, None] = None) -> bool:

		return (self.value == entry) if (entry != None) else (self.value == self.default_value)

	def is_not_equal_to (self, entry : Union[dict, None] = None) -> bool:

		return (self.value != entry) if (entry != None) else (self.value != self.default_value)

class Ext_Dict (Dict):

	def __repr__ (self) -> str:

		return (f"Dict : {self.value}")

	def __setitem__ (self, entry : Any, key : Any) -> None:

		self.value[key] = entry

	def __getitem__ (self, key : Any) -> Any:

		return self.value[key]