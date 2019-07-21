# -*- coding: utf-8 -*-
"""

@author: ramon, bojana
"""
import re
import numpy as np
import ColorNaming as cn
from skimage import color
import KMeans as km

def NIUs():
    return [1423957,1460646,1425083]

def loadGT(fileName):
    """@brief   Loads the file with groundtruth content
    
    @param  fileName  STRING    name of the file with groundtruth
    
    @return groundTruth LIST    list of tuples of ground truth data
                                (Name, [list-of-labels])
    """

    groundTruth = []
    fd = open(fileName, 'r')
    for line in fd:
        splitLine = line.split(' ')[:-1]
        labels = [''.join(sorted(filter(None,re.split('([A-Z][^A-Z]*)',l)))) for l in splitLine[1:]]
        groundTruth.append( (splitLine[0], labels) )
        
    return groundTruth


def evaluate(description, GT, options):
    """@brief   EVALUATION FUNCTION
    @param description LIST of color name lists: contain one lsit of color labels for every images tested
    @param GT LIST images to test and the real color names (see  loadGT)
    @options DICT  contains options to control metric, ...
    @return mean_score,scores mean_score FLOAT is the mean of the scores of each image
                              scores     LIST contain the similiraty between the ground truth list of color names and the obtained
    """
    scores = []
    for i in range(len(description)):
        scores.append(similarityMetric(description[i],GT[i][1],options))
    print scores
    
    return sum(scores)/float(len(scores)), scores



def similarityMetric(Est, GT, options):
    """@brief   SIMILARITY METRIC
    @param Est LIST  list of color names estimated from the image ['red','green',..]
    @param GT LIST list of color names from the ground truth
    @param options DICT  contains options to control metric, ...
    @return S float similarity between label LISTs
    """
    
    if options == None:
        options = {}
    if not 'metric' in options:
        options['metric'] = 'basic'
        
    if options['metric'].lower() == 'basic'.lower():
        intersect = np.intersect1d(np.array(Est), np.array(GT))        
        return intersect.size/float(len(Est))
    else:
        return 0
    
        
def getLabels(kmeans, options):
    """@brief   Labels all centroids of kmeans object to their color names
    
    @param  kmeans  KMeans      object of the class KMeans
    @param  options DICTIONARY  options necessary for labeling
    
    @return colors  LIST    colors labels of centroids of kmeans object
    @return ind     LIST    indexes of centroids with the same color label
    """
##  remind to create composed labels if the probability of 
##  the best color label is less than  options['single_thr']
    #np.set_printoptions(threshold=np.inf)
    centroidesInfo = {}
    #miramos para cada uno de los clusters, cuantos pixeles tienen en total y le asignamos un color
    #lo guardamos como un diccionario con clave igual al indice del cluster que representa, y dentro un diccionario con la informacion del cluster
    for i in range(kmeans.K):       
        info = {}
        info["totalPixels"] = np.where(kmeans.clusters == i)[0].size
        info["centroide"] = kmeans.centroids[i]
        indicesPosColores = np.argsort(kmeans.centroids[i])[::-1]
        
        if kmeans.centroids[i][indicesPosColores[0]] > options['single_thr']:
            info["color"] = cn.colors[indicesPosColores[0]]
        else:
            if cn.colors[indicesPosColores[0]] < cn.colors[indicesPosColores[1]]:
                info["color"] = cn.colors[indicesPosColores[0]]+cn.colors[indicesPosColores[1]]
            else:
                info["color"] = cn.colors[indicesPosColores[1]]+cn.colors[indicesPosColores[0]]            
            
        centroidesInfo[i] = info
    
    colores = {}
    
    for centroid in range(kmeans.K):
        
        if centroidesInfo[centroid]['color'] not in colores:
            colores[centroidesInfo[centroid]['color']] = centroidesInfo[centroid]['totalPixels']
        else:
            colores[centroidesInfo[centroid]['color']] += centroidesInfo[centroid]['totalPixels']
    
    #Ordenamos los colores por su numero de pixeles. Para ello usaremos 
    #los valores guardados en colores, lo pasaremos a una lista solo con los valores numericos del
    #total de pixeles y guardaremos los indices para recoger el nombre del color
    coloresToNpArray = np.array(list(colores.items()))
    coloresOrdenados = np.argsort(np.array(list(colores.values())))[::-1]    
    
    meaningful_colors = [coloresToNpArray[color][0] for color in coloresOrdenados]
    count = 0
    unique = []
    
    for color in meaningful_colors:
        unique.append([])
        for centroid in range(kmeans.K):            
            if centroidesInfo[centroid]['color'] == color:
                unique[count].append(centroid)
        count += 1
    
    return meaningful_colors, unique
    

def processImage(im, options):
    """@brief   Finds the colors present on the input image
    
    @param  im      LIST    input image
    @param  options DICTIONARY  dictionary with options
    
    @return colors  LIST    colors of centroids of kmeans object
    @return indexes LIST    indexes of centroids with the same label
    @return kmeans  KMeans  object of the class KMeans
    """

#########################################################
##  YOU MUST ADAPT THE CODE IN THIS FUNCTIONS TO:
##  1- CHANGE THE IMAGE TO THE CORRESPONDING COLOR SPACE FOR KMEANS
##  2- APPLY KMEANS ACCORDING TO 'OPTIONS' PARAMETER
##  3- GET THE NAME LABELS DETECTED ON THE 11 DIMENSIONAL SPACE
#########################################################

##  1- CHANGE THE IMAGE TO THE CORRESPONDING COLOR SPACE FOR KMEANS
    if options['colorspace'].lower() == 'ColorNaming'.lower():
        im = cn.ImColorNamingTSELabDescriptor(im)        
    elif options['colorspace'].lower() == 'RGB'.lower(): 
        pass        
        
    elif options['colorspace'].lower() == 'Lab'.lower():
        im = color.rgb2lab(im)

    
    else:
        im = color.rgb2hsv(im)
        
   ##  2- APPLY KMEANS ACCORDING TO 'OPTIONS' PARAMETER
    if options['K'] < 1:  # find the best K
        kmeans = km.KMeans(im, 3, options)
        kmeans.bestK()
    else:
        kmeans = km.KMeans(im, options['K'], options)
        kmeans.run()


    ##  3- GET THE NAME LABELS DETECTED ON THE 11 DIMENSIONAL SPACE

    if options['colorspace'].lower() == 'ColorNaming'.lower():
        pass

    elif options['colorspace'].lower() == 'RGB'.lower():
        kmeans.centroids = cn.ImColorNamingTSELabDescriptor(kmeans.centroids)
        
    elif options['colorspace'].lower() == 'Lab'.lower():
        dimensionesTmp = kmeans.centroids.shape
        kmeans.centroids = (color.lab2rgb(kmeans.centroids.reshape((1, -1, 3))) * 255)
        kmeans.centroids = cn.ImColorNamingTSELabDescriptor(kmeans.centroids.reshape(dimensionesTmp))
    else:
        dimensionesTmp = kmeans.centroids.shape
        kmeans.centroids = (color.hsv2rgb(kmeans.centroids.reshape((1, -1, 3))) * 255)
        kmeans.centroids = cn.ImColorNamingTSELabDescriptor(kmeans.centroids.reshape(dimensionesTmp))


    #########################################################
    ##  THE FOLLOWING 2 END LINES SHOULD BE KEPT UNMODIFIED
    #########################################################
    colors, which = getLabels(kmeans, options)
    return colors, which, kmeans