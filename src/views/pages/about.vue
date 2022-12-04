<template>
    <div id="about">
        <ParallelChart v-if="dataExists" />
    </div>
    
</template>

<script>
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
}

</style>
