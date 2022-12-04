<template>
    <div id="col1">
        <div id="parallel"></div>
        <div id="legend"></div>
    </div>
    <div id="col2">
        <div id="bar_view"><h1>Average playtime by different genres</h1></div>
        <div id="scatter_view"><Dropdown @selectedChange="handleChange" /></div> 
    </div>
</template>

<script>
import * as d3 from "d3";
import Dropdown from "./dropdown.vue"
import rawdata from "../../assets/data/filtered.json"

let selected_data = [];
export default {
    name: 'ParallelChart',
    data() {
        return {
            process_data: undefined,
            dataExists: false,
            dropdown_selected: { id: 0, text: 'price'},
            keys: ["price", "metacritic_score", "achievements", "recommendations", "average_playtime_forever"],
            genres: ["Action", "Adventure", "Strategy", "Indie",  "RPG", 
                    "Simulation", "Casual", "Free to Play", "Sports", "Early Access"],
        }
    },
    components: {
        Dropdown
    },
    props: {
        myParallelChartData: Array,
        mySelection: Object
    },
    mounted() {
        this.processData(rawdata)
        this.drawLegend('#legend')
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
        drawLegend(id) {
            const height = 120;
            const width = 800;
            
            const svg = d3.select(id).append("svg")
                            .attr("width", width)
                            .attr("height", height);

            const colors = d3.scaleOrdinal().domain(this.genres).range(d3.schemeCategory10);

            let dataL = 0;
            let offset = 70;

            const legend = svg.selectAll(".legend")
                                .data(this.genres)
                                .enter()
                                .append("g")
                                .attr("class", "legend")
                                .attr("transform", function(d, i) {
                                    if (i == 0) {
                                        dataL = d.length + offset;
                                        return "translate(0, 0)"
                                    } else {
                                        let newdataL = dataL;
                                        dataL += d.length + offset;
                                        return `translate(${newdataL}, 0)`
                                    }
                                })

            legend.append("rect")
                    .attr("x", 0)
                    .attr("y", 0)
                    .attr("width", 10)
                    .attr("height", 10)
                    .style("fill", function(d) { return (colors(d)); })

            legend.append("text")
                    .attr("x", 10)
                    .attr("y", 10)
                    .text(function(d, i) { return d; })
                    .attr("class", "textselected")
                    .style("text-anchor", "start")
                    .style("font-size", 12)
        },
        drawParallelChart(data, parallel_id, bar_id, scatter_id, cb1, cb2) {
            const margin = { top: 0, right: 10, bottom: 30, left: 10 };
            const height = this.keys.length * 120;
            const width = 700;
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
                selected_data = selected;
                console.log(selected_data)
                cb1(selected_data, bar_id)
                cb2(selected_data, scatter_id)
                svg.property("value", selected).dispatch("input");
            }

            const colors = d3.scaleOrdinal().domain(this.genres).range(d3.schemeCategory10);

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
                //console.log(barData[d])
                const temp = {
                    genres: d,
                    time: barData[d].time/barData[d].count
                }
                finalData.push(temp)
            }

            //console.log(finalData)

            // draw
            const margin = { top: 0, right: 40, bottom: 40, left: 60 };
            const height = 250;
            const width = 400;

            d3.selectAll(".barchart").remove();

            const colors = d3.scaleOrdinal().domain(this.genres).range(d3.schemeCategory10);

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

            svg.append("text")
                .attr("text-anchor", "end")
                .attr("x", width)
                .attr("y", height + margin.top + 40)
                .text("Average playtime(Hour)")

            svg.append("text")
                .attr("text-anchor", "end")
                .attr("transform", "rotate(-90)")
                .attr("y", -margin.left + 10)
                .attr("x", -margin.top)
                .text("Genres")
        },
        drawScatter(data, id) {
            console.log("scatter " + this.dropdown_selected.text)
            console.log(data)

            const selection = this.dropdown_selected.text;

            const margin = { top: 40, right: 40, bottom: 60, left: 60 };
            const height = 250;
            const width = 400;

            d3.selectAll(".scatterplot").remove();
            d3.selectAll(".tooltip").remove();

            const colors = d3.scaleOrdinal().domain(this.genres).range(d3.schemeCategory10);

            const svg = d3.select(id).append("svg")
                            .attr("class", "scatterplot")
                            .attr("width", width + margin.left + margin.right)
                            .attr("height", height + margin.top + margin.bottom)
                            .append("g")
                            .attr("transform", `translate(${margin.left}, ${margin.top})`);

            const x = d3.scaleLinear().domain([0, d3.max(data, d => d.average_playtime_forever)]).range([0, width]);

            svg.append("g")
                .attr("transform", `translate(0, ${height})`)
                .call(d3.axisBottom(x))
                .selectAll("text")
                .attr("transform", "translate(-10, 0)rotate(-45)")
                .style("text-anchor", "end");

            const y = d3.scaleLinear().domain([d3.min(data, d => d[selection]), d3.max(data, d => d[selection])]).range([height, 0]);
            
            svg.append("g")
                .call(d3.axisLeft(y));

            const tooltip = d3.select(id).append("div")
                                .style("position", "absolute")
                                .style("opacity", 0)
                                .attr("class", "tooltip")
                                .style("background-color", "white")
                                .style("border", "solid")
                                .style("border-width", "1px")
                                .style("border-radius", "5px")
                                .style("padding", "10px");

            const mouseover = function(event, d) {
                tooltip.style("opacity", 1)
            }

            const mousemove = function(event, d) {
                tooltip
                    .html(`Name: ${d.name}<br>
                           Genre: ${d.genres}`)
                    .style("left", (event.x)/8 + "px") // It is important to put the +90: other wise the tooltip is exactly where the point is an it creates a weird effect
                    .style("top", (event.y)/8 + "px")
            }

            const mouseleave = function(event,d) {
                tooltip
                  .transition()
                  .duration(200)
                  .style("opacity", 0)
            }

            svg.append("g")
                .selectAll("dot")
                .data(data)
                .enter()
                .append("circle")
                .attr("class", function(d) { return "dot" + d.genres })
                .attr("cx", function(d) { return x(d.average_playtime_forever) })
                .attr("cy", function(d) { return y(d[selection])})
                .attr("r", 5)
                .style("fill", function(d) { return colors(d.genres)})
                .on("mouseover", mouseover )
                .on("mousemove", mousemove )
                .on("mouseleave", mouseleave )

            svg.append("text")
                .attr("text-anchor", "end")
                .attr("x", width)
                .attr("y", height + margin.top + 10)
                .text("Average playtime(Hour)")

            svg.append("text")
                .attr("text-anchor", "end")
                .attr("transform", "rotate(-90)")
                .attr("y", -margin.left + 20)
                .attr("x", -margin.top)
                .text(selection)
        },
        handleChange(selected) {
            console.log("change y axis " + selected.id + selected.text);
            this.dropdown_selected = selected
            this.drawScatter(selected_data, "#scatter_view")
        }
    }
}
</script>

<style>
#col1 {
    height: 100%;
    width: 60%;
    position: relative;
}

#parallel {
    height: 90%;
    width: 100%;
    position: relative;
}

#legend {
    height: 10%;
    width: 100%;
    position: relative;
}

#col2 {
    height: 100%;
    width: 40%;
    position: relative;
}

#bar_view, #scatter_view {
    height: 50%;
    width: 100%;
    position: relative;
}
</style>
