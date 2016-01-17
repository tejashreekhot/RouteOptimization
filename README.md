# RouteOptimization

This program gives route between two cities optimized for distance, segements or time using various tree search algorithms . 

Program called as:
python route.py [start-city] [end-city] [routing-option] [routing-algorithm]

where:
• start-city and end-city are the cities we need a route between.

• routing-option is one of:
– segments finds a route with the fewest number of “turns” (i.e. edges of the graph)
– distance finds a route with the shortest total distance
– time finds the fastest route, for a car that always travels at the speed limit

• routing-algorithm is one of:
– bfs uses breadth-first search
– dfs uses depth-first search
– astar uses A* search, with a suitable heuristic function

