<template>
  <div>
    <div class="newpanel">
      <br>
      <button id=graphView @click="showCleanGraph" class="graphsButtons">Clean <br> Graph</button>
      <br>
      <button id=historyView @click="showHistoryGraph" class="graphsButtons">History <br> Graph</button>
      <br>
      <div v-if="withTrueGraph == 'true'">
      <button id=trueView @click="showTrueGraph" class="graphsButtons" >True <br> Graph</button>
      </div>
    </div>
    <div class="page">

      <div class="popup"
			v-if="showPopup" 
			>
      <h4>Node {{popupid}}</h4>
      <input v-model="nodelabel"/>
			<button @click="labelNode">Submit Label</button>
      <button @click="snapshot">Get Snapshot</button>
		</div>
      <svg width="100%" height="100" id="true-view" v-if="trueGraph && cleanGraph">
      </svg>
      <svg width="100%" height="100" id="clean-graph" v-else-if="cleanGraph">
      </svg>
      <svg width="100%" height="100" id="history-view" v-else>
      </svg>
    </div>
  </div>
</template>

<script>

import router from '@/router';



export default {
  name: 'App',
  props: ['selected','labelnodedict', 'with_true_graph'],

  data() {
 

    return {
      withTrueGraph: this.with_true_graph,
      trueGraph: false,
      mapcleantohistory : {},
      nodelabeldict : this.labelnodedict,
      nodelabel : "0",
      popupid : 0,
      showPopup: false,
      edges: {},
      svgElementsToRemoveClean: [],
      svgElementsToRemoveHistory: [],
      selectedNode: this.selected,
      delay: 500,
      clicks: 0,
      timer: null,
      cleanGraph: true,
      colorList: ["red", "blue", "pink", "yellow", "green", "orange", "purple"],

    }
  },
  methods: {
    labelNode() {

      this.showPopup = false;
      this.nodelabeldict[this.popupid] = this.nodelabel;
      var label = document.getElementById("label"+this.popupid);
      label.textContent = this.nodelabel;
      this.$emit('changeDict', this.nodelabeldict)
    },

    showCleanGraph() {
      this.trueGraph = false
      this.cleanGraph = true
      this.svgElementsToRemoveClean = []
      this.svgElementsToRemoveHistory = []
      this.getGraph('clean-graph',this.$backend.getGraph())
    },
    showHistoryGraph() {
      this.trueGraph = false
      this.cleanGraph = false
      this.svgElementsToRemoveClean = []
      this.svgElementsToRemoveHistory = []
      this.getGraph('history-view',this.$backend.getHistoryGraph())
    },
    showTrueGraph() {
      this.trueGraph = true
      this.cleanGraph = true
      this.svgElementsToRemoveClean = []
      this.svgElementsToRemoveHistory = []
      this.getGraph('true-view',this.$backend.getTrueGraph())
    },
    getGraph(svg_id,fetch_from) {
      this.showPopup = false;
      try {
        this.fetch_from = fetch_from
        this.svg_id = svg_id
        this.axios.get(this.fetch_from)
          .then((json) => {
            console.log(json)
            this.edges = json.data;
            this.invertMap(this.edges.map)
            console.log(this.edges.map)
            console.log(this.edges)
            this.drawGraph()
            console.log("GET GRAPH SUCCEEDED");
          })
      }
      catch (e) {
        console.log(e);
      }
    },
    getWidth() {
      return Math.max(
        document.body.scrollWidth,
        document.documentElement.scrollWidth,
        document.body.offsetWidth,
        document.documentElement.offsetWidth,
        document.documentElement.clientWidth
      );
    },
    drawEdge(node1, operation, node2) {
      var graph = document.getElementById(this.svg_id);
      var edge;
      var label;
      var arrowpoint;
      var xParent;
      var yParent;
      var rectangle
      var label_n
      var rectHeight = 30;
      var rectWidth = 8 * operation.length + 5;
      var cornerRadius = 20
      if (node1 != node2) {   // TODO at some point address selfloops
        var parentNode = document.getElementById(node1);
        var childNode = document.getElementById(node2);
        xParent = parseFloat(parentNode.getAttribute("cx").replace("%", '')) / 100 * this.getWidth() * 0.8;
        yParent = parentNode.getAttribute("cy");
        var xChild = parseFloat(childNode.getAttribute("cx").replace("%", '')) / 100 * this.getWidth() * 0.8;
        var yChild = childNode.getAttribute("cy");
        var hypotenuse = Math.sqrt(
          Math.pow(parseFloat(xChild - xParent), 2) +
          Math.pow(parseFloat(yChild - yParent), 2)
        )
        var xFixParent = 50 / hypotenuse * parseFloat(xChild - xParent);
        var yFixParent = 50 / hypotenuse * parseFloat(yChild - yParent);
        var xFixChild = 50 / hypotenuse * parseFloat(xParent - xChild);
        var yFixChild = 50 / hypotenuse * parseFloat(yParent - yChild);

        xParent = parseFloat(xParent) + parseFloat(xFixParent) + 7;
        yParent = parseFloat(yParent) + parseFloat(yFixParent);
        xChild = parseFloat(xChild) + parseFloat(xFixChild) + 7;
        yChild = parseFloat(yChild) + parseFloat(yFixChild);


        edge = document.createElementNS("http://www.w3.org/2000/svg", "path");
        edge.setAttribute("d", "M " + xParent + " " + yParent + " L" + xChild + " " + yChild);
        edge.setAttribute("stroke", "red");
        edge.setAttribute("stroke-width", "3");

        label_n = 0
        while(document.getElementById("label" + node1 + node2 + label_n) != undefined){
          label_n += 1;
        }

        var x = parseFloat(parseFloat(xParent) + parseFloat(xChild - xParent) / 2)
        var y = parseFloat(parseFloat(yParent) + parseFloat(yChild - yParent) / 2) + (label_n * 20)
        label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("id", "label" + node1 + node2 + label_n);
        label.setAttribute("x", x);
        label.setAttribute("y", y);
        label.setAttribute("text-anchor", "middle");
        label.textContent = operation;

        var rectX = parseFloat(x - (rectWidth / 2))
        var rectY = parseFloat(y - (rectHeight / 2) - 4)
        rectangle = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rectangle.setAttribute("x", rectX);
        rectangle.setAttribute("y", rectY);
        rectangle.setAttribute("rx", cornerRadius);
        rectangle.setAttribute("ry", cornerRadius);
        rectangle.setAttribute("width", rectWidth);
        rectangle.setAttribute("height", rectHeight);
        rectangle.setAttribute("fill", "gray");

        graph.appendChild(edge);
        graph.appendChild(rectangle);
        graph.appendChild(label);


        var newHypotenuse = Math.sqrt(
          Math.pow(parseFloat(xChild - xParent), 2) +
          Math.pow(parseFloat(yChild - yParent), 2)
        )
        var distance = 15;
        var xArrowBase = (distance * Math.sqrt(2) / 2) / newHypotenuse * parseFloat(xParent - xChild);
        var yArrowBase = (distance * Math.sqrt(2) / 2) / newHypotenuse * parseFloat(yParent - yChild);
        xArrowBase = parseFloat(xChild) + parseFloat(xArrowBase);
        yArrowBase = parseFloat(yChild) + parseFloat(yArrowBase);
        var centerBasex = parseFloat(xChild) + parseFloat(distance / 2);
        var centerBasey = parseFloat(yChild) + parseFloat(distance / 2);
        var w = Math.sqrt(Math.pow((centerBasex - xArrowBase), 2) + Math.pow((centerBasey - yArrowBase), 2))
        var cosAngle = 1 - (Math.pow(w, 2) / (2 * Math.pow((distance * Math.sqrt(2) / 2), 2)))
        var sinAngle = Math.sqrt(1 - Math.pow(cosAngle, 2))

        var point2xI = distance
        var point2yI = 0
        var point3xI = 0
        var point3yI = -distance

        var point2x
        var point2y
        var point3x
        var point3y

        if (parseFloat(xParent - xChild) >= 0) {

          point2x = parseFloat(point2xI) * parseFloat(sinAngle) - parseFloat(point2yI) * parseFloat(cosAngle)
          point2y = parseFloat(point2xI) * parseFloat(cosAngle) + parseFloat(point2yI) * parseFloat(sinAngle)

          point3x = parseFloat(point3xI) * parseFloat(sinAngle) - parseFloat(point3yI) * parseFloat(cosAngle)
          point3y = parseFloat(point3xI) * parseFloat(cosAngle) + parseFloat(point3yI) * parseFloat(sinAngle)
        }
        else {

          point2x = parseFloat(point2xI) * parseFloat(cosAngle) + parseFloat(point2yI) * parseFloat(sinAngle)
          point2y = parseFloat(point2xI) * parseFloat(sinAngle) - parseFloat(point2yI) * parseFloat(cosAngle)

          point3x = parseFloat(point3xI) * parseFloat(cosAngle) + parseFloat(point3yI) * parseFloat(sinAngle)
          point3y = parseFloat(point3xI) * parseFloat(sinAngle) - parseFloat(point3yI) * parseFloat(cosAngle)
        }

        point2x = parseFloat(xChild) + parseFloat(point2x)
        point2y = parseFloat(yChild) + parseFloat(point2y)
        point3x = parseFloat(xChild) + parseFloat(point3x)
        point3y = parseFloat(yChild) + parseFloat(point3y)

        arrowpoint = document.createElementNS("http://www.w3.org/2000/svg", "path");
        arrowpoint.setAttribute("d", "M " + xChild + " " + yChild + " L" + point2x + " " + point2y + " L" + point3x + " " + point3y + "Z");
        arrowpoint.setAttribute("stroke", "red");
        arrowpoint.setAttribute("fill", "red");
        arrowpoint.setAttribute("stroke-width", "3");

        graph.appendChild(arrowpoint);


        if (this.cleanGraph) {

          this.svgElementsToRemoveClean.push(edge)
          this.svgElementsToRemoveClean.push(label)
          this.svgElementsToRemoveClean.push(arrowpoint)
          this.svgElementsToRemoveClean.push(rectangle);
        }
        else {
          this.svgElementsToRemoveHistory.push(edge)
          this.svgElementsToRemoveHistory.push(label)
          this.svgElementsToRemoveHistory.push(arrowpoint)
          this.svgElementsToRemoveHistory.push(rectangle);
        }
      }
      else {
        var node = document.getElementById(node1);
        xParent = parseFloat(node.getAttribute("cx").replace("%", '')) / 100 * this.getWidth() * 0.8;
        yParent = node.getAttribute("cy");
        edge = document.createElementNS("http://www.w3.org/2000/svg", "path");
        var x1 = xParent + 7
        var x2 = xParent + 100 + 7
        var x3 = xParent + 50 + 7
        var y1 = yParent - 50
        var y2 = yParent - 100
        var y3 = yParent
        edge.setAttribute("d", "M " + x1 + " " + y1 + " Q" + x2 + " " + y2 + " " + x3 + " " + y3);
        edge.setAttribute("fill", "none");
        edge.setAttribute("stroke", "red");
        edge.setAttribute("stroke-width", "3");
        
        label_n = 0
        while(document.getElementById("label" + node + node + label_n) != undefined){
          label_n += 1;
        }

        var xlabel = xParent + 110 + 7
        var ylabel = yParent - 50 + (label_n * 20)
        label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("id", "label" + node + node + label_n);
        label.setAttribute("x", xlabel);
        label.setAttribute("y", ylabel);
        label.setAttribute("text-anchor", "middle");
        label.textContent = operation;



        var rectXself = parseFloat(xlabel - (rectWidth / 2))
        var rectYself = parseFloat(ylabel - (rectHeight / 2) - 4)
        rectangle = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rectangle.setAttribute("x", rectXself);
        rectangle.setAttribute("y", rectYself);
        rectangle.setAttribute("rx", cornerRadius);
        rectangle.setAttribute("ry", cornerRadius);
        rectangle.setAttribute("width", rectWidth);
        rectangle.setAttribute("height", rectHeight);
        rectangle.setAttribute("fill", "gray");
        if (label_n == 0){

          graph.appendChild(edge);
        }
        graph.appendChild(rectangle);
        graph.appendChild(label);


        if (this.cleanGraph) {

          this.svgElementsToRemoveClean.push(edge)
          this.svgElementsToRemoveClean.push(label)
          this.svgElementsToRemoveClean.push(arrowpoint)
          this.svgElementsToRemoveClean.push(rectangle)

        }
        else {
          this.svgElementsToRemoveHistory.push(edge)
          this.svgElementsToRemoveHistory.push(label)
          this.svgElementsToRemoveHistory.push(arrowpoint)
          this.svgElementsToRemoveHistory.push(rectangle)

        }

      }
    },
    postChangeOfLog(id) {

      try {
        this.axios.post(this.$backend.changeSelectedNode(), { "id": id })
          .then(() => {
            console.log("CHANGED SELECTED ID IN BACKEND");
          })
      }
      catch (e) {
        console.log(e);
      }

    },
    snapshot() {
      this.showPopup = false;
      this.axios.post(this.$backend.snapshot(), { "id": this.popupid })
        .then(() => {
          console.log("Snapshot SUCCEEDED");
          this.axios.get(this.$backend.downloadsnapshot(), { responseType: 'blob' })
            .then(response => {
              const blob = new Blob([response.data], { type: 'application/python' })
              const link = document.createElement('a')
              link.href = URL.createObjectURL(blob)
              link.download = "snapshot.py"
              link.click()
              URL.revokeObjectURL(link.href)
            }).catch(console.error)
          this.axios.get(this.$backend.downloadrawLog(), { responseType: 'blob' })
            .then(response => {
              const blob = new Blob([response.data], { type: 'application/python' })
              const link = document.createElement('a')
              link.href = URL.createObjectURL(blob)
              link.download = "rawLog.py"
              link.click()
              URL.revokeObjectURL(link.href)
            }).catch(console.error)

        })
    },
    changeLog(id) {
      this.clicks++;
      var oldSelectedNode = document.getElementById(this.selectedNode);
      oldSelectedNode.setAttribute("stroke", "black")
      oldSelectedNode.setAttribute("stroke-width", 1)

      this.selectedNode = id
      var newSelectedNode = document.getElementById(this.selectedNode);
      newSelectedNode.setAttribute("stroke", "yellow")
      newSelectedNode.setAttribute("stroke-width", 10)

      this.$emit('changeSelected', id)
      this.postChangeOfLog(id)
      if (this.clicks === 1) {
        this.timer = setTimeout(() => {
          this.clicks = 0;
        }, this.delay);
      } else {
        clearTimeout(this.timer);
        router.push("/app/filter");
        this.clicks = 0;
      }
    },
    toFilterView(id) {
      console.log(id)
    },
    invertMap(map){
      var inverse = {};
      for (const [key, value] of Object.entries(map)){
        inverse[value] !== undefined ? inverse[value].push(key) : inverse[value] = [key]
      }
      this.mapcleantohistory = inverse
    },
    createCleanLabel(id){
      console.log(this.mapcleantohistory)
      var ids = this.mapcleantohistory[id]
      var label = ""
      for (const i in ids){
        var value = ids[i]
        if (this.nodelabeldict[value] !== undefined){
          label += '\n' + this.nodelabeldict[value]
        }else {

          label += '\n' +value
        }
      }
      return label
    },

    drawNode(x, y, node) {
      console.log(this.svg_id)
      var graph = document.getElementById(this.svg_id);
      console.log(graph)
      var circle;
      var label

      var id = node.id
      var description

      circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", x + "%");
      circle.setAttribute("cy", y + "");
      circle.setAttribute("r", 50);

      circle.setAttribute("fill", this.cleanGraph ? this.colorList[id] : this.colorList[this.edges.map[id]]);
      circle.setAttribute("stroke", this.cleanGraph ? (this.edges.map[this.selectedNode] == id ? 'yellow' : 'black') : (this.selectedNode == id ? 'yellow' : 'black'));
      circle.setAttribute("stroke-width", this.cleanGraph ? (this.edges.map[this.selectedNode] == id ? 10 : 1) : (this.selectedNode == id ? 10 : 1));
      circle.setAttribute("id", id);
      
      label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.setAttribute("id", "label"+id);
      label.setAttribute("x", x + "%");
      label.setAttribute("y", y + "");
      label.setAttribute("text-anchor", "middle");
      if (this.cleanGraph){
        this.multipleLines(this.createCleanLabel(id),15,label,x,y - parseInt(8 * (this.createCleanLabel(id).match(/\n/g) || []).length))

      }else{
        label.textContent = (this.nodelabeldict[id] !== undefined)? this.nodelabeldict[id]  : id  
      }
      if (!this.cleanGraph) {
        circle.addEventListener('contextmenu', (e) => { e.preventDefault(); this.nodelabel = label.textContent; this.popupid = id; this.showPopup = true; }, false);
        circle.addEventListener("click", this.changeLog.bind(null, id), false);
      }
      

      
      description = document.createElementNS("http://www.w3.org/2000/svg", "text");
      description.setAttribute("x", x + "%");
      description.setAttribute("y", y + "");
      description.setAttribute("id", "description"+id);
      this.multipleLines(node.description, 15, description, x + 4, y + 30)
     
      graph.appendChild(circle);
      graph.appendChild(label);
      graph.appendChild(description);


    },

    multipleLines(str, lineHeight, description,x=80,y=30) {
      for (var line in str.split('\n')){
        var tspan = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
        tspan.setAttribute("x", x + "%");
        tspan.setAttribute("y", parseFloat(y  + line * lineHeight));
        tspan.textContent = str.split('\n')[line] 
        description.appendChild(tspan);
      }
    },

    drawGraph() {
      var layerHeight = 100
      var betweenLayersHeight = 70
      // draw Nodes
      for (var level in this.edges.levels) {
        var nNodesInRow = this.edges.levels[level].nodes.length
        for (var node in this.edges.levels[level].nodes) {
          this.drawNode(100 / (nNodesInRow + 1) * (parseFloat(node) + 1), (layerHeight + betweenLayersHeight) * (parseFloat(level) + 1), this.edges.levels[level].nodes[node]);
        }
      }
      var nLevels = this.edges.levels.length
      document.getElementById(this.svg_id).setAttribute("height", layerHeight + ((layerHeight + betweenLayersHeight) * nLevels));

      // draw Edges
      this.drawEdges()
    },
    drawEdges() {
      this.removeOldEdges()
      for (var edge in this.edges.edges) {
        this.drawEdge(this.edges.edges[edge].parentNode, this.edges.edges[edge].operation, this.edges.edges[edge].childrenNode)
      }
    },
    removeOldEdges() {
      for (var element in this.cleanGraph ? this.svgElementsToRemoveClean : this.svgElementsToRemoveHistory) {
        console.log(this.cleanGraph ? this.svgElementsToRemoveClean[element] : this.svgElementsToRemoveHistory[element])
        document.getElementById(this.svg_id).removeChild(this.cleanGraph ? this.svgElementsToRemoveClean[element] : this.svgElementsToRemoveHistory[element]);
      }
      if (this.cleanGraph) {

        this.svgElementsToRemoveClean = [];
      }
      else {
        this.svgElementsToRemoveHistory = [];
      }


    }
    
    
  },
  mounted() {
    this.getGraph('clean-graph',this.$backend.getGraph());
    window.addEventListener('resize', this.drawEdges)
  },
  created() {
    console.log('Params: ', this.$route.params);
    if (this.$route.params.truedatagraph != undefined){

      this.withTrueGraph = this.$route.params.truedatagraph
      this.$emit('changewith_true_graph', this.withTrueGraph)
    }
  }
  

}
</script>

<style>
.newpanel {
  min-width: 80px;
  background-color: rgb(103, 146, 93);
  display: flex;
  flex-direction: column;

}

.page {
  width: 90%;
  display: flex;

}

.graphsButtons {
  margin-right: 20px;
  margin-top: 13px;
  align-self: center center;
  margin-left: 20px;
  width: 50px;
  height: 50px;
  cursor: pointer;
  text-align: center;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  font-size: 11px;
  font-weight: 300;
  color: rgb(0, 0, 0);
  border-radius: 5px;
  border-color: rgb(226, 226, 226);
  background-size: 88px;
  border-style: solid;
}

.graphsButtons:hover {
  font-size: 13px;
  font-weight: 400;

}
.popup {
  
  border: 2px solid black;
  
  
  position: absolute;

  height: 80;
  width: 120;
  display: flex;
  flex-direction: column;
  margin-left: 10px;
  margin-top: 10px;
}
</style>