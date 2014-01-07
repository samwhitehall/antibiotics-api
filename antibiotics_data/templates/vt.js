function Model(data) {
  this.tree = this.flattenData(data);
  this.options = this.extractOptions(data);
  this.completeTree = this.flattenData(data);
}

Model.prototype = {
    setChildren : function(node) {
        if("act" in node) {
            node.children = [];
            for(var i = 0; i < node.act.length; i++) {
                var child = node.act[i];
                child.parent = node.uid;
                node.children.push(child.uid);
            }
        }
    },
    descendants : function(tree) {
        d = [tree]  
        if("act" in tree) {
            for(var i =0; i < tree.act.length; i++) {
                d = d.concat(this.descendants(tree.act[i]));
            }
        }
        return d;
    },
    flattenData : function(data){
        var des =  this.descendants(data.DecisionTree); 
        var ret = [];
        for(var i = 0; i < des.length; i++) {
            des[i].uid = i;
        }
        for(var i = 0; i < des.length; i++) {
            var node = des[i];
            this.setChildren(node);

            newNode = {};
            newNode.id = node.id;
            newNode.uid = node.uid;
            if("children" in node) {
                newNode.children = node.children;
            }

            if("parent" in node) {
                newNode.parent = node.parent;
            }
            ret.push(newNode);
        }

        return ret;
    },
    extractOptions : function(data) {
        d = data.Questions.concat(data.Treatments); 
        opts = {};
        for(var i =0; i < d.length; i++) {
            var node = d[i];
            var n = {};

            n.desc = "desc" in node ? node.desc : node.text;
            n.type = "tid" in node ? "treatment" : "question";
            if("ans" in node) {
                n.ans = node.ans;
            }
            opts["tid" in node ? node.tid : node.qid] = n;
        }
        return opts;
    }
};
function Controller(model, view) {

 this.zoomLevel = 1.0;
 this.viewCenter = {x : 0, y : 0};
 this.viewAspectRatio = 1.0;

 this.highlightedID = null;
 this.selectedUID = null;
 this.previousHighlighted = null;
 this.previouslySelected = null;
}

Controller.prototype = {
  expandContract : function(uid) {
    var des = [];
    var tree = window.model.tree;
    var root = tree[uid];

    (function descendants(node) {
        des = des.concat(node.uid);
        if("children" in node) {
            for(var i = 0; i < node.children.length; i++) {
                descendants(tree[node.children[i].uid]);
            }
        }
    })(root);

    window.view.expandContract(des);
    this.changeView();
  },
  highlighted : function(id) {
      if(this.previouslyHighlighted != null) {
          window.view.unHighlight(this.previouslyHighlighted);
      }
      window.view.highlight(id);
      this.previouslyHighlighted = id;
      this.changeView();
  },
  selected : function(uid) {
      if(this.previouslySelected != null) {
          window.view.unSelect(this.previouslySelected);
      }
      window.view.select(uid);
      this.previouslySelected = uid;
      this.changeView();
      window.view.statePanel.html("");
      var statePanel = window.view.statePanel.append("div").attr('class', 'row');

     statePanel.append("div").attr("class", "col-md-1");

      var node = statePanel.append("div").attr("class", "col-md-2")
          .append("div")
          .attr("class", "panel panel-warning");

      var n = window.model.tree[uid];

          node.append("div").attr("class", "panel-heading").text(function(d) {
              return n.id;
          });
          node.append("div").attr("class", "panel-body").text(function(d) {
              return window.model.options[n.id].desc;
          });

     statePanel.append("div").attr("class", "col-md-1");

     statePanel.append("div")
         .attr("class", "col-md-7 well")
         .attr("style", "background-color: white")
         .html(function(d) {
            var path = [];  
            var node = window.model.tree[uid];
            while("parent" in node) {
                path.push(node.uid);
                node = node.parent;
            }
            path.push(node.uid);
            
         path.reverse();

         questions = [];
         answers = [];
         for(var i =0; i < path.length-1; i++) {
             var now = window.model.tree[path[i]];
             var next = window.model.tree[path[i+1]];
             var index = null;

             for(var j = 0; j < now.children.length; j++) {
                 if(now.children[j].uid == next.uid) {
                    index = j;
                 }
             }
             console.log(window.model.options);
             answers.push(window.model.options[now.id].ans[index]); 
             var id = window.model.tree[path[i]].id;
             questions.push(window.model.options[id].desc);
         }

         
         var string = "";
         for(var i = 0; i < questions.length; i ++) {
             string = string + "<div class='row'><div class='col-md-6'>" + questions[i] + ": </div><div class='col-md-6' style='text-align:right'>" + answers[i] + "</div></div>";
         }
         return string;
     });
     statePanel.append("div").attr("class", "col-md-1");

  },
  zoom : function(scale) {
        this.zoomLevel = scale;
        this.changeView();
  },
  drag : function(dx, dy) {
    this.viewCenter.x = this.viewCenter.x - this.zoomLevel * dy;
    this.viewCenter.y = this.viewCenter.y - this.zoomLevel * dx;
    
    this.changeView();
  },
  changeView : function() {
    var width = this.zoomLevel * this.viewHeight * this.viewAspectRatio; 
    var height = this.viewHeight * this.zoomLevel;

    var x = this.viewCenter.x,
        y = this.viewCenter.y;

    var ret = {};
    ret.left = x - width/2;
    ret.right = x + width/2;
    ret.top = y - height/2;
    ret.bot = y + height/2;

    window.view.setViewBox(ret);
  },
  setViewBox : function(vb) {
    this.viewCenter.x = (vb.right + vb.left)/2;    
    this.viewCenter.y = (vb.top + vb.bot)/2;    

    this.viewAspectRatio = (vb.right - vb.left)/ (vb.bot - vb.top);
    this.viewHeight = vb.bot - vb.top;
    this.changeView();
  }
};
function View(root, model) {
  this.model = model;
  this.root = root.append("div").attr("class" , "row");
  this.svgStatePanel = this.root.append("div").attr("class"," col-md-8");

  this.svg = this.svgStatePanel.append("div").attr("class", "row").append("svg");
  this.statePanel = this.svgStatePanel.append("div").attr("class", "row").append("div").attr('class', "well");
}

View.prototype = {
  draw : function() {
    var nodeSize = {width : 200, height :100}; 
    var tree = d3.layout.tree()
        .nodeSize([nodeSize.height * 1.5, nodeSize.width * 1.5])
        .children(
                function(d) {
                    c = [];
                    if("children" in d) {
                        for(var i =0; i < d.children.length; i++) {
                            c.push(window.view.model.tree[d.children[i]]);
                        }
                    }
                    return c;
                })
        .separation(function(d) {return 1;});

    var nodes = tree.nodes(this.model.tree[0]),
        links = tree.links(nodes);

    var stepLine = d3.svg.line()
        .x(function(d) {return d.y;})
        .y(function(d) {return d.x;})
        .interpolate("step");

    window.controller.setViewBox(this.boundingBox(nodes, nodeSize));


    var link = this.svg.selectAll("g").data(links).enter()
        .append("g");
        
        link.append("path")
            .attr("id", function(d) {return "link" + d.target.uid;})
            .attr("class", "link")
            .attr("d", function(d) {
                return stepLine([{x : d.source.x, y: d.source.y}, {x : d.target.x, y : d.target.y}]);
            });

    var labels = this.svg.selectAll("text.label")
        .data(links)
        .enter()
        .append("text")
            .attr("id", function(d) {return "textLabel"+d.target.uid;})
            .attr("x", function(d) {return d.target.y - 130;})
            .attr("y", function(d) {return d.target.x;})
            .attr("fill", "red")
            .text(function(d) {
                var source = d.source;
                var target = d.target;
                var children = window.model.tree[source.uid].children;
                var index = null;
                for(var i = 0; i < children.length; i++) {
                    if(children[i].uid == target.uid) {
                        index = i;
                    }
                }
                return window.model.options[source.id].ans[index];
            });


    var expandBox = this.svg.selectAll("g.expanderContractor").data(links).enter()
        .append("g").attr("transform", function(d) {
            var y = d.source.y/2 + d.target.y/2;
            var x = d.target.x;
            return "translate(" + y + "," + x + ")";})
        .append("g").attr("transform", "translate(-5,-5)")
        .append("rect")
            .attr("class", "expanderContractor")
            .attr("width", 10)
            .attr("height", 10)
            .attr("id", function(d) {return "expandbox" + d.target.uid;})
            .style("fill : rgb(0,255,255)")

            /*.append("line")
        .attr("x1", 5)
        .attr("y1", 0)
        .attr("x2", 5)
        .attr("y2", 10)
        .style("stroke:rgb(0,0,255); stroke-width:2");
        */
    
    var node = this.svg.selectAll("g.node").data(nodes).enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", function(d) {return "translate(" + d.y + "," + d.x + ")";});

    var nodeDiv = node.append("foreignObject")
        .attr("width", nodeSize.width)
        .attr("height", nodeSize.height)
        .attr("x", -nodeSize.width/2)
        .attr("y", -nodeSize.height/2)
        .append("xhtml:div")
            .attr("style", "width : " + nodeSize.width + "px; height: " + nodeSize.height + "px")
            .attr("id", function(d) {return d.uid;})
            .attr("class", function(d) {
                return d.id + " panel panel-" + (window.model.options[d.id].type == "question" ? "primary" : "success");
            });
    nodeDiv.append("div").attr("class", "panel-heading").text(function(d) {
        return d.id;
    })
    nodeDiv.append("div").attr("class", "panel-body").text(function(d) {
        return window.model.options[d.id].desc;
    });

    var qs = [],
        ts = [];

    for(var i in window.model.options) {
        var n = window.model.options[i];
        n.id = i;
        if(n.type =="question") {
            qs.push(n);
        } else {
            ts.push(n);
        }
    }


    var optionsDiv = view.root.append("div")
        .attr("id", "optionsDiv")
        .attr("class", "col-md-4 well");

    optionsDiv.append("h2").text("Questions");
    
    var qDiv = optionsDiv.append("div").attr("id", "qDiv").attr("class", "row list-group");
    optionsDiv.append("h2").text("Treatments");

    var tDiv = optionsDiv.append("div").attr("id", "tDiv").attr("class", "row list-group");

    var q = qDiv.selectAll("a")
        .data(qs)
        .enter()
        .append("a").attr("href", "javascript:void(0)").attr("id", function(d) {return d.id;}).attr("class", "list-group-item");

    var t = tDiv.selectAll("a")
        .data(ts)
        .enter()
        .append("a").attr("href", "javascript:void(0)").attr("id", function(d) {return d.id;}).attr("class", "list-group-item");

    q.text(function(d) {return d.id});
    q.append("p").text(function(d) {return d.desc;});

    t.text(function(d) {return d.id});
    t.append("p").text(function(d) {return d.text;});


  },
  setViewBox : function(vb) {
      var minx = vb.top;
      var miny = vb.left;
      var height = vb.right - vb.left;
      var width = vb.bot - vb.top;
      this.svg.attr("viewBox", minx + " " + miny + " " + width + " " + height);
  },
  boundingBox : function(nodes, nodeSize) {
     var bb = {top : 0, bot : 0, left: 0, right: 0}
     
     for(var i = 0; i < nodes.length; i++) {
         var n = nodes[i];
         if(i == 0) {
             bb.top = n.y;
             bb.left = n.x;
             bb.right = n.x+ nodeSize.width;
             bb.bot = n.y + nodeSize.height;
         }
         bb.top = bb.top < n.y ? bb.top : n.y;
         bb.right = bb.right > n.x + nodeSize.width ? bb.right : n.x + nodeSize.width;
         bb.left = bb.left < n.x ? bb.left : n.x;
         bb.bot = bb.bot > n.y + nodeSize.height ? bb.bot : n.y + nodeSize.height;

         }
    bb.left -= nodeSize.width/2;
    bb.right -= nodeSize.width/2;
     

     return bb;

  },
  highlight : function(id) {

    var $a = $("#" + id);
    $("." + id).addClass("panel-danger");

    $a.addClass("active");
    
  },
  unHighlight : function(id) {
    var $a = $("#" + id);
    $("." + id).removeClass("panel-danger");
    $a.removeClass("active");
  },
  select : function(uid) {
    var $a = $("#" + uid); 
    $a.addClass("panel-warning");
  },
  unSelect : function(uid) {
    var $a = $("#" + uid);
    $a.removeClass("panel-warning");
  },
  expandContract : function(des) {
    
      var root = des[0];
      for(var i = 0; i < des.length; i++) {
        var node = $("#"+ des[i]);
        var textLabel = $("#textLabel" + des[i]);
        var expandbox = $("#expandbox" + des[i]);
        var link = $("#link" + des[i]);

        
        node.toggle();
        textLabel.toggle();
        if(i != 0) {
        expandbox.toggle();
        link.toggle();

        }
      }
  },
  addListeners : function() {
    var svg = this.svg;
    var pan = d3.behavior.drag()
        .on("dragend", dragEnded)
        .on("drag", dragged);
    svg.call(pan);

    var zoom = d3.behavior.zoom()
        .scaleExtent([0.1, 2])
        .on("zoom", zoomed);
    svg.call(zoom);

    function dragEnded() {
        window.dragging = false;
    }

    function dragged() {
        window.dragging = true;
        if(d3.event.sourceEvent.type == 'mousemove') {
        var dx = d3.event.dx,
            dy = d3.event.dy;
        window.controller.drag(dx,dy);
        }
    }

    function zoomed() {
        if(d3.event.sourceEvent.type == 'wheel') {
        console.log(d3.event.scale);
        window.controller.zoom(d3.event.scale);  
        }
    }

    $(".list-group-item").click(function(e) {
      window.controller.highlighted($(this).attr("id")); 
      console.log($(this).attr("id"));
      //e.preventDefault();
    });

    window.view.svg.selectAll("div.panel").on("click", function(d,i) {
        console.log(d.uid);
        window.controller.selected(d.uid);
        
    });

    window.view.svg.selectAll("rect.expanderContractor").on('click', function(d,i) {
        console.log(i,d);
      window.controller.expandContract(d.target.uid);  
    });

  }
};
