from typing import Any, Union

class Listum ():

	_element_type : Any = None

	def __init__ (self, entry_type : Any, entry : list[Any] = []) -> Any:

		self._element_type = entry_type
		self._element : list = entry
		return (self._element[0] if (len (self._element) > 0) else None)

	def set_to (self, entry : list[_element_type] = []) -> list[_element_type]:

		if (entry != None):

			self._element = entry
		else:

			self._element = self._default_element

	def set_at (self, entry : _element_type, index : int = 0) -> _element_type:

		self._element[index] = entry

	def value_at (self, index : int = 0) -> Any:

		return (self._element[index])

	def clear (self) -> None:

		self._element.clear ()

	def length (self) -> int:

		return (len (self._element))

	def has (self, entry : Any) -> bool:

		return (entry in self._element)

	def is_empty (self) -> bool:

		return (len (self._element) == 0)

	def is_not_empty (self) -> bool:

		return (len (self._element) > 0)

	def is_equal_to (self, entry : Union[list, None] = None) -> bool:

		return (self._element == entry) if (entry != None) else (self._element == self._default_element)

	def is_not_equal_to (self, entry : Union[list, None] = None) -> bool:

		return (self._element != entry) if (entry != None) else (self._element != self._default_element)

	def append (self, entry : Any) -> None:

		self._element.append (entry)

test = Listum (int, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

test.append (11)

test.set_to ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])

print (test.value_at (3))

print (test.length ())

print (test.value ())