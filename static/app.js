$('document').ready(function() {

    $('.comment-box-button-container').hide();


    $('.comment-box').on('click', function() {
        $('.comment-box-button-container').show();
    })


    $('.comment-cancel-button').on('click', function(e) {
        e.preventDefault()
        $('.comment-box-button-container').hide();
    })

    function commentListElementHTML(username, userID, userPicURL, comment) {
        return `
        <li class="list-group-item">
            <a href="/users/${userID}">
                <img src="${userPicURL }" alt="" class="timeline-image">
            </a>
            <div class="message-area">
                <a href="/users/${userID}">@${username}</a>
                <span class="text-muted">Now</span>
                <p>${comment}</p>
            </div>
        </li>
     `;
    }


    $(".comment-submit-button").on("click", async function(e) {
        e.preventDefault();
        
        let username = $(".username").val();
        let userPicURL = $(".user-pic-url").val();
        let userID = $(".user-id").val();
        let content = $(".comment-box").val();
        let listID = $(".movie_list_id").val();
        
        const newCommentResponse = await axios.post('http://127.0.0.1:5000/api/new-comment', {
            userID, listID, content
        });
        
        if (newCommentResponse.data === true) {
            let newComment = commentListElementHTML(username, userID, userPicURL, content);
            $(".comment-list-body").prepend(newComment);
    
            $(".comment-box").val('');
            $('.comment-box-button-container').hide();
        }
    
    });

})