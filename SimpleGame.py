import pygame

pygame.init()
SW = 850
SH = 480
win =pygame.display.set_mode((SW,SH))
pygame.display.set_caption("PyGame Tutorial")
# another way - pygame.path.join('sprites','R1.png')
walkRight = [pygame.image.load('sprites/human/R1.png'),
			pygame.image.load('sprites/human/R2.png'),
			pygame.image.load('sprites/human/R3.png'),
			pygame.image.load('sprites/human/R4.png'),
			pygame.image.load('sprites/human/R5.png'),
			pygame.image.load('sprites/human/R6.png'),
			pygame.image.load('sprites/human/R7.png'),
			pygame.image.load('sprites/human/R8.png'),
			pygame.image.load('sprites/human/R9.png')]
			
walkLeft = [pygame.image.load('sprites/human/L1.png'),
			pygame.image.load('sprites/human/L2.png'),
			pygame.image.load('sprites/human/L3.png'),
			pygame.image.load('sprites/human/L4.png'),
			pygame.image.load('sprites/human/L5.png'),
			pygame.image.load('sprites/human/L6.png'),
			pygame.image.load('sprites/human/L7.png'),
			pygame.image.load('sprites/human/L8.png'),
			pygame.image.load('sprites/human/L9.png')]
			
bg = pygame.image.load('sprites/scenery/bg.png') # /home/philfy/Documents/Python/pygame
char = pygame.image.load('sprites/human/standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('sounds/bullet.mp3')
hitSound = pygame.mixer.Sound('sounds/hit.mp3')

#music = pygame.mixer.music.load('music.mp3')
#pygame.mixer.music.play(-1)


# Take this attributes and apply them to a class ###############
jumpHeight = 0.2
isJump = False
jumpCount = 10
left = False
right = False
radius = 5
# walkCount = 0
score = 0

############################
#### Create Enemy Alien ####
############################
class enemy(object):
	############################
	#### Load Enemy Pictures####
	############################
	alienWalkRight = [pygame.image.load('sprites/alien/R1E.png'),
			pygame.image.load('sprites/alien/R2E.png'),
			pygame.image.load('sprites/alien/R3E.png'),
			pygame.image.load('sprites/alien/R4E.png'),
			pygame.image.load('sprites/alien/R5E.png'),
			pygame.image.load('sprites/alien/R6E.png'),
			pygame.image.load('sprites/alien/R7E.png'),
			pygame.image.load('sprites/alien/R8E.png'),
			pygame.image.load('sprites/alien/R9E.png'),
			pygame.image.load('sprites/alien/R10E.png'),
			pygame.image.load('sprites/alien/R11E.png')]
			
	alienWalkLeft = [pygame.image.load('sprites/alien/L1E.png'),
			pygame.image.load('sprites/alien/L2E.png'),
			pygame.image.load('sprites/alien/L3E.png'),
			pygame.image.load('sprites/alien/L4E.png'),
			pygame.image.load('sprites/alien/L5E.png'),
			pygame.image.load('sprites/alien/L6E.png'),
			pygame.image.load('sprites/alien/L7E.png'),
			pygame.image.load('sprites/alien/L8E.png'),
			pygame.image.load('sprites/alien/L9E.png'),
			pygame.image.load('sprites/alien/L10E.png'),
			pygame.image.load('sprites/alien/L11E.png')]
			
	def __init__(self,x,y,width,height,end):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.end = end
		self.path = [self.x, self.end]	# start and end 
		self.walkCount = 0
		self.velocity = 3
		self.hitbox = (self.x+(self.width/4), self.y+15, self.width/2, self.height-(self.height/4))
		self.health = 100 # set health for healthbar
		self.visible = True
	############################
	#### Update Enemy Alien ####
	############################	
	def update(self, win):
		self.move()
		if self.visible == True:
			if self.walkCount +1 >= 33:						# 3 x enemt images = 33
				self.walkCount = 0
			if self.velocity > 0:
				win.blit(self.alienWalkRight[self.walkCount//3], (self.x,self.y))
				self.walkCount += 1
			else:
				win.blit(self.alienWalkLeft[self.walkCount//3], (self.x,self.y))
				self.walkCount += 1
			#############################
			#### Draw a health bar ######
			#### And collision box#######
			#############################
			
			
			self.healthboxRed = (self.x+10, self.y-20, 50, 10)
			pygame.draw.rect(win, (255,0,0), self.healthboxRed)
			
			self.healthboxGreen = (self.x+10, self.y-20, 0+(self.health/2), 10)
			pygame.draw.rect(win, (0,125,0), self.healthboxGreen)
			
			
			
			self.hitbox = (self.x+(self.width/4), self.y+10, self.width/2, self.height-(self.height/4))
			pygame.draw.rect(win, (255,0,0), self.hitbox,2)
	############################
	##### Move Enemy Alien #####
	############################	
	def move(self):
		if self.velocity > 0:	# i.e.is not -1
			if self.x < self.velocity + self.path[1]:	# the index of path 1 (end)
				self.x += self.velocity					# So moves left
			else:
				self.velocity = self.velocity * -1		# Turns the alien around
				self.x += self.velocity
				self.walkCount =0
		else:
			if self.x > self.path[0] - self.velocity:	# the index of path 0 (x)
				self.x += self.velocity					# So moves right (velocity remain the same (velocity*1)
			else:
				self.velocity = self.velocity * -1		# Turns the alien around
				self.x += self.velocity
				self.walkCount = 0
				
	def hit(self):
		print('HIT!')
		if self.health > 11:
			self.health -= 10
		else:
			self.visible = False
			
				
		
	
############################
####   Create Player    ####
############################	
class player(object):
	def __init__(self, x, y, width, height):
		self.x = x 
		self.y = y 
		self.width= width 
		self.height = height
		self.velocity = velocity
		self.isJump = False
		self.jumpCount = 10
		self.left = False
		self.right = False
		self.walkCount = 0
		self.standing = True
		self.hitbox = (self.x+(self.width/4), self.y+15, self.width/2, self.height-(self.height/4))
		self.score = 0
	############################
	####    Update Player   ####
	############################	
	def update(self, win):
		pygame.draw.rect(win, (255,0,0), self.hitbox,2)
		if self.y > 400:
			self.y = 400
		if self.walkCount +1 >= 27:		# walkCount is 27 - 3 times number of images (9)
			self.walkCount = 0
			
		if not (self.standing):
			
			if self.right:
				win.blit(walkRight[self.walkCount//3], (self.x,self.y))
				self.walkCount += 1
			elif self.left:
				win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
				self.walkCount += 1
		else:
			if self.right:
				win.blit(walkRight[0], (self.x, self.y))
			else:
				win.blit(walkLeft[0], (self.x, self.y))
		####Update the hitbox each move		
		self.hitbox = (self.x+(self.width/4), self.y+15, self.width/2, self.height-(self.height/4))
		text = font.render('Score: ' + str(self.score),1,(0,0,0))		#put score on sceen
		win.blit(text, (SW/2, 20))										# Position score on screen
		
	def hit(self):
		self.isJump = False	# if hits alien while jumping doesn't cause player to keep falling after respawn
		self.jumpCount = 10
		self.x = 800
		self.y = 400
		self.walkCount =0
		font1 = pygame.font.SysFont('comicsans', 100)
		text = font1.render('-10', 1 ,(255,0,0))
		win.blit(text, (SW/2-(text.get_width()/2),SH/2))
		pygame.display.update()
		self.score -= 10
		i = 0
		while i < 100:
			pygame.time.delay(10)
			i+=1
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					i = 301
					pygame.quit()
					
	def scored(self):
		self.score += 10
		
		
		
############################
####   Create Bullets   ####
############################
class projectile(object):
	def __init__(self, x,y,radius,color,facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.facing = facing
		self.velocity = 8 * facing # (facing -1 or 1 - so goes left or right)
		
	def draw(self, win):
		
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
		
		
		
				
x = 50			# position player1 in x axis
y = 400			# position player1 in y axis
width = 32		# same width as sprite
height = 64		# same height as sprite
velocity = 5
facing = -1		
############################
#### Refresh the screen ####
############################
def redrawGameWindow():
	
	win.blit(bg,(0,0))
	player1.update(win)
	for goblin in enemies:
		goblin.update(win)
	for bullet in bullets:
		bullet.draw(win)
	pygame.display.update()

# create a player-x----y-width-height
player1 = player(800, 400, 64, 64)
font = pygame.font.SysFont('comicsans', 30, True)		#	set font for score
shootTime = 0
bullets = []
enemies = []				#### create array for goblins
respawn = 50				#### space the goblins out
for goblin in range(10):	####create ten goblins
	enemies.append(enemy(50+respawn,406,64,64, 750))
	respawn +=50
	if respawn > 600:
		respawn = 50
run = True
		
while run:
		
	#pygame.time.delay(50) # so with clock we can now use
	clock.tick(27)
	if shootTime >0:
		shootTime +=1
	if shootTime > 5:
		shootTime = 0
	
	for goblin in enemies:			#### check collision for each goblin
		if goblin.visible == True:
			if player1.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and player1.hitbox[1] + player1.hitbox[3] > goblin.hitbox[1]:
				if player1.hitbox[0] + goblin.hitbox[2] > goblin.hitbox[0] and player1.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
					player1.hit()
				score -= 10
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	
	for goblin in enemies:			#### check each goblin
		if goblin.visible == True:	
			for bullet in bullets:	#### check each bullet
				if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
					if bullet.x +bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
						goblin.hit()
						#score += 10
						player1.scored()
						bullets.pop(bullets.index(bullet))
						hitSound.play()
					
	for bullet in bullets:			
		if bullet.x < 850 and bullet.x > 0:
			bullet.x += bullet. velocity
		else:
			bullets.pop(bullets.index(bullet)) # kill the bullet at the index(bullet) of bullets
				
	#######################################
	#### set up keys to move character ####
	#######################################	
	keys = pygame.key.get_pressed()
	if keys[pygame.K_f] and shootTime == 0:
		bulletSound.play()
		if player1.left:
			facing = -1
		else:
			facing = 1
			
		if len(bullets) < 5:
			bullets.append(projectile(round(player1.x + player1.width // 2), round(player1.y + player1.height//2), 5, (0,0,0), facing))
		
		shootTime = 1
			
	if keys[pygame.K_LEFT] and player1.x > 0-player1.width+player1.velocity+(player1.width/2):
		player1.x -= player1.velocity
		player1.left = True
		player1.right = False
		player1.standing = False
		
	elif keys[pygame.K_RIGHT] and x < (SW-player1.width-player1.velocity-(player1.width/2)):
		player1.x += player1.velocity
		player1.left = False
		player1.right = True
		player1.standing = False
	
	else:
		player1.standing = True
		player1.walkCount = 0
		
	if not(player1.isJump):		# Only if isJump == False
			
		if keys[pygame.K_SPACE]:
			player1.isJump = True
			player1.walkCount = 0
		
	else:
		if player1.jumpCount >= -10:
			negative = 1
			if player1.jumpCount < 0:
				negative = -1
			player1.y-= (player1.jumpCount ** 2) * 0.2 * negative
			player1.jumpCount -= 1
		else:
			player1.isJump =False
			player1.jumpCount = 10
	
	redrawGameWindow()
pygame.quit()
