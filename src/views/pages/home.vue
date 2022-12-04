<template>
    <div id="home">
        <PieChart v-if="dataExists" />
    </div>
    
</template>

<script>
import PieChart from '../components/pie_chart.vue'
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
        PieChart
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

</style>
