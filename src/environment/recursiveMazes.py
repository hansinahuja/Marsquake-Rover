import random

def recursiveMaze(self):

        def randomOddNumber(low, high):
            low = low // 2 
            if high % 2:
                high = high // 2
            else:
                high = high // 2 - 1
            return 2 * random.randrange(low, high+1) + 1
        def randomEvenNumber(low, high):
            low = low // 2 + low % 2
            high = high // 2 
            return 2 * random.randrange(low, high+1)

        def generate(left, right, top, bottom):
            if left >= right or top >= bottom:
                return
            if left >= right - 1 and top >= bottom - 1:
                return

            rnd = random.randrange(0, 2)   
            if left >= right - 1:
                rnd = 0
            if top >= bottom - 1:
                rnd = 1
            if(rnd == 0):                                                 # Horizontal division
                row = randomEvenNumber(top, bottom)
                for i in range(left, right + 1):
                    if self.grid[row][i].type != 'source' and self.grid[row][i].type != 'destination':
                        self.grid[row][i].type = 'wall'
                i = randomOddNumber(left, right)
                if self.grid[row][i].type != 'source' and self.grid[row][i].type != 'destination':
                    self.grid[row][i].type = 'free'                         
                generate(left, right, top, row - 1)
                generate(left, right, row + 1, bottom)
            
            else:                                                           # Vertical division
                clm = randomEvenNumber(left, right + 1)
                for i in range(top, bottom + 1):
                    if self.grid[i][clm].type != 'source' and self.grid[i][clm].type != 'destination':
                        self.grid[i][clm].type = 'wall'
            
                i = randomOddNumber(top, bottom)
                if self.grid[i][clm].type != 'source' and self.grid[i][clm].type != 'destination':
                    self.grid[i][clm].type = 'free'                         
                generate(left, clm - 1, top, bottom)
                generate(clm + 1, right, top, bottom)

        generate(0, self.length - 1, 0, self.breadth - 1)
