import random as rd

#---Define random---

dirs = ['U','L','D','R']

def rp():
    global map
    
    s = len(map)-2
    
    return int(rd.random()*s)
    
def rs():
    return int(rd.random()*4-0.5)
    
def rd_speed():
    return rd.random()/2+0.5
    
def rc():
    return 1-rd.random()/1.5
    
def rdir():
    global dirs
    
    dirs = [dirs[(i+1)%4] for i in range(4)]
    
    return dirs[int(rd.random()*4)]
    
#---Define environment functions---
    
def to_alph(index):
    use = index
    n = 1
    while use > 26:
        use /= 26
        n += 1
    res = [0 for i in range(n)]
    for i in range(n):
        res[n-i-1] = alph[index%26-1]
        index = (index % 26**(n-i))//26
    return ''.join([i for i in res])
    
def mprint():
    global map
    global fmap
    
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 0:
                if fmap[i][j] == 1:
                    print('•', end=' ')
                else:
                    print(' ', end=' ')
            else:
                print(map[i][j], end=' ')
        print()
    
    return None
    
def place_food(n):
    global fmap
    
    for i in range(n):
        (y,x) = (rp(), rp())
        while fmap[y][x] != 0:
            (y,x) = (rp(), rp())
        fmap[y][x] = 1
        
    return None
    
def food_count():
    global fmap
    
    c = 0
    
    for i in fmap:
        for j in i:
            if j == 1:
                c +=1
    
    return c

#---Define environment elements---

time = 0 # in milliseconds

size = (50,50)

map = [[0 for i in range(size[1])] for j in range(size[0])]

fmap = [[0 for i in range(size[1])] for j in range(size[0])]

alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

index = 1

e = 8
    
#---Define Rabbits---

class Rabbit:
    def __init__(self,speed,pos,sight,conv,energy=1,fed=0,age=3):
        global index
        global map
        
        id = to_alph(index)
        
        index += 1
        
        while map[pos[0]][pos[1]] != 0:
            pos = (rp(),rp())
        
        map[pos[0]][pos[1]] = id
        
        self.speed = speed
        self.pos = pos
        self.sight = sight
        self.energy = 1
        self.fed = 0
        self.age = 3
        self.moves = 0
        self.going = None
        self.conviction = conv
        self.id = id
        
        return None
        
    def next_day(self):
        self.energy = 1
        self.fed = 0
        self.age += 1
        self.moves = 0
        
    def scan(self):
        global map
        global fmap
    
        (y,x) = self.pos
        
        k = self.sight
        
        if self.sight > 0:
            u = [[fmap[i][j] for j in range(x-k,x+k+1) if j >= 0 and j < len(map[0])] for i in range(y-k,y+k+1) if i >= 0 and i < len(map)]
            loc = ('','')
            for i in range(len(u)):
                for j in range(len(u[i])):
                    if u[i][j] == 1:
                        loc = (i,j)
                        break
                if loc != ('',''):
                    break
            
            if loc != ('','') and len(u) == k*2+1 and len(u[0]) == k*2+1:
                if abs(loc[0]-k) > abs(loc[1]-k):
                    if loc[0] < k:
                        return 'U'
                    elif loc[0] > k:
                        return 'D'
                else:
                    if loc[1] < k:
                        return 'L'
                    elif loc[1] > k:
                        return 'R'
        
        a = rd.random()
        if a > self.conviction:
            return self.going
        
        return None
        
    def valid(self,dir):
        global map
        
        (x,y) = self.pos
        (i,j) = (len(map),len(map[0]))
        if dir == 'U' and x > 0 and map[x-1][y] == 0:
            return True
        elif dir == 'L' and y > 0 and map[x][y-1] == 0:
            return True
        elif dir == 'D' and x+1 < len(map) and map[x+1][y] == 0:
            return True
        elif dir == 'R' and y+1 < len(map[0]) and map[x][y+1] == 0:
            return True
        
        return False
    
    def mUp(self):
        global map
        global fmap
        
        (x,y) = self.pos
        (i,j) = (len(map),len(map[0]))
        if self.valid('U'):
            map[x][y] = 0
            map[x-1][y] = self.id
            self.pos = (x-1,y)
            if fmap[x-1][y] == 1:
                self.fed += 1
                fmap[x-1][y] = 0
        
        return None
        
    def mLeft(self):
        global map
        global fmap
        
        (x,y) = self.pos
        (i,j) = (len(map),len(map[0]))
        if self.valid('L'):
            map[x][y] = 0
            map[x][y-1] = self.id
            self.pos = (x,y-1)
            if fmap[x][y-1] == 1:
                self.fed += 1
                fmap[x][y-1] = 0
        
        return None
        
    def mDown(self):
        global map
        global fmap
        
        (x,y) = self.pos
        (i,j) = (len(map),len(map[0]))
        if self.valid('D'):
            map[x][y] = 0
            map[x+1][y] = self.id
            self.pos = (x+1,y)
            if fmap[x+1][y] == 1:
                self.fed += 1
                fmap[x+1][y] = 0
        
        return None
        
    def mRight(self):
        global map
        global fmap
        
        (x,y) = self.pos
        (i,j) = (len(map),len(map[0]))
        if self.valid('R'):
            map[x][y] = 0
            map[x][y+1] = self.id
            self.pos = (x,y+1)
            if fmap[x][y+1] == 1:
                self.fed += 1
                fmap[x][y+1] = 0
        
        return None
        
    def go(self,dir):
        if dir == 'U':
            return self.mUp()
        if dir == 'L':
            return self.mLeft()
        if dir == 'D':
            return self.mDown()
        if dir == 'R':
            return self.mRight()
        
    def move(self):
        global time
        global map
        global e
        
        dimension = len(map)*len(map[0])
        
        v_factor = 50/self.speed
        if time//v_factor > self.moves-0.1:
            if self.energy > ((self.speed)*(self.sight+1))*e/dimension:
                dir = self.scan()
                if dir == None:
                    dir = rdir()
                c = 0
                while self.valid(dir) == False and c <= 16:
                    dir = rdir()
                    c += 1
                    
                if self.valid(dir):
                    self.going = dir
                    self.moves += 1
                    self.go(dir)
                    self.energy -= ((self.speed)*(self.sight+1))*e/dimension
        
        return None

    def die(self):
        global map
        
        (y,x) = self.pos
        
        if self.fed == 0:
            map[y][x] = 0
            return True
            
        return False

#---Test map---

rabbits = {}

for i in range(25):
    name = to_alph(i+1)
    rabbits[name] = Rabbit(rd_speed(),(rp(),rp()),rs(),rc())

#mprint()

dimension = len(map)*len(map[0])

for i in range(20):
    print(i, len(rabbits))
    place_food(10)
    time = 0
    while len(rabbits) > 0:
        time += 1
        for rab in rabbits:
            rabbits[rab].move()
        print(chr(27)+"[2J")
            
        mprint()
        
        print(time)
        
        if food_count() == 0:
            break
        
        out = False
        
        for rab in rabbits:
            if rabbits[rab].energy <= ((rabbits[rab].speed)*(rabbits[rab].sight+1))*e/dimension:
                out = True
                
        if out:
            break
    
    dead = ['' for rab in rabbits]
    pregnant = ['' for rab in rabbits]
    
    c1 = 0
    c2 = 0
    
    for rab in rabbits:
        if rabbits[rab].fed >= 2:
            pregnant[c2] = rab
            c2 += 1
        case = False
        case = rabbits[rab].die()
        rabbits[rab].next_day()
        if case == True:
            dead[c1] = rab
            c1 += 1
    
    for each in pregnant:
        if each != '':
            rabbits[to_alph(index)] = Rabbit(rabbits[each].speed,(rp(),rp()),rabbits[each].sight,rabbits[each].conviction)
    
    for each in dead:
        if each != '':
            del rabbits[each]

    for rab in rabbits:
        print(rabbits[rab].id,rabbits[rab].speed,rabbits[rab].sight,rabbits[rab].conviction)
print(i+1, len(rabbits))



    
