$('document').ready(function() {

    $('.comment-box-button-container').hide();


    $('.comment-box').on('click', function() {
        $('.comment-box-button-container').show();
    })


    $('.comment-cancel-button').on('click', function(e) {
        e.preventDefault()
        $('.comment-box-button-container').hide();
    })


    // $(".comment-submit-button").on("click", function(e) {
    //     // e.preventDefault();
     
    //     let comment = $(".comment-box").val();
    //     console.log(comment);
    //     const $newP = $('<p>');
    //     $newP.text($(".comment-box").val());

        
    //     // $(".comment-list").prepend(newComment);
    //     const $newCommentListItem = $('<li>').append($newP)
    //     $(".comment-list").prepend($newCommentListItem);
    //     $(".comment-box").val('');
    //     $('.comment-box-button-container').hide();
    //   });

})