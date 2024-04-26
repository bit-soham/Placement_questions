directions = [-2, -1, 0, 1, 2]

# Nested loop to iterate through all combinations of pairs
for x in directions:
    for y in directions:
        # Skip the combination (0, 0) as it's not needed
        if x == 0 and y == 0:
            continue
        print(f"{x}px {y}px black, ", end="")

# Output:
# -1px -1px black, -1px 0px black, -1px 1px black, 0px -1px black, 0px 1px black, 1px -1px black, 1px 0px black, 1px 1px black,
