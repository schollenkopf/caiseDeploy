import app.event_log as event_log
import app.logs_graph as logs_graph
import app.filter_class as filter_class

class Control():

    def __init__(self):
        self.currentEventLog = event_log.EventLog()  # Maybe this is not needed
        self.graph = None
        #self.filters = self.initFilters()
        self.filtersdict = {"filterOut": filter_class.FilterOut, "flowSelection": filter_class.FlowSelection,
                            "throughPut": filter_class.ThroughPut, "removeBehavior": filter_class.RemoveBehavior}

    def loadRawfile(self, json):
        self.currentEventLog.populateTracesFromCSV(
            json["content"]["data"], json["timestampformat"], json["timestampcolumn"], json["activitycolumn"], json["tracecolumn"])
        self.graph = logs_graph.Graph(self.currentEventLog,json["truedatagraph"])

        self.graph.logdetails = json
        print(self.currentEventLog)

    def parse_parameters(self, parameters_string):
        print(parameters_string)
        p = parameters_string.split(";")
        return p

    def filterFromJson(self, json):  # TODO: this method could probably be written more agile
        return self.filtersdict[json["filterName"]].generateFilter(self.parse_parameters(json["activityName"]))

    # TODO: this method could probably be written more agile
    def filterFromJson_no_parsing(self, json):
        return self.filtersdict[json["filterName"]].generateFilter(json["activityName"])

    # maybe the filter is going to be json format, the idea of the code should still hold
    def applyFilter(self, json):
        print(json)
        # something else  json with id: , filtertype:, parater:,
        # get id of node to be filtered
        id = json["id"]
        # create filter to be applied
        filter = self.filterFromJson(json)

        allOperations = list(
            map(self.filterFromJson_no_parsing, json["previousOperations"]))

        allOperations.append(filter)
        print("Applying FIlter")
        print("ID IN GET NODE FROM ID", id)
        self.graph.addOperation(
            currentTrieNodeId=id,
            operations=allOperations,
            newEventLog=filter.filter(self.graph.getNodefromId(
                id).eventLog.copy())
        )
    def getEdgesAsJsonTrue(self):
        map = self.reverseTrueGraphTrieMap()
        print(str({"levels": self.graph.getTrueGraph(),
              "edges": self.graph.getTrueEdges()}).replace("\'", "\""))
        return str({"levels": self.graph.getTrueGraph(), "edges": self.graph.getTrueEdges(), "map": map}).replace("\'", "\"")

    def getEdgesAsJson(self):
        map = self.reverseGraphTrieMap()
        print(str({"levels": self.graph.getCleanGraph(),
              "edges": self.graph.getEdges()}).replace("\'", "\""))
        return str({"levels": self.graph.getCleanGraph(), "edges": self.graph.getEdges(), "map": map}).replace("\'", "\"")

    def reverseGraphTrieMap(self):
        reverse = {}
        for key in self.graph.clean_graph_2_trie_graph.keys():
            for elemnt in self.graph.clean_graph_2_trie_graph[key]:
                st_elem = str(elemnt)
                reverse[st_elem] = key
        return reverse
    
    def reverseTrueGraphTrieMap(self):
        reverse = {}
        for key in self.graph.true_graph_2_trie_graph.keys():
            for elemnt in self.graph.true_graph_2_trie_graph[key]:
                st_elem = str(elemnt)
                reverse[st_elem] = key
        return reverse

    def getEdgesAsJsonHistory(self):
        nod, ed, hist = self.graph.getCleanGraphTrie(False)
        levels = []
        for key in nod.keys():
            levels.append({"id": int(key), "nodes": nod[key]})
        print(str({"levels": levels,
              "edges": ed}).replace("\'", "\""))
        print(self.graph.clean_graph_2_trie_graph)
        print("historys:", hist)
        map = self.reverseGraphTrieMap()
        print(map)
        return str({"levels": levels, "edges": ed, "map": map}).replace("\'", "\"")

    def getEventLog(self):
        log = self.graph.lastNode
        nod, ed, history = self.graph.getCleanGraphTrie(False)
        print("LASTNODEID", self.graph.lastNode)
        return str({"logId": self.graph.lastNode, "eventLog": self.graph.getEventLogFromId(log), "history": history[self.graph.lastNode]}).replace("\'", "\"")

    def changeLastNode(self, json):
        print(json)
        self.graph.lastNode = json["id"]

    def create_snapshot(self, json):
        fname = 'snapshot.py'
        rawlogname = 'rawLog.py'
        nod, ed, history = self.graph.getCleanGraphTrie(True)

        dependencies = 'app/event_log.py'

        with open(dependencies, 'r') as d:
            dep_str = d.read()
            d.close()

        script = "\n\n\n\n #DEPENDENCIES:  \nfrom rawLog import rawlog\nimport random\n " + dep_str
        script = script + \
            "\n\n\neventLog = EventLog()\nif (path_to_file == \"\"):\n    eventLog.populateTracesFromCSV(\nrawlog, \"{0}\", {1}, {2}, {3})\nelse:\n    eventLog.actuallyPopulateTracesFromCSV(path_to_file, timestring, timeColumn, activityColumn, traceColumn, seperator)".format(
                self.graph.logdetails["timestampformat"], self.graph.logdetails["timestampcolumn"], self.graph.logdetails["activitycolumn"], self.graph.logdetails["tracecolumn"])

        var_string = "#VARIABLES: \nSEED = 10\n"
        for i, filter in enumerate(history[json["id"]]):
            cmt = filter.get_comment()
            fct, vars, vals = filter.get_function(i)
            var_string += "\n\n#Filter " + str(i) + ":"
            for j, var in enumerate(vars):
                var_string += "\n" + var + " = " + str(vals[j])

            script = script + "\n" + cmt + "\n" + fct
        print(script)
        script = var_string + "\n" + "# For using different eventlog (leave path_to_file empty to use original eventlog): \npath_to_file = \"\" \ntimestring = \"\"\ntimeColumn = 0\nactivityColumn = 0\ntraceColumn = 0\nseperator = \",\" \n\n\n" + script + \
            "\neventLog.export(\"final.csv\")"

        rawlog = "rawlog ={}".format(self.graph.logdetails["content"]["data"])
        with open(rawlogname, 'w') as r:
            r.write(rawlog)
            r.close()

        with open(fname, 'w') as f:
            f.write(script)
            f.close()
