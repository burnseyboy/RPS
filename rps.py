import random
import time

def main():
    #display menu
    menu = "\n==< ROCK, PAPER, SCISSORS >==\n 1) Standard game\n 2) Rock, Paper, Scissors, Lizard, Spock\n 3) How to play\n 4) Toggle fast mode\n 5) Exit"
    print(menu)

    #continuous menu loop, broken when player quits
    playing = True
    fastmode = 1
    while playing:
        #take input
        selected = input("\nType a number to select an option: ")

        #validate input, retrieve again if invalid
        while selected not in ["1", "2", "3", "4", "5"]:
            selected = input()
        
        #menu selection cases
        if selected == "1":
            playGame("standard", {"r":"ROCK!", "p":"PAPER!", "s":"SCISSORS!"}, fastmode)
            print(menu)
        
        elif selected == "2":
            playGame("lizardspock", {"r":"ROCK!", "p":"PAPER!", "s":"SCISSORS!", "sp":"SPOCK!", "l":"LIZARD!"}, fastmode)
            print(menu)

        elif selected == "3":
            print("\n-Type 'r', 'p' or 's' to select Rock, Paper and Scissors respectively.")
            print("-Type 'l' or 'sp' to select Lizard or Spock when playing the Lizard Spock mode.")
            print("-Rounds are replayed in the event of a draw.")
            print("-Type 'x' during the game to exit back to the menu.")

        elif selected == "4":
            #fastmode is a divider for all the time-sleeps in the program. Turning it on sets it to 3 (i.e. all pauses are 1/3 as long)
            if fastmode == 1:
                print("\nFast mode is now ON")
                fastmode = 3
            else:
                print("\nFast mode is now OFF")
                fastmode = 1
        else:
            playing = False

def playGame(ruleset, weaponDict, fastmode):
    #retrieve round maximum, catch round values of <1.
    rounds = retrieveGameLength()
    if rounds < 1:
        return
    #find necessary rounds to win - use inverse floor division to avoid floating points and importing math module
    roundGoal = -((rounds + 1) // -2)
    
    #set up game data
    scores = {"Player":0, "CPU":0}
    weaponKeys = list(weaponDict.keys())
    gameOver = False

    #processWin inner function: reusable code for when either the player or CPU wins a round
    #returns 1 if the game has ended, 0 otherwise.
    def processWin(playerName):
        print("\n"+playerName.upper()+" WINS!")
        scores[playerName]+=1
        if scores[playerName] >= roundGoal:
            print("\n"+playerName.upper()+" HAS WON THE MATCH!")
            return 1
        return 0
    
    #displayScore inner function: reusable code for displaying the game score
    def displayScore():
        print("\nScore: Player - "+str(scores["Player"])+", CPU - "+str(scores["CPU"]))

    #loop through each round
    for i in range(rounds):
        #set up replaying in case of a draw
        replay = True
        while replay:
            replay = False

            #display game countdown
            print("\nROUND "+str(i+1)+":\n")
            time.sleep(0.8/fastmode)
            print("Rock...")
            time.sleep(0.5/fastmode)
            print("Paper...")
            time.sleep(0.5/fastmode)
            if ruleset == "lizardspock":
                print("Scissors...")
                time.sleep(0.5/fastmode)
                print("Lizard...")
                time.sleep(0.5/fastmode)

            #retrieve player choice and generate CPU choice
            playerChoice = input("Enter your choice: ").lower()
            while playerChoice not in weaponKeys and playerChoice != "x":
                playerChoice = input("Enter a valid choice ('r', 'p' or 's'): ").lower()
            cpuChoice = random.choice(weaponKeys)

            #check for exit
            if playerChoice == "x":
                return

            #display players' choices
            print("Player: "+weaponDict[playerChoice]+" | CPU: "+weaponDict[cpuChoice])
            time.sleep(0.8/fastmode)

            #check for draw
            if playerChoice == cpuChoice:
                print("\nDRAW!")
                replay = True
                time.sleep(0.8/fastmode)
            #player wins (player's weapon value is 1 or 3 ahead of cpu's in the option list)
            #(being 3 ahead is only applicable in lizardspock)
            elif weaponKeys.index(playerChoice) == (weaponKeys.index(cpuChoice)+1)%len(weaponKeys) or (ruleset == "lizardspock" and weaponKeys.index(playerChoice) == (weaponKeys.index(cpuChoice)+3)%len(weaponKeys)):
                if processWin("Player"):
                    gameOver = True
                time.sleep(0.8/fastmode)
                displayScore()
                time.sleep(1/fastmode)
            #CPU wins
            else:
                if processWin("CPU"):
                    gameOver = True
                time.sleep(0.8/fastmode)
                displayScore()
                time.sleep(1/fastmode)

        #exit loop if processWin() flagged the game as over.
        if gameOver:
            break

    #if the loop finishes without the gameOver flag, it was a draw (possible if the player chose an even number of rounds)
    if not gameOver:
        print("\nTHE MATCH WAS A DRAW!")
    return
    
#retrieveGameLength function: code for retrieving and validating a round count for a match. includes inputting 'x' to cancel.
def retrieveGameLength():
    while True:
        try:
            count = input("Enter maximum rounds: ")
            if count == "x" or count == "X":
                return -1
            return int(count)

        except(ValueError):
            print("Please enter a number.")

if __name__ == '__main__':
    main()