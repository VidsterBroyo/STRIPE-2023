from math import sqrt # import square root function

# function to append lengths of pipes to distances list
distances = []
def appendDistances(pipesToCalculate):
    pointA = None
    pointB = None

    # for each pipe 
    for pipe in pipesToCalculate:

        # look through each point
        for point in points:

            # find coords of pointA of the pipe
            if pipe[0] == point[0]:
                pointA = point

            # find coords of pointB of the pipe
            elif pipe[1] == point[0]:
                pointB = point

            # once both are found:
            if pointA != None and pointB != None:
                # calculate distance between pointA and pointB
                dis = sqrt( (pointB[-1][0] - pointA[-1][0])**2 + (pointB[-1][-1] - pointA[-1][-1])**2)
                distances.append([pointA, pointB, dis]) # add to distances

                # reset points
                pointA = None
                pointB = None


# # input for points
# points = []
# for i in range(int(input("How many points? "))):
#     points.append((input("\nPoint Letter: "), (int(input("X-Coordinate: ")), int(input("Y-Coordinate: ")))))

# # input for pipes
# pipes = []
# for i in range(int(input("\n\nHow many pipes? "))):
#     pipes.append((input("\nPoint A: "), input("Point B: ")))


points = [("W", (5, 9)), ("A", (3, 7)), ("B", (4, 5)), ("C", (8, 1)),
         ("D", (7, 0)), ("E", (0, 3)), ("F", (5, 2)), ("G", (6, 8))]

pipes = [("W", "C"), ("W", "F"), ("A", "D"), ("A", "E"), ("A", "F"),
         ("B", "C"), ("B", "E"), ("B", "G"), ("C", "G"), ("E", "F"),
         ("E", "G"), ("F", "G")]


# appending list of distances and order in ascending order
appendDistances(pipes)
distances = sorted(distances, key=lambda list: list[-1])


# print("\nLENGTHS OF PIPES")
# for i in distances:
#      print(i)


finalPath = [] # list for optimized path to be added to

# for each pipe
for pipe in distances:
    pointAHere = False
    pointBHere = False

    pointA = pipe[0][0]
    pointB = pipe[1][0]

    # check if pointA and pointB of the pipe are already in finalPath
    for path in finalPath:
        if pointA in path:
            pointAHere = True

        if pointB in path:
            pointBHere = True

    # if one point not in finalPath, add the pipe
    if pointAHere == False or pointBHere == False:
        finalPath.append((pointA, pointB))

print("\nFINAL PATH\n", finalPath)



newHouse = ("H", (4, 0))
proposedPipes = [("C", "H"), ("E", "H"), ("F", "H")]
points.append(newHouse)

# # input for new house
# newHouse = ((input("\nPoint Letter of New House: "), (int(input("X-Coordinate: ")), int(input("Y-Coordinate: ")))))
# points.append(newHouse)

# # input for proposed pipes
# proposedPipes = []
# for i in range(int(input("\n\nHow many proposed pipes? "))):
#     proposedPipes.append((input("\nPoint A: "), input("Point B: ")))


appendDistances(proposedPipes)

# print("\nLENGTHS OF PROPOSED PIPES")
# for i in distances:
#     print(i)


# add points & their shortest path to W to a dictionary (distToW)
# point : [lengthOfShortestPath, pointItGetsWaterFrom]
distToW = {}
for point in points:
    if point[0] == "W":
        distToW["W"] = [0, None] # set W to 0
    else:
         distToW[point[0]] = [10000, None] # add large number as a placeholder


# repeat for n-1 times (n = # of points)
for i in range(len(points) - 1):
    for pipe in distances:
        pointA = pipe[0][0]
        pointB = pipe[1][0]
        
        # get distance from W - point A/B by adding distance from W - point B/A + pipe length
        distToPointB = distToW[pointA][0] + pipe[2]
        distToPointA = distToW[pointB][0] + pipe[2]

        # if the distance from W - point A/B we found is shorter than what the dictionary says the distance from W - point A/B is, update it
        # also add the point it is connected to
        if distToPointB < distToW[pointB][0]:
             distToW[pointB] = [distToPointB, pointA] # update shortest distance with point pipe is also connected to

        if distToPointA < distToW[pointA][0]:
            distToW[pointA] = [distToPointA, pointB] # update shortest distance with point pipe is also connected to


# print("\nSHORTEST PATH TO WATER PER POINT")
# for i in distToW:
#     print(i, ":", distToW[i])


# traceback shortest path from newHouse to W
shortestPath = []
currentPoint = newHouse[0]

# repeat until we reach W
while "W" not in shortestPath:
    # add currentPoint to shortestPath
    shortestPath.insert(0, currentPoint)

    # set currentPoint to the house the last point got water from
    currentPoint = distToW[currentPoint][1]

print("\nSHORTEST PATH FROM ", newHouse[0], " TO W\n", shortestPath)


pipes += proposedPipes # add proposedPipes to pipes

pointGroups = [] # empty list to add cliques to
for pipe1 in pipes:
    pointSearch = [] # list to add points of clique to

    # add first 2 points to points list
    pointA = pipe1[0]
    pointB = pipe1[1]
    pointSearch.append(pipe1[0])
    pointSearch.append(pipe1[1])

    for pipe2 in pipes:
        # make sure pipe we're looking at isn't the same we already have
        if pipe1 == pipe2:
            continue
        
        # find a pipe that connects to starting point, get other point
        if pipe2[0] == pointA:
            pointBof2 = pipe2[1]
        
        elif pipe2[1] == pointA:
            pointBof2 = pipe2[0]

        # look for a pipe that connects to pointB of pipe2 and the pointB of pipe1
        for pipe3 in pipes:
            if pipe3[0] == pointBof2:
                if pipe3[1] == pointB:
                    # if found, add pointB of the pipe to pointSearch
                    pointSearch.append(pipe3[0])
                    
                    # check the clique is greater than 2, add it
                    if len(pointSearch) > 2:
                        pointGroups.append(pointSearch)
                    pointSearch = [] # restart points

            if pipe3[1] == pointBof2:
                if pipe3[0] == pointB:
                    pointSearch.append(pipe3[1])
                    
                    if len(pointSearch) > 2:
                        pointGroups.append(pointSearch)
                    pointSearch = []


# print("\nPoint Groups:", pointGroups)

# print("\nPOINTS: ")
# for i in points:
#     print(i)

# print("\nDISTANCES: ")
# for i in distances:
#     print(i)


maxDistance = [0, None]
for group in pointGroups:
    currentDistance = 0

    for i in range(len(group)-1):
        # getting distance between each point connected next to each other
        for pipe in distances:
            if (pipe[0][0] == group[i] and pipe[1][0] == group[i+1]) or (pipe[0][0] == group[i+1] and pipe[1][0] == group[i]):
                currentDistance += pipe[-1]

    # getting distance between first and last point
    for pipe in distances:
        if (pipe[0][0] == group[0] and pipe[1][0] == group[-1]) or (pipe[0][0] == group[-1] and pipe[1][0] == group[0]):
            currentDistance += pipe[-1]

    # see if we find a group bigger than the current biggest
    if currentDistance > maxDistance[0]:
        maxDistance = [currentDistance, group] # if so, change maxDistance

print('\n', maxDistance)