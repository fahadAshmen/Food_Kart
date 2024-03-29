$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
      // add to cart
        e.preventDefault();

        product_id=$(this).attr('data-id');
        url=$(this).attr('data-url');
        
        $.ajax({
          type: 'GET',
          url: url,          
          success: function(response){
            console.log(response) 
            if(response.status == 'login_required'){
              swal(response.message, '', 'info').then(function(){
                  window.location = '/accounts/signin/';
              })
            }
            else 
            if(response.status == 'Failed'){
                swal(response.message, '', 'error');
            }else{
                $('#cart_counter').html(response.cart_counter['cart_count']);
                $('#qty-'+product_id).html(response.qty);

                apply_cart_amount(
                response.cart_amount['total'],
                response.cart_amount['tax_dict'],
                response.cart_amount['grand_total']
                )
                
              }   
          }
        })
    })
    //place the cart item quantity on load
    $('.item_qty').each(function(){
      var the_id = $(this).attr('id');
      var qty = $(this).attr('data-qty');
      $('#'+the_id).html(qty)
    }) 
   
    //decrease cart

    $('.decrease_cart').on('click', function(e){
      e.preventDefault();

      product_id=$(this).attr('data-id');
      url=$(this).attr('data-url');
      cart_id=$(this).attr('id');
      
   
      $.ajax({
        type: 'GET',
        url: url,               
        success: function(response){
          console.log(response)
          if(response.status == 'login_required'){
            swal(response.message, '', 'info').then(function(){
                window.location = '/accounts/signin/';
            })
          }
          else if(response.status == 'Failed'){
            swal(response.message, '', 'error')
          }
          else{
            $('#cart_counter').html(response.cart_counter['cart_count']);
            $('#qty-'+product_id).html(response.qty);

               // subtotal, tax and grand total
               apply_cart_amount(
                response.cart_amount['total'],
                response.cart_amount['tax_dict'],
                response.cart_amount['grand_total']
              )


            if (window.location.pathname == '/cart_page/')
            {
            removeCartItem(response.qty, cart_id);
            checkEmptyCart();
            }

            }            
        }
      });
  });

  //DELETE CART
  $('.delete_cart').on('click', function(e){
    e.preventDefault();

    cart_id=$(this).attr('data-id');
    url=$(this).attr('data-url');
        
    $.ajax({
      type: 'GET',
      url: url,      
      success: function(response){
        console.log(response)
        if(response.status == 'Failed'){
          swal(response.message, '', 'error')
        }
        else{
          $('#cart_counter').html(response.cart_counter['cart_count']);
          swal(response.status, response.message, "success");
          
           // subtotal, tax and grand total
            apply_cart_amount(
            response.cart_amount['total'],
            response.cart_amount['tax_dict'],
            response.cart_amount['grand_total']
          )

          removeCartItem(0, cart_id);
          checkEmptyCart();
          
        }  
      }
    });
  });

  //DELETE THE CART ELEMENT IF THE QUANTITY IS ZERO
    function removeCartItem(cartItemQty, cart_id){
      if (cartItemQty <=0){
        // remove the cart item element
        document.getElementById("cart-item"+cart_id).remove()
      }
    }
      // check if cart is empty
    function checkEmptyCart(){
    var cart_counter = document.getElementById('cart_counter').innerHTML
      if (cart_counter == 0)
      {
        document.getElementById('empty-cart').style.display = "block";
      }
    
    }

 // FUCTION TO APPLY CART AMOUNT
      function apply_cart_amount(total,tax_dict,grand_total){
        if (window.location.pathname == '/cart_page/') {
         $('#total').html(total);         
         $('#grand-total').html(grand_total);

         for(key1 in tax_dict){
          // console.log(tax_dict[key1])
          for(key2 in tax_dict[key1]){
            // console.log(tax_dict[key1][key2])
            $('#tax-'+key1).html(tax_dict[key1][key2])

          }
         }
         
       }
      }


      //ADD OPENING HOUR
      $('.add_hour').on('click', function(e){
        e.preventDefault();
        var day = document.getElementById('id_day').value
        var from_hour = document.getElementById('id_from_hour').value
        var to_hour = document.getElementById('id_to_hour').value
        var is_closed = document.getElementById('id_is_closed').checked
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        var url = document.getElementById('add_hour_url').value
        

        console.log(day, from_hour, to_hour, is_closed, csrf_token)

        if(is_closed){
          is_closed='True'
          condition = "day!=''"
        }else{
          is_closed='False'         
          condition="day!='' && from_hour!='' && to_hour!=''"
        }
        if(eval(condition)){
          $.ajax({
            type:'POST',
            url:url,
            data: {
              'day': day,
              'from_hour' : from_hour,
              'to_hour' : to_hour,
              'is_closed' : is_closed,
              'csrfmiddlewaretoken' : csrf_token,
            },
            success: function(response){
              if (response.status == 'success'){
                if(response.is_closed == 'Closed'){
                  html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>Closed</td><td><a href="#" class="remove_hour" data-url="/vendor/opening_hour/remove/'+response.id+'/">Remove</a></td></tr>';                
                }else{
                  html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td> '+response.from_hour+' - '+response.to_hour+'</td><td><a href="#" class="remove_hour" data-url="/vendor/opening_hour/remove/'+response.id+'/">Remove</a></td></tr>';
                }

                $('.opening_hours').append(html)
                document.getElementById('opening_hours').reset();                
              }else{
                alert(response.message)
              }

            }

          })
        }else{
          alert('Please fill fields')
        }
      })

      // REMOVE OPENING HOUR
      $(document).on('click', '.remove_hour', function(e){      
        e.preventDefault();
        url=$(this).attr('data-url');
        console.log(url)

        $.ajax({
          type:'GET',
          url:url,
          success:function(response){
            if(response.status == 'success'){
              document.getElementById('hour-'+response.id).remove()
            }
          }
        })
        

      })
      //document close
 });


