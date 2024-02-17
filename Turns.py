def count_turns(points):
    # Initialize variables to store the previous x and y coordinates
    prev_x, prev_y = None, None
    # Initialize variable to count turns
    num_turns = 0

    # Initialize variables to track whether x or y is constant
    x_constant = False
    y_constant = False

    # Iterate through the points
    for point in points:
        x, y = point.x, point.y

        # Check if both the x-coordinate and y-coordinate have been initialized
        if prev_x is not None and prev_y is not None:
            # Check if x-coordinate is constant and y-coordinate is changing
            if not x_constant and x == prev_x and y != prev_y:
                num_turns += 1
                # Set the flag for x being constant
                x_constant = True
                # Reset the flag for y being constant
                y_constant = False
            # Check if y-coordinate is constant and x-coordinate is changing
            elif not y_constant and y == prev_y and x != prev_x:
                num_turns += 1
                # Reset the flag for x being constant
                x_constant = False
                # Set the flag for y being constant
                y_constant = True

        # Update previous coordinates
        prev_x, prev_y = x, y

    # Return the total number of turns
    return num_turns

