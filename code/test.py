
class papa:
    
    all = []
    
    def __init__(self, name) -> None:
        self.name = name
        self.all.append(self)
        
    def __str__(self):
        return self.name
    
        
test1 = papa("1")
test2 = papa("2")
test3 = papa("3")
test4 = papa("4")
test5 = papa("5")

for i in test5.all:
    print(i.name)
