function viz(input_net, input_seq, hashtag, speed) {

var width = 960,
    height = 720;

var node_size_multiplier = 5;
var link_size_multiplier = 0.5;

var color = d3.scale.linear().domain([1,10]).range(['#85c6dc','#ff9d1f']);
//var color = d3.scale.category20();

var nodes = [],
    links = [];

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

var force = d3.layout.force()
    .nodes(nodes)
    .links(links)
    .charge(-120)
    .linkDistance(50)
    //.linkStrength(function(d) {return d.value;} )
    //.gravity(0.15)
    .size([width, height])
    .on("tick", tick);

var node = svg.selectAll(".node"),
    link = svg.selectAll(".link"),
    label = svg.selectAll(".label");

// Helper
Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

// Change the graph
function start() {
    //console.log("#nodes: "+nodes.length + " #links: " + links.length);
    
    link = link.data(force.links(), function(d) {return d.source.id + "-" + d.target.id;});
    link.enter().insert("line", ".node")
    .attr("class", "link")
    .style("stroke-width", function(d) {return d.value;});
    link.exit().remove();
    
    
    node = node.data(force.nodes(), function(d) {return d.id;});
    node.enter().append("circle")
    .attr("id", function(d) {return d.id;})
    .attr("class", function(d) {return "node "+d.id;})
    .style("fill", function(d) {return color(d.value);})
    .attr("r", function(d) {
        return Math.sqrt(d.value)*node_size_multiplier; 
    });
    node.call(force.drag);
    
    node.exit().remove();
    
    force.start();
}

// tick function
function tick() {
  node.attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; })
  
  link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });
  
  label.attr("transform", function(d) {
    return "translate(" + d.x + "," + d.y + ")";
  });
  
}

// Read the graph
d3.json(input_net, function(error, graph) {
  
  var nodes_hash = {};
  var links_cache = {};
  if (typeof graph.links != 'undefined' && graph.links.length > 0) {
      for (var i = 0; i < graph.links.length; i++) {
          var s = "n"+graph.links[i].source;
          var t = "n"+graph.links[i].target;
          var val = graph.links[i].value;
          val = Math.sqrt(Math.sqrt(val)) * link_size_multiplier;
          
          if (!links_cache.hasOwnProperty(s)) links_cache[s] = {};
          if (!links_cache.hasOwnProperty(t)) links_cache[t] = {};
          
          links_cache[t][s] = val;
          links_cache[s][t] = val;
      }
  }
  
  //Add the SVG Text Element to the svgContainer
  var text = svg.append("text")
                .attr('id', 'viz-title');
  
  //Add SVG Text Element Attributes
  var textLabels = text
                   .attr("x", width/2-200)
                   .attr("y", 30)
                   .text("There are 0 users in 0 community.")
                   .attr("z-index", -1)
                   .attr("font-family", "sans-serif")
                   .attr("font-size", "18px")
                   .attr("fill", "#666");
  
  //console.log("Size of links_cache:" + Object.size(links_cache));
  
  var num_user = 0;
  var cur_date_string = "";
  
  // Read the sequence
  d3.json(input_seq, function(error, seq) {
    
    // Add one by one
    var interval = setInterval( function() { 
      
      if (typeof seq != 'undefined' && seq.length > 0) {
        
        var nodeinfo = seq.shift();
        num_user = num_user + 1;
        cur_date_string = nodeinfo[2];
        
        if ( nodes_hash.hasOwnProperty(nodeinfo[0]) ) {
          var node = nodes_hash[nodeinfo[0]];
          node.value = nodeinfo[1];
          nodes_hash[nodeinfo[0]] = node;
          svg.select( "#" + node.id )
             .transition()
             .attr("r", Math.sqrt(node.value)*node_size_multiplier)
             .style("fill", color(node.value));
        }
        else {
          
          // node does not exist:
          var node = {"id": nodeinfo[0], "value": nodeinfo[1]};
          nodes.push(node);
          nodes_hash[node.id] = node;
          
          // add node text
          /*
          svg.append("text").data(force.nodes())
              .attr("class", "label")
              .attr("x", function(d) {return d.x;})
              .attr("y", function(d) {return d.y;})
              .text(function(d) {return d.value;});
          */
          
          // add links of this node
          if (links_cache.hasOwnProperty(node.id)) {
              for (other_id in links_cache[node.id])
                  if (links_cache[node.id].hasOwnProperty(other_id))
                      if (nodes_hash.hasOwnProperty(other_id)) {
                          var other = nodes_hash[other_id];
                          links.push({
                              "source":node,
                              "target":other,
                              "value":links_cache[node.id][other_id]
                          });
                      }
          }
          
          start();
          
        }
        
        // Update text
        svg.select('#viz-title')
           .text(hashtag.charAt(0).toUpperCase() + hashtag.slice(1) + 
                 ": "+num_user+" users in "+
                 nodes.length+" community. "+
                 cur_date_string);
      }
    }, speed);

  });

});


}