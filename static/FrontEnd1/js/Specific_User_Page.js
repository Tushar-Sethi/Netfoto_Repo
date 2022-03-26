var tabs = document.querySelectorAll("[data-tab-target]");
var tabContents = document.querySelectorAll("[data-tab-content]");
tabs.forEach(tab => {
    tab.addEventListener("click", function() {
        const target = document.querySelector(this.dataset.tabTarget);
        tabContents.forEach(tabContent => {
            tabContent.classList.remove("active");
        });
        tabs.forEach(tab => {
            tab.classList.remove("active");
        });
        target.classList.add("active");
        tab.classList.add("active");
    });
});


function copy_profile_link(id){
    var URL = encodeURI(window.location.href);
    navigator.clipboard.writeText(URL);
    document.getElementById('copy_link_profile').style.visibility = 'visible';
    setTimeout(function () {
        document.getElementById('copy_link_profile').style.visibility = 'hidden';
      }, 2000);

}

function Follow_Unfollow(id){
    console .log('Unfollow',id);
    element = document.getElementsByClassName("user_my_account");
    console.log(element);
    $.ajax({
        url: follow_unfollow_user,
        type: 'POST',
        headers: {
            "X-CSRFToken": csrfToken
          },
        data: {
            'user_id': id
        },
        dataType: 'json',
        success: function(data){
            if(data.status == 200){
                element[0].innerHTML = data.followstatus;
            }
        }
    });
}