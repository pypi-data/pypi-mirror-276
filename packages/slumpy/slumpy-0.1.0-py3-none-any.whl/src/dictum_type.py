from general import *

class Dict ():

	def __init__ (self, entry : dict = {}) -> None:

		self._element : dict = entry
		self._default_element : dict = self._element

	def set_to (self, entry : Union[dict, None] = None) -> None:

		self._element = entry if (entry != None) else self._default_element

	def value (self) -> dict:

		return (self._element)

	def set_at (self, entry : Any, key : Any) -> None:

		self._element[key] = entry

	def value_at (self, key : Any) -> Any:

		return (self._element[key])
	
	def has (self, entry : Any) -> bool:

		return (entry in self._element)

	def is_equal_to (self, entry : Union[dict, None] = None) -> bool:

		return (self._element == entry) if (entry != None) else (self._element == self._default_element)

	def is_not_equal_to (self, entry : Union[dict, None] = None) -> bool:

		return (self._element != entry) if (entry != None) else (self._element != self._default_element)

class Ext_Dict (Dict):

	def __repr__ (self) -> str:

		return (f"Dict : {self._element}")

	def __setitem__ (self, entry : Any, key : Any) -> None:

		self._element[key] = entry

	def __getitem__ (self, key : Any) -> Any:

		return self._element[key]