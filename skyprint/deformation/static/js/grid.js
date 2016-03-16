+ function($) {
    'use strict';

  var canvas = document.getElementById('canvas');
  var context = canvas.getContext('2d');
  var radius = 10;
  var selected = null;
  var dragging = false;

  function toCenter(coord) {
      var coord_c = new Object();
      coord_c.x = coord.x - 400;
      coord_c.y = 175 - coord.y;
      return coord_c;
  }

  function fromCenter(coord_c) {
      var coord = new Object();
      coord.x = coord_c.x + 400;
      coord.y = 175 - coord_c.y;
      return coord;
  }

  function getMousePos(evt) {
    var rect = canvas.getBoundingClientRect();
    var coord = new Object();
    coord.x = Math.floor(evt.clientX - rect.left)+1;
    coord.y = Math.floor(evt.clientY - rect.top);
    var coord_c = new Object();
    coord_c = toCenter(coord);
    return ([coord_c.x , coord_c.y ]);
  }

  function getArray() {
    return $.parseJSON($("#coords").val());
  }

  function setArray(arr) {
    $("#coords").val(JSON.stringify(arr));
  }

  function drawDisk(p) {
  var coord_c = new Object();
  coord_c.x = p[0];
  coord_c.y = p[1];
  var coord = fromCenter(coord_c);
  context.beginPath();
  context.arc(coord.x, coord.y, radius, 0, 2 * Math.PI, false);
  context.fillStyle = 'green';
  context.fill();
  context.lineWidth = 1;
  context.strokeStyle = '#003300';
  context.stroke();
  }

  function drawSelected(p) {
  var coord_c = new Object();
  coord_c.x = p[0];
  coord_c.y = p[1];
  var coord = fromCenter(coord_c);
  context.beginPath();
  context.arc(coord.x, coord.y, radius, 0, 2 * Math.PI, false);
  context.fillStyle = 'green';
  context.fill();
  context.lineWidth = 2;
  context.strokeStyle = '#CCAB1B';
  context.stroke();
  }

  function drawArray() {
    var arr = getArray();
    for (var i = 0; i < arr.length; i ++) {
      drawDisk(arr[i]);
    }
  }

  function clear() {
    context.clearRect(0, 0, canvas.width, canvas.height);
  }

  function update() {
    clear();
    drawArray();
  }

  function addCoord(mousePos) {
   var arr = getArray();
   arr.unshift(mousePos);
   setArray(arr);
  }

  function dist2(p1,p2) {
    return Math.pow(p1[0]-p2[0],2) + Math.pow(p1[1]-p2[1],2);
  }

  function closestPoint(mousePos) {
    var arr = getArray();
    var i_min_dist = 0;
    var min_dist = dist2(mousePos,arr[0])
    for (var i = 0; i < arr.length; i ++) {
      var d =dist2(mousePos,arr[i])
      if (min_dist > d) {
        i_min_dist = i;
        min_dist = d;
      }
    }
    return i_min_dist;
  }

  function removeFirstPoint() {
    var arr = getArray();
    arr.shift();
    setArray(arr);
    update();
 }

  $("#canvas")
    .click(function(evt) {
      var mousePos = getMousePos(evt);
      if (evt.shiftKey) {
        if (selected != null) {
           var arr = getArray();
           arr.splice(selected,1);
           setArray(arr);
           update();
        }
      }
      else {
        addCoord(mousePos);
        update();
      }
    })
    .mousemove(function(evt) {
      var mousePos = getMousePos(evt);
      $("#cur").html(mousePos[0] + ',' + mousePos[1]);
      update();
      var arr = getArray()
      if (arr.length != 0) {
        var i = closestPoint(mousePos)
        var closest = arr[i];
        if (dist2(closest, mousePos) < radius * radius) {
          selected = i;
          drawSelected(closest);
        }
        else {
          selected = null;
        }
      }
    });


  $("#raz").click(function(evt) {
    $("#coords").val("[]");
    clear();
  });


  $("#back").click(function() {
    removeFirstPoint();
  });

  $("#coords").keypress(function(evt) {
    console.log(evt.keyCode);
  });

  $("#coords").keyup(function() {
    try{
      update();
      $("#back").prop('disabled',false);
      $("#ok").prop('disabled',false);
      $("#pointGrid").prop('disabled',false);
      $("#err").html('');
    }
    catch(err) {
      $("#back").prop('disabled',true);
      $("#ok").prop('disabled',true);
      $("#pointGrid").prop('disabled',true);
      $("#err").html('Syntaxe incorrecte');
    }
  });

  }(jQuery);
