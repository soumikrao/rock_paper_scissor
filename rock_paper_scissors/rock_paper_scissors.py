import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False

scores = [0, 0]  # [ai score, player score
playerMove = None


while True:
    bg_img = cv2.imread('rock_paper_scissors/assets/BG.png')
    success, img = cap.read()
    scaled = cv2.resize(img, (0, 0), None, 0.640, 0.640)
    scaled = scaled[:, 25:390]
    success, img = cap.read()
    scaled = cv2.flip(scaled, 1)
    # hands, img = detector.findHands(img)  # with draw
    hands = detector.findHands(img, draw=False)  # without drawing

    if startGame:

        if stateResult is False:
            if scores[0] == 5 or scores[1] == 5:
                if scores[0] == 5:
                    cv2.putText(bg_img, str("Ai Won!"), (550, 440), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
                if scores[1] == 5:
                    cv2.putText(bg_img, str("You Won!"), (530, 440), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
                scores[0] = 0
                scores[1] = 0
            randomNumber = random.randint(1, 3)
            timer = time.time() - initialTime
            # cv2.putText(bg_img, str(int(timer)), (610, 460), cv2.FONT_HERSHEY_PLAIN, 6, (0, 200, 255), 4)
            if int(timer) == 0:
                cv2.putText(bg_img, str('Rock'), (545, 455), cv2.FONT_HERSHEY_PLAIN, 5, (0, 200, 255), 4)
            if int(timer) == 1:
                cv2.putText(bg_img, str('Paper'), (525, 455), cv2.FONT_HERSHEY_PLAIN, 5, (0, 200, 255), 4)
            if int(timer) == 2:
                cv2.putText(bg_img, str('Scissors'), (517, 450), cv2.FONT_HERSHEY_PLAIN, 3.5, (0, 200, 255), 4)
            if int(timer) == 3:
                cv2.putText(bg_img, str('Shoot!'), (535, 455), cv2.FONT_HERSHEY_PLAIN, 4, (0, 200, 255), 4)
            if timer > 3.3:
                stateResult = True
                timer = 0

                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    print(fingers)
                    if fingers == [1, 0, 0, 0, 0] or fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [1, 1, 1, 0, 0] or fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    print(playerMove)

                    #Player Wins
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1
                    #Ai Wins
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

    bg_img[315:622, 817:1182] = scaled

    if stateResult:
        imgAi = cv2.imread(f'rock_paper_scissors/assets/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
        bg_img = cvzone.overlayPNG(bg_img, imgAi, (146, 329))
        if scores[0] == 5 or scores[1] == 5:
            if scores[0] == 5:
                cv2.putText(bg_img, str("Ai Won!"), (550, 440), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
            if scores[1] == 5:
                cv2.putText(bg_img, str("You Won!"), (530, 440), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)

    cv2.putText(bg_img, str(scores[0]), (365, 285), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 4)
    cv2.putText(bg_img, str(scores[1]), (1085, 285), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 4)

    cv2.imshow("Rock, Paper, Scissors", bg_img)

    if cv2.waitKey(1) == ord('s'):
        initialTime = time.time()
        startGame = True
        stateResult = False

    if cv2.waitKey(1) == ord('q'):
        break
