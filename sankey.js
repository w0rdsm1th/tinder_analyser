/* jshint esversion: 6 */
/*
This file contains the JavaScript implementation of a Bokeh custom extension.
The "sankey.py" contains the python counterpart that submits data.

This custom model wraps the sankey microlibrary of the third-party D3.js library:
https://github.com/d3/d3-sankey
 */


import {HTMLBox, HTMLBoxView} from "models/layouts/html_box"
import {ColumnDataSource} from "models/sources/column_data_source"
import {LayoutItem} from "core/layout"
import * as p from "core/properties"


const OPTIONS = {
//     width: "975px",
//     height: "600px",
};


export class SankeyView extends HTMLBoxView {

    set_data() {
        // transform CDS data into JSON of nodes and links
        // adapted from transformation here http://bl.ocks.org/d3noob/c9b90689c1438f57d649
        // using the dragmove functionality from here https://jarrettmeyer.com/2018/05/31/creating-a-d3-sankey-graph

        const source = this.model.source;
        var graph = {"nodes": [], "links": []};

        for (let i = 0; i < source.get_length(); i++) {
            graph.nodes.push({ "name": source.data["source"][i] });
            graph.nodes.push({ "name": source.data["target"][i] });
            graph.links.push({ "source": source.data["source"][i] ,
                "target": source.data["target"][i],
                "value": source.data["amount"][i]
            });
        }

        // return only th distinct / unique nodes
        graph.nodes = d3.keys(d3.nest()
            .key(function (d) { return d.name; })
            .object(graph.nodes));

        // loop through each link replacing the text with its index from node
        graph.links.forEach(function(d, i) {
            graph.links[i].source = graph.nodes.indexOf(graph.links[i].source);
            graph.links[i].target = graph.nodes.indexOf(graph.links[i].target);
        });

        // now loop through each nodes to make nodes an array of objects rather than array of strings
        graph.nodes.forEach( function (d, i) {
            graph.nodes[i] = { "name": d };
        });
        return graph
    }

    render() {
        super.render();
        //    adapted from https://jsfiddle.net/s3opcnm8

        const width = 500;
        const height = 200;

        let edgeColor = 'path';
        const _sankey = d3.sankey()
            .nodeWidth(15)
            .nodePadding(10)
            .extent([[1, 1], [width - 1, height - 5]])
            .nodeAlign(d3.sankeyLeft);

        const sankey = ({nodes, links}) => _sankey({
            nodes: nodes.map(d => Object.assign({}, d)),
            links: links.map(d => Object.assign({}, d))
        });


        const f = d3.format(",.0f");
        const format = d => `${f(d)} widgets`;

        const _color = d3.scaleOrdinal(d3.schemeCategory10);
        const color = name => _color(name.replace(/ .*/, ""));

        const svg = d3.select('#chart')
            .attr("viewBox", `0 0 ${width} ${height}`)
            .style("width", "100%")
            .style("height", "auto");

        const data = this.set_data();

        const {nodes, links} = sankey(data);

        svg.append("g")
            .attr("stroke", "#000")
            .selectAll("rect")
            .data(nodes)
            .join("rect")
            .attr("x", d => d.x0)
            .attr("y", d => d.y0)
            .attr("height", d => d.y1 - d.y0)
            .attr("width", d => d.x1 - d.x0)
            .attr("fill", d => color(d.name))
            .append("title")
            .text(d => `${d.name}\n${format(d.value)}`);

        // TODO - get node drag working as per below link (uses D3.v4 and different sankey.js)
        // https://bl.ocks.org/d3noob/3337957c360d55c245f6057ab0866c05
        //     .call(d3.drag()
        //     .subject(function(d) { return d; })
        //     .on("start", function() { this.parentNode.appendChild(this); })
        //     .on("drag", dragmove));

        const link = svg.append("g")
            .attr("fill", "none")
            .attr("stroke-opacity", 0.5)
            .selectAll("g")
            .data(links)
            .join("g")
            .style("mix-blend-mode", "multiply");


        function update() {
            if (edgeColor === "path") {
                const gradient = link.append("linearGradient")
                    .attr("id", (d,i) => {
                        //  (d.uid = DOM.uid("link")).id
                        const id = `link-${i}`;
                        d.uid = `url(#${id})`;
                        return id;
                    })
                    .attr("gradientUnits", "userSpaceOnUse")
                    .attr("x1", d => d.source.x1)
                    .attr("x2", d => d.target.x0);

                gradient.append("stop")
                    .attr("offset", "0%")
                    .attr("stop-color", d => color(d.source.name));

                gradient.append("stop")
                    .attr("offset", "100%")
                    .attr("stop-color", d => color(d.target.name));
            }

            link.append("path")
                .attr("d", d3.sankeyLinkHorizontal())
                .attr("stroke", d => edgeColor === "path" ? d.uid
                    : edgeColor === "input" ? color(d.source.name)
                        : color(d.target.name))
                .attr("stroke-width", d => Math.max(1, d.width));
        }

        update();

        // mouse-over formatted flow titles
        link.append("title")
            .text(d => `${d.source.name} → ${d.target.name}\n${format(d.value)}`);

        // add titles to the nodes
        svg.append("g")
            .style("font", "10px sans-serif")
            .selectAll("text")
            .data(nodes)
            .join("text")
            .attr("x", d => d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6)
            .attr("y", d => (d.y1 + d.y0) / 2)
            .attr("dy", "0.35em")
            .attr("text-anchor", d => d.x0 < width / 2 ? "start" : "end")
            .text(d => d.name);

    };

    // TODO - callback if data changes,
    // This is the callback executed when the Bokeh data has an change (e.g. when
    // the server updates the data). It's basic function is simply to translate
    // Bokeh data source to Sankey JSON format
    connect_signals() {
        super.connect_signals();
        // Set BokehJS listener so that when the Bokeh data source has a change
        // event, we can process the new data
        this.connect(this.model.source.change, () => this.render())
    }

}


export class Sankey extends HTMLBox {

    constructor(attrs) {
        super(attrs)
    }

    static initClass() {
        // This is usually boilerplate. In some cases there may not be a view.
        this.prototype.default_view = SankeyView;

        this.define({
            source: [ p.Instance ],
            options:     [ p.Any,     OPTIONS ],
        })
    }
}
Sankey.initClass();
