/*
This file contains the JavaScript (TypeScript) implementation
for a Bokeh custom extension. The "sankey.py" contains the
python counterpart.

This custom model wraps the sankey microlibrary of the third-party D3.js library:
https://github.com/d3/d3-sankey
 */


import {HTMLBox, HTMLBoxView} from "models/layouts/html_box"
import {ColumnDataSource} from "models/sources/column_data_source"
import * as p from "core/properties"
import * as d3 from "d3";

declare namespace d3 {
    class sankey {
        // OPTIONS: object  - TODO, add ability to pass and parse OPTIONS dictionary
        constructor()
        link()

    }
}
// OPTIONS = {
// const width = 975;
// const height = 600;
// };


// To create custom model extensions that will render on to the HTML canvas or
// into the DOM, we must create a View subclass for the model. In this case we
// will subclass from the existing BokehJS ``HTMLBoxView``, corresponding to our.
export class SankeyView extends HTMLBoxView {
    model: Sankey;

    private _graph: d3.sankey;

    render(): void {
        super.render();
        var units = "Widgets";

        // set the dimensions and margins of the graph
        let margin = {top: 10, right: 10, bottom: 10, left: 10},
            width = 700 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;

        // format variables
        let formatNumber = d3.format(",.0f"),    // zero decimal places
            format = function(d) { return formatNumber(d) + " " + units; },
            color = d3.scaleOrdinal(d3.schemeCategory20);

        // append the svg object to the body of the page
        var svg = d3.select("body").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");

        // Set the sankey diagram properties
        this._graph = new d3.sankey()
            .nodeWidth(36)
            .nodePadding(40)
            .size([width, height]);
    }

    // TODO - callback if data changes,
    // connect_signals(): void {
    //     super.connect_signals();
    //     // Set listener so that when the Bokeh data source has a change
    //     // event, we can process the new data
    //     this.connect(this.model.data_source.change, () => this._graph.constructor(this.el, this.parse_data()))
    // }

    // This is the callback executed when the Bokeh data has an change (e.g. when
    // the server updates the data). It's basic function is simply to translate
    // Bokeh data source to Sankey JSON format
    parse_data(): {} {
        //set up graph in same style as original example but empty
        const graph: { [id: string]: any } = {"nodes" : [], "links" : []};
        const source = this.model.data_source;

        for (let i = 0; i < source.get_length()!; i++) {
            graph.nodes.push({ "name": source.data.source[i] });
            graph.nodes.push({ "name": source.data.target[i] });
            graph.links.push(
                { "source": source.data.source[i],
                    "target": source.data.target[i],
                    "value": source.data.value[i] });

        }
        return graph
    }
}

// We must also create a corresponding JavaScript model subclass to
// correspond to the python Bokeh model subclass. In this case, since we want
// an element that can position itself in the DOM according to a Bokeh layout,
// we subclass from ``HTMLBox``

export namespace Sankey {
    export type Attrs = p.AttrsOf<Props>

    export type Props = HTMLBox.Props & {
        data_source: p.Property<ColumnDataSource>
        // options: p.Property<{[key: string]: unknown}>
    }
}

export interface Sankey extends Sankey.Attrs {}

export class Sankey extends HTMLBox {
    properties: Sankey.Props;

    constructor(attrs?: Partial<Sankey.Attrs>) {
        super(attrs);
    }

    // The ``__name__`` class attribute should generally match exactly the name
    // of the corresponding Python class. Note that if using TypeScript, this
    // will be automatically filled in during compilation, so except in some
    // special cases, this shouldn't be generally included manually, to avoid
    // typos, which would prohibit serialization/deserialization of this model.
    // static __name__ = "Sankey";

    static init_Sankey(): void {
        // This is usually boilerplate. In some cases there may not be a view.
        this.prototype.default_view = SankeyView;

        // The @define block adds corresponding "properties" to the JS model. These
        // should basically line up 1-1 with the Python model class. Most property
        // types have counterparts, e.g. ``bokeh.core.properties.String`` will be
        // ``p.String`` in the JS implementatin. Where the JS type system is not yet
        // as rich, you can use ``p.Any`` as a "wildcard" property type.
        this.define<Sankey.Props>({
            data_source: [ p.Instance         ],
            // options:     [ p.Any,     OPTIONS ],
        })
    }
}
Sankey.init_Sankey();
