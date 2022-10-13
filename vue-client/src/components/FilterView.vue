<template>
  <div>
    <div class="filterpanel">
      <h3>Working on: <br> EventLog {{ (labelnodedict[filter.id] !== undefined)? labelnodedict[filter.id] : filter.id }}
      </h3>
      <input type="text" v-model="filter.activityName" placeholder="Parameters" />
      <br> 
      <table class="filter-table">
      <tbody>
      <tr v-for="filtername in filternames"  v-bind:key="'filter-' + filtername">
        <td><button  @click="submitFilter(filtername)"> {{filtername}} </button><br>
          <label>Parameter Format:</label><br> <label>{{parameters[filtername] }}</label></td>
      </tr>
      </tbody>
    </table>

    </div>
    <div class="page">
      <table class="styled-table">
        <thead>
          <tr>
            <th v-for="(header, key) in eventLog.headers" v-bind:key="'header-' + key">
              {{ header }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowKey) in eventLog.traces" v-bind:key="'row-' + rowKey">
            <td v-for="(column, columnKey) in eventLog.traces[rowKey]"
              v-bind:key="'row-' + rowKey + '-column-' + columnKey">
              {{ eventLog.traces[rowKey][columnKey] }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- <div class="loader" v-else>
      <svg class="circular-loader" viewBox="25 25 50 50">
        <circle class="loader-path" cx="50" cy="50" r="20" fill="none" stroke="#70c542" stroke-width="2" />
      </svg>
    </div> -->
  </div>
</template>

<script>
export default {
  name: 'App',
  props: ['selected', 'labelnodedict'],
  components: {

  },
  data() {
    return {
      filternames: ["filterOut", "flowSelection", "throughPut", "removeBehavior"],
      parameters: {filterOut: "Activity or Activities ; = and", 
                   flowSelection: "Event_1 -> Event_2 ; = ->", 
                   throughPut: "Event_1; Event_2; time_in_seconds; 'longer' or 'shorter'", 
                   removeBehavior: "Percentage 80% = 0.8", 
                  },
      filter: {
        filterName: "",
        activityName: "",
        previousOperations: [],
        id: this.selected,


      },
      eventLog: {},
      array: [],
      isEventLogReady: false,
    }
  },
  methods: {
    submitFilter(filterName) {
      this.filter.filterName = filterName
      try {

        this.axios.post(this.$backend.filter(), this.filter)
          .then(() => {
            this.filter.activityName = "";
            this.filter.filterName = "";
            this.isEventLogReady = false;
            this.getEventLog();
            console.log("FILTER SUCCEEDED");
          })
      }
      catch (e) {
        console.log(e);
      }
    },
    getEventLog() {
      try {
        this.axios.get(this.$backend.getEventLog())
          .then((json) => {
            this.eventLog = json.data.eventLog;
            this.$emit('changeSelected', json.data.logId)
            this.filter.id = json.data.logId
            this.isEventLogReady = true;
            this.filter.previousOperations = json.data.history
            console.log("GET EVENTLOG SUCCESS");
          })
      }
      catch (e) {
        console.log(e);
      }
    },
  },
  mounted() {
    this.getEventLog();
    this.isEventLogReady = false
  }
}
</script>

<style>
.filterpanel {
  width: 20%;
  flex-direction: column;
  display: flex;
  background-color: aquamarine;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  padding: 8px;

  color: rgb(10, 48, 0);

}

.page {
  width: 90%;
  display: flex;

}

.profile-main-loader .loader {
  position: relative;
  margin: 0px auto;
  width: 200px;
  height: 200px;
}

.profile-main-loader .loader:before {
  content: '';
  display: block;
  padding-top: 100%;
}

.circular-loader {
  -webkit-animation: rotate 2s linear infinite;
  animation: rotate 2s linear infinite;
  height: 100%;
  -webkit-transform-origin: center center;
  -ms-transform-origin: center center;
  transform-origin: center center;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
  margin: auto;
}

.loader-path {
  stroke-dasharray: 150, 200;
  stroke-dashoffset: -10;
  -webkit-animation: dash 1.5s ease-in-out infinite, color 6s ease-in-out infinite;
  animation: dash 1.5s ease-in-out infinite, color 6s ease-in-out infinite;
  stroke-linecap: round;
}

.filter-table {
  border-collapse: collapse;
  font-size: 0.9em;
  font-family: sans-serif;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}

.filter-table thead tr {
  background-color: #009879;
  color: #ffffff;
  text-align: left;
}

.filter-table tbody tr {
  border-bottom: 1px solid #dddddd;
}

.filter-table tbody tr:nth-of-type(even) {
  background-color: #f3f3f3;
}

.styled-table {
  border-collapse: collapse;
  font-size: 0.9em;
  font-family: sans-serif;
  min-width: 400px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}

.styled-table thead tr {
  background-color: #009879;
  color: #ffffff;
  text-align: left;
}

.styled-table th,
.styled-table td {
  padding: 12px 15px;
}

.styled-table tbody tr {
  border-bottom: 1px solid #dddddd;
}

.styled-table tbody tr:nth-of-type(even) {
  background-color: #f3f3f3;
}

.styled-table tbody tr:last-of-type {
  border-bottom: 2px solid #009879;
}

@-webkit-keyframes rotate {
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}

@keyframes rotate {
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}

@-webkit-keyframes dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }

  50% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -35;
  }

  100% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -124;
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }

  50% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -35;
  }

  100% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -124;
  }
}

@-webkit-keyframes color {
  0% {
    stroke: #70c542;
  }

  40% {
    stroke: #70c542;
  }

  66% {
    stroke: #70c542;
  }

  80%,
  90% {
    stroke: #70c542;
  }
}

@keyframes color {
  0% {
    stroke: #70c542;
  }

  40% {
    stroke: #70c542;
  }

  66% {
    stroke: #70c542;
  }

  80%,
  90% {
    stroke: #70c542;
  }
}
</style>