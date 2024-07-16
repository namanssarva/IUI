document.getElementById('upload-trigger').addEventListener('click', function() {
    document.getElementById('file-upload').click();
});

document.getElementById('submit-post').addEventListener('click', function() {
    const postText = document.getElementById('create-post-text').value;
    const postImage = document.getElementById('file-upload').files[0];

    if (postText || postImage) {
        const post = document.createElement('div');
        post.className = 'feed';

        const head = document.createElement('div');
        head.className = 'head';

        const userDiv = document.createElement('div');
        userDiv.className = 'user';

        const profilePhoto = document.createElement('div');
        profilePhoto.className = 'profile-photo';

        const userImg = document.createElement('img');
        userImg.src = 'https://www.befunky.com/images/wp/wp-2021-01-linkedin-profile-picture-focus-face.jpg?auto=avif,webp&format=jpg&width=944';
        profilePhoto.appendChild(userImg);

        const infoDiv = document.createElement('div');
        infoDiv.className = 'info';

        const userName = document.createElement('h3');
        userName.textContent = 'Lana Rose';

        const userTitle = document.createElement('small');
        userTitle.textContent = 'Computer Science Student';

        infoDiv.appendChild(userName);
        infoDiv.appendChild(userTitle);

        userDiv.appendChild(profilePhoto);
        userDiv.appendChild(infoDiv);

        head.appendChild(userDiv);
        post.appendChild(head);

        const postDiv = document.createElement('div');
        postDiv.className = 'post';

        if (postText) {
            const textElement = document.createElement('div');
            textElement.className = 'post-text pt-1';
            textElement.textContent = postText;
            postDiv.appendChild(textElement);
        }

        if (postImage) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imgElement = document.createElement('img');
                imgElement.className = 'post-image';
                imgElement.src = e.target.result;
                postDiv.appendChild(imgElement);
            }
            reader.readAsDataURL(postImage);
        }

        // Create post ratings and comments container
        const postRatingsContainer = document.createElement('div');
        postRatingsContainer.className = 'post-ratings-container';

        const likeDiv = document.createElement('div');
        likeDiv.className = 'post-rating';
        likeDiv.innerHTML = `
            <span class="post-rating-button material-icons">thumb_up</span>
            <span class="post-rating-count">0</span>
        `;

        const dislikeDiv = document.createElement('div');
        dislikeDiv.className = 'post-rating';
        dislikeDiv.innerHTML = `
            <span class="post-rating-button material-icons">thumb_down</span>
            <span class="post-rating-count">0</span>
        `;

        const commentDiv = document.createElement('div');
        commentDiv.className = 'comment';
        commentDiv.innerHTML = `
            <span class="post-rating-button material-icons">comment</span>
            <span class="post-rating-count">0</span>
        `;

        postRatingsContainer.appendChild(likeDiv);
        postRatingsContainer.appendChild(dislikeDiv);
        postRatingsContainer.appendChild(commentDiv);

        postDiv.appendChild(postRatingsContainer);
        post.appendChild(postDiv);

        // Add comment card functionality
        const commentCard = document.createElement('div');
        commentCard.className = 'comment-card';
        commentCard.innerHTML = `
            <h2>Leave a Comment</h2>
            <textarea id="comment-text" placeholder="Write your comment..."></textarea>
            <button class="submit-comment">Comment</button>
            <button class="close-comment-card">Close</button>
            <div class="comments-list"></div>
        `;
        postDiv.appendChild(commentCard);

        // Add notification functionality
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = 'Comment Posted';
        postDiv.appendChild(notification);

        document.getElementById('feed').appendChild(post);

        // Clear the form
        document.getElementById('create-post-text').value = '';
        document.getElementById('file-upload').value = '';

        // Add event listeners for like, dislike, and comment buttons
        let liked = false;
        let disliked = false;

        likeDiv.querySelector('.post-rating-button').addEventListener('click', function() {
            const count = likeDiv.querySelector('.post-rating-count');
            if (!liked) {
                count.textContent = parseInt(count.textContent) + 1;
                likeDiv.querySelector('.post-rating-button').classList.add('liked');
                liked = true;

                // Reset dislike button if previously disliked
                if (disliked) {
                    const dislikeCount = dislikeDiv.querySelector('.post-rating-count');
                    dislikeCount.textContent = parseInt(dislikeCount.textContent) - 1;
                    dislikeDiv.querySelector('.post-rating-button').classList.remove('disliked');
                    disliked = false;
                }
            } else {
                count.textContent = parseInt(count.textContent) - 1;
                likeDiv.querySelector('.post-rating-button').classList.remove('liked');
                liked = false;
            }
        });

        dislikeDiv.querySelector('.post-rating-button').addEventListener('click', function() {
            const count = dislikeDiv.querySelector('.post-rating-count');
            if (!disliked) {
                count.textContent = parseInt(count.textContent) + 1;
                dislikeDiv.querySelector('.post-rating-button').classList.add('disliked');
                disliked = true;

                // Reset like button if previously liked
                if (liked) {
                    const likeCount = likeDiv.querySelector('.post-rating-count');
                    likeCount.textContent = parseInt(likeCount.textContent) - 1;
                    likeDiv.querySelector('.post-rating-button').classList.remove('liked');
                    liked = false;
                }
            } else {
                count.textContent = parseInt(count.textContent) - 1;
                dislikeDiv.querySelector('.post-rating-button').classList.remove('disliked');
                disliked = false;
            }
        });

        commentDiv.querySelector('.post-rating-button').addEventListener('click', function() {
            commentCard.style.display = 'block';
        });

        commentCard.querySelector('.submit-comment').addEventListener('click', function() {
            const commentText = commentCard.querySelector('#comment-text').value;
            if (commentText) {
                const comment = document.createElement('div');
                comment.className = 'comment-item';
                comment.innerHTML = `
                    <div class="comment-content">${commentText}</div>
                    <button class="edit-comment">Edit</button>
                    <button class="delete-comment">Delete</button>
                `;
                commentCard.querySelector('.comments-list').appendChild(comment);
                commentCard.querySelector('#comment-text').value = '';
                commentCard.style.display = 'none'; // Automatically close comment card
                notification.style.display = 'block';
                setTimeout(() => {
                    notification.style.display = 'none';
                }, 2000);
                const commentCount = commentDiv.querySelector('.post-rating-count');
                commentCount.textContent = parseInt(commentCount.textContent) + 1;

                // Add event listeners for edit and delete buttons
                comment.querySelector('.edit-comment').addEventListener('click', function() {
                    const commentContent = comment.querySelector('.comment-content');
                    const newText = prompt('Edit your comment:', commentContent.textContent);
                    if (newText !== null) {
                        commentContent.textContent = newText;
                    }
                });

                comment.querySelector('.delete-comment').addEventListener('click', function() {
                    comment.remove();
                    commentCount.textContent = parseInt(commentCount.textContent) - 1;
                });
            }
        });

        commentCard.querySelector('.close-comment-card').addEventListener('click', function() {
            commentCard.style.display = 'none';
        });
    } else {
        alert('Please write something or upload an image.');
    }
});
