"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)



def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False
    platform_arrived=False
    ball_dir=0
    ball_preposition=-1
    destination=-1
    position=0
    fall=False


    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
            platform_arrived=False
            ball_dir=0
            ball_preposition=-1
            destination=-1
            position=0
            fall=False
        else:
            position=scene_info.platform[0]+20
            
            if scene_info.ball[1]>=280 and scene_info.ball[1]<=320 and fall==True:
                if ball_dir==0 and platform_arrived==False:
                    if scene_info.ball[0]>=10 and scene_info.ball[0]<=190:
                        if ball_preposition==-1 :
                            ball_preposition=scene_info.ball[0]
                        else:
                            if scene_info.ball[0]-ball_preposition>0:
                                ball_dir=1
                            else:
                                ball_dir=-1
            
            if scene_info.ball[1]>=350:
                ball_dir=0
                ball_preposition=-1

            if platform_arrived==False and destination==-1:
                if scene_info.ball[1]>=280 and not ball_dir==0:
                    temp=400-scene_info.ball[1]
                    destination=scene_info.ball[0]+ball_dir*temp
                    fall=False
                    if destination>200:
                        destination=200-(destination-200)
                    if destination<0:
                        destination=-destination
            
            if abs(position-destination)<=5:
                platform_arrived=True
                destination=-1
            
            if scene_info.ball[1]<270:
                platform_arrived=False
                fall=True
            if scene_info.ball[1]>395:
                platform_arrived=False

            if platform_arrived==True:
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)

            else:
                if destination==-1:
                    if position<90:
                        ##print(1)
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    if position>=90 and position<=110:
                        ##print(2)
                        comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                    if position>110:
                        ##print(3)
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                else:
                    if position-destination>5:
                        ##print(4)
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    if position-destination<-5:
                        ##print(5)
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                 
                    

