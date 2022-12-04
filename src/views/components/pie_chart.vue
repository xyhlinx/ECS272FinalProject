<template>
    <div id="pie-col1">
        <div id="pie">Distrubution of <Dropdown @home_selection="handleChange" /></div>
        <div id="pielegend"></div>
    </div>
    <div id="pie-col2">
        <div>playtime of the game</div>
        <div id="beeswarm"></div>
    </div>
</template>

<script>
import { formatTimeStr } from "ant-design-vue/lib/statistic/utils";
import * as d3 from "d3";
import Dropdown from "./dropdown2.vue"
import { object } from "vue-types";
import rawdata from "../../assets/data/filtered.json"
export default {
    name: 'PieChart',
    data() {
        return {
            process_data: undefined,
            dataExists: false,
            dropdown_selected: {id: 0, text: 'genres'},
            keys: ["genres"],
            color_binding: undefined,
        }
    },
    props: {
        myPieChartData: Array,
    },
    components: {
        Dropdown
    },
    mounted() {
        this.processData(rawdata, this.dropdown_selected.text)
        this.drawPieChart(this.process_data, '#pie', '#pielegend')
        this.drawBeeswarmChart(rawdata, '#beeswarm')
    },
    methods: {
        handleChange(selected) {
            console.log("change" + selected.id + selected.text);
            this.dropdown_selected = selected
            this.processData(rawdata, this.dropdown_selected.text)
            this.drawPieChart(this.process_data, '#pie', '#pielegend')
            this.drawBeeswarmChart(rawdata, '#beeswarm')
        },
        processData(data, prop) {
            console.log(data)
            if (prop == 'genres' || prop == 'estimated_owners' || prop == 'price_tag'){
                const preData = []
                const c = new Map()
                for (const gid in data){
                    var row_prop = data[gid][prop]
                    if (c.has(row_prop)) {
                        c.set(row_prop, c.get(row_prop) + 1)
                    } 
                    else {
                        c.set(row_prop, 1)
                    }
                }
                const cc = new Map([...c.entries()].sort((a, b) => b[1] - a[1]))
                var counter = 0
                var color = []
                for(const entry of cc.entries()) {
                    console.log(entry)
                    const tmp = new Map()
                    tmp.set('key', entry[0])
                    tmp.set('value', entry[1])
                    color.push(entry[0])
                    preData.push(Object.fromEntries(tmp))
                    if (preData.length >= 10) {
                        break
                    }
                }
                this.process_data = preData
                this.color_binding = color
            }
        },
        drawPieChart(data, id, legendid) {
            console.log(5566, id, legendid, data)
            const margin = { top: 150, right: 10, bottom: 30, left: 10 };
            const height = 320;
            const width = 320;
            const dss = this.dropdown_selected.text

            d3.selectAll('.pietooltipsvg').remove()
            d3.selectAll('.pielegend').remove()
            d3.selectAll('.piesvg').remove()

            const svg = d3.select(id).append("svg")
                .attr('class', 'piesvg')
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", `translate(${width / 2}, ${height / 2 + margin.top})`);

            const radius = Math.min(width, height) / 2 - 10

            const pie = d3.pie()
                .value(d => d.value)

            const arcGenerator = d3.arc()
                .innerRadius(0)
                .outerRadius(radius)

            const data_ready = pie(data)

            var colors = d3.scaleOrdinal()
                .domain(this.color_binding)
                .range(d3.schemeCategory10)

            const paths = svg.selectAll('path')
                .data(data_ready)
                .join('path')
                .transition()
                .duration(1000)
                .attr('class', 'path')
                .attr('d', arcGenerator)
                .attr('fill', d => colors(d.data.key))
                .attr('stroke', 'white')
                .attr('stroke-width', 1)
                .attr('opacity', 1)
                
            const tooltip = d3.select(id).append("div")
                .style("position", "absolute")
                .style("opacity", 0)
                .attr("class", "pietooltip")
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
                    .html(`${dss}: ${d.data.key}<br>
                           Count: ${d.data.value}`)
                    .style("left", (event.x)/8 + "px") // It is important to put the +90: other wise the tooltip is exactly where the point is an it creates a weird effect
                    .style("top", (event.y)/8 + "px")
            }
            const mouseleave = function(event,d) {
                tooltip
                  .transition()
                  .duration(200)
                  .style("opacity", 0)
            }
            
            svg.selectAll('path')
                .on('click', (e, d) => {
                    console.log(e, d)
                    var res = []
                    for (const [_id, v] of Object.entries(rawdata)){
                        if (d.data.key == v[dss]){
                            res.push(v)
                        }
                    }
                    this.single_genre_bs(res, '#beeswarm')
                })
                .on("mouseover", mouseover )
                .on("mousemove", mousemove )
                .on("mouseleave", mouseleave )


            const legend_svg = d3.select(legendid)
                .append('svg')
                .attr('class', 'pietooltipsvg')
                .attr('width', width)
                .attr('height', height)
            
            const legend = legend_svg.selectAll('legend')
                .data(data_ready)
                .enter()
                .append('g')
                .attr('class', 'pielegend')
                .attr('transform', (d, i) => `translate(${Math.floor(i / 5) * 120 + 60}, ${i % 5 * 15})`)
            
            legend.append('rect')
                .attr('x', 0)
                .attr('y', 2)
                .attr('width', 8)
                .attr('height', 8)
                .attr('fill', d => colors(d.data.key))

            legend.append('text')
                .attr('x', 10)
                .attr('y', 4)
                .attr('dy', '.5em')
                // .style('text-anchor', 'end')
                .style('font-size', 12)
                .text(d => d.data.key)

        },
        drawBeeswarmChart(data, id){

            // console.log(9999999, data)
            
            d3.selectAll(".beeswarmsvg").remove()
            d3.selectAll(".beeswarmtooltipsvg").remove()

            var res = []
            for (const [_id, v] of Object.entries(data)) {
                // console.log(234, _id, v)
                if (this.dropdown_selected.text in v && this.color_binding.includes(v[this.dropdown_selected.text])){
                    res.push(v)
                }
            }
            data = res

            const margin = { top: 0, right: 20, bottom: 40, left: 20 };
            const height = 650;
            const width = 1000;
            const dss = this.dropdown_selected.text

            var colors = d3.scaleOrdinal()
                .domain(this.color_binding)
                .range(d3.schemeCategory10)

            const x = d3.scaleLinear()
                // .domain(new Set(data.map(d => d.genres)))
                .domain([-1000, d3.max(data.map(d => d.average_playtime_forever))]).nice()
                .range([margin.left, width - margin.right]);

            const y = d3.scaleBand()
                // .domain(d3.extent(data.map(d => d.average_playtime_forever)))
                .domain(this.color_binding)
                .range([height - margin.bottom, margin.top]);

            const xAxis = g => g
                .attr("transform", `translate(0,${height - margin.bottom})`)
                .call(d3.axisBottom(x))

            const yAxis = g => g
                .attr("transform", `translate(${margin.left},0)`)
                .call(d3.axisLeft(y))

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
                console.log(d)
                tooltip
                    .html(`Name: ${d.name}<br>
                           avg playtime: ${d.average_playtime_forever}`)
                    .style("left", (event.x)/4 + "px") // It is important to put the +90: other wise the tooltip is exactly where the point is an it creates a weird effect
                    .style("top", (event.y)/4 + "px")
            }
            const mouseleave = function(event,d) {
                tooltip
                  .transition()
                  .duration(200)
                  .style("opacity", 0)
            }

            const svg = d3.select(id)
                .append("svg")
                .attr('class', 'beeswarmsvg')
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", `translate(${margin.left}, ${margin.right})`);
                
            function size(d) {
                return 1.7
            }
            
            let simulation = d3.forceSimulation(data)                
                .force("x", d3.forceX((d) => {
                    return x(d.average_playtime_forever)
                    })
                    .strength(0.2))
                .force("y", d3.forceY((d) => {
                    return y(d[dss])
                    })
                    .strength(1))
                .force("collide", d3.forceCollide((d) => {
                    return size(d);
                    }))          
                .alphaDecay(0)
                .alpha(0.3)
                .on("tick", tick);

            console.log(444333, this.dropdown_selected, this.color_binding)
            const circles = svg.selectAll("circle")
                .data(data)
                .enter()
                .append("circle")
                .attr('stroke', 'black')
                .attr("class", function(d) { return "dot" + d.genres })
                .attr("cx", function(d) { return x(d.average_playtime_forever) })
                .attr("cy", function(d) { return y(d[dss])})
                .attr("r", d => size(d))
                .attr("fill", function(d) { return colors(d[dss])})
                .on("mouseover", mouseover )
                .on("mousemove", mousemove )
                .on("mouseleave", mouseleave )
            
            function tick() {
                d3.selectAll("circle")
                    .attr("cx", (d) => d.x)
                    .attr("cy", (d) => d.y);
                }

            const gx = svg.append("g")
                .attr("class", "x-axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis)
                .call(g => g.select('.tick:last-of-type text')
                    .clone()
                    .attr("transform", "rotate(-65)")
                    .style("text-anchor", "end")
                    .selectAll("text")
                    .attr("dx", "-.8em")
                    .attr("dy", ".15em")
                    .attr("font-weight", "bold")
                )
                                

            let init_decay = setTimeout(function () {
                // console.log("start alpha decay");
                simulation.alphaDecay(0.1);
                }, 1000);
        },
        single_genre_bs(data, id){
            
            console.log(9999999, data)
            
            d3.selectAll(".beeswarmsvg").remove()
            d3.selectAll(".beeswarmtooltipsvg").remove()

            var res = []
            for (const [_id, v] of Object.entries(data)) {
                // console.log(234, _id, v)
                res.push(v)
            }
            data = res

            const margin = { top: 0, right: 20, bottom: 40, left: 20 };
            const height = 650;
            const width = 1000;
            const dss = this.dropdown_selected.text

            var colors = d3.scaleOrdinal()
                .domain(this.color_binding)
                .range(d3.schemeCategory10)

            const x = d3.scaleLinear()
                // .domain(new Set(data.map(d => d.genres)))
                .domain([-1000, d3.max(data.map(d => d.average_playtime_forever))]).nice()
                .range([margin.left, width - margin.right]);

            const y = d3.scaleBand()
                // .domain(d3.extent(data.map(d => d.average_playtime_forever)))
                .domain(this.color_binding)
                .range([(height - margin.bottom + margin.top) / 2, (height - margin.bottom + margin.top) / 2]);

            const xAxis = g => g
                .attr("transform", `translate(0,${height - margin.bottom})`)
                .call(d3.axisBottom(x))

            const yAxis = g => g
                .attr("transform", `translate(${margin.left},0)`)
                .call(d3.axisLeft(y))

            const svg = d3.select(id)
                .append("svg")
                .attr('class', 'beeswarmsvg')
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", `translate(${margin.left}, ${margin.right})`)

            function size(d) {
                return 4
            }
            
            let simulation = d3.forceSimulation(data)                
                .force("x", d3.forceX((d) => {
                    return x(d.average_playtime_forever)
                    })
                    .strength(0.2))
                .force("y", d3.forceY((d) => {
                    return y(d[dss])
                    })
                    .strength(1))
                .force("collide", d3.forceCollide((d) => {
                    return size(d);
                    }))          
                .alphaDecay(0)
                .alpha(0.3)
                .on("tick", tick);

            const tooltip = d3.select(id).append("div")
                .style("position", "absolute")
                .style("opacity", 0)
                .attr("class", "beeswarmtooltipsvg")
                .style("background-color", "white")
                .style("border", "solid")
                .style("border-width", "1px")
                .style("border-radius", "5px")
                .style("padding", "10px");
            const mouseover = function(event, d) {
                tooltip.style("opacity", 1)
            }
            const mousemove = function(event, d) {
                console.log(d)
                tooltip
                    .html(`Name: ${d.name}<br>
                           avg playtime: ${d.average_playtime_forever}`)
                    .style("left", (event.x)/4 + "px") // It is important to put the +90: other wise the tooltip is exactly where the point is an it creates a weird effect
                    .style("top", (event.y)/4 + "px")
            }
            const mouseleave = function(event,d) {
                tooltip
                  .transition()
                  .duration(200)
                  .style("opacity", 0)
            }

            const circles = svg.selectAll("circle")
                .data(data)
                .enter()
                .append("circle")
                .attr('stroke', 'black')
                .attr("class", function(d) { return "dot" + d.genres })
                .attr("cx", function(d) { return x(d.average_playtime_forever) })
                .attr("cy", function(d) { return y(d[dss])})
                .attr("r", d => size(d))
                .attr("fill", function(d) { return colors(d[dss])})
                .on("mouseover", mouseover )
                .on("mousemove", mousemove )
                .on("mouseleave", mouseleave )

            
            function tick() {
                d3.selectAll("circle")
                    .attr("cx", (d) => d.x)
                    .attr("cy", (d) => d.y);
                }

            const gx = svg.append("g")
                .attr("class", "x-axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis)
                .call(g => g.select('.tick:last-of-type text')
                    .clone()
                    .attr("transform", "rotate(-65)")
                    .style("text-anchor", "end")
                    .selectAll("text")
                    .attr("dx", "-.8em")
                    .attr("dy", ".15em")
                    .attr("font-weight", "bold")
                )
                                
            // const gy = svg.append("g")
            //     .attr("class", "y-axis")
            //     .call(yAxis)
            //     .call(g => g.select(".tick:last-of-type text")
            //     .clone()
            //     .attr("transform", `rotate(-90)`)
            //     .attr("text-anchor", "middle")
            //     .attr("x", -(15 - margin.top - margin.bottom) / 2)
            //     .attr("y", -80)
            //     .attr("font-weight", "bold"))

            let init_decay = setTimeout(function () {
                console.log("start alpha decay");
                simulation.alphaDecay(0.1);
                }, 1000);
        }
    }
}
</script>


<style>
#pie-col1 {
    height: 100%;
    width: 25%;
    position: relative;
}
#pie {
    height: 80%;
    width: 100%;
    position: relative;
}
#pielegend {
    height: 20%;
    width: 100%;
    position: relative;
}
#pie-col2 {
    height: 100%;
    width: 75%;
    position: relative;
}

</style>