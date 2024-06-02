class model:  
    def __init__(self, model=0):  
        self.model = model  
    def print(self, *args, **kwargs):  
        if self.model == 0:  
            print(*args, **kwargs) 
    def help(self):  
           print("""
The process of constantly commenting on print during debugging drives me crazy!
So I invented this:
Y=TorU (x)
When x equals 0, all your prints are normal
When x equals 1, all your prints become invalid
----------example-------------
from TorU  import TorU
y=TorU.model(0)
y.print("hello")
----------example-------------
Author ysw""") 


