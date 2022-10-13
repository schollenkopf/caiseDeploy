export default class Backend{

    constructor(){
        this.url = "http://127.0.0.1:5000"
    }

    getUrlData(){
        return this.url + "/import_raw_data"
    }

    getGraph(){
        return this.url + "/get_graph"
    }
    getTrueGraph(){
        return this.url + "/get_true_graph"
    }
    getHistoryGraph(){
        return this.url + "/get_history_graph"
    }

    filter(){
        return this.url + "/filter"
    }

    getEventLog(){
        return this.url + "/get_event_log"
    }

    changeSelectedNode(){
        return this.url + "/change_selected_node"
    }

    snapshot(){
        return this.url + "/snapshot"
    }
    downloadsnapshot(){
        return this.url + "/downloadsnapshot"
    }
    downloadrawLog(){
        return this.url + "/downloadrawlog"
    }

}