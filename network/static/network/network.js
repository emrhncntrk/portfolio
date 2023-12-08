
//Editing post
function editPost(post_id){
    
    const content = document.querySelector(`#textarea-${post_id}`).value;
    const post = document.querySelector(`#textarea-${post_id}`).name;
    console.log(`${content}`);
    fetch(`/posts/${post}`, {
        method: "PUT",
        headers: {
            "Content-type": "application/json", 
            "X-CSRFToken": getCsrf()
            },
        body: JSON.stringify({
            content: content
        })
        })
    document.querySelector(`.content-${post_id}`).innerHTML = content;
    document.querySelector('.edit-post').style.display = 'block';
    document.querySelector(`.content-${post_id}`).style.display = 'block';
    document.querySelector(`#edit-window-${post_id}`).style.display = 'none';
}
//Function to get the csrf token value from the cookies
function getCsrf(){
    const value= `; ${document.cookie}`;
    const parts = value.split('; csrftoken=');
    if(parts.length == 2) return parts.pop().split(';').shift();       
}




document.addEventListener("DOMContentLoaded", function() {
    
    //Hide/show new post section
    document.querySelector('#new-post-btn').addEventListener('click', function() {
        document.querySelector('#new-post-div').style.display = 'block';
    });
    document.querySelector('#all-posts-btn').addEventListener('click', function() {
        document.querySelector('#new-post-div').style.display = 'none';
        document.querySelector('#all-posts-div').style.display = 'block';
    });


    //for each element(button) set an event listener that gets the values and triggers editing function
    document.querySelectorAll('.edit-post').forEach(function (element){
        element.addEventListener('click', function() {
            const post_id = element.name;
            console.log("clicked");
            document.querySelector(`.edit-post`).style.display = 'none';
            document.querySelector(`.content-${post_id}`).style.display = 'none';
            document.querySelector(`#edit-window-${post_id}`).style.display = 'block';
            document.querySelector(`#savebtn-${post_id}`).addEventListener('click', function() {
                console.log("click save");
                editPost(post_id);
            });
        });    
    });    
    //Liking. Depending on the value of the element like or un-like the post
    document.querySelectorAll('.likebtn').forEach(function (element){
        element.addEventListener('click', function() {
            const post_id = element.name;
            const action = element.innerHTML;
            var likeCount = document.querySelector(`#likes-${post_id}`).innerHTML;
            var count = Number(likeCount);
            fetch(`/like/${action}/${post_id}`)
            .then(response=> {
                if(response.ok){
                    if(action == "Like"){
                        element.innerHTML = "Un-Like"
                        ++count;
                    }else{
                        element.innerHTML = "Like"
                        --count;
                    }
                    document.querySelector(`#likes-${post_id}`).innerHTML = count;
                }else{
                    throw new Error('Failed to fetch data');
                }
            });
            
            
        });
    });


});