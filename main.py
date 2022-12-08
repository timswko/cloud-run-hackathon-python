
# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import random
import json
from flask import Flask, request

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ['F', 'T', 'L', 'R']
moveOnly = ['F', 'L', 'R']
throwRange=3
#targetedMeAttackerList = {}

class coordination :
    def __init__(self, x, y):
        self.x = x
        self.y = y

class coordinationAndDirection :
    def __init__(self, x, y,direction):
        self.x = x
        self.y = y
        self.direction = direction


class playerInfo:
    def __init__(self, url, x, y,direction,wasHit,score):
        self.url = url
        self.x = x
        self.y = y
        self.direction = direction
        self.wasHit = wasHit
        self.score = score

#############
# Debug - print log
#############

def printPlayerList(playerList):
    for pUrl,pInfo in playerList.items():
        logger.info(pUrl)
        logger.info(pInfo.x)
        logger.info(pInfo.y)
        logger.info(pInfo.direction)
        logger.info(pInfo.wasHit)
        logger.info(pInfo.score)



#############
# Random
#############

def randomMoveOrAttack():
    resultMove = moves[random.randrange(len(moves))] 
    logger.info("(randomMoveOrAttack , result = "+resultMove)
    return resultMove

def randomMove():
    resultMove = moveOnly[random.randrange(len(moveOnly))] 
    logger.info("(randomMove , result = "+resultMove)
    return resultMove

#############
#To be Develop
#############

#def findShield(maxX, maxY, selfInfo, playerList):
#    # Logic => find a place no player (for defende)
#    return 'F'

#def moveForwardClosestPlayer(maxX, maxY, selfInfo, playerList):
#    # Logic=> find closest player and move towards 
#    # find the throwRange +1 , +2 .... until player find
#    return 'F'

#############
#Utility
#############

def newCoordinationAndDirectionAfterMove(maxX,maxY,currentDirection,currentX,currentY,newMove):
    
    newX = currentX
    newY = currentY
    newDirection = currentDirection

    logger.info("(newCoordinationAndDirectionAfterMove) newMove = "+newMove)
    #1. if face North
    if currentDirection == 'N':
        if newMove == 'F':
            newX = currentX
            newY = currentY-1
        if newMove == 'L':
            newDirection = 'W'
        if newMove == 'R':
            newDirection = 'E'
    
    #2. if face East 
    if currentDirection == 'E':
        if newMove == 'F':
            newX = currentX+1
            newY = currentY
        if newMove == 'L':
            newDirection = 'N'
        if newMove == 'R':
            newDirection = 'S'
    
    #3. if face South
    if currentDirection == 'S':
        if newMove == 'F':
            newX = currentX
            newY = currentY+1
        if newMove == 'L':
            newDirection = 'E'
        if newMove == 'R':
            newDirection = 'W'
    
    #4. if face West
    if currentDirection == 'W':
        if newMove == 'F':
            newX = currentX-1
            newY = currentY
        if newMove == 'L':
            newDirection = 'S'
        if newMove == 'R':
            newDirection = 'N'
    
    resultCoordinationAndDirection = coordinationAndDirection(newX, newY, newDirection)

    logger.info("(newCoordinationAndDirectionAfterMove) newX ="+str(newX)+", newY="+str(newY)+",newDirection="+newDirection)
    
    return resultCoordinationAndDirection

def findNearbyCoordination(maxX, maxY, currentDirection, currentX, currentY, nearbyRange):
    nearbyCoordination ={}
    frontCoordinationArr = []
    leftCoordinationArr = []
    rightCoordinationArr = []
    rearCoordinationArr = []
    
    #i. Face North
    if currentDirection=='N':
        for i in range(1, nearbyRange+1):     
            targetX = currentX 
            targetY = currentY-i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                front = coordination(targetX, targetY)
                frontCoordinationArr.append(front)

            targetX = currentX-i 
            targetY = currentY
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                left = coordination(targetX, targetY)
                leftCoordinationArr.append(left)

            targetX = currentX+i 
            targetY = currentY
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                right = coordination(targetX, targetY)
                rightCoordinationArr.append(right)
            
            targetX = currentX 
            targetY = currentY+i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                rear = coordination(targetX, targetY)
                rearCoordinationArr.append(rear)

    #ii. Face East 
    if currentDirection=='E':
        for i in range(1, nearbyRange+1):     
            targetX = currentX+i 
            targetY = currentY
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                front = coordination(targetX, targetY)
                frontCoordinationArr.append(front)

            targetX = currentX
            targetY = currentY-i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                left = coordination(targetX, targetY)
                leftCoordinationArr.append(left)

            targetX = currentX
            targetY = currentY+i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                right = coordination(targetX, targetY)
                rightCoordinationArr.append(right)
            
            targetX = currentX-i 
            targetY = currentY
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                rear = coordination(targetX, targetY)
                rearCoordinationArr.append(rear)
    
    #iii. Face South
    if currentDirection=='S':
        for i in range(1, nearbyRange+1):     
            targetX = currentX
            targetY = currentY+i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                front = coordination(targetX, targetY)
                frontCoordinationArr.append(front)

            targetX = currentX+i 
            targetY = currentY
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                left = coordination(targetX, targetY)
                leftCoordinationArr.append(left)

            targetX = currentX-i 
            targetY = currentY
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                right = coordination(targetX, targetY)
                rightCoordinationArr.append(right)
            
            targetX = currentX 
            targetY = currentY-i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                rear = coordination(targetX, targetY)
                rearCoordinationArr.append(rear)

    #iv. Face West 
    if currentDirection=='W':
        for i in range(1, nearbyRange+1):     
            targetX = currentX-i
            targetY = currentY
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                front = coordination(targetX, targetY)
                frontCoordinationArr.append(front)

            targetX = currentX 
            targetY = currentY+i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                left = coordination(targetX, targetY)
                leftCoordinationArr.append(left)

            targetX = currentX 
            targetY = currentY-i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                right = coordination(targetX, targetY)
                rightCoordinationArr.append(right)
            
            targetX = currentX+i 
            targetY = currentY
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                rear = coordination(targetX, targetY)
                rearCoordinationArr.append(rear)
    
    #Debug
    for f in frontCoordinationArr:
        logger.debug('Front=['+str(f.x)+','+str(f.y)+']')
    for l in leftCoordinationArr:
        logger.debug('Left=['+str(l.x)+','+str(l.y)+']')
    for r in rightCoordinationArr:
        logger.debug('Right=['+str(r.x)+','+str(r.y)+']')
    for rear in rearCoordinationArr:
        logger.debug('Rear=['+str(rear.x)+','+str(rear.y)+']')

    nearbyCoordination['front']=frontCoordinationArr
    nearbyCoordination['left']=leftCoordinationArr
    nearbyCoordination['right']=rightCoordinationArr
    nearbyCoordination['rear']=rightCoordinationArr


    return nearbyCoordination

def getTargetedMeAttacker(maxX, maxY, selfInfo, playerList):
    #1. check attacker from North (i.e. attacker should face S)
    # (x,y-1) (x, y-2) ....
    targetedMeAttackerList={}
    for i in range(1, throwRange+1):
        checkX = selfInfo.x
        checkY = selfInfo.y  - i
        if checkX >=0 and  checkX < maxX and checkY>=0 and checkY<maxY:
            for pUrl,pInfo in playerList.items():
                if checkX==pInfo.x and checkY==pInfo.y and pInfo.direction=='S':
                    targetedMeAttackerList[pUrl]=pInfo              

    #2. check attacker from East  (i.e attack should face W)
    # (x+1,y) (x+2,y) ....
    for i in range(1, throwRange+1):
        checkX = selfInfo.x + i
        checkY = selfInfo.y
        if checkX >=0 and  checkX < maxX and checkY>=0 and checkY<maxY:
            for pUrl,pInfo in playerList.items():
                if checkX==pInfo.x and checkY==pInfo.y and pInfo.direction=='W':
                    targetedMeAttackerList[pUrl]=pInfo              
    
    #3. check attacker from South  (i.e attack should face N)
    # (x,y+1) (x, y+2) ....
    for i in range(1, throwRange+1):
        checkX = selfInfo.x 
        checkY = selfInfo.y + i
        if checkX >=0 and  checkX < maxX and checkY>=0 and checkY<maxY:
            for pUrl,pInfo in playerList.items():
                if checkX==pInfo.x and checkY==pInfo.y and pInfo.direction=='N':
                    targetedMeAttackerList[pUrl]=pInfo              
        

    #4. check attacker from West  (i.e attack should face E)
    # (x-1,y) (x-2,y) ....
    for i in range(1, throwRange+1):
        checkX = selfInfo.x - i
        checkY = selfInfo.y
        if checkX >=0 and  checkX < maxX and checkY>=0 and checkY<maxY:
            for pUrl,pInfo in playerList.items():
                if checkX==pInfo.x and checkY==pInfo.y and pInfo.direction=='E':
                    targetedMeAttackerList[pUrl]=pInfo              
        
    

    #for aUrl,aInfo in targetedMeAttackerList.items():
    #    logger.info(aURL)
    return targetedMeAttackerList





#############
#Set of action
#############

def escape(maxX, maxY, selfInfo, playerList, targetedMeAttackerList):
    ###Logic=> Prevent targetted by multiple player, still intend to atack
    #Assuming have more than one 

    #1. If no player in front (up to throwRange + 1 )
    #   => go forward
    #2. else (i.e. player in front)
    #  2.1 if no player on Left (up to throwRange + 1)
    #      => go Left    
    #  2.2 if no player on Right (up to throwRange +1 )
    #       => go Right
    #       else (i.e. no way go )
    #       => random one step 
    
    nearbyCoordination = findNearbyCoordination(maxX, maxY, selfInfo.direction, selfInfo.x, selfInfo.y , 1)

    #1. If no player or Boundary in front (next 1 step)
    #   => go forward
    
    frontHasPlayer = False
    frontIsBoundary = False
    frontCoordinationArr=nearbyCoordination['front']
    #if len(frontCoordinationArr) == throwRange+1: 
    if len(frontCoordinationArr) == 1: 
        for f in frontCoordinationArr:
            logger.info('Front=['+str(f.x)+','+str(f.y)+']')
            for pUrl,pInfo in playerList.items():
                if f.x==pInfo.x and f.y==pInfo.y:
                    frontHasPlayer = True
                    logger.info("Player find in front:"+pUrl)
                    break
            if frontHasPlayer:
                break
    else:
        logger.info("Boundary in front")
        frontIsBoundary =True

    if not frontHasPlayer and not frontIsBoundary:
        logger.info("(findBetterPlace) move F")    
        return 'F'

    #2. else (i.e. player in front)
    #  2.1 if no player and Boundary on Left (up to throwRange + 1)
    #      => go Left    
    LeftHasPlayer = False    
    leftIsBoundary = False
    leftCoordinationArr=nearbyCoordination['left']
    if len(leftCoordinationArr) == 1: 
        for l in leftCoordinationArr:
            logger.info('Left=['+str(l.x)+','+str(l.y)+']')
            for pUrl,pInfo in playerList.items():
                if l.x==pInfo.x and l.y==pInfo.y:
                    LeftHasPlayer = True
                    logger.info("Player find in left:"+pUrl)
                    break
            if LeftHasPlayer:
                break
    else:
        logger.info("Boundary in left")
        leftIsBoundary = True

    if not LeftHasPlayer and not leftIsBoundary: 
        logger.info("(escape) move L")   
        return 'L'
    
    #  2.2 if no player and Boundary on Right (up to throwRange +1 )
    #       => go Right
    
    RightHasPlayer = False    
    rightIsBoundary = False
    rightCoordinationArr=nearbyCoordination['right']
    if len(rightCoordinationArr) == 1: 
        for r in rightCoordinationArr:
            logger.info('Right=['+str(r.x)+','+str(r.y)+']')
            for pUrl,pInfo in playerList.items():
                if r.x==pInfo.x and r.y==pInfo.y:
                    RightHasPlayer = True
                    logger.info("Player find in right:"+pUrl)
                    break
            if RightHasPlayer:
                break
    else:
        logger.info("Boundary in right")
        rightIsBoundary = True

    if not RightHasPlayer and not rightIsBoundary:
        logger.info("(escape) move R")   
        return 'R'

    logger.info("(escape) only can go rear, return 'R'")
    return 'R'

    #logger.info("(findBetterPlace) move random")
    #return moves[random.randrange(len(moves))] 





#############
#Strategy 
#############

def findBetterPlaceAndAttack(maxX, maxY, selfInfo, playerList):
    # 1. if more than 1 player targeted 
    #  => escape 
    # 2. if only 1 player targeted
    #  => face to attacker
    # 3. if no one targeted
    #  => Attack 
    targetedMeAttackerList = getTargetedMeAttacker(maxX, maxY, selfInfo, playerList)
    for aUrl,aInfo in targetedMeAttackerList.items():
        logger.info("Attacker found: "+aUrl)
    

    #if wasHit 
    if selfInfo.wasHit:
<<<<<<< Updated upstream
        logger.info("(findBetterPlaceAndAttack) xxxx Was Hit by someone, escape!!!.")
        return escape(maxX, maxY, selfInfo, playerList, targetedMeAttackerList)
=======
        if len(targetedMeAttackerList) > 1:
            logger.info("(findBetterPlaceAndAttack) xxxx Was Hit more than one attacker, escape!!!.")
            return escape(maxX, maxY, selfInfo, playerList, targetedMeAttackerList)
        if len(targetedMeAttackerList) <= 1:
            logger.info("(findBetterPlaceAndAttack) Targeted by only 1 player , ATTACK or face to attacker!!! ")
            return AttackOrfaceToAttacker(maxX, maxY, selfInfo, playerList, targetedMeAttackerList)
    
        

    # 1. if more than 1 player targeted 
    #if len(targetedMeAttackerList) > 1: 
    #    logger.info("(findBetterPlaceAndAttack) xxxx Targeted by more than 1 player xxxx, find Better Place!!!.")
    #    return findBetterPlace(maxX, maxY, selfInfo, playerList, targetedMeAttackerList)

    # 13:30 prvenvt dead lock with attacher 
    #if len(targetedMeAttackerList) == 1:
    #    #face to attacker
    #    logger.info("(findBetterPlaceAndAttack) Targeted by only 1 player , face to attacker!!! ")
    #    return faceToAttacker(maxX, maxY, selfInfo, playerList, targetedMeAttackerList)

>>>>>>> Stashed changes

    logger.info("(findBetterPlaceAndAttack) NOT BEING TARGETED, GO ATTACK!!!!")
    return attackOrFindPlayer(maxX, maxY, selfInfo, playerList)

def attackOrFindPlayer(maxX, maxY, selfInfo, playerList):
    logger.info("(attackOrFindPlayer) start")
    #1. if available Target in front of me and with throwRange, 
    # => Attack
    #2. Find highest score available Target  on exist L/R(within throw Range) or front /R 
    #       =>turn to that side
    #3. else (i.e no ppl within my throwRange)
    #       => moveForwardClosestPlayer
    frontAvailTargetFound = False
    
    nearbyCoordination = findNearbyCoordination(maxX, maxY, selfInfo.direction, selfInfo.x, selfInfo.y, throwRange)

    #1. if available Target in front of me and with throwRange, 
    # => Attack    
    frontAvailTargetList = {}
    frontIsBoundary = False
    frontCoordinationArr=nearbyCoordination['front']
    for f in frontCoordinationArr:
        logger.debug('(attackOrFindPlayer) Front=['+str(f.x)+','+str(f.y)+']')
        for pUrl,pInfo in playerList.items():
            if f.x==pInfo.x and f.y==pInfo.y:
                frontAvailTargetList[pUrl] = pInfo
                logger.info("(attackOrFindPlayer) Avail target find in front:"+pUrl)

      
    if len(frontCoordinationArr) == throwRange+1: 
        frontIsBoundary =True

    if len(frontAvailTargetList) > 0:
        logger.info("(attackOrFindPlayer) Avail target found , ATTACK!!")    
        return 'T'
    
    #######################
    #2. Find highest score available Target  on exist L/R(within throw Range) or front /R 
    #       =>turn to that side
    ######################## 
    ifMoveForwardAvailTargetList = {}
    ifMoveRightAvailTargetList = {}
    ifMoveLeftAvailTargetList = {}
    nextFrontIsBoundary = False

    #
    # 2.1 Find Avail Target if move forward
    #
    newCoordinationAndDirection=newCoordinationAndDirectionAfterMove(maxX,maxY,selfInfo.direction, selfInfo.x, selfInfo.y, 'F')
    ifMoveForwardNearbyCoordination = findNearbyCoordination(maxX, maxY, newCoordinationAndDirection.direction, newCoordinationAndDirection.x, newCoordinationAndDirection.y, throwRange)

    if newCoordinationAndDirection.x >= maxX or newCoordinationAndDirection.y >= maxY:
        nextFrontIsBoundary = True
    if len(ifMoveForwardNearbyCoordination['front'])==0:
        nextFrontIsBoundary = True

    frontCoordinationArr=ifMoveForwardNearbyCoordination['front']
    for f in frontCoordinationArr:
        logger.debug('(attackOrFindPlayer) ifMoveForwardNearbyCoordination - Front=['+str(f.x)+','+str(f.y)+']')
        for pUrl,pInfo in playerList.items():
            #logger.debug('(attackOrFindPlayer) ifMoveForwardNearbyCoordination - pInfo=['+str(pInfo.x)+','+str(pInfo.y)+']')
            if f.x==pInfo.x and f.y==pInfo.y:
                ifMoveForwardAvailTargetList[pUrl] = pInfo
                logger.debug("(attackOrFindPlayer) ifMoveForwardNearbyCoordination - Avail target find in front:"+pUrl)
    '''
    leftCoordinationArr=ifMoveForwardNearbyCoordination['left']
    for l in leftCoordinationArr:
        logger.debug('(attackOrFindPlayer) ifMoveForwardNearbyCoordination - Left=['+str(l.x)+','+str(l.y)+']')
        for pUrl,pInfo in playerList.items():
            logger.debug('(attackOrFindPlayer) ifMoveForwardNearbyCoordination - pInfo=['+str(pInfo.x)+','+str(pInfo.y)+']')
            if l.x==pInfo.x and l.y==pInfo.y:
                ifMoveForwardAvailTargetList[pUrl] = pInfo
                logger.debug("(attackOrFindPlayer) ifMoveForwardNearbyCoordination - Avail target find in left:"+pUrl)

    rightCoordinationArr=ifMoveForwardNearbyCoordination['right']
    for r in rightCoordinationArr:
        logger.debug('(attackOrFindPlayer) ifMoveForwardNearbyCoordination - Right=['+str(r.x)+','+str(r.y)+']')
        for pUrl,pInfo in playerList.items():
            logger.debug('(attackOrFindPlayer) ifMoveForwardNearbyCoordination - pInfo=['+str(pInfo.x)+','+str(pInfo.y)+']')
            if r.x==pInfo.x and r.y==pInfo.y:
                ifMoveForwardAvailTargetList[pUrl] = pInfo
                logger.debug("(attackOrFindPlayer) ifMoveForwardNearbyCoordination - Avail target find in left:"+pUrl)
    '''

    #
    # 2.2 Find Avail Target if move Left
    #
    newCoordinationAndDirection=newCoordinationAndDirectionAfterMove(maxX,maxY,selfInfo.direction, selfInfo.x, selfInfo.y, 'L')
    ifMoveLeftNearbyCoordination = findNearbyCoordination(maxX, maxY, newCoordinationAndDirection.direction, newCoordinationAndDirection.x, newCoordinationAndDirection.y, throwRange)
    
    frontCoordinationArr=ifMoveLeftNearbyCoordination['front']
    for f in frontCoordinationArr:
        logger.debug('(attackOrFindPlayer) ifMoveLeftNearbyCoordination - Front=['+str(f.x)+','+str(f.y)+']')
        for pUrl,pInfo in playerList.items():
            #logger.debug('(attackOrFindPlayer) ifMoveLeftNearbyCoordination - pInfo=['+str(pInfo.x)+','+str(pInfo.y)+']')
            #logger.debug('(attackOrFindPlayer) ifMoveLeftNearbyCoordination - Type=['+str(type(f.x))+','+str(type(pInfo.x)+']')
            if f.x==pInfo.x and f.y==pInfo.y:
                ifMoveLeftAvailTargetList[pUrl] = pInfo
                logger.debug("(attackOrFindPlayer) ifMoveLeftNearbyCoordination - Avail target find in front:"+pUrl)
    '''
    leftCoordinationArr=ifMoveLeftNearbyCoordination['left']
    for l in leftCoordinationArr:
        logger.debug('(attackOrFindPlayer) ifMoveLeftNearbyCoordination - Left=['+str(l.x)+','+str(l.y)+']')
        for pUrl,pInfo in playerList.items():
            logger.debug('(attackOrFindPlayer) ifMoveLeftNearbyCoordination - pInfo=['+str(pInfo.x)+','+str(pInfo.y)+']')
            if l.x==pInfo.x and l.y==pInfo.y:
                ifMoveLeftAvailTargetList[pUrl] = pInfo
                logger.debug("(attackOrFindPlayer) ifMoveLeftNearbyCoordination - Avail target find in left:"+pUrl)

    rightCoordinationArr=ifMoveLeftNearbyCoordination['right']
    for r in rightCoordinationArr:
        logger.debug('(attackOrFindPlayer) ifMoveLeftNearbyCoordination - Right=['+str(r.x)+','+str(r.y)+']')
        for pUrl,pInfo in playerList.items():
            logger.debug('(attackOrFindPlayer) ifMoveLeftNearbyCoordination - pInfo=['+str(pInfo.x)+','+str(pInfo.y)+']')
            if r.x==pInfo.x and r.y==pInfo.y:
                ifMoveLeftAvailTargetList[pUrl] = pInfo
                logger.debug("(attackOrFindPlayer) ifMoveLeftNearbyCoordination - Avail target find in left:"+pUrl)
    '''

    #
    #2.3 Find Avail Target if move Right
    #
    newCoordinationAndDirection=newCoordinationAndDirectionAfterMove(maxX,maxY,selfInfo.direction, selfInfo.x, selfInfo.y, 'R')
    ifMoveRightNearbyCoordination = findNearbyCoordination(maxX, maxY, newCoordinationAndDirection.direction, newCoordinationAndDirection.x, newCoordinationAndDirection.y, throwRange)

    frontCoordinationArr=ifMoveRightNearbyCoordination['front']
    for f in frontCoordinationArr:
        logger.debug('(attackOrFindPlayer) ifMoveRightNearbyCoordination - Front=['+str(f.x)+','+str(f.y)+']')
        for pUrl,pInfo in playerList.items():
            #logger.debug('(attackOrFindPlayer) ifMoveRightNearbyCoordination - pInfo=['+str(pInfo.x)+','+str(pInfo.y)+']')
            if f.x==pInfo.x and f.y==pInfo.y:
                ifMoveRightAvailTargetList[pUrl] = pInfo
                logger.debug("(attackOrFindPlayer) ifMoveRightNearbyCoordination - Avail target find in front:"+pUrl)

    '''
    leftCoordinationArr=ifMoveRightNearbyCoordination['left']
    for l in leftCoordinationArr:
        logger.debug('(attackOrFindPlayer) ifMoveRightNearbyCoordination - Left=['+str(l.x)+','+str(l.y)+']')
        for pUrl,pInfo in playerList.items():
            logger.debug('(attackOrFindPlayer) ifMoveRightNearbyCoordination - pInfo=['+str(pInfo.x)+','+str(pInfo.y)+']')
            if l.x==pInfo.x and l.y==pInfo.y:
                ifMoveRightAvailTargetList[pUrl] = pInfo
                logger.debug("(attackOrFindPlayer) ifMoveRightNearbyCoordination - Avail target find in left:"+pUrl)

    rightCoordinationArr=ifMoveRightNearbyCoordination['right']
    for r in rightCoordinationArr:
        logger.debug('(attackOrFindPlayer) ifMoveRightNearbyCoordination - Right=['+str(r.x)+','+str(r.y)+']')
        for pUrl,pInfo in playerList.items():
            logger.debug('(attackOrFindPlayer) ifMoveRightNearbyCoordination - pInfo=['+str(pInfo.x)+','+str(pInfo.y)+']')
            if r.x==pInfo.x and r.y==pInfo.y:
                ifMoveRightAvailTargetList[pUrl] = pInfo
                logger.debug("(attackOrFindPlayer) ifMoveRightNearbyCoordination - Avail target find in left:"+pUrl)
    '''

    ifMoveForwardNumOfAvailTarget = len(ifMoveForwardAvailTargetList)
    ifMoveLeftNumOfAvailTarget = len(ifMoveLeftAvailTargetList)
    ifMoveRightNumOfAvailTarget = len(ifMoveRightAvailTargetList)

    logger.info("(attackOrFindPlayer) Avail Target , if Forward:"+str(ifMoveForwardNumOfAvailTarget)+", Left:"+str(ifMoveLeftNumOfAvailTarget)+", Right:"+str(ifMoveRightNumOfAvailTarget))

    if ifMoveForwardNumOfAvailTarget==0 and ifMoveLeftNumOfAvailTarget==0 and ifMoveRightNumOfAvailTarget==0:
        if nextFrontIsBoundary: 
            logger.info("(attackOrFindPlayer) Hit boundary , return R ")
            return 'R'
        else:
            logger.info("(attackOrFindPlayer) No avail target for next step, return F ")
            return 'F'

    #if forward is Max 
    if ifMoveForwardNumOfAvailTarget >= ifMoveLeftNumOfAvailTarget and ifMoveForwardNumOfAvailTarget >= ifMoveRightNumOfAvailTarget:
        logger.info("(attackOrFindPlayer) Move Forward have most Available Target, Move Forward")
        return 'F'
    
    #if Left > Right, turn L
    if ifMoveLeftNumOfAvailTarget > ifMoveRightNumOfAvailTarget:
        logger.info("(attackOrFindPlayer) Move Left have most Available Target, Move Left")
        return 'L'

    #if Right > Left turn R
    if ifMoveRightNumOfAvailTarget > ifMoveLeftNumOfAvailTarget:
        logger.info("(attackOrFindPlayer) Move Right have most Available Target, Move Right")
        return 'R'

    #if ight==Left  turn R
    if ifMoveRightNumOfAvailTarget == ifMoveLeftNumOfAvailTarget:
        logger.info("(attackOrFindPlayer) Move Right and Left have same number of Available Target, Move Right")
        return 'R'
    

<<<<<<< Updated upstream
=======
def AttackOrfaceToAttacker(maxX, maxY, selfInfo, playerList, targetedMeAttackerList):
    logger.info("(faceToAttacker) start")
    # 1. if attacker in front of me , shoot
    # 2. if on left , go L
    # 3. if on Rigt or rear , go R 

    currentNearbyCoordination = findNearbyCoordination(maxX, maxY, selfInfo.direction, selfInfo.x, selfInfo.y, throwRange)
    
    frontCoordinationArr=currentNearbyCoordination['front']
    for f in frontCoordinationArr:
        logger.debug('(faceToAttacker) currentNearbyCoordination - Front=['+str(f.x)+','+str(f.y)+']')
        for aUrl,aInfo in targetedMeAttackerList.items():
            #logger.debug('(faceToAttacker) currentNearbyCoordination - aInfo=['+str(aInfo.x)+','+str(aInfo.y)+']')
            if f.x==aInfo.x and f.y==aInfo.y:
                # Found target, attack
                logger.debug("(faceToAttacker) currentNearbyCoordination - Target find in front:"+aUrl)
                logger.debug("(faceToAttacker) Find target in front, ATTACK  'F'")
                return 'T'
            

    leftCoordinationArr=currentNearbyCoordination['left']
    for l in leftCoordinationArr:
        logger.debug('(faceToAttacker) currentNearbyCoordination - Left=['+str(l.x)+','+str(l.y)+']')
        for aUrl,aInfo in targetedMeAttackerList.items():
            #logger.debug('(faceToAttacker) currentNearbyCoordination - aInfo=['+str(aInfo.x)+','+str(aInfo.y)+']')
            if l.x==aInfo.x and l.y==aInfo.y:
                # Found target, attack
                logger.debug("(faceToAttacker) currentNearbyCoordination - Target find in Left:"+aUrl)
                logger.debug("(faceToAttacker) Find target on left side , turn  'L'")
                return 'L'
    
    rightCoordinationArr=currentNearbyCoordination['right']
    for r in rightCoordinationArr:
        logger.debug('(faceToAttacker) currentNearbyCoordination - Right=['+str(r.x)+','+str(r.y)+']')
        for aUrl,aInfo in targetedMeAttackerList.items():
            #logger.debug('(faceToAttacker) currentNearbyCoordination - aInfo=['+str(aInfo.x)+','+str(aInfo.y)+']')
            if r.x==aInfo.x and r.y==aInfo.y:
                # Found target, attack
                logger.debug("(faceToAttacker) currentNearbyCoordination - Target find in Right :"+aUrl)
                logger.debug("(faceToAttacker) Find target on Right side , turn  'R'")
                return 'R'

    rearCoordinationArr=currentNearbyCoordination['rear']
    for rear in rearCoordinationArr:
        logger.debug('(faceToAttacker) currentNearbyCoordination - Rear=['+str(rear.x)+','+str(rear.y)+']')
        for aUrl,aInfo in targetedMeAttackerList.items():
            #logger.debug('(faceToAttacker) currentNearbyCoordination - aInfo=['+str(aInfo.x)+','+str(aInfo.y)+']')
            if rear.x==aInfo.x and rear.y==aInfo.y:
                # Found target, attack
                logger.debug("(faceToAttacker) currentNearbyCoordination - Target find in Rear :"+aUrl)
                logger.debug("(faceToAttacker) Find target on Back , turn  'R'")
                return 'R'

    #Should not reach this point.
    return moves[random.randrange(len(moves))] 
>>>>>>> Stashed changes


@app.route("/", methods=['GET'])
def index():
    #return "RANDOM!!!"
    return "Balance mod1_1!"
    

@app.route("/", methods=['POST'])
def main():
    # initialize variable 
    maxX = 0 
    maxY = 0
    selfURL = ""
    playerList = {}

    #############
    # 0 - get post content
    #############
    
    request.get_data()
    #logger.info(request.json)
    rawJson = request.get_json()
    logger.info(rawJson)
    
    #############
    # 1 - parse JSON
    #GET maxX, maxY, selfURL, selfInfo, playerList,
    ###############
    
    selfURL=rawJson['_links']['self']['href']
    logger.info('selfURL='+selfURL)  
    
    dims=rawJson['arena']['dims']
    maxX=dims[0]   
    maxY=dims[1]
    
    logger.info('maxX='+str(maxX)+',maxY='+str(maxY))

    state=rawJson['arena']['state']
    #logger.info(playerList)

    for url,info in state.items():

        pInfo=playerInfo(url, info['x'],info['y'],info['direction'],info['wasHit'],info['score'])
        playerList[url]=pInfo
        if url==selfURL:
            selfInfo = playerInfo(url, info['x'],info['y'],info['direction'],info['wasHit'],info['score'])

    if selfInfo is None:
        logger.info("[MAJOR] Fail to find myself in arena.")
        return randomMove()

    if len(playerList)==0:
        logger.info("[INFO] No player in arena.")
        return randomMove()

    
    logger.info(selfInfo)

    #for debug
    #printPlayerList(playerList)
    

    #############
    # 2 - findBetterPlaceAndAttack()
    ###############
    #logger.info("RANDOM!!")
    #return randomMoveOrAttack()
    return findBetterPlaceAndAttack(maxX, maxY, selfInfo, playerList)


    

    


    #return findBetterPlace()
    #return attack()

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  

