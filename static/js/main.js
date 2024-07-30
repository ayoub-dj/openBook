if (location.href === 'http://127.0.0.1:8000/login/') {
    const passwordVisibility = document.querySelector('.login .col:last-child .field span');
    const passwordInput = document.querySelector('.login .col:last-child input[type="password"]')

    passwordVisibility.onclick = () => {
        if (passwordVisibility.innerText === 'visibility_off') {
            passwordVisibility.innerText = 'visibility';
            passwordInput.type = 'text';
    
        } else {
            passwordVisibility.innerText = 'visibility_off';
            passwordInput.type = 'password';
        }
    };
}

if (location.href === 'http://127.0.0.1:8000/register/') {
    const passwordsInput = Array.from(document.querySelectorAll('.register .col:last-child input[type="password"]'));
    // const passwordVisibility = document.querySelector('.register .col:last-child .field span');

    passwordsInput.forEach((elem) => {
        elem.parentElement.classList.add('field');
        const showHidePasswordSpan = document.createElement('span')
        showHidePasswordSpan.className = 'material-symbols-outlined'
        showHidePasswordSpan.innerText = 'visibility_off'
        elem.parentElement.prepend(showHidePasswordSpan)

        showHidePasswordSpan.onclick = () => {
            if (showHidePasswordSpan.innerText === 'visibility_off') {
                showHidePasswordSpan.innerText = 'visibility';
                elem.type = 'text';
            }
            else {
                showHidePasswordSpan.innerText = 'visibility_off';
                elem.type = 'password';
            }
        }
    

        
    });

}


if (location.href === 'http://127.0.0.1:8000/') {
    const searchIconMiniScreen = document.querySelector('nav .container .left #search-icon');
    const closeSearchButton = document.querySelector('nav .container .left #close-search');

    searchIconMiniScreen.onclick = () => {
        closeSearchButton.classList.add('show')
        searchIconMiniScreen.style.display = 'none !important';
        document.querySelector('nav .container .left form').style.display = 'flex';
    };
    
    closeSearchButton.onclick = () => {
        closeSearchButton.classList.remove('show')
        closeSearchButton.classList.add('none')
    
        closeSearchButton.style.display = 'none !important';
        searchIconMiniScreen.style.display = 'flex';
        document.querySelector('nav .container .left form').style.display = 'none';
    };
}

function loadMessages() {
    document.addEventListener('DOMContentLoaded', function() {
        const messages = document.querySelectorAll('.messages li');
        
        messages.forEach(function(message) {
            // Set a timeout to add the fade-out class after 5 seconds
            setTimeout(function() {
                message.classList.add('fade-out');
            }, 4000);
        });
    });
};

loadMessages();


const dropDown = document.querySelector('nav .container .right .profile-icon .dropdown');
const dropDownButton = document.querySelector('.container .right button');
const closePostButtonFirstChild = document.querySelector('main .posts .dropdown .col:first-child .title .close');
const closePostButtonLastChild = document.querySelector('main .posts .dropdown .col:last-child .title .close');
const closePostButtonChildTwo = document.querySelector('main .posts .dropdown .col:nth-child(2) .title .close');
const openCreatePostDropDown = document.querySelector('main .posts .open-create-post');
const openCreatePostDropDownTwo = document.querySelector('main .create-post #new-post');
const addLocationButton = document.querySelector('main .posts .dropdown .create-post-form .create-post-form-icons .icons div span#location');
const dropDownColLastChild = document.querySelector('main .posts .dropdown .col:last-child')
const dropDownColChildTwo = document.querySelector('main .posts .dropdown .col:nth-child(2)')
const dropDownColFirstChild = document.querySelector('main .posts .dropdown .col:first-child')
const addFeelingButton = document.querySelector('main .posts .dropdown .create-post-form .create-post-form-icons .icons div span#sentiment_satisfied')


dropDownButton.onclick = () => {
    dropDown.classList.toggle('show');
};

if (location.href === 'http://127.0.0.1:8000/') {
    openCreatePostDropDownTwo.onclick = () => {
        document.querySelector('main .posts .dropdown').classList.toggle('flex')
        if (dropDownColLastChild.classList.contains('show-col')) {
            dropDownColLastChild.classList.remove('show-col')
        }
    };


    openCreatePostDropDown.onclick = () => {
        Array.from(document.querySelectorAll('main .edit-dropdown')).forEach((elem) => {
            if (!elem.classList.contains('hide-to-middle')) {
                elem.classList.add('hide-to-middle')
            }
        });
        document.querySelector('main .posts .dropdown').classList.toggle('flex')
        if (dropDownColLastChild.classList.contains('show-col')) {
            dropDownColLastChild.classList.remove('show-col')
        }
        if (dropDownColChildTwo.classList.contains('show-col')) {
            dropDownColChildTwo.classList.toggle('show-col');
        }
    };
    

    closePostButtonFirstChild.onclick = () => {
        document.querySelector('main .posts .dropdown').classList.toggle('flex')
    };


    addLocationButton.addEventListener("click", () => {
        dropDownColLastChild.classList.toggle('show-col');
    });

    addFeelingButton.addEventListener("click", () => {
        dropDownColChildTwo.classList.toggle('show-col');
    });

    closePostButtonLastChild.onclick = () => {
        dropDownColLastChild.classList.toggle('show-col');
    };

    closePostButtonChildTwo.onclick = () => {
        dropDownColChildTwo.classList.toggle('show-col');
    };

    const locationsLisText = Array.from(document.querySelectorAll('main .posts .dropdown .col:last-child .locations li.location'))
    const feelingsLisText = Array.from(document.querySelectorAll('main .posts .dropdown .col:nth-child(2) .feelings li.feeling'))

    const locationsLis = (lis, name) => {
        lis.forEach(elem => {
            elem.addEventListener("click", (e) => {
                const event = e.target;
                const chosenLocationText = event.querySelector('span:last-child').innerText;
                const chosenLocationElem = document.querySelector('main .posts .dropdown .profile .name .chosen-location');
                chosenLocationText.innerText = '';
                chosenLocationElem.append(chosenLocationText)

                const locationInput = document.querySelector('main .posts .dropdown .create-post-form input[type="hidden"]')
                locationInput.value = chosenLocationText

                if (dropDownColLastChild.classList.contains('show-col')) {
                    dropDownColLastChild.classList.remove('show-col')
                };
        
                if (dropDownColChildTwo.classList.contains('show-col')) {
                    dropDownColChildTwo.classList.remove('show-col')
                };
            })
        });

    }

    locationsLis(locationsLisText)


    const addPhotoIconButton = document.querySelector('main .posts .dropdown .create-post-form .create-post-form-icons .icons span#add_photo');
    const fileInput = document.querySelector('main .posts .dropdown .create-post-form .create-post-form-icons div input[type="file"]')


    addPhotoIconButton.onclick = () => {
        fileInput.click();
    };

    const uploadedMessageForImage = (elem, name) => {
        // messagesText = document.querySelector('main .posts .dropdown').classList.add('flex');

        const messagesText = document.createTextNode('the image was uploaded successfully, Now compose a post');
        fileInput.onchange = () => {
            const messagesUl = document.createElement('ul');
            const messagesLi = document.createElement('li');
        
            messagesUl.className = 'messages';
            messagesLi.className = 'success';
        
            messagesLi.append(messagesText);
            messagesUl.append(messagesLi);
            document.body.prepend(messagesUl);
        
            const messages = document.querySelectorAll('.messages li');
            
            messages.forEach(function(message) {
                setTimeout(function() {
                    message.classList.add('fade-out');
                }, 4000);
            });
        };
    };


    uploadedMessageForImage(fileInput, 'dropdown')


    const showEditAndDeletePost = (moreButton) => {
        moreButton.forEach((moreBtn) => {
            moreBtn.addEventListener("click", (e) => {
                Array.from(document.querySelectorAll('.delete-dropdown')).forEach((deleteDropdown) => {
                });
                e.target.parentElement.querySelector('.post-settings').classList.toggle('none');
            });
        });
    }

    showEditAndDeletePost(Array.from(document.querySelectorAll('#more-button')));

    const deletePostButton = (deleteButton) => {
        deleteButton.forEach((deleteBtn) => {
            deleteBtn.addEventListener("click", (e) => {
                e.target.parentNode.parentElement.parentNode.classList.add('none');
                e.target.parentNode.parentElement.parentElement.parentElement.querySelector('.delete-dropdown').classList.toggle('hide-to-top');
            });
        });
    }

    deletePostButton(Array.from(document.querySelectorAll('main .posts .posts-list .post-list .col .field .post-settings button.delete-post-btn')))


    const editPostView = (editButtons) => {
        editButtons.forEach((editBtns) =>  {
            editBtns.addEventListener("click", (e) => { 
                e.target.parentElement.parentElement.parentElement.parentElement.querySelector('main .edit-dropdown').classList.toggle('hide-to-middle');
            });
        });
    };

    editPostView(document.querySelectorAll('main .posts .posts-list .post-list .col .field .post-settings button.edit-post-btn'));


    const editPhotoButtonView = (editPhotoButtons) => {
        editPhotoButtons.forEach((editPhotoBtns) =>  {
            editPhotoBtns.addEventListener("click", (e) => { 
                e.target.parentElement.querySelector("input[type='file']").click();

                e.target.parentElement.querySelector("input[type='file']").onchange = () => {
                    const messagesUl = document.createElement('ul');
                    const messagesLi = document.createElement('li');
                    const messagesText = document.createTextNode('the image was uploaded successfully, Now update your post');

                
                    messagesUl.className = 'messages';
                    messagesLi.className = 'success';
                
                    messagesLi.append(messagesText);
                    messagesUl.append(messagesLi);
                    document.body.prepend(messagesUl);
                
                    const messages = document.querySelectorAll('.messages li');
                    
                    messages.forEach(function(message) {
                        setTimeout(function() {
                            message.classList.add('fade-out');
                        }, 4000);
                    });
                };
            });
        });
    };
    editPhotoButtonView(Array.from(document.querySelectorAll('.edit-dropdown #add_photo')));
}  



const createCommentDropdown = Array.from(document.querySelectorAll('main .posts .posts-list .create-comment-drop-down'));
const createCommentView = (createCommentButtons) => {
    createCommentButtons.forEach((btns) => {
        btns.addEventListener("click", (e) => {
            createCommentDropdown.forEach((elem) => {
                if (!elem.classList.contains('none')) {
                    elem.classList.add('none');
                }
            });
            e.target.parentElement.parentElement.querySelector('.create-comment-drop-down').classList.toggle('none');
        })
    })
}

createCommentView(Array.from(document.querySelectorAll('main .posts .posts-list .likes #create-comment-btn')));

const postsList = document.querySelector('.profile-container .box .posts-list')
const sharedPosts = document.querySelector('.profile-container .box #shared_posts')
const followers = document.querySelector('.profile-container .box #followers')
const following = document.querySelector('.profile-container .box #following')

let profileList = [postsList, sharedPosts, followers, following]

const profileWorker = () => {
    const navigatorLinks = Array.from(document.querySelectorAll('.profile-container .box .navigator li a'));
    navigatorLinks.forEach((li) => {
        li.addEventListener("click", (e) => {
            navigatorLinks.forEach((one) => {
                one.classList.remove('active')
            })
            e.target.classList.add('active')
            profileList.forEach((element) => {
                if (!element.classList.contains('none')) {
                    element.classList.add('none')
                }
            })

            if (e.target.innerText.toLowerCase() === 'followers') {
                followers.classList.remove('none')

            } else if (e.target.innerText.toLowerCase() === 'following') {
                following.classList.remove('none')

            } else if (e.target.innerText.toLowerCase() === 'posts') {
                postsList.classList.remove('none')

            } else if (e.target.innerText.toLowerCase() === 'shared posts') {
                sharedPosts.classList.remove('none')

            }
            
        });


    })
};

profileWorker()


