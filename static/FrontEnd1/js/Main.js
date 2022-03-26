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
    var multiple_elements = document.getElementsByClassName('follow_state_change_'+id);
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
          for(var i=0; i < multiple_elements.length; i++){
            // console.log(multiple_elements[i]);
            multiple_elements[i].innerHTML = data.followstatus;
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

  function showcomments(id){
    $.ajax({
      url: getcomments,
      type: 'GET',
      data: {
        'post_id': id,
      },
      dataType: 'json',
      success: function(data){
        // console.log(data);
        if(data.status == 200){
          console.log(data);
          var div_comments = document.getElementById('comment_model_box_space_'+id)
          console.log('comment_model_box_space_'+id)
          // div_comments.innerHTML = '';
          html = ''
          for(var i=0; i<data.comments.length; i++){
          html += '<div class="comment_box" style="display:flex;">\
          <div style="margin-right:50px;">\
            <img src="'+data.comments[i].people.photo+'" alt="No photo" style="height:60px; width:60px; border-radius:50%;">\
          </div>\
          <div>\
            <div><p style="color:rgb(218, 33, 125); display:inline; font-size:22px;">'+data.comments[i].user.username+'</p><em> Says</em></div>\
            <div style="font-size:25px;">' + data.comments[i].comment+'</div>\
          </div>\
        </div>\
        <hr>'
          } 
          if(data.total_comments > 2){
            html += '<a href="#"> Read all comments</a>'
          }
          div_comments.innerHTML = html; 
        }
      }
    });
  }

  // function submit_comment(post_id){
  //   var comment_div = document.getElementById('comment_model_box_space_'+post_id);
  //   var comment_text = document.getElementById('comment_text_'+post_id).value;
  //   $.ajax({
  //     url: submit_comment,
  //     type: 'POST',
  //     headers: {
  //       "X-CSRFToken": csrfToken
  //     },
  //     data: {
  //       'post_id': post_id,
  //       'comment': comment_text,
  //     },
  //     dataType: 'json',
  //     success: function(data){
  //       console.log(data);
  //     }

  //   });
  // }