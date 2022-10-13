<template>
    <div class="parent">
        <div class="panel">
            <br>
            <button id=graphView @click="goToGraphView" class="navigationButton graphButton" ></button>
            <br>
            <button id=filterView @click="goToFilterView" class="navigationButton filterButton" ></button>

        </div>
        <router-view :selected="this.selected" @changeSelected="newSelected" :labelnodedict="this.labelnodedict" @changeDict="newLabelDict" :with_true_graph="this.with_true_graph" @changewith_true_graph="newTrueGraph" class="page" />
    </div>
</template>

<script>
import router from '@/router';

export default {
    data() {
        return {
            labelnodedict: {},
            selected: 0,
            with_true_graph: false
        }
    },
    methods: {
        newLabelDict(dict) {
            this.labelnodedict = dict
        },
        newSelected(id) {
            this.selected = id
        },
        newTrueGraph(b) {
            this.with_true_graph = b
        },
        goToGraphView() {
            router.push("/app/graph");
        },
        goToFilterView() {
            router.push("/app/filter");
        }
    },
}
</script>

<style>
.parent {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: row;

}

.panel {
    min-width: 60px;
    background-color: grey;
    flex-direction: column;
    display: flex;
    padding: 10px 10px 10px 10px;
}

.page {

    display: flex;

}
.filterButton {
    background-size: 48px;
    background-image: url(../assets/filter.png);
}
.graphButton {
    background-size: 48px;
    background-image: url(../assets/presentation.png);
}

.navigationButton:hover {
    background-size: 58px;
    
}
.navigationButton {
    background-repeat: no-repeat;
    border-color: transparent;
    background-color: transparent;
    align-self: center center;
    
    width: 60px;
    height: 60px;
    cursor: pointer;

    color: rgb(226, 226, 226);
    



}

</style>