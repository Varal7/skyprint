+ function($) {
    'use strict';
  function getMousePos(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
      x: Math.floor(evt.clientX - rect.left)+1,
      y: Math.floor(evt.clientY - rect.top)
    };
  }

  function drawCircle(canvas, center_x, center_y, radius) {
  var context = canvas.getContext('2d');
  context.beginPath();
  context.arc(center_x, center_y, radius, 0, 2 * Math.PI, false);
  context.fillStyle = 'green';
  context.fill();
  context.lineWidth = 1;
  context.strokeStyle = '#003300';
  context.stroke();
  }

  function drawArray(arr) {
    for (var i = 0; i < arr.length; i ++) {
      drawCircle(canvas, arr[i][0], arr[i][1], 10);
    }
  }

  function clear(canvas) {
    var context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);
  }

  function addCoord(mousePos) {
   //  $("#coords").value(mousePos.x +  ", " mousePos.y);
   var arr = $.parseJSON($("#coords").val());
   arr.unshift([mousePos.x,mousePos.y]);
   $("#coords").val(JSON.stringify(arr));
  }

  function readCoord(str) {
    var arr = $.parseJSON($("#coords").val());
    console.log(arr);
  }

  function removeFirstPoint() {
    var arr = $.parseJSON($("#coords").val());
    arr.shift();
    $("#coords").val(JSON.stringify(arr));
    clear(canvas);
    drawArray(arr);
 }

  var canvas = document.getElementById('pointGrid');
  var context = canvas.getContext('2d');

  canvas.addEventListener('click', function(evt) {
    var mousePos = getMousePos(canvas, evt);
    drawCircle(canvas, mousePos.x, mousePos.y, 10);
    addCoord(mousePos);

  }, false);

  canvas.addEventListener('mousemove', function(evt) {
    var mousePos = getMousePos(canvas, evt);
    $("#cur").html(mousePos.x + ',' + mousePos.y);
  }, false);

  document.getElementById('raz').addEventListener('click', function(evt) {
    clear(canvas);
  }, false);

  document.getElementById('ok').addEventListener('click', function(evt) {
    readCoord($("#coords").val());
  }, false);

  document.getElementById('back').addEventListener('click', function(evt) {
    removeFirstPoint();
  }, false);

  }(jQuery);
