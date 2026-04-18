import sys

def linear_alignment(match_reward, mismatch_penalty, indel_penalty, s, t):
    
    # Best Values Computed thus far
    bestStart = (0,0)
    bestEnd = (0,0)
    bestLength = 0
    bestScore = -sys.maxsize

    # Paths ending at each index of prev row
    prevRow = [0] * (len(s) + 1)
    starts = [(0,0)] * (len(s) + 1)
    lengths = [0] * (len(s) + 1)

    for i in range(1, len(t) + 1):

        # Paths ending at each index of current row (computed from prevRow)
        row = [0] * (len(s) + 1)
        newS = [(0,0)] * (len(s) + 1)
        newL = [0] * (len(s) + 1)

        for j in range(1, len(s) + 1):
            row[j] = max(
                0,
                prevRow[j] + indel_penalty,
                row[j - 1] + indel_penalty,
                prevRow[j - 1] + (match_reward if s[j - 1] == t[i - 1] else mismatch_penalty)
            )

            if row[j] == 0:
                newS[j] = (i,j)
                newL[j] = 0 
            elif row[j] == prevRow[j] + indel_penalty:
                newS[j] = starts[j]
                newL[j] = lengths[j] + 1
            elif row[j] == row[j - 1] + indel_penalty:
                newS[j] = newS[j - 1]
                newL[j] = newL[j - 1] + 1
            else:
                newS[j] = starts[j - 1]
                newL[j] = lengths[j - 1] + 1

            if row[j] > bestScore:
                bestScore = row[j]
                bestStart = newS[j]
                bestEnd = (i,j)
                bestLength = newL[j]

        starts = newS
        lengths = newL
        prevRow = row

    return (bestStart[1], bestEnd[1] - 1, bestStart[0], bestEnd[0] - 1, bestScore, bestLength)


def local_alignment(match_reward, mismatch_penalty, indel_penalty, s, t):
    # Initialize dp and backtracking array
    n = len(s)
    m = len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    backtrack = [[None] * (m + 1) for _ in range(n + 1)]
    
    # Recurrence
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = max(
                0, 
                dp[i - 1][j - 1] + (match_reward if s[i - 1] == t[j - 1] else mismatch_penalty), 
                dp[i][j - 1] + indel_penalty, 
                dp[i - 1][j] + indel_penalty
            )
            
            # Update back pointer
            if dp[i][j] == 0:
                backtrack[i][j] = "S"
            elif dp[i][j] == dp[i - 1][j] + indel_penalty:
                backtrack[i][j] = "D"
            elif dp[i][j] == dp[i][j - 1] + indel_penalty:
                backtrack[i][j] = "I"
            else:
                backtrack[i][j] = "M"
    
    return output_alignment(backtrack, dp, s, t)


def output_alignment(backtrack, dp, s, t):
    a = ""
    b = ""
    
    best = 0
    start = (0,0)
    for x in range(len(s) + 1):
        for y in range(len(t) + 1):
            if backtrack[x][y] and dp[x][y] > best:
                best = dp[x][y]
                start = (x,y)

    # Start building alignment at largest vertex
    i, j = start
    while i > 0 and j > 0:
        if backtrack[i][j] == "D":
            a = s[i - 1] + a
            b = "-" + b
            i -= 1
        elif backtrack[i][j] == "I":
            a = "-" + a
            b = t[j - 1] + b
            j -= 1
        elif backtrack[i][j] == "M":
            a = s[i - 1] + a
            b = t[j - 1] + b
            i -= 1
            j -= 1
        else:
            break
    
    output = [i, start[0] - 1, j, start[1] - 1, best, len(a), a, b]
    return output