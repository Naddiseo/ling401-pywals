class Singleton(type):
	def __init__(cls, name, bases, dict):  #@ReservedAssignment
		super(Singleton, cls).__init__(name, bases, dict)
		cls.instance = None 
	
	def __call__(cls, *args, **kw):  #@NoSelf
		if cls.instance is None:
			cls.instance = super(Singleton, cls).__call__(*args, **kw)
		return cls.instance
