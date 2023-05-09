fileInput = document.getElementById('id_submit_file');
 let valid = false;
 let inputs = document.querySelectorAll('input[type="text"]');
 let button = document.querySelector('#submitTask');
 inputs.forEach(a => {
  a.addEventListener('change', checkForValid);
 });
 function checkForValid() {
    if(inputs[0].value != ""||inputs[1].value!="" || fileInput.files.length != 0) {
      button.classList.remove('hidden');
    }
    else {
      button.classList.add('hidden');
    }
  }
 function checkFile(){
  fileInput.click();
 }
  addDialogClosedListener(fileInput, function () {
    file_txt = document.getElementById('file-txt');
    if (fileInput.files.length == 0) {
      file_txt.innerHTML = "No files selected";
    } else {
      file_txt.innerHTML = fileInput.files[0].name;
    }
    checkForValid();
  });
 function addDialogClosedListener(input, callback) {
    var id = null;
    var active = false;
    var wrapper = function () {
      if (active) {
        active = false;
        callback();
      }
    };
    var cleanup = function () {
      clearTimeout(id);
    };
    var shedule = function (delay) {
      id = setTimeout(wrapper, delay);
    };
    var onFocus = function () {
      cleanup();
      shedule(1000); // change the value to bigger if needed
    };
    var onBlur = function () {
      cleanup();
    };
    var onClick = function () {
      cleanup();
      active = true;
    };
    var onChange = function () {
      cleanup();
      shedule(0);
    };
    if(input != null) {
      input.addEventListener('click', onClick);
      input.addEventListener('change', onChange);
      window.addEventListener('focus', onFocus);
      window.addEventListener('blur', onBlur);
      return function () {
        input.removeEventListener('click', onClick);
        input.removeEventListener('change', onChange);
        window.removeEventListener('focus', onFocus);
        window.removeEventListener('blur', onBlur);
      };
    }
  }
 
 let data = JSON.parse(
  document.getElementById('single-task-passed-data').textContent
 );
 let canvas = document.getElementById("canvas");
 let ctx = canvas.getContext("2d");
 let radius = Math.floor(canvas.height/2)-10;
 let totalArc = 0;

 function drawWedge2(percent, color, cX, cY) {
  let arcRadians = percent / 100 * 360 * Math.PI / 180;
  ctx.save();
  ctx.beginPath();
  ctx.moveTo(cX, cY);
  ctx.arc(cX, cY, radius, totalArc, totalArc + arcRadians, false);
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.fill();
  ctx.restore();
  totalArc += arcRadians;
 }
 function drawDonut(cX, cY, color, data, txt) {

  drawWedge2(100-data, "#dadada", cX, cY);
  drawWedge2(data, color, cX, cY);
  ctx.beginPath();
  ctx.moveTo(cX, cY);
  ctx.fillStyle = '#fff';
  ctx.arc(cX, cY, radius * .80, 0, 2 * Math.PI, false);
  ctx.fill();
  ctx.fillStyle = color;
  ctx.font = "bold 16px Arial";
  ctx.textAlign = 'center';
  ctx.fillText(data + '%', cX + 1, cY + 5);
  ctx.fillStyle = '#000';
  ctx.font = "semibold 18px sans-serif";
  ctx.textAlign = 'left';
  ctx.fillText(txt, cX + radius + 15, cY + 5);
 }
 let taking = Math.floor(100 * data['taking'] / data['students'])
 let completed = Math.floor(100 * data['completed'] / data['students'])
 drawDonut(Math.floor(canvas.width / 8), Math.floor(canvas.height / 2), "#1968FF", data['students'] == 0 ? 0 : taking, 'are taking');
 drawDonut(5 * Math.floor(canvas.width / 8), Math.floor(canvas.height / 2), "#00B633", data['students'] == 0 ? 0 : completed, 'completed');