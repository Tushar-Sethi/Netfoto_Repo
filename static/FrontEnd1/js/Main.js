function Hello(){
    console.log('Hello');
html='';
$.ajax({
    url: '/api/view_All_Ads/',
    type: 'GET',
    dataType: 'json',
    success: function(data){
        console.log(data);
        }
    });
}

function LikePost(id){
    html='';
    $.ajax({
      url: likeUrL,
      type: 'POST',
      headers: {
        "X-CSRFToken": csrfToken
      },
      data: {
        'post_id': id,
      },
      dataType: 'json',
      success: function(data){
        if(data.status == 200){
          if(data.message == "Liked"){
            document.getElementById('like_image_state_change_' + data.id).src=like_red_photo_path;
            // console.log(document.getElementById('like_count_index_' + data.id).innerHTML);
            document.getElementById('like_count_index_' + data.id).innerHTML=data.likesCount;
          } 
          else if(data.message == 'Like Removed'){
            document.getElementById('like_image_state_change_' + data.id).src=like_white_photo_path;
            
            console.log(document.getElementById('like_count_index_' + data.id).innerHTML);
            document.getElementById('like_count_index_' + data.id).innerHTML=data.likesCount;
          }
        }
        else{
          console.log('wrong');
        }
      }
    });
  }


  function share(id){
    var URL = encodeURI(window.location.href);
    var completeURL = URL + 'view-post/' + id;
    $('#myInput'+id).attr('placeholder',
                completeURL);
  }

  function shareTwitter(id){
    var URL = encodeURI(window.location.href);
    var tweet = encodeURIComponent($('meta[property="og:title"]').attr('content'));
    var completeURL = 'https://www.twitter.com/intent/tweet?url=' + URL + 'view-post/' + id + '&text=' + tweet;
    window.open(completeURL, '_blank');
  }

  function shareFB(id){
    var URL = encodeURI(window.location.href);
    var completeURL = 'https://www.facebook.com/sharer/sharer.php?u=' + URL + 'view-post/' + id;
    window.open(completeURL, '_blank');

  }
  function shareTele(id){
    var URL = encodeURI(window.location.href);
    var completeURL = 'https://t.me/share/url?url=' + URL + 'view-post/' + id;
    window.open(completeURL, '_blank');

  }
  function shareWA(id){
    var URL = encodeURI(window.location.href);
    var cu = "https://wa.me/?text=" + URL + 'view-post/' + id;
    window.open(cu, '_blank');
  }

  function copyURLFunction(id){
    document.getElementById('messages_modal_box'+id).style.visibility = 'visible';
    var URL = encodeURI(window.location.href);
    var completeURL = URL + 'view-post/' + id;
    navigator.clipboard.writeText(completeURL);
    setTimeout(function () {
      document.getElementById('messages_modal_box'+id).style.visibility = 'hidden';
    }, 2000);
  }

  function HidePost(id){
    console.log(id);
    $.ajax({
      url: hidePost,
      type: 'POST',
      headers: {
        "X-CSRFToken": csrfToken
      },
      data: {
        'post_id': id,
      },
      dataType: 'json',
      success: function(data){
        if(data.status == 200){
          if(data.message == "Hidden"){
            window.location.reload();
          }
        }
      }
      });
  }

  function SavePost(id){
    $.ajax({
      url: savePost,
      type: 'POST',
      headers: {
        "X-CSRFToken": csrfToken
      },
      data: {
        'post_id': id,
      },
      dataType: 'json',
      success: function(data){
        if(data.status == 200){
          if(data.message == "Favourite Removed"){
            document.getElementById('save_image_state_change_' + data.id).src = Notsaved;
            document.getElementById('save_status_' + data.id).innerHTML = data.savestatus;
          }
          else if(data.message == "Favourited"){
            document.getElementById('save_image_state_change_' + data.id).src = saved;
            document.getElementById('save_status_' + data.id).innerHTML = data.savestatus;
          }
          else{
            console.log('Something went wrong');
          }
        }
      }
      });
  }


  function Follow_Unfollow_user(id){
    console.log(id);
    $.ajax({
      url: follow_unfollow_user,
      type: 'POST',
      headers: {
        "X-CSRFToken": csrfToken
      },
      data: {
        'user_id': id,
      },
      dataType: 'json',
      success: function(data){
        if(data.status == 200){
          if(data.message == "Followed"){
            document.getElementById('follow_state_change_' + data.id).innerHTML = 'Unfollow';
            // document.getElementById('follow_status_' + data.id).innerHTML = data.followstatus;
          }
          else if(data.message == "Unfollowed"){
            document.getElementById('follow_state_change_' + data.id).innerHTML = 'Follow';
            // document.getElementById('follow_status_' + data.id).innerHTML = data.followstatus;
          }
          else{
            console.log('Something went wrong');
          }
        }
      }
      });
  }

  function tag_box_show(id){
    document.getElementById('tag_box_'+id).style.visibility = 'visible';
  }

  function hide_tag_box(id){
    document.getElementById('tag_box_'+id).style.visibility = 'hidden';
  }