<template>
    <div id="about">
        <div id="col1">
            <div id="bar_view">
                <h1>Welcome About</h1>
                <ParallelChart v-if="dataExists" />
            </div>
        </div>
        <div id="col2">
            <h1>Welcome About2</h1>
        </div>
    </div>
    
</template>

<script>
import BarChart from "../components/barchart.vue"
import ParallelChart from "../components/parallelchart.vue"
import csvPath from "../../assets/data/SF_Historical_Ballot_Measures.csv"
import * as d3 from "d3";

export default {
    data() {
        return {
            dataExists: false,
            myData: []
        }
    },
    components: {
        BarChart,
        ParallelChart
    },
    created() {
        this.drawBarFromCsv()
    },
    mounted() {},
    methods: {
        drawBarFromCsv() {
            d3.csv(csvPath).then((data) => {
                console.log(data.length)
                console.log(data);
                this.dataExists = true;
                this.myData = data
            })
        }
    }
}
</script>

<style>
#about {
    display: flex;
    height: 100%;
    position: relative;
    justify-content: center;
}
#col1 {
    height: 100%;
    width: 50%;
    position: relative;
}
#bar_view {
    height: 100%;
    width: 80%;
    position: relative;
}
#col2 {
    height: 100%;
    width: 50%;
    position: relative;
}

</style>