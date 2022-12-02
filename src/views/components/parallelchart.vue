<template>
    <div id="col1">
        <div id="parallel"></div>
    </div>
    <div id="col2">
        <div id="bar"><h1>bar</h1></div>
        <div id="scatter"><h1>scatter</h1></div> 
    </div>
</template>

<script>
import * as d3 from "d3";
import rawdata from "../../assets/data/filtered_data.json"
export default {
    name: 'ParallelChart',
    data() {
        return {
            process_data: undefined,
            selected_data: [],
            keys: ["price", "metacritic_score", "achievements", "recommendations", "average_playtime_forever"],
            genres: ["Indie", "Action", "Casual", "Adventure","Simulation", 
                    "Strategy", "RPG", "Early Access", "Free to Play", "Sports"],
        }
    },
    props: {
        myParallelChartData: Array,
    },
    mounted() {
        this.processData(rawdata)
        this.drawParallelChart(this.process_data, '#parallel', "#bar")
    },
    methods: {
        processData(data) {
            console.log("parallel chart process data")
            let count = 0
            //console.log(data)
            const preData = []
            for (const prop in data) {
                //console.log(data[prop])
                count  = count + 1
                preData.push(data[prop])
            }
            console.log("total games: ", count)
            console.log(preData)
            this.process_data = preData
        },
        drawParallelChart(data, parallel_id, bar_id) {
            const margin = { top: 30, right: 10, bottom: 30, left: 10 };
            const height = this.keys.length * 120;
            const width = 800;
            const brushHeight = 50;

            const svg = d3.select(parallel_id).append("svg")
                            .attr("width", width + margin.left + margin.right)
                            .attr("height", height + margin.top + margin.bottom)
                            .append("g")
                            .attr("transform", `translate(${margin.left}, ${margin.top})`);

            const selections = new Map();
            
            function brushed({selection}, key) {
                if (selection === null) selections.delete(key);
                else selections.set(key, selection.map(x.get(key).invert));
                const selected = [];
                path.each(function(d) {
                  const active = Array.from(selections).every(([key, [min, max]]) => d[key] >= min && d[key] <= max);
                  d3.select(this).style("stroke", active ? colors(d.genres) : "#ddd");
                  if (active) {
                    d3.select(this).raise();
                    selected.push(d);
                  }
                });
                console.log(selected)
                this.selected_data = selected;
                svg.property("value", selected).dispatch("input");
            }

            const colors = d3.scaleOrdinal().domain(this.genres).range(d3.schemeSet3);

            const brush = d3.brushX()
                            .extent([
                            [margin.left, -(brushHeight / 2)],
                            [width - margin.right, brushHeight / 2]
                            ])
                            .on("start brush end", brushed);

            const x = new Map(Array.from(this.keys, key => [key, d3.scaleLinear(d3.extent(data, d => d[key]), [margin.left, width - margin.right])]))
            const y = d3.scalePoint(this.keys, [margin.top, height - margin.bottom])
            
            const line = d3.line().defined(([, value]) => value != null)
                            .x(([key, value]) => x.get(key)(value))
                            .y(([key]) => y(key))

            // line
            const path = svg.append("g")
                .attr("fill", "none")
                .attr("stroke-width", 1.5)
                .attr("stroke-opacity", 0.4)
                .selectAll("path")
                .data(data)
                .join("path")
                .attr("stroke", function(d) { return (colors(d.genres)); })
                .attr("d", d => line(d3.cross(this.keys, [d], (key, d) => [key, d[key]])))

            // axis
            svg.append("g")
                .selectAll("g")
                .data(this.keys)
                .join("g")
                .attr("transform", d => `translate(0, ${y(d)})`)
                .each(function(d) { d3.select(this).call(d3.axisBottom(x.get(d))); })
                .call(g => g.append("text")
                    .attr("x", margin.left)
                    .attr("y", -6)
                    .attr("text-anchor", "start")
                    .attr("fill", "currentColor")
                    .text(d => d))
                .call(g => g.selectAll("text")
                    .clone(true).lower()
                    .attr("fill", "none")
                    .attr("stroke-width", 5)
                    .attr("stroke-linejoin", "round")
                    .attr("stroke", "white"))
                .call(brush)
        },
    }
}
</script>

<style>
#col1 {
    height: 100%;
    width: 50%;
    position: relative;
}

#parallel {
    height: 100%;
    width: 100%;
    position: relative;
}

#col2 {
    height: 100%;
    width: 30%;
    position: relative;
}

#bar, #scatter {
    height: 50%;
    width: 50%;
    position: relative;
}
</style>