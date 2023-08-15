from stack import Stack

def main():
    print("\nLet's play Towers of Hanoi!!")

    # Create the Stacks
    stacks = []
    left_stack = Stack("Left")
    middle_stack = Stack("Middle")
    right_stack = Stack("Right")

    stacks.extend([left_stack, middle_stack, right_stack])

    # Set up the Game
    num_user_moves = 0
    num_disks = get_valid_number_of_disks()

    for disk in range(num_disks, 0, -1):
        left_stack.push(disk)

    num_optimal_moves = (2 ** num_disks) - 1
    print(f"\nThe fastest you can solve this game is in {num_optimal_moves} moves")

    # Play the Game
    while right_stack.get_size() != num_disks:
        print("\n\n\n...Current Stacks...")
        print_stack(stacks)

        while True:
            print("\nWhich stack do you want to move from?\n")
            from_stack = get_input(stacks)
            if from_stack.is_empty():
                print("\n\nERROR: Invalid choice, stack is empty. Try Again\n")
                print_stack(stacks)
                continue

            print("\nWhich stack do you want to move to?\n")
            to_stack = get_input(stacks)

            if to_stack.is_empty() or from_stack.peek() < to_stack.peek():
                disk = from_stack.pop()
                to_stack.push(disk)
                num_user_moves += 1
                break
            else:
                print("\n\nERROR: Invalid Move. Try Again")
                print_stack(stacks)

    print(f"\n\nYou completed the game in {num_user_moves} moves, and the optimal number of moves is {num_optimal_moves}")
    print_stack(stacks)



def get_valid_number_of_disks():
    while True:
        try:
            num_disks = int(input("\nHow many disks do you want to play with?\n"))
            if num_disks < 3:
                print("Enter a number greater than or equal to 3")
            else:
                return num_disks
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def print_stack(stacks):
    for stack in stacks:
        stack.print_items()

def get_input(stacks):
    choices = [stack.get_name()[0] for stack in stacks]

    while True:
        for i, stack in enumerate(stacks):
            name = stack.get_name()
            letter = choices[i]
            print(f"Enter {letter} for {name}")

        user_input = input("")
        if user_input in choices:
            for i, stack in enumerate(stacks):
                if user_input == choices[i]:
                    return stack

if __name__ == "__main__":
    main()
