let modal = document.querySelector('.modal-view');
let span = document.querySelector('#modal-close');
let filter = document.querySelectorAll('.filter-wrapper-button');
let delete_cancel = document.querySelector('.delete-cancel');
let bars = document.querySelector('.upper_flex .bars_icon');
let side_nav = document.querySelector('.side-menu');
let close_nav = side_nav.querySelector('.closeBtn');
let second_logo = document.querySelector('.upper_flex .logo');

if(bars) {
 bars.onclick = function() {
  side_nav.classList.toggle('opened');
  second_logo.style.display="none";
 }
}
if(close_nav) {
 close_nav.onclick = function() {
  side_nav.classList.toggle('opened');
  second_logo.style.display="block";
 }
}
const hidemodal = () => {
 modal.classList.add('hidden');
}
window.onclick = function (event) {
 if (event.target == modal) {
  hidemodal();
 }
}
if (span != null) {
 span.onclick = function () {
  hidemodal();
 }
}
if (delete_cancel != null) {
 delete_cancel.onclick = function () {
  hidemodal();
 }
}
filter.forEach(f => {
 f.addEventListener('click',e=> {
  let filter_window = f.parentNode.querySelector('.filter-window');
  filter_window.classList.toggle('hidden');
 });
});
document.querySelectorAll('.delete').forEach(e => {
 e.addEventListener('click', function () {
  modal.classList.remove('hidden');
 });
 if(e.dataset.id){
  let url = '/delete-category/' + e.dataset.id + '/';
  modal.getElementsByTagName('form')[0].action = url;
 }
});
//  Script to put rating on each track
document.querySelectorAll('.rating').forEach(rating => {
 grade = rating.dataset.value;
 stars = rating.querySelectorAll('.star');
 rounded = Math.floor(grade);
 for (i = 0; i < rounded; i++) {
  stars[i].classList.add('full');
 }
 if (grade - rounded >= 0.5) {
  stars[rounded].classList.add('half');
 }
})