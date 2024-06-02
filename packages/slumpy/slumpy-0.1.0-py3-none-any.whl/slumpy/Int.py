from .general import *

class Int ():
	
	def __init__ (self, entry : int = 0) -> None:

		self.value : int = entry
		self.default_value : int = self.value

	def set_to (self, entry : Union[int, None] = None) -> None:

		self.value = entry if (entry != None) else self.default_value

	def value (self) -> int:

		return (self.value)

	def plus (self, entry : int = 0) -> int:

		return (self.value + entry)

	def minus (self, entry : int = 0) -> int:

		return (self.value - entry)

	def multiplied_by (self, entry : int = 1) -> int:

		return (self.value * entry)

	def divided_by (self, entry : int = 1) -> int:

		return (self.value // entry)

	def module_of (self, entry : int = 1) -> int:

		return (self.value % entry)

	def power_of (self, entry : int = 1) -> int:

		return (self.value ** entry)

	def set_plus (self, entry : int = 0) -> None:

		self.value += entry

	def set_minus (self, entry : int = 0) -> None:

		self.value -= entry
	
	def set_multiplied_by (self, entry : int = 1) -> None:

		self.value *= entry
	
	def set_divided_by (self, entry : int = 1) -> None:

		self.value //= entry
	
	def set_module_of (self, entry : int = 1) -> None:

		self.value %= entry
	
	def set_power_of (self, entry : int = 1) -> None:

		self.value **= entry

	def is_equal_to (self, entry : Union[int, None] = None) -> bool:

		return (self.value == entry) if (entry != None) else (self.value == self.default_value)

	def is_not_equal_to (self, entry : Union[int, None] = None) -> bool:

		return (self.value != entry) if (entry != None) else (self.value != self.default_value)

	def is_greater_than (self, entry : Union[int, None] = None) -> bool:

		return (self.value > entry) if (entry != None) else (self.value > self.default_value)

	def is_less_than (self, entry : Union[int, None] = None) -> bool:

		return (self.value < entry) if (entry != None) else (self.value < self.default_value)

	def is_more_or_equal_than (self, entry : Union[int, None] = None) -> bool:

		return (self.value >= entry) if (entry != None) else (self.value >= self.default_value)

	def is_less_or_equal_than (self, entry : Union[int, None] = None) -> bool:

		return (self.value <= entry) if (entry != None) else (self.value <= self.default_value)

class Ext_Int (Int):

	def __repr__ (self) -> str:

		return (f"Int : {self.value}")

	def __add__ (self, entry : int = 0) -> int:

		return (self.value + entry)

	def __sub__ (self, entry : int = 0) -> int:

		return (self.value - entry)

	def __mul__ (self, entry : int = 1) -> int:

		return (self.value * entry)

	def __truediv__ (self, entry : int = 1) -> int:

		return (self.value // entry)

	def __mod__ (self, entry : int = 1) -> int:

		return (self.value % entry)

	def __pow__ (self, entry : int = 1) -> int:

		return (self.value ** entry)

	def __iadd__ (self, entry : int = 0) -> None:

		self.value += entry

	def __isub__ (self, entry : int = 0) -> None:

		self.value -= entry

	def __imul__ (self, entry : int = 1) -> None:

		self.value *= entry

	def __itruediv__ (self, entry : int = 1) -> None:

		self.value //= entry

	def __imod__ (self, entry : int = 1) -> None:

		self.value %= entry

	def __ipow__ (self, entry : int = 1) -> None:

		self.value **= entry