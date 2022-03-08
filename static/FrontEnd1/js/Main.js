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
    console.log('id-> ',id);
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
          console.log(data);
          if(data.message == "Liked"){
            document.getElementById('like_image_state_change_' + data.id).src=like_red_photo_path;
            console.log(document.getElementById('like_count_index_' + data.id).innerHTML);
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