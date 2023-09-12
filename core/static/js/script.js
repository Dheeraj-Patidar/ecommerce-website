
    
    let login=document.getElementById('login');
    function run(){
        if (login.style.display!='block'){
            login.style.display='block';
        }
    }
    function out() {
        if(login.style.display!='none')
        {
            login.style.display='none';
        }
    }

let items_container1=document.getElementById('items-container1');
function run1() {
   if (items_container1.style.display!='block') 
        {
    items_container1.style.display='flex';
   }
}
function out1() {
    if (items_container1.style.display!='none')
    {
        items_container1.style.display='none';
    } 
}

let items_container2=document.getElementById('items-container2');
function run2() {
   if (items_container2.style.display!='block') 
        {
    items_container2.style.display='flex';
   }
}
function out2() {
    if (items_container2.style.display!='none')
    {
        items_container2.style.display='none';
    } 
}

let items_container3=document.getElementById('items-container3');
function run3() {
   if (items_container3.style.display!='block') 
   {
    items_container3.style.display='flex';
   }     
}
function out3() {
    if (items_container3.style.display!='none')
    {
        items_container3.style.display='none';
    } 
}

let items_container4=document.getElementById('items-container4');
function run4() {
   if (items_container4.style.display!='block') 
   {
    items_container4.style.display='flex';
   }     
}
function out4() {
    if (items_container4.style.display!='none')
    {
        items_container4.style.display='none';
    } 
}

let items_container5=document.getElementById('items-container5');
function run5() {
   if (items_container5.style.display!='block') 
   {
    items_container5.style.display='flex';
   }     
}
function out5() {
    if (items_container5.style.display!='none')
    {
        items_container5.style.display='none';
    } 
}





// ADD PRODUCT IN SHOP ....................



$(document).on('submit', '#addproductform', function(e) {
    e.preventDefault();
    $('.error').empty();
    var form = $(this);
    var formData = new FormData(form[0]);

    $.ajax({
        type: 'POST',
        url:'/core/shop/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if(response.errors){

                for (const field in response.errors) {
                    const errors = response.errors[field];
                    const errorMessages = errors.join('<br>'); // Combine error messages with line breaks
                    const errorElement = $('#' + field + '-error'); // Assuming you have elements with IDs ending in '-error'
                    
                    if (errorElement.length > 0) {
                        errorElement.html(errorMessages); // Display the error messages below the field
                    } else {
                        console.error('Error element not found for field:', field);
                    }
                }
            }
            else{
                window.location.href = '/core/shop/';
            }
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
            // Handle other errors here if necessary
        }
    });
});





// ORDERITEM MODAL..................


    $(document).ready(function () {
        $(document).on('click', '.btn-view-order-details', function() {
            var orderID = $(this).data('order-id');
            var modal = $('#ordermodal');
    
            // AJAX call to fetch the order details and populate the modal
            $.ajax({
                url: "/core/orderdetail/0".replace('0', orderID),
                type: 'get',
                success: function (data) {
                    modal.find('.items-modal-body').html(data);
                    modal.modal('show'); // Show the modal after loading the content
                },
                error: function (xhr, status, error) {
                    console.error(error);
                }
            });
        });
    });
    



// UPDATE STATUS MODAL...........................


$(document).ready(function () {
    $(document).on('click', '.btn-update-status', function() {
        var orderID = $(this).val();
       
        $('#updateStatusModal').modal('show');
        
        $('#updateStatusForm').on('submit', function (e){
            e.preventDefault();
            var status=$('#status').val()
        // AJAX call to fetch the order details and populate the modal
        $.ajax({ 
            type: 'post',
            url: "/core/updatestatus/"+orderID+"/",
            data:{
                status:status,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()

            },
            success: function (response) {
                
                    $('#status_').text(status);
                    $('#updateStatusModal').modal('hide');
                    
                    // window.location.href = '/core/customer_order/';

                    window.location.reload();
                

            },
            
        });
    });
});
})


// update shop name...........


$(document).ready(function () {
    $(document).on('click', '.btn-update-shop', function() {
        var shopID = $(this).data('shop-id');
        
        // Store the shop ID as a data attribute on the form
        $('#updateShopForm').attr('data-shop-id', shopID);
        
        $.ajax({
            type: 'GET',
            url: "/core/updateshop/" + shopID + '/',
            success: function (response) {
                if (response.initial_data) {
                    const initialData = response.initial_data;
                    for (const field in initialData) {
                        const fieldValue = initialData[field];
                        $(`[name=${field}]`).val(fieldValue);
                    }
                }
                
                // Open the modal after fetching and setting the initial data
                $('#updateshopmodal').modal('show');
            }
        });
    });

    $('#updateShopForm').on('submit', function (e) {
        e.preventDefault();
        var shopID = $(this).data('shop-id');
        var formData = $(this).serialize();
        $('.error').empty();
        $.ajax({
            type: 'post',
            url: "/core/updateshop/" + shopID + '/',
            data: formData,
            success: function (response) {
                if (response.errors) {
                    for (const field in response.errors) {
                        const errors = response.errors[field];
                        const errorMessages = errors.join('<br>');
                        const errorElement = $('#' + field + '-error');
                        
                        if (errorElement.length > 0) {
                            errorElement.html(errorMessages);
                        } else {
                            console.error('Error element not found for field:', field);
                        }
                    }
                } 
                else {
                    $('#shopname_').text(response.shopname);
                    
                    
                    $('#updateshopmodal').modal('hide');
                    $('#updateShopForm').trigger('reset');
                    window.location.reload();
                }
            }
        });
    });
});







//FILTER PRODUCTS.............................


    $(document).ready(function() {
        // Listen for changes in the checkboxes
        var urlParams = new URLSearchParams(window.location.search);
        var categoryId = urlParams.get('catagories');
        var currentPage = 1; 
       $('input.filter-checkbox').on('change', function() {
            // Get the form data
                
            var formData =$('#filterForm').serialize();
            
            // Update the URL with the form data using history.replaceState (no page reload)
            history.replaceState(null, null, '?catagories'+'='+categoryId+'&' + formData );
    
            // Call the function to update the filtered results
            if (formData || categoryId) {
                updateFilteredResults(1);
            }
        });
        
        // Function to update the filtered results
        function updateFilteredResults(pageNumber) {
             // Send the AJAX request to the Django view
            if ($('input.filter-checkbox:checked').length > 0 ) {
                $.ajax({
                    type: 'GET',
                    url: '/core/filter_product/', // Replace "filtered_products" with your Django view URL
                    data:'catagories='+categoryId+'&'+$('#filterForm').serialize() + '&page=' + pageNumber,
                    
                    success: function(data) {
                        $('#filteredResults').empty();
                        // Update the "filteredResults" container with the filtered data
                        $('#filteredResults').html(data);
                        currentPage = pageNumber

                        // Handle Next and Previous buttons
                        $('#nextPage').on('click', function() {
                            updateFilteredResults(currentPage + 1);
                           
                        });
                        
                         $('.pagenum').on('click', function() {
                            var pagenum = $(this).data('page');
                            if (pagenum) {
                                updateFilteredResults(currentPage=pagenum);
                            }
                        });

                        $('#prevPage').on('click', function() {
                            if (currentPage > 1) {
                                updateFilteredResults(currentPage - 1);
                            }
                        });
                    },
                    error: function() {
                        // Handle errors if necessary
                    }
                });
            } else {
                // If no checkbox is checked, clear the filtered results
                window.location.reload();
            }
        }
        
      
    });


    


// update shop product................



$(document).ready(function () {
    $(document).on('click', '.btn-update-product', function() {
        var productID = $(this).data('product-id');
        
        // Store the product ID as a data attribute on the form
        $('#updateProductForm').attr('data-product-id', productID);
        
        // Fetch existing data for the product using AJAX
        $.ajax({
            type: 'GET',
            url: "/core/updateproduct/" + productID + '/',
            success: function (response) {
                if (response.initial_data) {
                    const initialData = response.initial_data;
                    for (const field in initialData) {
                        const fieldValue = initialData[field];
                        $(`[name=${field}]`).val(fieldValue);
                    }
                }
                
                // Open the modal after fetching and setting the initial data
                $('#updateProductModal').modal('show');
            }
        });
    });

    $('#updateProductForm').on('submit', function (e) {
        e.preventDefault();
        var productID = $(this).data('product-id');
        var formData = $(this).serialize();
        $('.error').empty();
        $.ajax({
            type: 'post',
            url: "/core/updateproduct/" + productID + '/',
            data: formData,
            success: function (response) {
                if (response.errors) {
                    for (const field in response.errors) {
                        const errors = response.errors[field];
                        const errorMessages = errors.join('<br>');
                        const errorElement = $('#' + field + '-error');
                        
                        if (errorElement.length > 0) {
                            errorElement.html(errorMessages);
                        } else {
                            console.error('Error element not found for field:', field);
                        }
                    }
                } 
                else {
                    $('#catagory_').text(response.catagory);
                    $('#name_').text(response.name);
                    $('#desc_').text(response.desc);
                    $('#price_').text(response.price);
                    $('#quantity_').text(response.quantity);
                    $('#brand_').text(response.brand);
                    $('#price_filter_').text(response.price_filter);
                    $('#size_').text(response.size);
                    $('#discount_').text(response.discount);
                    
                    $('#updateProductModal').modal('hide');
                    $('#updateProductForm').trigger('reset');
                    window.location.reload();
                }
            }
        });
    });
});


// Add Coupon .......................



$(document).on('submit', '#addcouponform', function(e) {
    e.preventDefault();
    $('.error').empty();
    var form = $(this);
    var formData = new FormData(form[0]);

    $.ajax({
        type: 'POST',
        url:'/core/coupon/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if(response.errors){

                for (const field in response.errors) {
                    const errors = response.errors[field];
                    const errorMessages = errors.join('<br>'); // Combine error messages with line breaks
                    const errorElement = $('#' + field + '-error'); // Assuming you have elements with IDs ending in '-error'
                    
                    if (errorElement.length > 0) {
                        errorElement.html(errorMessages); // Display the error messages below the field
                    } else {
                        console.error('Error element not found for field:', field);
                    }
                }
            }
            else{
                window.location.href = '/core/coupon/';
            }
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
            // Handle other errors here if necessary
        }
    });
});





// Update Coupon 


$(document).ready(function () {
    $(document).on('click', '.btn-update-coupon', function() {
        var couponid = $(this).data('coupon-id');
        $('#updateCouponForm').attr('data-coupon-id', couponid);
        
        $.ajax({
            type: 'GET',
            url: "/core/updatecoupon/" + couponid + '/',
            
            success: function (response) {
                if (response.initial_data) {
                    const initialData = response.initial_data;
               
                    console.log("Initial Data:", initialData); 
                    for (const field in initialData) {
                        const fieldValue = initialData[field];
                        if (field === 'is_expired') {
                            // Set the value of the checkbox input based on the boolean value
                            $(`[name=${field}]`).prop('checked', fieldValue);
                        } else {
                            // For other fields, set the value as usual
                            $(`[name=${field}]`).val(fieldValue);
                        }
                    }
                   
                }
                   // Open the modal after fetching and setting the initial data
                   $('#updateCouponModal').modal('show');
            }

        });
    });

        $('#updateCouponForm').on('submit', function (e){
            e.preventDefault();
            var couponid = $(this).data('coupon-id');
            var formData = $(this).serialize();
            $('.error').empty();
        $.ajax({
            type: 'post',
            url: "/core/updatecoupon/" + couponid + '/',
            data: formData,
            success: function (response) {
                
                if (response.errors) {
                    for (const field in response.errors) {
                        const errors = response.errors[field];
                        // console.log("field"+field)
                        const errorMessages = errors.join('<br>');
                        const errorElement = $('#' + field + '-error');
                        if (errorElement.length > 0) {
                            errorElement.html(errorMessages);
                        } else {
                            console.error('Error element not found for field:', field);
                        }
                    }
                } 
                else {
                    $('#couponcode_').text(response.coupon_code);
                    $('#discount_amount_').text(response.discount_amount);
                    $('#minimum_amount_').text(response.minimum_amount);
                    $('#is_expired_').text(response.is_expired);
                    $('#updateCouponForm').modal('hide');
                    
                    window.location.reload();
                }
            }
        });
    });
});

