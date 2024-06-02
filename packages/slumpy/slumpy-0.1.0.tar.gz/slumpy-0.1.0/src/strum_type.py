class Strum ():

	def __init__ (self, entry : str = "") -> str:

		self._element : str = entry
		return (self._element)

	def set_to (self, entry : str = "") -> str:

		self._element = entry
		return (self._element)

	def value (self) -> str:

		return (self._element)

	def concatenate (self, entry : str = "", separator : str = "") -> str:

		return (f"{self._element}{separator}{entry}")

	def length (self) -> int:

		return (len (self._element))

	def set_concatenate (self, entry : str = "", separator : str = "") -> str:

		self._element = f"{self._element}{separator}{entry}"
		return (self._element)

	def has (self, entry : str = "") -> bool:

		return (entry in self._element)
	
	def is_equal_to (self, entry : str = "") -> bool:

		return (self._element == entry)

	def is_not_equal_to (self, entry : str = "") -> bool:

		return (self._element != entry)

	def to_string (self) -> str:

		return (f"Strum : {self._element}")
	
	# Extra methods are not in the original Intum class of Slum standard, they are exclusive for slumpy.

	def __repr__ (self) -> str:

		return (str (self._element))
	
	def __len__ (self) -> int:

		return (len (self._element))