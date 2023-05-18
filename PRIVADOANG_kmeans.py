#  Andrea Nicole G Privado
#  2019-03716 (X-1L)
#  K-means CLustering

#!/usr/bin/env python
import math                         # Sqrt function
import pygame                       # GUI
from random import randint          # Randomizer
import matplotlib.pyplot as plt     # Scatter plot

pygame.init()

window_surface = pygame.display.set_mode((700, 500))
pygame.display.set_caption('Kmeans Clustering')

background = pygame.Surface((700, 500))
background.fill(pygame.Color('#657ea6'))

clock = pygame.time.Clock()

# Input and Output file
inputFile = "Wine.csv"
outputFile = "output.csv"

# Reading Input file
fileInput = open(inputFile,"r")
inputData = fileInput.readlines()
fileInput.close()

# Processing data
for i in range(len(inputData)):
    inputData[i] = inputData[i].strip()
    inputData[i] = inputData[i].split(',')

attributes = inputData[0]           # First line of input file
inputData = inputData[1:]           # Rest of the lines

# Attribute Choices Elements
y_att1_items = []
att1_rects = []
y_att2_items = []
att2_rects = []
y_k_items = []
k_rects = []
# Appending the attributes to list and their respective y-value in GUI
for y in range(len(attributes)):      
    y_att1_items.append((y * 20) + 18)
    att1_rects.append(pygame.Rect(335,y_att1_items[y], 165, 22))
    y_att2_items.append((y * 20) + 48)
    att2_rects.append(pygame.Rect(335,y_att2_items[y], 165, 22))
for i in range(9):
    y_k_items.append((i * 20) + 100)
    k_rects.append(pygame.Rect(170,y_k_items[i], 50, 22))

# Initial values, based on the initial attributes and k-value shown in GUI
attribute1_index = 0
attribute2_index = 1
k = 2

selectAtt1 = False      # Whether to show the choices for Att1
selectAtt2 = False
selectK = False
error = False           # Whether to flash the error message
showImage = False       # Whether to show the image of scatterplot
cleared = True

# Font used
text_font = pygame.font.SysFont('montserrat',13)
text_font_small = pygame.font.SysFont('montserrat',12)
# Texts used
text_select1 = text_font.render('Select Attributes 1',True, '#FFFFFF')
text_select2 = text_font.render('Select Attributes 2',True, '#FFFFFF')
text_enterK = text_font.render('Enter k clusters',True, '#FFFFFF')
text_cenclus= text_font.render('Centroids & Clusters',True, '#FFFFFF')
text_plot = text_font.render('Kmeans Scatter Plot',True, '#FFFFFF')
# Buttons
text_run = text_font.render('RUN',True, '#0c0c0c')
text_reset = text_font.render('RESET',True, '#0c0c0c')
# Initial attributes
text_att1 = text_font.render(attributes[0],True, '#0c0c0c')
text_att2 = text_font.render(attributes[1],True, '#0c0c0c')
# Initial k-value
text_k = text_font.render("2",True, '#0c0c0c')
# Error message
text_error= text_font.render("Attribute1 and Attribute2 should not be the same!",True, '#ffffff')

# Selecting attributes
att1_rect = pygame.Rect(170,18, 165, 22)
att2_rect = pygame.Rect(170,48, 165, 22)
k_rect = pygame.Rect(170,78, 50, 22)

# Button elements
runbtn_rect = pygame.Rect(20,110, 50, 28) 
resetbtn_rect = pygame.Rect(80,110, 60, 28) 
runbtn_color = "#c2dafc"
resetbtn_color = "#c2dafc"

# Table elements
table_rect = pygame.Rect(175,150, 300, 340)
table_items = [] 
y_table_items = []

# Scroll Bar Elements
table_scrollStart = False
table_scroll = pygame.Rect(475, 150, 8, 340)

# 10 colors that can be used in the scatter plot
colors = ["red","blue","green","yellow","orange","purple","lime","aquamarine","pink","darkslategray"]

# Identifying centroids and creating clusters
def createClusters():
    global attribute2_index
    global attribute1_index
    global k
    max = len(inputData)-1      # maximum index
    # Randomize initial centroids
    index_centroids = []
    for i in range(k):
        while(1):
            x = randint(0,max)
            if not x in index_centroids:
                index_centroids.append(x)
                break
    # Initial centroids
    centroids = []
    for index in index_centroids:
        x = (float(inputData[index][attribute1_index]),float(inputData[index][attribute2_index]))
        centroids.append(x)
    plotpoints = []     # plot points 
    for i in range(len(inputData)):
        x = (float(inputData[i][attribute1_index]),float(inputData[i][attribute2_index]))
        plotpoints.append(x)

    while 1:
    # Compute for distances
        clusters = {}   # dictionary where the key= index of centroid (in centroid list), 
                        # value = dictionary with keys 'x' and 'y'
                        # 'x' and 'y' are both lists where the x and y values of the plotpoints are stored
        for p in plotpoints:
            c_distances = []    # The plotpoint's distances from the centroids
            for c in centroids:
                d = (p[0] - c[0])**2 + (p[1] - c[1])**2
                d = math.sqrt(d) 
                c_distances.append(d)
            # Get index of closest centroid
            closest_centroid_index = 0
            for i in range(len(c_distances)):
                if c_distances[i] < c_distances[closest_centroid_index]:
                    closest_centroid_index = i
            ### Place in dictionary the plotpoints based on its closest index
            # If the centroid is not yet on the clusters, create new key-value pair in dict
            if not closest_centroid_index in clusters:
                clusters[closest_centroid_index] = {}
                clusters[closest_centroid_index]['x'] = [p[0]]
                clusters[closest_centroid_index]['y'] = [p[1]]
            # If the centroid is already in dict, append the plotpoints
            else:
                clusters[closest_centroid_index].update({'x':clusters[closest_centroid_index]['x']+[p[0]]})
                clusters[closest_centroid_index].update({'y':clusters[closest_centroid_index]['y']+[p[1]]})
        
        # Compute for new centroids
        prev_centroids = centroids
        centroids = []
        x = 0
        y = 0
        for i in range(len(clusters)):
            x = sum(clusters[i]['x'])/len(clusters[i]['x'])
            y = sum(clusters[i]['y'])/len(clusters[i]['y'])
            centroids.append((x,y)) 

        # Check if the previous set of centroids is equal to the new set of centroids
        if(prev_centroids == centroids):   
            break
    showOutput(clusters,centroids)

# For showing the output to GUI and writing to file
def showOutput(clusters,centroids):
    global table_items
    global y_table_items
    global width
    global image
    global showImage
    global cleared
    cleared = False
    table_items = []
    y_table_items = []
    # Writing to output file
    fileOutput = open(outputFile,"w").close()
    fileOutput = open(outputFile,"a")

    # Clearing the scatter plot: https://www.activestate.com/resources/quick-reads/how-to-clear-a-plot-in-python/
    plt.clf()
    # For every cluster
    for i in range(len(clusters)):
        # Plotting in scatter plot: https://moonbooks.org/Articles/How-to-create-a-scatter-plot-with-several-colors-in-matplotlib-/
        plt.scatter(clusters[i]['x'], clusters[i]['y'],c = colors[i])
        # Appending the centroid to the list (For GUI table)
        table_items.append("Centroid "+str(i)+": ("+str(centroids[i][0])+", "+str(centroids[i][1])+")")
        # Writing the centroid to the output file
        fileOutput.write("Centroid "+str(i)+": ("+str(centroids[i][0])+", "+str(centroids[i][1])+")\n")

        # Assigning datapoints to a list (by category)
        for j in range(len(clusters[i]['x'])):
            x = clusters[i]['x'][j]
            y = clusters[i]['y'][j]
            # Appending the datapoints to the list (For GUI table)
            table_items.append(str(x)+'   '+str(y))
            # Writing the data points to the output file
            fileOutput.write("["+str(x)+', '+str(y)+"]\n")

    # Close output file
    fileOutput.close()

    # Creating y-values for the items in table (Centroids and clusters)
    for i in range(len(table_items)):
        y_table_items.append((i * 20) + 156)

    # Labels
    plt.xlabel(attributes[attribute1_index])
    plt.ylabel(attributes[attribute2_index])

    # Save as img
    plt.savefig('kmeans_scatterplot.png')
    image = pygame.image.load('kmeans_scatterplot.png')
    image = pygame.transform.smoothscale(image, (460, 350)) # https://stackoverflow.com/a/65492828
    showImage = True

# GUI Main loop
while 1:
    time_delta = clock.tick(60) / 1000.0

    # Stores the (x,y) mouse position coordinates to variable(tuple)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        # Exit button is clicked
        if event.type == pygame.QUIT:       
            quit()

        # Mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN:    
            # Attribute1 field is clicked
            if att1_rect.collidepoint(mouse):
                selectAtt1 = True
                selectAtt2 = False
                selectK = False
            # Check what attribute is clicked
            for i in range(len(att1_rects)):
                if att1_rects[i].collidepoint(mouse) and selectAtt1 == True:
                    attribute1_index = i
                    text_att1 = text_font.render(attributes[i],True, '#0c0c0c')
                    selectAtt1 = False
            # Attribute2 field is clicked
            if att2_rect.collidepoint(mouse):
                selectAtt2 = True
                selectAtt1 = False
                selectK = False
            # Check what attribute is clicked
            for i in range(len(att2_rects)):
                if att2_rects[i].collidepoint(mouse) and selectAtt2 == True:
                    attribute2_index = i
                    text_att2 = text_font.render(attributes[i],True, '#0c0c0c')
                    selectAtt2 = False
            # K-value field is clicked
            if k_rect.collidepoint(mouse):
                selectK = True
                selectAtt1 = False
                selectAtt2 = False
            # Check what value is clicked
            for i in range(len(k_rects)):
                if k_rects[i].collidepoint(mouse) and selectK == True:
                    k = i+2
                    text_k = text_font.render(str(i+2),True, '#0c0c0c')
                    selectK = False
            # Run button is clicked
            if runbtn_rect.collidepoint(mouse):
                if attribute1_index != attribute2_index :
                    if cleared:
                        error = False
                        createClusters()
                    else:
                        text_error= text_font.render("    RESET first before running another set of data.",True, '#ffffff')
                        error = True
                else: #
                    text_error= text_font.render("Attribute1 and Attribute2 should not be the SAME!",True, '#ffffff')
                    error = True
            # Reset button is clicked
            if resetbtn_rect.collidepoint(mouse):
                table_items = []
                y_table_items = []
                showImage = False
                cleared = True
                error = False

        # Hover events
        if event.type == pygame.MOUSEMOTION:
            # Run button hover
            if runbtn_rect.collidepoint(mouse):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                runbtn_color = "#aac8f0"
            # Reset button hover
            elif resetbtn_rect.collidepoint(mouse):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                resetbtn_color = "#aac8f0"
            # Fields hover
            elif att1_rect.collidepoint(mouse) or att2_rect.collidepoint(mouse) or k_rect.collidepoint(mouse):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            # Scroll bar hover
            elif table_scroll.collidepoint(mouse) :
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                runbtn_color = "#c2dafc"
                resetbtn_color = "#c2dafc"

        ## Scroll Event (c) https://stackoverflow.com/a/66370052
        mousePressed = pygame.mouse.get_pressed()[0]
        if(len(table_items) != 0 ):
            if mousePressed and table_scroll.collidepoint(mouse):
                table_scrollStart = True
        
            if mousePressed and table_scrollStart:
                table_scroll.y = max(150, min(490 - table_scroll.height, mouse[1]))
                scroll_height = 340 - table_scroll.height 
                scroll_rel = (table_scroll.y - 150) / scroll_height
            
                box_height = 340
                list_height = len(table_items) * 20
                offset = (list_height - box_height) * scroll_rel
            
                for i in range(len(y_table_items)):
                    y_table_items[i] = (i * 20) + 150 - offset
            
            if not mousePressed and table_scrollStart:
                table_scrollStart = False 
        
    # Scatter plot image
    if showImage:
        window_surface = pygame.display.set_mode((1000, 500))
        background = pygame.Surface((1000, 500))
        window_surface.blit(image,(520,80))
        # Adjustment Rects
        pygame.draw.rect(window_surface, '#657ea6', [0,0,520,500]) # left
        pygame.draw.rect(window_surface, '#657ea6', [520,0,480,80]) # top
        pygame.draw.rect(window_surface, '#657ea6', [980,0,20,500]) # right
        pygame.draw.rect(window_surface, '#657ea6', [515,430,485,70]) # bottom
        window_surface.blit(text_plot,(520,50))
    else: # Default
        pygame.draw.rect(window_surface, '#657ea6', [0,0,1000,500]) # background
        window_surface.blit(text_plot,(680,230))
        
    # Centroids & Clusters table
    pygame.draw.rect(window_surface, 'white', table_rect)
    pygame.draw.rect(window_surface, '#405169', table_rect,1)
    
    for x in range(len(table_items)) :
        data = text_font_small.render(table_items[x], True, (0, 0, 0))
        window_surface.blit(data, (180, y_table_items[x]))
     
    # Adjustment Rects
    pygame.draw.rect(window_surface, '#657ea6', [475,0,45,500]) # right side
    pygame.draw.rect(window_surface, '#657ea6', [175,0,345,150]) # top
    pygame.draw.rect(window_surface, '#657ea6', [175,490,345,20]) # bottom

    # Scroll bar
    table_scroll.height = (30 if len(y_table_items) > 0 else 340) 
    if (table_scroll.y < 150): table_scroll.y = 150
    if (table_scroll.y + table_scroll.height) > 490: table_scroll.y = 490 - table_scroll.height
    pygame.draw.rect(window_surface, 'gray', [475, 150, 8, 340])
    pygame.draw.rect(window_surface, '#646464', table_scroll)
    
    # Texts
    window_surface.blit(text_select1,(20,20))
    window_surface.blit(text_select2,(20,50))
    window_surface.blit(text_enterK,(20,80))
    window_surface.blit(text_cenclus,(20,290))
    
    # Line
    pygame.draw.line(window_surface , "#ffffff", (500, 495), (500, 5))

    # Buttons
    pygame.draw.rect(window_surface, runbtn_color, runbtn_rect)
    pygame.draw.rect(window_surface, '#405169', runbtn_rect,1)
    window_surface.blit(text_run,(30,115))
    pygame.draw.rect(window_surface, resetbtn_color, resetbtn_rect)
    pygame.draw.rect(window_surface, '#405169', resetbtn_rect,1)
    window_surface.blit(text_reset,(89,115))

    # Message for same attributes
    if error == True:
        pygame.draw.rect(window_surface,"red",[165,112,333,24])
        window_surface.blit(text_error,(170,115))

    # Enter N
    pygame.draw.rect(window_surface, 'white', k_rect)
    window_surface.blit(text_k,(175,80))
    if selectK == True:
        for y in range(9) :
            pygame.draw.rect(window_surface, '#f0f6ff', k_rects[y])
            word = text_font.render(str(y+2), True, (0, 0, 0))
            window_surface.blit(word, (175, y_k_items[y]))
            
    # Attribute Selection
    # Attribute2
    pygame.draw.rect(window_surface, 'white', att2_rect)
    window_surface.blit(text_att2,(175,50))
    if selectAtt2 == True:
        for y in range(len(attributes)) :
            pygame.draw.rect(window_surface, '#f0f6ff', att2_rects[y])
            word = text_font.render(attributes[y], True, (0, 0, 0))
            window_surface.blit(word, (340, y_att2_items[y]))
    # Attribute1
    pygame.draw.rect(window_surface, 'white', att1_rect)
    window_surface.blit(text_att1,(175,20))
    if selectAtt1 == True:
        for y in range(len(attributes)) :
            pygame.draw.rect(window_surface, '#f0f6ff', att1_rects[y])
            word = text_font.render(attributes[y], True, (0, 0, 0))
            window_surface.blit(word, (340, y_att1_items[y]+2)) 
    
    # Display update
    pygame.display.update()