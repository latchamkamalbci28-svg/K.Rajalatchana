def print_raji():
    for row in range(7):
        # Pattern for R
        for col in range(5):
            if col == 0 or (row == 0 or row == 3) and (col > 0 and col < 4) or \
               (col == 4 and row > 0 and row < 3) or (col == row - 2 and row > 3):
                print("*", end="")
            else:
                print(" ", end="")
        print("  ", end="") # Space between letters

        # Pattern for A
        for col in range(5):
            if ((col == 0 or col == 4) and row != 0) or \
               (row == 0 and col > 0 and col < 4) or (row == 3):
                print("*", end="")
            else:
                print(" ", end="")
        print("  ", end="")

        # Pattern for J
        for col in range(5):
            if (row == 0) or (col == 2) or (row == 6 and col < 2) or (row == 5 and col == 0):
                print("*", end="")
            else:
                print(" ", end="")
        print("  ", end="")

        # Pattern for I
        for col in range(5):
            if (row == 0 or row == 6) or (col == 2):
                print("*", end="")
            else:
                print(" ", end="")
        
        print() # Move to th

print_raji()
