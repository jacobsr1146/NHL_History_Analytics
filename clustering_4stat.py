from scrubData import importFiles
import random
import math
import matplotlib.pylab as plt

def distance4D(x1, x2, x3, x4, y1, y2, y3, y4):
    return math.sqrt(((x1-y1)**2)+((x2-y2)**2)+((x3-y3)**2)+((x4-y4)**2))

def findPlayer(name, player_list):
    for i in range(len(players_list)):
        if player_list[i] == name:
            return i

# [Name, Pos, GP, G, A, Pts, +/-, S, S%, GPG, APG, PtsPG]

def kMeans_4stat(players_list, players_stats):
    k = 4
    centroids = []
    clusters = []
    found = []
    high = 0
    for i in range(len(players_stats)):         # initialize first centroid at the player farthest from the orgin
        distance = distance4D(0, 0, 0, 0, players_stats[i][1], players_stats[i][2], players_stats[i][3], players_stats[i][4])
        if distance > high:
            high = distance
            key = i
    name = players_stats[key][0]   # Name
    num1 = players_stats[key][1]   # Goals
    num2 = players_stats[key][2]   # Assist
    num3 = players_stats[key][3]   # +/-
    num4 = players_stats[key][4]   # Shots
    centroids.append((num1, num2, num3, num4))
    clusters.append([])
    clusters[0].append((name, num1, num2, num3, num4))
    found.append(name)

    low = 10000
    for i in range(len(players_stats)):         # initialize second centroid at the player closest to the orgin
        distance = distance4D(0, 0, 0, 0, players_stats[i][1], players_stats[i][2], players_stats[i][3], players_stats[i][4])
        if distance < low:
            low = distance
            key = i
    name = players_stats[key][0]   # Name
    num1 = players_stats[key][1]   # Goals
    num2 = players_stats[key][2]   # Assist
    num3 = players_stats[key][3]   # +/-
    num4 = players_stats[key][4]   # Shots
    centroids.append((num1, num2, num3, num4))
    clusters.append([])
    clusters[1].append((name, num1, num2, num3, num4))
    found.append(name)

    points = []
    k_need = k-2
    x_dist = (centroids[0][0] - centroids[1][0])/(k_need+1)
    y_dist = (centroids[0][1] - centroids[1][1])/(k_need+1)
    z_dist = (centroids[0][2] - centroids[1][2])/(k_need+1)
    r_dist = (centroids[0][3] - centroids[1][3])/(k_need+1)
    for i in range(1, k_need+1):
        points.append((centroids[1][0]+(x_dist*i), centroids[1][1]+(y_dist*i), centroids[1][2]+(z_dist*i), centroids[1][3]+(r_dist*i)))

    for i in range(len(points)):
        low = 1000
        for j in range(len(players_stats)):
            distance = distance4D(points[i][0], points[i][1], points[i][2], points[i][3], players_stats[j][1], players_stats[j][2], players_stats[j][3], players_stats[j][4])
            if distance < low:
                low = distance
                key = j
        name = players_stats[key][0]   # Name
        num1 = players_stats[key][1]   # Goals
        num2 = players_stats[key][2]   # Assist
        num3 = players_stats[key][3]   # +/-
        num4 = players_stats[key][4]   # Shots
        centroids.append((num1, num2, num3, num4))
        clusters.append([])
        clusters[i+2].append((name, num1, num2, num3, num4))
        found.append(name)

    for i in range(len(players_list)):  #go through each point and find its closest centroid
        name = players_stats[i][0]   # Name
        num1 = players_stats[i][1]   # Goals
        num2 = players_stats[i][2]   # Assist
        num3 = players_stats[i][3]   # +/-
        num4 = players_stats[i][4]   # Shots
        if name not in found:
            closest_key = 0
            closest_dist = 10000
            for j in range(len(centroids)):
                distance = distance4D(centroids[j][0], centroids[j][1], centroids[j][2], centroids[j][3], num1, num2, num3, num4)
                if distance < closest_dist:
                    closest_dist = distance
                    closest_key = j
            clusters[closest_key].append((name, num1, num2, num3, num4))
            x = [p[1] for p in clusters[closest_key]]   #updating the cluster corrisponding to "closest_key"'s centroid
            y = [p[2] for p in clusters[closest_key]]
            z = [p[3] for p in clusters[closest_key]]
            r = [p[4] for p in clusters[closest_key]]
            centroids[closest_key] = (sum(x) / len(clusters[closest_key]), sum(y) / len(clusters[closest_key]), sum(z) / len(clusters[closest_key]), sum(r) / len(clusters[closest_key]))

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
        ax.scatter(masterList[i][3], masterList[i][4], s=5, color=colors[i])
    plt.title('k='+str(k))
    plt.xlabel('+/- per game')
    plt.ylabel('shot%')
    #plt.xlabel('Assist')
    #plt.ylabel('Goals')
    #plt.xlabel('Assist per Game')
    #plt.ylabel('Goals per Game')

    key = findPlayer("Wayne Gretzky", players_list)
    plt.text(players_stats[key][3], players_stats[key][4], "Gretzky", fontdict=dict(color="black", size=7))
    key = findPlayer("Sidney Crosby", players_list)
    plt.text(players_stats[key][3], players_stats[key][4], "Crosby", fontdict=dict(color="black", size=7))
    key = findPlayer("Mario Lemieux", players_list)
    plt.text(players_stats[key][3], players_stats[key][4], "Lemieux", fontdict=dict(color="black", size=7))
    key = findPlayer("Connor McDavid", players_list)
    plt.text(players_stats[key][3], players_stats[key][4], "McDavid", fontdict=dict(color="black", size=7))
    key = findPlayer("Bobby Orr", players_list)
    plt.text(players_stats[key][3], players_stats[key][4], "Orr", fontdict=dict(color="black", size=7))
    key = findPlayer("Mike Bossy", players_list)
    plt.text(players_stats[key][3], players_stats[key][4], "Bossy", fontdict=dict(color="black", size=7))

    plt.show()

    print(clusters[0])

# [Name, Pos, GP, G, A, Pts, +/-PG, S, S%, GPG, APG, PtsPG, SPG]
players_list, players_stats = importFiles("NHLScoringHistory.csv")
test1 = []
for i in players_stats:
    test1.append([i[0], i[3], i[4], i[6], i[7]])    # [Name, Goals, Assists, +/-PG, Shots]
test2 = []
for i in players_stats:
    test2.append([i[0], i[9], i[10], i[6], i[8]])    # [Name, Goals/Game, Assists/Game, +/-PG, Shot%]

kMeans_4stat(players_list, test2)



