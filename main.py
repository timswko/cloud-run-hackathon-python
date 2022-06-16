
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
throwRange=3
#targetedMeAttackerList = {}

class coordination :
    def __init__(self, x, y):
        self.x = x
        self.y = y



class playerInfo:
    def __init__(self, url, x, y,direction,wasHit,score):
        self.url = url
        self.x = x
        self.y = y
        self.direction = direction
        self.wasHit = wasHit
        self.score = score
    
def printPlayerList(playerList):
    for pUrl,pInfo in playerList.items():
        logger.info(pUrl)
        logger.info(pInfo.x)
        logger.info(pInfo.y)
        logger.info(pInfo.direction)
        logger.info(pInfo.wasHit)
        logger.info(pInfo.score)


def attackOrFindPlayer(maxX, maxY, selfInfo, playerList):


    return 'F'

    
def escape(maxX, maxY, selfInfo, playerList):
    #1. If no player in front (up to throwRange + 1 )
    #   => go forward
    #2. else (i.e. player in front)
    #  2.1 if no player on Left (up to throwRange + 1)
    #      => go Left    
    #  2.2 if no player on Right (up to throwRange +1 )
    #       => go Right
    #       else (i.e. no way go )
    #       => random one step 
    
    frontCoordinationArr = []
    leftCoordinationArr = []
    rightCoordinationArr = []
    rearCoordinationArr = []
    
    #i. Face North
    if selfInfo.direction=='N':
        for i in range(1, throwRange+2):     
            targetX = selfInfo.x 
            targetY = selfInfo.y-i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                front = coordination(targetX, targetY)
                frontCoordinationArr.append(front)

            targetX = selfInfo.x-i 
            targetY = selfInfo.y
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                left = coordination(targetX, targetY)
                leftCoordinationArr.append(left)

            targetX = selfInfo.x+i 
            targetY = selfInfo.y
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                right = coordination(targetX, targetY)
                rightCoordinationArr.append(right)
            
            targetX = selfInfo.x 
            targetY = selfInfo.y+i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                rear = coordination(targetX, targetY)
                rearCoordinationArr.append(rear)

    #ii. Face East 
    if selfInfo.direction=='E':
        for i in range(1, throwRange+2):     
            targetX = selfInfo.x+i 
            targetY = selfInfo.y
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                front = coordination(targetX, targetY)
                frontCoordinationArr.append(front)

            targetX = selfInfo.x 
            targetY = selfInfo.y-i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                left = coordination(targetX, targetY)
                leftCoordinationArr.append(left)

            targetX = selfInfo.x 
            targetY = selfInfo.y+i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                right = coordination(targetX, targetY)
                rightCoordinationArr.append(right)
            
            targetX = selfInfo.x-i 
            targetY = selfInfo.y
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                rear = coordination(targetX, targetY)
                rearCoordinationArr.append(rear)
    
    #iii. Face South
    if selfInfo.direction=='S':
        for i in range(1, throwRange+2):     
            targetX = selfInfo.x 
            targetY = selfInfo.y+i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                front = coordination(targetX, targetY)
                frontCoordinationArr.append(front)

            targetX = selfInfo.x+i 
            targetY = selfInfo.y
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                left = coordination(targetX, targetY)
                leftCoordinationArr.append(left)

            targetX = selfInfo.x-i 
            targetY = selfInfo.y
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                right = coordination(targetX, targetY)
                rightCoordinationArr.append(right)
            
            targetX = selfInfo.x 
            targetY = selfInfo.y-i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                rear = coordination(targetX, targetY)
                rearCoordinationArr.append(rear)

    #iv. Face West 
    if selfInfo.direction=='W':
        for i in range(1, throwRange+2):     
            targetX = selfInfo.x-i
            targetY = selfInfo.y
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                front = coordination(targetX, targetY)
                frontCoordinationArr.append(front)

            targetX = selfInfo.x 
            targetY = selfInfo.y+i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                left = coordination(targetX, targetY)
                leftCoordinationArr.append(left)

            targetX = selfInfo.x 
            targetY = selfInfo.y-i
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                right = coordination(targetX, targetY)
                rightCoordinationArr.append(right)
            
            targetX = selfInfo.x+i 
            targetY = selfInfo.y
            if targetX >=0 and  targetX < maxX and targetY>=0 and targetY<maxY:
                rear = coordination(targetX, targetY)
                rearCoordinationArr.append(rear)
    
    #Debug
    for f in frontCoordinationArr:
        logger.info('Front=['+str(f.x)+','+str(f.y)+']')
    for l in leftCoordinationArr:
        logger.info('Left=['+str(l.x)+','+str(l.y)+']')
    for r in rightCoordinationArr:
        logger.info('Right=['+str(r.x)+','+str(r.y)+']')




    #1. If no player or Boundary in front (up to throwRange + 1 )
    #   => go forward
    
    frontHasPlayer = False
    frontIsBoundary = False
    if len(frontCoordinationArr) == throwRange+1: 
        for f in frontCoordinationArr:
            logger.info('Front=['+str(f.x)+','+str(f.y)+']')
            for pUrl,pInfo in playerList.items():
                if f.x==pInfo.x and f.x==pInfo.y:
                    frontHasPlayer = True
                    logger.info("Player find in front:"+pUrl)
                    break
            if frontHasPlayer:
                break
    else:
        logger.info("Boundary in front")
        frontIsBoundary =True

    if not frontHasPlayer and not frontIsBoundary:
        logger.info("escape: move F")    
        return 'F'

    #2. else (i.e. player in front)
    #  2.1 if no player and Boundary on Left (up to throwRange + 1)
    #      => go Left    
    LeftHasPlayer = False    
    leftIsBoundary = False
    if len(leftCoordinationArr) == throwRange+1: 
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
        logger.info("escape: move L")   
        return 'L'
    
    #  2.2 if no player and Boundary on Right (up to throwRange +1 )
    #       => go Right
    
    RightHasPlayer = False    
    rightIsBoundary = False
    if len(rightCoordinationArr) == throwRange+1: 
        for r in rightCoordinationArr:
            logger.info('Right=['+str(r.x)+','+str(r.y)+']')
            for pUrl,pInfo in playerList.items():
                if r.x==pInfo.x and r.x==pInfo.y:
                    RightHasPlayer = True
                    logger.info("Player find in right:"+pUrl)
                    break
            if RightHasPlayer:
                break
    else:
        logger.info("Boundary in right")
        rightIsBoundary = True

    if not RightHasPlayer and not rightIsBoundary:
        logger.info("escape: move R")   
        return 'R'

    #       else (i.e. no way go )
    #       => random one move 
    logger.info("escape: move random")
    return moves[random.randrange(len(moves))] 


def faceToAttacker(maxX, maxY, selfInfo, playerList):
    return moves[random.randrange(len(moves))] 

def randomMove():
    return moves[random.randrange(len(moves))] 

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


def checkIfTargetedAndResp(maxX, maxY, selfInfo, playerList):
    # 1. if more than 1 player targeted 
    #  => escape 
    # 2. if only 1 player targeted
    #  => face to attacker
    # 3. if no one targeted
    #  => Attack 
    targetedMeAttackerList = getTargetedMeAttacker(maxX, maxY, selfInfo, playerList)
    for aUrl,aInfo in targetedMeAttackerList.items():
        logger.info("Attacker found: "+aUrl)
    # 1. if more than 1 player targeted 
    if len(targetedMeAttackerList) > 1: 
        return escape(maxX, maxY, selfInfo, playerList)

    if len(targetedMeAttackerList) == 1:
        #face to attacker
        return faceToAttacker(maxX, maxY, selfInfo, playerList)

    return attackOrFindPlayer(maxX, maxY, selfInfo, playerList)




    


@app.route("/", methods=['GET'])
def index():
    return "Balance mode!"

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
    printPlayerList(playerList)
    

    #############
    # 2 - checkIfTargetedAndResp()
    ###############
    
    return checkIfTargetedAndResp(maxX, maxY, selfInfo, playerList)


    

    


    #return escape()
    #return attack()

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  

