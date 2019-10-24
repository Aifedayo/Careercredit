
        var modal = $('#modal');


        $(document).ready(function(){
            $('#close-button,#close').click(function(){
                closeModal()
            });
            function closeModal(){
                modal.removeClass('is-active')
            }
            function openModal(){
                modal.addClass('is-active')
            }

/** code by webdevtrick ( https://webdevtrick.com ) **/
$('#rating-form').on('change','[name="rating"]',function(){
    var value = $('[name="rating"]:checked').val()
    console.log(
        	value
    )
});


        });

