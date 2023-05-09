 document.querySelectorAll('.progress').forEach(p => {
  let percentage = Math.floor(100 * p.dataset.completed / p.dataset.total);
  p.style.width=`${percentage}%`;
 })
  // Script to check if carousel needs side buttons/can be slided
 document.querySelectorAll('.category-window, .carousel-window').forEach(a => {
  b = a.querySelector('.flex');
  if (b.clientWidth == b.scrollWidth) {
    a.parentNode.querySelector('.button-prev').style.display = "none";
    a.parentNode.querySelector('.button-next').style.display = "none";
    a.classList.add('margined');
  }
 });
// Script to move carousel when button is clicked
 document.querySelectorAll('.carousel-button').forEach(button => {
    button.addEventListener('click', function () {
      let carousel = null;
      let multiplier = 1;
      let itemwidth = 0;
      let gap = 0;
      let pos = 0;
      

      if (button.classList.contains('button-next')) {
        multiplier = -1;
      }

      if (button.parentNode.querySelector('.category-window')==null){
        carousel = button.parentNode.querySelector('.carousel-window').querySelector('.flex');
        itemwidth = carousel.querySelector('.task-block').clientWidth;
        gap = 10;
      }
      else {
        carousel = button.parentNode.querySelector('.category-window').querySelector('.flex');
        // itemwidth = 180;
        itemwidth = carousel.querySelector('.small-track').clientWidth;
        gap = 15;
      }
      var style = window.getComputedStyle(carousel);
      var matrix = new WebKitCSSMatrix(style.transform);
      let prev_val = matrix.m41;
      pos = multiplier * (itemwidth + gap);
      let translate_val = Math.floor(prev_val + pos);
      let carousel_right = Math.floor(carousel.clientWidth - translate_val);
      console.log(carousel.clientWidth + ' - ' + translate_val + ' = ' + (carousel.clientWidth - translate_val));
      console.log(carousel_right + ' <= ' + carousel.scrollWidth + ' = ' + (carousel_right <= carousel.scrollWidth));
      if (translate_val <= 0 && carousel_right <= carousel.scrollWidth) {
        string = "translateX(" + (translate_val) + "px)";
        carousel.style.transform = string;
        carousel.style.transition = " all 1s";
      }
      let button_prev = button.parentNode.querySelector('.button-prev');
      let button_next = button.parentNode.querySelector('.button-next');
      check4Toggle(button_prev, translate_val, 0);
      check4Toggle(button_next, carousel_right, carousel.scrollWidth);
      
    });
  });
  function check4Toggle(button, val, condition_val) {
    
    if (val >= condition_val) {
      button.classList.toggle('disabled');
    }
    else {
      if (button.classList.contains('disabled')){
        button.classList.toggle('disabled');
      }
    }
  }