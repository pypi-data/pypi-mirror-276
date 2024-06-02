class Boolum ():
	
	def __init__ (self, entry : bool = False) -> bool:

		self._element : bool = entry
		return (self._element)

	def set_to (self, entry : bool = False) -> bool:

		self._element = entry
		return (self._element)

	def value (self) -> bool:

		return (self._element)

	def opposite (self) -> bool:

		return (not self._element)
	
	def set_opposite (self) -> bool:

		self._element = (not self._element)
		return (self._element)
	
	def is_true (self) -> bool:

		return (self._element == True)

	def is_false (self) -> bool:

		return (self._element == False)
	
	def to_string (self) -> str:

		return (f"Boolum : {self._element}")

	# Extra methods are not in the original Intum class of Slum standard, they are exclusive for slumpy.

	def __repr__ (self) -> str:

		return (str (self._element))

	def __not__ (self) -> bool:

		return (not self._element)
