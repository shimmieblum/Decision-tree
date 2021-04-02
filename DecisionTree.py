import random
import numpy as np
from collections import Counter

class TreeNode:
    '''this is a simple tree node. it simply contains the feature it represents and its right and left children.
    the left child is the result of taking action 0 on feature f and right is action 1 on feature f
    there is a method traverse which will traverse the tree with an input and respond with a decision '''
    def __init__(self, feature, impurity, left, right):
        self.f = feature
        self.impurity = impurity
        self.l = left
        self.r = right
        
    def traverse(self, input):
        if input[self.f] == 0: return self.l.traverse(input)
        elif input[self.f] == 1: return self.r.traverse(input)
        
    def __str__(self):
        f = self.f
        l = self.l 
        r = self.r
        
        return '(node ' + str(f) +'\nleft: '+str(l)+' || right: '+str(r)    
                
                
    def __repr__(self):
        return str(self)

class ClassNode:
    ''' this represents a terminal leaf node which will define a class. its travers method simply returns the class description'''
    def __init__(self, value):
        self.v = value
    
    def traverse(self, input):
        return self.v
    
    def __str__(self):
        return 'c'+str(self.v)
    
    def __repr__(self):
        return str(self)
    
    
class DecisionTree:
    
    def __init__(self, trainX ,trainY):
        ''' input the training examples X and targets Y and create a decision tree'''
        print 'making tree'
        self.features = list(range(len(trainX[0])))
        self.probs = self.__initialProbs(trainY)
        self.root = self.__growTree(trainX, trainY)
    
    def getDecision(self, inp):
        return self.root.getDecision(inp)
        
    def __initialProbs(self, target):
        ''' create the initial probability of each class. if a leaf is reached and there is no data for that combination, 
        simply use the initial probability to assign it a value stochastically'''
        a = {x:0.0 for x in list(set(target))}
        for t in target: a[t] += 1.0
        length = len(target)
        b = {k:(v/length) for k,v in a.items()}
        return b
    
    def __assignClass(self):
        '''choose the class of a path with no data according to the probability of each class'''
        val = random.random()
        tot = 0.0
        for c,prob in self.probs.items():
            tot +=prob
            if val < tot: return c
        
    def __growTree(self, data, target):
        ''' recursively create the tree'''
        if len(list(set(target))) == 1: return ClassNode(target[0]) # if there is only one target, this is a decision
        elif len(list(set(target))) == 0: return ClassNode(self.__assignClass()) # if there is no data, randomly assign a decision
        elif [j for i in data for j in i if j != None] == []: # if all the features have been assessed and there is still no decision, choose most likely
            v = (Counter(target).most_common(1)[0][0])
            return ClassNode(value=v)
        feature = self.__pick_a_feature(data,target) # else, choose the best feature using gini index for each node
        left_data, left_target = self.__get_data_and_target(data, target, feature, 0) #split data into right and left at this feature
        right_data, right_target = self.__get_data_and_target(data,target,feature, 1)
        return TreeNode(feature=feature, impurity=0, # return a tree node and create right and left children using the new data for each
                        left=self.__growTree(left_data, left_target),
                        right = self.__growTree(right_data,right_target))
      
    
    def __pick_a_random_feature(self, data, target):
        '''simple method of picking feature to split on - pick one at random
        not in use, just for interest'''
        choices = []
        for row in data:
            for i,a in enumerate(row):
                if a !=None: choices.append(i)
        return random.choice(choices)
    
    def __pick_a_feature(self, data, target):
        '''identify the feature with the highest gini average and return that feature index'''
        bestF = -1
        bestGini = -1
        for f in range(len(data[0])):    # loop for all features in data
            if data[0][f] == None: continue # use None to identify features already in the tree.
            m = {1:[],0:[]} # create dict for each possible value and its set of targets
            for r in range(len(data)): # for each row in the data get value of this feature and associated target and place in dictionary 
                value = data[r][f] # value of feature
                rowTarget = target[r] # associated target
                m[value].append(rowTarget) 
            giniavg = 0
            for val, t in m.items(): 
                gini = self.__gini(t) # for each value, find gini index
                giniavg += gini * (len(t)/len(target)) # gini average is the index * the num values associated divided by the total number of values
            if giniavg > bestGini: 
                bestGini = giniavg
                bestF = f
        if bestF == -1 and bestGini == -1: return None # ie no data was provided to be used
        return bestF
                
    def __gini(self, targets):
        '''calculate gini impurity of a set of given set of targets and return'''
        G = 1
        for k in set(targets):
            pk = len([x for x in targets if x == k])/len(targets)
            G -= pk**2
        return G
    
    def __poss_vals_of(self, data, feature):
        ''' get all possible values for data'''
        all_vals = []
        for d in data:
            all_vals.append(d[feature])
        return all_vals
    
    def __get_data_and_target(self, data, target, feature, val):
        ''' return lists of the data and target remaining when assigning a given value to a given feature
        used to split data at a given feature'''
        returnData = []
        returnTarget = []
        for i,d in enumerate(data):
            d = list(d)
            target_val = target[i]
            if d[feature] == val:
                d[feature] = None
                returnData.append(d)
                returnTarget.append(target_val)
        return returnData,returnTarget
    
class RandomForest:
    
    def __init__(self, numTrees, sampleSize, trainX, trainY):
        self.forest = []
        self.__trainRandom_forest(numTrees, sampleSize, trainX, trainY)
    
    def __trainRandomForest(self,numTrees, sampleSize, trainX, trainY):
        '''create a random forest by using samples from the training data and making multiple trees from these samples'''
        self.forest = []
        for i in range(0,numTrees):
            sampleX, sampleY = self.__getTrainingSample(sampleSize, trainX, trainY)
            tree = DecisionTree(sampleX, sampleY)
            self.forest.append(tree)
            
    def __getTrainingSample(self, n, trainX, trainY):
        '''generate set of examples and targets of size n and return tuple of examples and associated targets'''
        dataSample = []
        targets = []
        for i in random.sample(range(0, len(trainX) - 1), n):    
            dataSample.append(trainX[i])
            targets.append(trainY[i])
        return dataSample, targets
        
    def getDecisionFromForest(self,array):
        '''run an input on all the trees in the random forest and take the most common decision'''
        decisions = []
        for tree in self.forest:
            decision = tree.traverse(array)
            decisions.append(decision)
        return Counter(decisions).most_common(1)[0][0]
    
    def getProbabilityVectorFromForest(self, array):
        '''run an input on all the trees in the random forest and return a dictionary of each possible target and its probability'''
        decisions = []
        for tree in self.forest:
            decision = tree.traverse(array)
            decisions.append(decision)
        numberOfDecisions = len(decisions)
        vector = {x: (decisions.count(x)/numberOfDecisions) for x in set(decisions)}
        return vector
