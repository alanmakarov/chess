class Square:
    def __init__(self,str: str):
        if len(str) !=2:
            raise ValueError("Square must be two char i.e e2")
        if str[0] not in 'abcdefgh':
            raise ValueError("Column must be a letter between a and h")
        
        self.col = str[0]
        self.row = int(str[1])
        if self.row < 1 or self.row > 8:
            raise ValueError("Row must be a number between 1 and 8")
    
    def __str__(self):
        return f'{self.col}{self.row}'
    
    def __eq__(self,other):
        if isinstance(other,Square): 
            return self.col == other.col and self.row == other.row
        return False

    def RowIndex(self):
        return 8-self.row
    
    def ColIndex(self):
        return ord(self.col)-ord('a')

    @property 
    def x(self)-> int:
        return self.RowIndex()
    @property
    def y(self) -> int:
        return self.ColIndex()