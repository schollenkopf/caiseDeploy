import app.trie as trie


class Node:  # alias Log

    def __init__(self, eventLog, id):
        self.eventLog = eventLog
        self.hash = self.hashNode(eventLog)
        self.id = id

    def hashNode(self, eventLog):
        hash = ""
        # NOTE maybe since the order of the traces should not matter they should be ordered with respect to the alphabetical order of the ids
        traces = eventLog.traces
        for trace in traces:
            hash += trace.getHash()  # NOTE all equivalent event-log must have the same hash
        return hash

    def getEventLog(self):
        return self.eventLog.getAsList()

    def getDescription(self):
        return self.eventLog.getDescription()
    
    def equals(self,node):
        return self.eventLog.equals(node.eventLog)


class Graph:

    def __init__(self, eventLog, truedatagraph):
        print("truedatagraph", truedatagraph)
        print("truedatagraph TYPE", type(truedatagraph))
        self.truedatagraph = truedatagraph
        self.root = Node(eventLog.copy(), 0)  
        self.nodes = [self.root]
        if (self.truedatagraph):
            self.true_nodes = [self.root]
            self.true_adjecency_graph = [[]]
            self.true_graph_2_trie_graph = {0: [0]}

        self.trie = trie.Trie()
        self.adjecency_graph = [[]]
        self.lastNode = 0

        self.nr_trie_nodes = 1
        self.clean_graph_2_trie_graph = {0: [0]}

        # I just need this info stored somewhere:
        self.logdetails = {}

    # Whenever a diff (filter) is created we need to generate a new node
    # [operation] or list of diff/filter that have been applied in the path
    def addOperation(self, currentTrieNodeId, newEventLog, operations):
        id = self.trie.search(operations)
        currentNode = self.getNodefromId(currentTrieNodeId)
        if not id:
            print("ID IN ADD OPERATION", currentNode.id)

            # NOTE is going to be a problem if we delete nodes
            newNodeNotChecked = Node(newEventLog, len(self.nodes))
            

            # check if node already exists
            newNode = self.checkForMatch(newNodeNotChecked)
            self.trie.insert(operations, self.nr_trie_nodes)

            self.clean_graph_2_trie_graph[newNode.id].append(self.nr_trie_nodes)

            self.lastNode = self.nr_trie_nodes


            if (self.truedatagraph):
                newTrueNodeNotChecked = Node(newEventLog, len(self.true_nodes))
                newTrueNode = self.checkForTrueMatch(newTrueNodeNotChecked)
                print("THE CURRENT ID",currentNode.id)
                self.true_graph_2_trie_graph[newTrueNode.id].append(self.nr_trie_nodes)
                self.true_adjecency_graph[currentNode.id].append((operations[-1], newTrueNode.id))

                #convert Trie node to Clean Node for Clean Graph:

                for key in self.clean_graph_2_trie_graph:
                    if (currentTrieNodeId in self.clean_graph_2_trie_graph[key]):
                        clean_id = key

                self.adjecency_graph[clean_id].append(
                (operations[-1], newNode.id))
            else:
                
                self.adjecency_graph[currentNode.id].append(
                (operations[-1], newNode.id))

            self.nr_trie_nodes += 1
            print("AG", self.adjecency_graph)

        else:
            print("IDi", id)
            self.lastNode = id

    def getEventLogFromId(self, id):
        print(self.trie)
        node = self.getNodefromId(id)
        return node.getEventLog()

    # returns the new node or the equivalent old one

    def checkForMatch(self, newNode):
        for node in self.nodes:
            if node.hash == newNode.hash:

                if True:  # TODO here we need a further check, maybe done line by line in each trace between the two eventlogs

                    return node
        # if node does not match with any other node, add an entry to node list and adjacency graph
        self.nodes.append(newNode)
        self.adjecency_graph.append([])
        self.clean_graph_2_trie_graph[newNode.id] = []
        return newNode

    def checkForTrueMatch(self, newNode):
        for node in self.true_nodes:
            if node.hash == newNode.hash:

                if (node.equals(newNode)):

                    return node
        # if node does not match with any other node, add an entry to node list and adjacency graph
        self.true_nodes.append(newNode)
        self.true_adjecency_graph.append([])
        self.true_graph_2_trie_graph[newNode.id] = []
        return newNode

    def getNodefromId(self, id):
        if (self.truedatagraph):
            return self.true_nodes[self.trueNodeFromTrieNode(id)]
        return self.nodes[self.cleanNodeFromTrieNode(id)]

    def getEdges(self):
        result = []
        for node_id, next_nodes in enumerate(self.adjecency_graph):
            for (operation, next_node_id) in next_nodes:
                result.append({"parentNode": node_id,
                              "childrenNode": next_node_id, "operation": operation.getName()})
        return result
    
    def getTrueEdges(self):
        result = []
        print("TRUE GRAPH",self.true_adjecency_graph)
        for node_id, next_nodes in enumerate(self.true_adjecency_graph):
            for (operation, next_node_id) in next_nodes:
                result.append({"parentNode": node_id,
                              "childrenNode": next_node_id, "operation": operation.getName()})
        return result

    def getTrueGraph(self):
        result = [{"id": 0, "nodes": [{"id": 0, "description" : self.true_nodes[0].getDescription()}]}]
        self.getTrueGraphRecursive(1, [0], [0], result)
        return result

    def getTrueGraphRecursive(self, level, alradyScoutedNodes, nodesFromPreviousLayer, result):
        nodes = []
        nodesForNextLayer = []
        for previousNode in nodesFromPreviousLayer:
            for operation, node in self.true_adjecency_graph[previousNode]:
                if node not in alradyScoutedNodes:
                    nodes.append({"id": node, "description" : self.true_nodes[node].getDescription()})
                    alradyScoutedNodes.append(node)
                    nodesForNextLayer.append(node)
        if len(nodes) > 0:
            result.append({"id": level, "nodes": nodes})
            self.getTrueGraphRecursive(
                level + 1, alradyScoutedNodes, nodesForNextLayer, result)

    def getCleanGraph(self):
        result = [{"id": 0, "nodes": [{"id": 0, "description" : self.nodes[0].getDescription()}]}]
        self.getCleanGraphRecorsive(1, [0], [0], result)
        return result

    def getCleanGraphRecorsive(self, level, alradyScoutedNodes, nodesFromPreviousLayer, result):
        nodes = []
        nodesForNextLayer = []
        for previousNode in nodesFromPreviousLayer:
            for operation, node in self.adjecency_graph[previousNode]:
                if node not in alradyScoutedNodes:
                    nodes.append({"id": node, "description" : self.nodes[node].getDescription()})
                    alradyScoutedNodes.append(node)
                    nodesForNextLayer.append(node)
        if len(nodes) > 0:
            result.append({"id": level, "nodes": nodes})
            self.getCleanGraphRecorsive(
                level + 1, alradyScoutedNodes, nodesForNextLayer, result)

    def getCleanGraphTrie(self, for_snapshot):
        nodes = {"0": [{"id": 0, "description" : self.nodes[0].getDescription()}]}
        edges = []
        node_history = {0: []}
        self.getCleanGraphRecursiveTrie(
            0, edges, nodes, node_history, self.trie.child, for_snapshot)
        return nodes, edges, node_history

    def getCleanGraphRecursiveTrie(self, level, edges, nodes, node_history, current, for_snapshot):
        next = []
        for key in current.keys():
            if type(key) != str:
                print(current[key])
                next.append(current[key])
                if level+1 not in nodes:
                    nodes[level+1] = []
                nodes[level+1].append({"id": current[key]["#"], "description" : self.nodes[self.cleanNodeFromTrieNode(current[key]["#"])].getDescription()})
                history = node_history[current["#"]].copy()
                if (for_snapshot):
                    history.append(key)
                else:
                    history.append(key.getDict())

                node_history[current[key]["#"]] = history
                edges.append(
                    {"parentNode": current["#"], "childrenNode": current[key]["#"], "operation": key.getName()})

        for n in next:
            self.getCleanGraphRecursiveTrie(
                level+1, edges, nodes, node_history, n, for_snapshot)

    def cleanNodeFromTrieNode(self, trieNodeId):

        for key in self.clean_graph_2_trie_graph.keys():

            if trieNodeId in self.clean_graph_2_trie_graph[key]:
                return key
    
    def trueNodeFromTrieNode(self, trueNodeId):

        for key in self.true_graph_2_trie_graph.keys():

            if trueNodeId in self.true_graph_2_trie_graph[key]:
                return key
