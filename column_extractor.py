# Open scraped stock list
with open('stonks_100.txt') as f:
    # Initialize counter variable
    i = 0
    # Create string to append stock symbols and stocks
    output_line = ""
    for line in f:
        # Add column 1 to output string
        if i%12 == 0:
            output_line = line.strip()
            print(output_line)
        # Add column 2 to output string
        elif i%12 == 1:
            output_line = line.strip()
            print(output_line)
        # Increment counter
        i += 1