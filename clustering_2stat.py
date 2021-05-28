from scrubData import importFiles
import random
import math
import matplotlib.pylab as plt

def distance2D(x1, y1, x2, y2):
    return math.sqrt(((x1-x2)**2)+((y1-y2)**2))

def findPlayer(name, player_list):
    for i in range(len(players_list)):
        if player_list[i] == name:
            return i

# [Name, Pos, GP, G, A, Pts, +/-, S, S%, GPG, APG, PtsPG]

def kMeans_2stat(players_list, players_stats):
    k = 2
    centroids = []
    clusters = []
    found = []
    high = 0
    for i in range(len(players_stats)):         # initialize first centroid at the player farthest from the orgin
        distance = distance2D(0, 0, players_stats[i][1], players_stats[i][2])
        if distance > high:
            high = distance
            key = i
    name = players_stats[key][0]   # Name
    num1 = players_stats[key][1]   # Goals
    num2 = players_stats[key][2]   # Assist
    centroids.append((num1, num2))
    clusters.append([])
    clusters[0].append((name, num1, num2))
    found.append(name)

    low = 10000
    for i in range(len(players_stats)):         # initialize second centroid at the player closest to the orgin
        distance = distance2D(0, 0, players_stats[i][1], players_stats[i][2])
        if distance < low:
            low = distance
            key = i
    name = players_stats[key][0]   # Name
    num1 = players_stats[key][1]   # Goals
    num2 = players_stats[key][2]   # Assist
    centroids.append((num1, num2))
    clusters.append([])
    clusters[1].append((name, num1, num2))
    found.append(name)

    points = []
    k_need = k-2
    x_dist = (centroids[0][0] - centroids[1][0])/(k_need+1)
    y_dist = (centroids[0][1] - centroids[1][1])/(k_need+1)
    for i in range(1, k_need+1):
        points.append((centroids[1][0]+(x_dist*i), centroids[1][1]+(y_dist*i)))

    for i in range(len(points)):
        low = 1000
        for j in range(len(players_stats)):
            distance = distance2D(points[i][0], points[i][1], players_stats[j][1], players_stats[j][2])
            if distance < low:
                low = distance
                key = j
        name = players_stats[key][0]   # Name
        num1 = players_stats[key][1]   # Goals
        num2 = players_stats[key][2]   # Assist
        centroids.append((num1, num2))
        clusters.append([])
        clusters[i+2].append((name, num1, num2))
        found.append(name)

    for i in range(len(players_list)):  #go through each point and find its closest centroid
        name = players_stats[i][0]   # Name
        num1 = players_stats[i][1]   # Goals
        num2 = players_stats[i][2]   # Assist
        if name not in found:
            closest_key = 0
            closest_dist = 10000
            for j in range(len(centroids)):
                distance = distance2D(centroids[j][0], centroids[j][1], num1, num2)
                if distance < closest_dist:
                    closest_dist = distance
                    closest_key = j
            clusters[closest_key].append((name, num1, num2))
            x = [p[1] for p in clusters[closest_key]]   #updating the cluster corrisponding to "closest_key"'s centroid
            y = [p[2] for p in clusters[closest_key]]
            centroids[closest_key] = (sum(x) / len(clusters[closest_key]), sum(y) / len(clusters[closest_key]))

    changes = 1
    while changes == 0:     #sorting the clusters and centroids
        changes = 0
        for i in range(len(centroids)-1):
            if centroids[i][0] < centroids[i+1][0]:
                changes = 1
                temp = centroids[i]
                centroids[i] = centroids[i+1]
                centroids[i+1] = temp
                temp = clusters[i]
                clusters[i] = clusters[i+1]
                clusters[i+1] = temp

    colors = []
    colorsKey = ["Blue", "red", "green", "orange", "purple", "pink", "black", "brown"]
    masterList = []
    for i in range(len(clusters)):
        for j in range(len(clusters[i])):
            colors.append(colorsKey[i])
            masterList.append(clusters[i][j])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(len(masterList)):
        ax.scatter(masterList[i][2], masterList[i][1], s=5, color=colors[i])
    plt.title('k='+str(k))
    plt.xlabel('Assist')
    plt.ylabel('Goals')
    #plt.xlabel('Assist per Game')
    #plt.ylabel('Goals per Game')

    key = findPlayer("Wayne Gretzky", players_list)
    plt.text(players_stats[key][2], players_stats[key][1], "Gretzky", fontdict=dict(color="black", size=7))
    key = findPlayer("Sidney Crosby", players_list)
    plt.text(players_stats[key][2], players_stats[key][1], "Crosby", fontdict=dict(color="black", size=7))
    key = findPlayer("Mario Lemieux", players_list)
    plt.text(players_stats[key][2], players_stats[key][1], "Lemieux", fontdict=dict(color="black", size=7))
    key = findPlayer("Connor McDavid", players_list)
    plt.text(players_stats[key][2], players_stats[key][1], "McDavid", fontdict=dict(color="black", size=7))
    key = findPlayer("Bobby Orr", players_list)
    plt.text(players_stats[key][2], players_stats[key][1], "Orr", fontdict=dict(color="black", size=7))
    key = findPlayer("Mike Bossy", players_list)
    plt.text(players_stats[key][2], players_stats[key][1], "Bossy", fontdict=dict(color="black", size=7))

    plt.show()

    print(clusters[0])


# [Name, Pos, GP, G, A, Pts, +/-, S, S%, GPG, APG, PtsPG, SPG]
players_list, players_stats = importFiles("NHLScoringHistory.csv")
test1 = []
for i in players_stats:
    test1.append([i[0], i[3], i[4]])    # [Name, Goals, Assists]
test2 = []
for i in players_stats:
    test2.append([i[0], i[9], i[10]])    # [Name, Goals/Game, Assists/Game]

kMeans_2stat(players_list, test1)



