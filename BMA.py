# Boyer–Moore Algorithm
# Ethan Trott
# COS 350 - Assignment 6

# returns the index of the first character (searching right to left) that doesn't match for the current alignment (or -1 if all match)
def IndexThatDoesntMatch(T,P,curPos,alphabet='abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + ' '):
    idx = len(P) - 1
    while ((idx >= 0 and T[idx+curPos] is P[idx]) or (T[idx+curPos] not in alphabet)):
        idx -= 1
    return idx


# returns max alignment skips allowed by the bad character rule
def BadCharacterRule(T,P,curPos,alphabet='abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + ' '):
    badIndex = IndexThatDoesntMatch(T, P, curPos, alphabet)
    
    if (badIndex != -1):
        charToFind = T[badIndex + curPos]
        
        idx = len(P) - 1
        #decrease idx until we find the character we're looking for (or run out of characters)
        while (idx >= 0 and P[idx] is not charToFind):
            idx -= 1
        
        # if the character we want is in our pattern, skip to align it
        if (idx != -1):
            return badIndex - idx

        # if it isn't, skip to next possible alignment
        else:
            return (len(P)-1) - badIndex

    return -1

# returns max alignment skips allowed by the good suffix rule
def GoodSuffixRule(T,P,curPos,alphabet='abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + ' '):
    badIndex = IndexThatDoesntMatch(T, P, curPos, alphabet)

    # if there is a good suffix, continue
    if (badIndex != len(P)-1):
        # get the good suffix (t)
        t = T[badIndex+curPos+1 : curPos+len(P)]

        offset = 1
        startPos = max(len(P)-len(t)-offset, 0)
        endPos = len(P)-offset
        substringToCheck = P[startPos:endPos]

        # find number of alignment skips until no mismatches between P and t
        while (IndexThatDoesntMatch(t, substringToCheck, len(t)-len(substringToCheck), alphabet) != -1):
            offset += 1
            startPos = max(len(P)-len(t)-offset, 0)
            endPos = len(P)-offset
            substringToCheck = P[startPos:endPos]

        # if there is an aliginment with no mismatches, return number of steps to that alignment
        if (len(substringToCheck) > 0):
            return offset
        
        # else, return number of steps to next possible alignment
        else:
            return len(P)

    return -1

#returns the position of the first occurence of P inside of T, or -1 if there isn't one
def match(T,P,alphabet='abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + ' '):
    curPos = 0

    #run the loop until we find a complete match to the pattern (or we search the entire thing)
    while (curPos + len(P) <= len(T) and IndexThatDoesntMatch(T, P, curPos, alphabet) != -1):
        # increase the current position by the maximum amount allowed by the BadCharacter and GoodSuffix Rules
        curPos += max(BadCharacterRule(T,P,curPos, alphabet), GoodSuffixRule(T,P,curPos,alphabet), 1)

    #if we searched the entire thing with no match, return -1
    if (curPos + len(P) > len(T)):
        return -1
    #else return the match position
    else:
        return curPos