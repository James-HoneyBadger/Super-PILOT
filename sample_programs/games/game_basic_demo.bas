10 PRINT "🎮 BASIC Game Development Demo"
20 PRINT "Creating a simple collision test"
30 PRINT ""

40 REM Setup game objects
50 GAMECREATE player rectangle 100 100 32 32
60 GAMECREATE enemy1 rectangle 200 150 24 24
70 GAMECREATE enemy2 rectangle 300 200 24 24
80 GAMECREATE powerup circle 400 250 16 16

90 REM Set physics
100 GAMEPHYSICS GRAVITY 2.0
110 GAMEPHYSICS player VELOCITY 5 0
120 GAMEPHYSICS enemy1 VELOCITY -3 2
130 GAMEPHYSICS enemy2 VELOCITY 2 -1

140 REM Game loop
150 FOR STEP = 1 TO 50
160   PRINT "--- Game Step "; STEP; " ---"
170   GAMEUPDATE 0.02
180   
190   REM Check collisions
200   GAMECOLLISION player enemy1 HIT1
210   IF HIT1 = 1 THEN PRINT "Player hit Enemy 1!"
220   
230   GAMECOLLISION player enemy2 HIT2
240   IF HIT2 = 1 THEN PRINT "Player hit Enemy 2!"
250   
260   GAMECOLLISION player powerup GOTPOWER
270   IF GOTPOWER = 1 THEN PRINT "Player got power-up!"
280   
290   REM Show positions
300   IF STEP MOD 10 = 0 THEN PRINT "Player at ("; GAME_PLAYER_X; ","; GAME_PLAYER_Y; ")"
310   
320 NEXT STEP

330 PRINT ""
340 PRINT "Game simulation complete!"
350 PRINT "Use GAMERENDER to visualize the scene"