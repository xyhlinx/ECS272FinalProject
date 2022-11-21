<template>
    <div id="home">
        <div id="col1">
            <div id="bar_view">
                <h1>Welcome Home</h1>
                <BarChart v-if="dataExists" :myBarchartData="myBarData" />
            </div>
        </div>
        <div id="col2"></div>
    </div>
    
</template>

<script>
import BarChart from "../components/barchart.vue"
import * as d3 from "d3";
import csvPath from '../../assets/data/SF_Historical_Ballot_Measures.csv';

export default {
    data(){
        return {
            dataExists: false,
            myBarData: [],
        }
    },
    components: {
        BarChart
    },
    created(){
        /* Fetch via CSV */
        this.drawBarFromCsv()
    },
    mounted(){},
    methods: {
        drawBarFromCsv(){
            //async method
            d3.csv(csvPath).then((data) => {
                // array of objects
                console.log(data.length);
                console.log(data);
                this.dataExists = true; // updates the v-if to conditionally show the barchart only if our data is here.
                this.myBarData = data; // updates the prop value to be the recieved data, which we hand in to our bar-chart

            });
        }
    }
}

</script>

<style>
#home {
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