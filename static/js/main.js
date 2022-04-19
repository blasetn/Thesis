function OpenMenu(key) {
  var x = document.getElementById(key);
  if (x.classList.contains('show-menu')) {
    x.classList.remove('show-menu');
  } else {
    x.classList.add("show-menu");
  }
}
function add_input(location) {
  var loc = document.getElementById(location);
  var x = document.createElement("INPUT");
  x.setAttribute("type", "text");
  x.setAttribute("value", "Hello World!");
  loc.appendChild(x);
}