function add_input(location, inputname) {
    var loc = document.getElementById(location);
    var div = document.createElement("div");
    var input = document.createElement("input");
    var del = document.createElement("i");
    del.className = "bx bx-x";
    del.onclick = function(){
        this.parentNode.remove();
    }
    input.type = "text";
    input.className = "input_text";
    input.name = inputname;
    div.className = "div-option-add";
    loc.appendChild(div);
    div.appendChild(input);
    div.appendChild(del);
}


document.querySelectorAll('.sidebar-submenu').forEach(e => {
    e.querySelector('.sidebar-menu-dropdown').onclick = (event) => {
        event.preventDefault()
        e.querySelector('.sidebar-menu-dropdown .dropdown-icon').classList.toggle('active')

        let dropdown_content = e.querySelector('.sidebar-menu-dropdown-content')
        let dropdown_content_lis = dropdown_content.querySelectorAll('li')

        let active_height = dropdown_content_lis[0].clientHeight * dropdown_content_lis.length

        dropdown_content.classList.toggle('active')

        dropdown_content.style.height = dropdown_content.classList.contains('active') ? active_height + 'px' : '0'
    }
})

let overlay = document.querySelector('.overlay')
let sidebar = document.querySelector('.sidebar')

document.querySelector('#mobile-toggle').onclick = () => {
    sidebar.classList.toggle('active')
    overlay.classList.toggle('active')
}

document.querySelector('#sidebar-close').onclick = () => {
    sidebar.classList.toggle('active')
    overlay.classList.toggle('active')
}