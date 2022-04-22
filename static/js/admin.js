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

function add_input(location, inputname) {
    var loc = document.getElementById(location);
    var div = document.createElement("div");
    var input = document.createElement("input");
    var del = document.createElement("i");
    del.className = "bx bx-x";
    del.onclick = function () {
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

// Get Data Category Update
$(document).on('click', '.category_update', function (e) {
    e.preventDefault();
    var category_id = $(this).attr("id");
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: "/admin/get_category",
        method: "POST",
        data: { category_id: category_id, 'csrfmiddlewaretoken': csrf_token },
        dataType: "json",
        success: function (response) {
            $('#category_update_id').val(response[0]['category_id']);
            $('#category_update_input_name').val(response[0]['category_name']);
            if (response[0]['category_status'] == '1') {
                $('#category_status').attr('checked', true);
            }else{
                $('#category_status').attr('checked', false);
            }
            // $('#category_status').attr('checked', false);
        }
    });
})

// Get Data Product Update
$(document).on('click', '.product_update', function (e) {
    e.preventDefault();
    var product_id = $(this).attr("id");
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: "/admin/get_product",
        method: "POST",
        data: { product_id: product_id, 'csrfmiddlewaretoken': csrf_token },
        dataType: "json",
        success: function (response) {
            $('#product_id').val(response['product_detail'][0]['pd_id']);
            $('#product_name').val(response['product_detail'][0]['pd_name']);
            $('#product_price').val(response['product_detail'][0]['pd_price']);
            $('#product_quantity').val(response['product_detail'][0]['pd_quantity']);
            $('#product_spec').text(response['product_detail'][0]['pd_price']);
            $('#product_description').text(response['product_detail'][0]['pd_description']);
            if (response['product_detail'][0]['pd_status'] == 1) {
                $('#product_status').attr('checked', true);
            }else{
                $('#product_status').attr('checked', false);
            }
            $('#product_category option[value=' + response['product_detail'][0]['category_id'] + ']').prop("selected", true);
            var image_data = response['product_img'];
            image_data.forEach(element=>{
                var image_card = '<div class="card"><img src="/media/'+ element['ip_url'] +'" class="card-img-top"></div>'
                $('#image_update_product').append(image_card);
            })
        }
    });
})

$(document).on('click', '.product_discount', function (e) {
    e.preventDefault();
    var product_id = $(this).attr("id");
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: "/admin/get_product",
        method: "POST",
        data: { product_id: product_id, 'csrfmiddlewaretoken': csrf_token },
        dataType: "json",
        success: function (response) {
            console.log(response);
            $('#product_price1').val(response['product_price'][0]['pd_price']);
            $('#product_price2').val(response['product_price'][0]['productdiscount__pdd_discount']);
        }
    });
})