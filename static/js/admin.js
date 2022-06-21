window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple);
    }
});

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
        url: "/admin/ajax_get_category/",
        method: "POST",
        data: { category_id: category_id, 'csrfmiddlewaretoken': csrf_token },
        dataType: "json",
        success: function (response) {
            $('#category_update_id').val(response[0]['category_id']);
            $('#category_update_input_name').val(response[0]['category_name']);
        }
    });
})

// Get Data Brand Update
$(document).on('click', '.brand_update', function (e) {
    e.preventDefault();
    var brand_id = $(this).attr("id");
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: "/admin/ajax_get_brand/",
        method: "POST",
        data: { brand_id: brand_id, 'csrfmiddlewaretoken': csrf_token },
        dataType: "json",
        success: function (response) {
            $('#category_update_id').val(response[0]['brand_id']);
            $('#category_update_input_name').val(response[0]['brand_name']);
        }
    });
})

// Get Data Product Update
$(document).on('click', '.product_update', function (e) {
    e.preventDefault();
    var product_id = $(this).attr("id");
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: "/admin/ajax_get_product/",
        method: "POST",
        data: { product_id: product_id, 'csrfmiddlewaretoken': csrf_token },
        dataType: "json",
        success: function (response) {
            $('#product_id').val(response['product_detail'][0]['pd_id']);
            $('#product_name').val(response['product_detail'][0]['pd_name']);
            $('#product_price').val(response['product_detail'][0]['pd_price']);
            $('#product_pricesale').val(response['product_detail'][0]['pd_pricesale']);
            $('#product_quantity').val(response['product_detail'][0]['pd_quantity']);
            $('#product_spec').text(response['product_detail'][0]['pd_spec']);
            $('#product_description').text(response['product_detail'][0]['pd_description']);
            if (response['product_detail'][0]['pd_status'] == 1) {
                $('#product_status').attr('checked', true);
            } else {
                $('#product_status').attr('checked', false);
            }
            $('#product_category option[value=' + response['product_detail'][0]['category_id'] + ']').prop("selected", true);
            $('#product_brand option[value=' + response['product_detail'][0]['brand_id'] + ']').prop("selected", true);
            var image_data = response['product_img'];
            $('#image_update_product').html('');
            $('#image_update_product').append('<div class="card"><img src="/media/' + response['product_detail'][0]['pd_img'] + '" class="card-img-top"></div>');
            image_data.forEach(element => {
                var image_card = '<div class="card"><img src="/media/' + element['ip_url'] + '" class="card-img-top"></div>'
                $('#image_update_product').append(image_card);
            })
        }
    });
})

// $(document).on('click', '.product_discount', function (e) {
//     e.preventDefault();
//     var product_id = $(this).attr("id");
//     var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
//     $.ajax({
//         url: "/admin/ajax_get_product/",
//         method: "POST",
//         data: { product_id: product_id, 'csrfmiddlewaretoken': csrf_token },
//         dataType: "json",
//         success: function (response) {
//             $('#product_price_id').val(response['product_price'][0]['pd_id']);
//             $('#product_price1').val(response['product_price'][0]['pd_price']);
//             $('#product_price2').val(response['product_price'][0]['productdiscount__pdd_discount']);
//             if (response['product_price'][0]['productdiscount__pdd_active'] == '1') {
//                 $('#product_price_active').attr('checked', true);
//             } else {
//                 $('#product_price_active').attr('checked', false);
//             }
//             $('#product_price_datestart').val("");
//             $('#product_price_dateend').val("");
//             $('#product_price_datestart').attr('max', "");
//             $('#product_price_dateend').attr('min', "");
//             if (response['product_price'][0]['productdiscount__pdd_date_start'] || response['product_price'][0]['productdiscount__pdd_date_end']) {
//                 var date_start = response['product_price'][0]['productdiscount__pdd_date_start'];
//                 var date_end = response['product_price'][0]['productdiscount__pdd_date_end'];
//                 $('#product_price_time_active').attr('checked', true);
//                 $('.product_price_time_start').removeClass("d-none");
//                 $('.product_price_time_end').removeClass("d-none");
//                 // $('#product_price_datestart').attr('max', date_end);
//                 $('#product_price_dateend').attr('min', date_start);
//                 if(date_start == null){
//                     $('#product_price_datestart').val("");
//                 }else{
//                     date_start = new Date(date_start).toISOString().slice(0, 19);
//                     $('#product_price_datestart').val(date_start);
//                 }
//                 if(date_end == null){
//                     $('#product_price_dateend').val("");
//                 }else{
//                     date_end = new Date(date_end).toISOString().slice(0, 19);
//                     $('#product_price_dateend').val(date_end);
//                 }
//             } else {
//                 $('#product_price_time_active').attr('checked', false);
//                 $('.product_price_time_start').addClass("d-none");
//                 $('.product_price_time_end').addClass("d-none");
//             }
//         }
//     });
// })

$(document).on('change', '.product_price_time_active', function () {
    if (this.checked) {
        $('.product_price_time_start').removeClass("d-none");
        $('.product_price_time_end').removeClass("d-none");
    } else {
        $('.product_price_time_start').addClass("d-none");
        $('.product_price_time_end').addClass("d-none");
    }
});

$(document).on('change', '.voucher_value_type', function () {
    if (this.checked) {
        $('.input_voucher_value').attr("max", 100);
    } else {
        $('.input_voucher_value').removeAttr("max");
    }
});

$(document).on('click', '.btn_voucher_update', function (e) {
    e.preventDefault();
    var voucher_id = $(this).attr("id");
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: "/admin/ajax_get_voucher/",
        method: "POST",
        data: { voucher_id: voucher_id, 'csrfmiddlewaretoken': csrf_token },
        dataType: "json",
        success: function (response) {
            $('#voucher_id').val(response['voucher_detail'][0]['voucher_id']);
            $('#voucher_code').val(response['voucher_detail'][0]['voucher_code']);
            if (response['voucher_detail'][0]['voucher_value'] > 1) {
                $('#voucher_value_type_update').attr('checked', false);
                $('#voucher_value').val(response['voucher_detail'][0]['voucher_value']);
            } else {
                $('#voucher_value_type_update').attr('checked', true);
                $('#voucher_value').val(response['voucher_detail'][0]['voucher_value']*100);
            }
            $('#voucher_quantity').val(response['voucher_detail'][0]['voucher_quantity']);
            if (response['voucher_detail'][0]['voucher_active'] == 1) {
                $('#voucher_active_update').attr('checked', true);
            } else {
                $('#voucher_active_update').attr('checked', false);
            }
            $('#voucher_date_start').val("");
            $('#voucher_date_end').val("");
            $('#voucher_date_start').attr('max', "");
            $('#voucher_date_end').attr('min', "");
            if (response['voucher_detail'][0]['voucher_date_start'] || response['voucher_detail'][0]['voucher_date_end']) {
                var date_start = response['voucher_detail'][0]['voucher_date_start'];
                var date_end = response['voucher_detail'][0]['voucher_date_end'];
                $('#voucher_time_active').attr('checked', true);
                $('.product_price_time_start').removeClass("d-none");
                $('.product_price_time_end').removeClass("d-none");
                // $('#product_price_datestart').attr('max', date_end);
                $('#voucher_date_end').attr('min', date_start);
                if(date_start == null){
                    $('#voucher_date_start').val("");
                }else{
                    $('#voucher_date_start').val(date_start);
                }
                if(date_end == null){
                    $('#voucher_date_end').val("");
                }else{
                    $('#voucher_date_end').val(date_end);
                }
            } else {
                $('#voucher_time_active').attr('checked', false);
                $('.product_price_time_start').addClass("d-none");
                $('.product_price_time_end').addClass("d-none");
            }
        }
    });
})

$(document).on('click', '.orderdetail_view', function (e) {
    console.clear();
    e.preventDefault();
    var order_id = $(this).attr("id");
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: "/admin/ajax_get_order/",
        method: "POST",
        data: { order_id: order_id, 'csrfmiddlewaretoken': csrf_token },
        dataType: "json",
        success: function (response) {
            $('#order_detail_id').html(response['order'][0]['order_id']);
            $('#order_detail_time').html(response['order'][0]['order_time']);
            if(response['order'][0]['order_status']=='1'){
                $('#order_detail_status').html('Đã xác nhận');
            }else if(response['order'][0]['order_status']=='2'){
                $('#order_detail_status').html('Đã hủy');
            }else{
                $('#order_detail_status').html('Chưa xác nhận');
            }
            $('#order_detail_account').html(response['order'][0]['user_id']);
            if(response['order'][0]['order_payment']==1){
                $('#order_detail_payment').html("VNPAY");
            }else{
                $('#order_detail_payment').html("COD");
            }
            $('#order_detail_code_payment').html(response['order'][0]['order_code_payment']);
            $('#order_detail_voucher').html(response['order'][0]['order_voucher_code']);
            $('#order_detail_discount').html(response['order'][0]['order_discount']);
            $('#order_detail_totalprice').html(response['order'][0]['order_totalprice']);
            $('#order_detail_totalpayment').html(response['order'][0]['order_totalprice']);
            $('#order_detail_name').html(response['order'][0]['order_name']);
            $('#order_detail_phone').html(response['order'][0]['order_phone']);
            $('#order_detail_address').html(response['order'][0]['order_address']);
            $('#order_detail_email').html(response['order'][0]['order_email']);
            var order_detail = response['order_detail'];
            $('#order_detail_products').html('');
            order_detail.forEach(element => {
                var product = '<tr><td>' + element['product_id'] + '</td><td>' + element['od_nameproduct'] + '</td><td>' + 
                element['od_price'] + '</td><td>' + element['od_pricesale'] + '</td><td>' + element['od_quantity'] + '</td></tr>'
                $('#order_detail_products').append(product);
            })
        }
    });
})

$(document).on('click', '.order_update', function (e) {
    console.clear();
    e.preventDefault();
    var order_id = $(this).attr("id");
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: "/admin/ajax_get_order/",
        method: "POST",
        data: { order_id: order_id, 'csrfmiddlewaretoken': csrf_token },
        dataType: "json",
        success: function (response) {
            $('#order_id_update').val(order_id);
            if(response['order'][0]['order_status'] == $('#order_status_1').val()){
                $('#order_status_1').attr('checked', true);
            }
            if(response['order'][0]['order_status'] == $('#order_status_2').val()){
                $('#order_status_2').attr('checked', true);
            }
            if(response['order'][0]['order_status'] == $('#order_status_3').val()){
                $('#order_status_3').attr('checked', true);
            }
            if(response['order'][0]['order_payment'] == $('#order_payment_1').val()){
                $('#order_payment_1').attr('checked', true);
            }
            if(response['order'][0]['order_payment'] == $('#order_payment_2').val()){
                $('#order_payment_2').attr('checked', true);
            }
        }
    });
})