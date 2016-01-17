# -*- coding: utf-8 -*-
'''
Routing algorithm:
distance-distance calculations consisting fast due expansion of only promising nodes
time- calculation fast but still slowed than distance due to precomputing.

bfs- great in shallow searches but as searches get deeper, due increased space complexity  and increased complexity of structure slowed. 
dfs- mostly the slowest. But can find result fastest, most random time distribution which completely depends on how the tree is constructed.  least time spent on each single search due to lack of computation. 

For the routing option: 
--------------------------------------------------------------------------------------------------------
segments : find a route with the fewest number of turns.  
bfs will give us a correct answer. 
dfs won’t work. It will give you a answer but might not be the “fewest” number. 
astar could work in this option if we let h(n)=0 and g(n)= number of segment. 
-----------------------------------------------------------------------------------------------------------
distance : find a route with the shortest total distance. 
We cann’t use bfs and dfs to find the answer. 
We can only use astar in here.The heuristic function 

h(N)= the geodesic distance from current-city to end-city 
=  great-circle distances between two points on a sphere from their longitudes and latitudes. 
g(N)=sum of distance that traveled from start-city to N state.
For the specific function we refer it to haversine formula 
[1] https://en.wikipedia.org/wiki/Haversine_formula 
------------------------------------------------------------------------------------------------------------------
time : find the fastest route, for a car that always travels at the speed limit. 
bfs and dfs won’t work.
We can only use astar in here.The heuristic function 
h(N)= the geodesic distance from current-city to end-city / max {speed of all city except the city have already been visited}
g(N)=sum of time that traveled from start-city to N state. time=(each route)/(each max speed). precomputed time for each segment. 
--------------------------------------------------------------------------------------------------------------------

successor: All road segment are also received and kept in a list. So two instance of each road set in list, both start and end city received. 

successor: find all cities speed just from nonvisited cities. if the max speed of those city are decreasing then replace the old max speed to the new max speed and then calculate the time for h(N).
'''
__author__ = "Owner"
__date__ = "$15 Sep, 2015 11:27:13 AM$"
import copy
import Queue as Q
import math
import sys
import timeit
class node(object):
    
    def __init__(self, s, cost,  path, costt):
        global goalx, astard, astart
        self.s = s
        self.cost=cost
        self.path=path
	self.costt=costt
        if astard:
            self.hd=self.distance(self.s[0],goalx,-1)
        #print self.s
        #ll=[x[1:3] 
        #global goalx
            self.fd=cost+self.hd
	    	
        if astart:
            global maxspeed
            self.ht=self.distance(self.s[0],goalx,-1)/maxspeed
            #self.costt=costt
            self.ft=self.ht+self.cost
            
            
    def distance(self, currx, goalx,y):
        found=False
        
        for x in cityinfolist:
            if x[0]==currx:
                clat=float(x[1])
                clon=float(x[2])
                if clat!=1000 and clon!=1000:
                    found=True
                #print lat, lon
            if x[0]==goalx:
                glat=float(x[1])
                glon=float(x[2])
        if found:
            dislat = math.radians(glat-clat)
            dislon = math.radians(glon-clon)
            a = math.sin(dislat/2) * math.sin(dislat/2) + math.cos(math.radians(clat)) * math.cos(math.radians(glat)) * math.sin(dislon/2) * math.sin(dislon/2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            self.hd = 3959 * c
            
        if not found:
            y=y-1
            prevcity=self.path.split(" ")[y]
            
            for k in roadseglist:
                if k[0]==prevcity and k[1]==currx:
                    dpc=int(k[3])
                    
            self.hd=self.distance(prevcity,goalx,y)+dpc
        return self.hd
            
            
    def check(self, goal):
        #print self.path.split(" ")[-1]
        if self.path.split(" ")[-1]==goal:
            return True
        else:
            return False    
    
    def succ(self):
        s=  self.path.split(" ")[-1]
        y=[x for x in roadseglist if x[0]==s]
        newnodes=[]
        for z in y:
            newstate=[z[1], "1000", "1000"]
            for n in cityinfolist:
                if n[0]==z[1]:
                    newstate=n
            if not astart:
		if float(z[3])!=0:
                	newnode=node(newstate , self.cost+int(z[2]), self.path+" "+z[1], self.costt+(float(z[2])/float(z[3])))
			newnodes.append(newnode)
            if astart:
                newnode=node(newstate , self.cost+float(z[5]), self.path+" "+z[1],self.costt+int(z[2]))
        	newnodes.append(newnode)
            
        return newnodes
    
if __name__ == "__main__":
    s=timeit.default_timer()
    f=[]
    for arg in sys.argv: 
    	f.append(arg)
    goalx=f[2]
    inix=f[1]
    rotop=f[3]
    roalgo=f[4]
    bfs=False
    dfs=False
    astard=False
    astart=False
    #print f		
    if roalgo=="bfs":
	bfs=True
	if rotop=="segments":
		print "bfs gives least number of segments"
	if rotop=="distance":
		print "bfs will not give best distance results, displaying route using bfs"
	if rotop=="time":
		print "bfs will not give best time results, displaying route using bfs"
    if roalgo=="dfs":
	dfs=True
        if rotop=="segments":
		print "dfs will not give best segments results, displaying route using dfs"
	if rotop=="distance":
		print "dfs will not give best distance results, displaying route using dfs"
	if rotop=="time":
		print "dfs will not give best time results, displaying route using dfs"
    if roalgo=="astar":
	if rotop=="segments":
		print "astar and bfs give best resultd on segments:"
		bfs=True
		
    	
	if rotop=="distance":
		print "astar will give best distance results, displaying route using astar"
		
        	astard=True
    		
    	
	if rotop=="time":
		print "astar will give best time results, displaying route using astar"
		
    		astart=True
    	
	
    
    if(bfs):
        citygpsfile=open("city-gps.txt","r")
        city=citygpsfile.readlines()

        cityinfolist=[]
        for i in city:
            i=i.rstrip("\n")
     #       i=i+" False"
            cityinfo=i.split(" ")

            cityinfolist.append(cityinfo)
        #print cityinfolist    
        roadsegfile=open("road-segments.txt","r")
        roadseg=roadsegfile.readlines()

        roadseglist=[]

        for i in roadseg:
            i=i.rstrip("\n")

            roadseginfo=i.split(" ")
        #print cityinfo
            roadsegrev=[roadseginfo[1]]+[roadseginfo[0]]+roadseginfo[2:5]
        #print roadsegrev
            roadseglist.append(roadseginfo)
            roadseglist.append(roadsegrev)
    #ini=node()
        #print roadseglist
        for i in cityinfolist:
            if i[0]==inix:
                ini=node(i , 0, inix,0)
   
        visited=[]
        fringe=Q.Queue()
        fringe.put(ini)
        goalfound=False
    #print goalfound
        visited.append(ini.s)
        if not ini.check(goalx):
            while not (fringe.empty() or goalfound):
            #print "hey"
                y=fringe.get()
                #print y.s, y.cost, y.path
                for x in y.succ():
                    if x.check(goalx):
                        print "Goal state reached\n", x.cost, x.costt, x.path
                        goalfound=True
                        break
                    else:
                        if(x.s not in visited):
                            fringe.put(x)
                            visited.append(x.s)
                            
            if fringe.empty() and not goalfound:
                print "Failure fringe empty"

    
        else:
            print "Initial state is goal"
        citygpsfile.close()
        roadsegfile.close()
    if(astart):
        citygpsfile=open("city-gps.txt","r")
        city=citygpsfile.readlines()

        cityinfolist=[]
        for i in city:
            i=i.rstrip("\n")

            cityinfo=i.split(" ")

            cityinfolist.append(cityinfo)
#       # print cityinfolist    
        roadsegfile=open("road-segments.txt","r")
        roadseg=roadsegfile.readlines()

        roadseglist=[]

        for i in roadseg:
            i=i.rstrip("\n")

            roadseginfo=i.split(" ")
        #print cityinfo
            roadsegrev=[roadseginfo[1]]+[roadseginfo[0]]+roadseginfo[2:5]
        #print roadsegrev
            roadseglist.append(roadseginfo)
            roadseglist.append(roadsegrev)
        maxspeed=0
        #print [i for i in roadseglist if i[3]=='']
        for i in roadseglist:
          #  print i
            if (i[3]!=''):
                k=int(i[3])
                if k>maxspeed:
                    maxspeed=k
        for j in roadseglist:
            if (j[3])=='':
                j[3]=maxspeed
                
        for k in roadseglist:
           # print "hey"
            #print k
            if float(k[3])==0.0:
                roadseglist.remove(k)
            else:
                k.append(float(k[2])/float(k[3]))
            
        #print roadseglist
        for i in cityinfolist:
            if i[0]==inix:
                ini=node(i , 0, inix,0)
   
        visited=[]
        fringe=Q.PriorityQueue()
        if(not ini.check(goalx)):
            
            fringe.put((ini.ft,ini))
        #print fringe.empty()
        visited.append(ini.s)
        goalfound=False
        #print "heya"
    #print goalfound

        if not ini.check(goalx):
            print "hi"
            while not (fringe.empty()):
               # print "hey"
                y=fringe.get()[1]
                #print y.s
                
                if y.check(goalx):
                    print "Goal state reached\n", x.costt, x.cost, x.path
                    goalfound=True
                    break
                for x in y.succ():
                    if x.s not in visited:
                        fringe.put((x.ft,x))
                        visited.append(x.s)
        
            if fringe.empty() and not goalfound:
                print "Failure fringe empty"

    
        else:
            print "Initial state is goal"

        citygpsfile.close()
        roadsegfile.close()
    if(astard):
        citygpsfile=open("city-gps.txt","r")
        city=citygpsfile.readlines()

        cityinfolist=[]
        for i in city:
            i=i.rstrip("\n")

            cityinfo=i.split(" ")

            cityinfolist.append(cityinfo)
#        #print cityinfolist    
        roadsegfile=open("road-segments.txt","r")
        roadseg=roadsegfile.readlines()

        roadseglist=[]

        for i in roadseg:
            i=i.rstrip("\n")

            roadseginfo=i.split(" ")
        #print cityinfo
            roadsegrev=[roadseginfo[1]]+[roadseginfo[0]]+roadseginfo[2:5]
        #print roadsegrev
            roadseglist.append(roadseginfo)
            roadseglist.append(roadsegrev)
        for i in cityinfolist:
            if i[0]==inix:
                ini=node(i , 0, inix,0)
   
        visited=[]
        fringe=Q.PriorityQueue()
        if(not ini.check(goalx)):
            
            fringe.put((ini.fd,ini))
       # print fringe.empty()
        visited.append(ini.s)
        goalfound=False
      #  print "heya"
    #print goalfound

        if not ini.check(goalx):
       #     print "hi"
            while not (fringe.empty()):
         
#       print "hey"
                y=fringe.get()[1]
           #     print y.s
                
                if y.check(goalx):
                    print "Goal state reached\n", x.cost, x.costt, x.path
                    goalfound=True
                    break
                for x in y.succ():
                    if x.s not in visited:
                        fringe.put((x.fd,x))
                        visited.append(x.s)
        
            if fringe.empty() and not goalfound:
                print "Failure fringe empty"

    
        else:
            print "Initial state is goal"

        citygpsfile.close()
        roadsegfile.close()
    if(dfs):
        citygpsfile=open("city-gps.txt","r")
        city=citygpsfile.readlines()

        cityinfolist=[]
        for i in city:
            i=i.rstrip("\n")

            cityinfo=i.split(" ")

            cityinfolist.append(cityinfo)
#        print cityinfolist    
        roadsegfile=open("road-segments.txt","r")
        roadseg=roadsegfile.readlines()

        roadseglist=[]

        for i in roadseg:
            i=i.rstrip("\n")

            roadseginfo=i.split(" ")
        #print cityinfo
            roadsegrev=[roadseginfo[1]]+[roadseginfo[0]]+roadseginfo[2:5]
        #print roadsegrev
            roadseglist.append(roadseginfo)
            roadseglist.append(roadsegrev)
        for i in cityinfolist:
            if i[0]==inix:
                ini=node(i , 0, inix,0)
   
        visited=[]
        fringe=Q.LifoQueue()
        fringe.put(ini)
        visited.append(ini.s)
        goalfound=False
    #print goalfound

        if not ini.check(goalx):
            while not (fringe.empty() or goalfound):
            #print "hey"
                y=fringe.get()
             #   print y.s, y.cost
                for x in y.succ():
                    if x.check(goalx):
                        print "Goal state reached\n", x.cost, x.costt, x.path
                        goalfound=True
                        break
                    else:
                        if x.s not in visited:
                            fringe.put(x)
                            visited.append(x.s)
        
            if fringe.empty() and not goalfound:
                print "Failure fringe empty"

    
        else:
            print "Initial state is goal"

        citygpsfile.close()
        roadsegfile.close()
    e=timeit.default_timer()
 #   print e-s
