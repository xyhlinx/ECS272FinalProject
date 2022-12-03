<template>
    <div id="col1">
        <div id="parallel"></div>
    </div>
    <div id="col2">
        <div id="bar_view"><h1>bar</h1></div>
        <div id="scatter_view"><h1>scatter</h1></div> 
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
            dataExists: false,
            selected_data: [],
            keys: ["price", "metacritic_score", "achievements", "recommendations", "average_playtime_forever"],
            genres: ["Indie", "Action", "Casual", "Adventure","Simulation", 
                    "Strategy", "RPG", "Early Access", "Free to Play", "Sports"],
        }
    },
    props: {
        myParallelChartData: Array
    },
    mounted() {
        this.processData(rawdata)
        this.drawParallelChart(this.process_data, '#parallel', '#bar_view', '#scatter_view', this.drawBarChart, this.drawScatter)
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
        drawParallelChart(data, parallel_id, bar_id, scatter_id, cb1, cb2) {
            const margin = { top: 30, right: 10, bottom: 30, left: 10 };
            const height = this.keys.length * 120;
            const width = 800;
            const brushHeight = 50;

            d3.selectAll(".parallelchart").remove();

            const svg = d3.select(parallel_id).append("svg")
                            .attr("class", "parallelchart")
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
                //console.log(selected)
                this.dataExists = true;
                this.selected_data = selected;
                //console.log(this.selected_data)
                cb1(this.selected_data, bar_id)
                cb2(this.selected_data, scatter_id)
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
        drawBarChart(data, id) {
            console.log("bar")
            let barData = {};

            let finalData = []
            
            // process data
            data.forEach(e => {
                //console.log(e.genres)
                if (e.genres in barData) {
                    barData[e.genres].time = barData[e.genres].time + e.average_playtime_forever
                    barData[e.genres].count = barData[e.genres].count + 1
                }
                else {
                    const temp = {
                        time: e.average_playtime_forever,
                        count: 1
                    }
                    barData[e.genres] = temp
                }
            })
            
            //console.log(barData)

            for (const d in barData) {
                console.log(barData[d])
                const temp = {
                    genres: d,
                    time: barData[d].time/barData[d].count
                }
                finalData.push(temp)
            }

            console.log(finalData)

            // draw
            const margin = { top: 40, right: 40, bottom: 120, left: 100 };
            const height = 300;
            const width = 500;

            d3.selectAll(".barchart").remove();

            const colors = d3.scaleOrdinal().domain(this.genres).range(d3.schemeSet3);

            const svg = d3.select(id).append("svg")
                                    .attr("class", "barchart")
                                    .attr("width", width + margin.left + margin.right)
                                    .attr("height", height + margin.top + margin.bottom)
                                    .append("g")
                                    .attr("transform", `translate(${margin.left}, ${margin.top})`);

            const x = d3.scaleLinear().domain([0, d3.max(finalData, d => d.time)]).range([0, width]);
            svg.append("g")
                .attr("transform", `translate(0, ${height})`)
                .call(d3.axisBottom(x))
                .selectAll("text")
                .attr("transform", "translate(-10, 0)rotate(-45)")
                .style("text-anchor", "end");

            const y = d3.scaleBand().range([0, height]).domain(data.map(d => d.genres)).padding(.1);
            svg.append("g")
                .call(d3.axisLeft(y));

            svg.selectAll("myRext")
                .data(finalData)
                .join("rect")
                .attr("x", x(0))
                .attr("y", d => y(d.genres))
                .attr("width", d => x(d.time))
                .attr("height", y.bandwidth())
                .attr("fill", function(d) { return (colors(d.genres)); })
        },
        drawScatter(data, id) {
            console.log("scatter")
        }
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

#bar_view, #scatter_view {
    height: 50%;
    width: 50%;
    position: relative;
}
</style>