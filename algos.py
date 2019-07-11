'''
1. subset template
2. binary search template
3. dfs template
4. bfs template
5. dp templates
6. linked list insert/delete
'''

graph = {
	"A": ["B", "C"],
	"B": ["C", "D", "A"],
	"C": ["A", "B", "D", "E"],
	"D": ["B", "C", "E", "F"],
	"E": ["C", "D"],
	"F": ["D"]
}

#BFS:

def BFS(graph, root):
	queue = []
	queue.append(root)
	visited = set()

	while(queue):
		vertex = queue.pop(0)
		candidates = graph[vertex]
		for w in candidates:
			if w not in visited:
				queue.append(w)
				visited.add(w)
		print(vertex)

#BFS(graph, "A")

#DFS:
#replace queue with stack(name only)
#change queue.pop(0) to stack.pop()

def DFS(graph, root):
	stack = []
	stack.append(root)
	visited = set()

	while(stack):
		vertex = stack.pop()
		candidates = graph[vertex]
		for w in candidates:
			if w not in visited:
				stack.append(w)
				visited.add(w)
		print(vertex)

#DFS(graph, "A")


#Simplified version:

def DFS(graph, root):
	stack = []
	stack.append(root)
	visited = set()
	while(stack):
		vertex = stack.pop()
		visited.add(vertex)
		candidates = graph[vertex]
		candidates = list(set(candidates) - visited)
		stack = stack + candidates
		visited = visited.union(set(candidates))
		print(vertex)
DFS(graph, "F")



'''
tuple: (), []
string: [], len(), *, + , [:], in, %, find(), 
list: [], append, pop, pop(n), remove(), if(list), max(), min(), count(item), reverse(), sort()
set: set(), add(), remove, in, if(len(set) == 0), -, intersection, update, sorted(), 
dict: keys(), items(), values(), has_key(), del, cmp, len, copy, 

'''