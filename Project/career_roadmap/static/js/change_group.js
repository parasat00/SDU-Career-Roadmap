const group = document.querySelector('span.group');
let div = document.querySelector('.change-group');
const form = document.querySelector('#change-group-form');
const links = document.querySelectorAll('.change-profile-links');
let cancel = document.querySelector('#cancel-group-change');

if(div) {
 div.addEventListener('click', hideAndShow);
}
if(cancel) {
 cancel.addEventListener('click', hideAndShow);
}
function hideAndShow(e) {
 form.classList.toggle('hidden');
  links.forEach(link => {
   link.classList.toggle('hidden');
  });
  group.classList.toggle('hidden');
  div.classList.toggle('hidden');
}