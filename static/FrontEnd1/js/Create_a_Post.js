var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
    document.getElementById("nextBtn").style.float = "right";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Post";
    document.getElementById("Footer_Buttons").style.display = "flex";
    document.getElementById("Footer_Buttons").style.justifyContent = "space-between";
    document.getElementById("nextBtn").style.float = "none";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  if( n == (x.length)){
    document.getElementById("nextBtn").onclick = Send();
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
    // document.getElementById("nextBtn").onclick = Send();
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}
function Send(){
  var x = document.getElementById("modal-id").value;
  console.log(x)
  console.log('Sent');
}
function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "") {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false:
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  console.log(x);
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class to the current step:
  x[n].className += " active";
}



let fileInput = document.getElementById("file-input");
let imageContainer = document.getElementById("images-space");
let numOfFiles = document.getElementById("num-of-files");
let images2ndContainer = document.getElementById("images_2nd");

function preview(){
    imageContainer.innerHTML = "";
    images2ndContainer.innerHTML = "";
    numOfFiles.textContent = `${fileInput.files.length} Files Selected`;
    $("#images_2nd_div_heading").html('<p><b>Total ' + `${fileInput.files.length}` + ' Images in this Ad.</b> (Click a Part of Image and insert valid URL/Link)</p>');
    // var count = 1;
    for(i of fileInput.files){
      var html2='';
      console.log(i);
        let reader = new FileReader();
        let figure = document.createElement("figure");
        let figCap = document.createElement("figcaption");
        figCap.innerText = i.name;
        figure.appendChild(figCap);
        // console.log(count);
        reader.onload=()=>{
            let img = document.createElement("img");
            img.setAttribute("src",reader.result);
            // img.setAttribute("id","img"+count++);
            figure.insertBefore(img,figCap);
            // console.log(reader.result);
        }
        // console.log(count);
        imageContainer.appendChild(figure);
        reader.readAsDataURL(i);
        
        //To view Images on next tab
        let reader2 = new FileReader();
        let figure2 = document.createElement("figure");
        let figCap2 = document.createElement("figcaption");
        // console.log(figCap2);
        // figCap_for_identification = figCap2.innerText;
        figCap2.innerText = '';
        figure2.appendChild(figCap2);
        reader2.onload=()=>{
            let img2 = document.createElement("img");
            img2.setAttribute("src",reader2.result);
            img2.setAttribute("data-bs-toggle","modal");
            img2.setAttribute("data-bs-target", '#mymodal');
            img2.setAttribute("title","Add Tag");
            // img2.setAttribute("name","img"+count);
            figure2.insertBefore(img2,figCap2);
        }
        images2ndContainer.appendChild(figure2);
        reader2.readAsDataURL(i);

        //console.log(i);
      //   html2 += '<div class="modal fade" id="mymodal' + count-- +'" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">'+
      //    '<div class="modal-dialog">'+
      //     '<div class="modal-content">' +
      //       '<div class="modal-header">'+
      //         '<h5 class="modal-title" id="exampleModalLabel">Modal title</h5>'+
      //         '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'+
      //       '</div>'+
      //       '<div class="modal-body">'+
      //         '...'+
      //       '</div>'+
      //       '<div class="modal-footer">'+
      //         '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>'+
      //         '<button type="button" class="btn btn-primary">Save changes</button>'+
      //       '</div>'+
      //     '</div>'+
      //   '</div>'+
      // '</div>'
      // $("#modal-box-div").append(html2);
      // count++;
    }
    
}


function show_tags(){
  let tag1name = document.getElementById("Tag1-Name");
  let tag2name = document.getElementById("Tag2-Name");
  let tag3name = document.getElementById("Tag3-Name");
  let tag1URL = document.getElementById("Tag1");
  let tag2URL = document.getElementById("Tag2");
  let tag3URL = document.getElementById("Tag3");
  console.log(tag1name.value);
  console.log(tag2name.value);
  console.log(tag3name.value);
  console.log(tag1URL.value);
  console.log(tag2URL.value);
  console.log(tag3URL.value);

  if(tag1URL.value != '' && tag2URL.value != '' && tag3URL.value != ''){
    var html='';
      html += '<div class="col-md-4" style="margin:auto;">'+
      '<div class="card">'+
      '<div class="card-body">'+
      '<p class="card-title">'+
      '<a href="'+tag1URL.value+'" target="_blank">'+tag1name.value+'</a>'+
      '</p>'+
      '<p class="card-text">'+
      '<a href="'+tag2URL.value+'" target="_blank">'+tag2name.value+'</a>'+
      '</p>'+
      '<p class="card-text">'+
      '<a href="'+tag3URL.value+'" target="_blank">'+tag3name.value+'</a>'+
      '</p>'+
      '</div>'+
      '</div>'+
      '</div>';
      $("#Tags-div").empty();
      $("#Tags-div").append(html);
}
  else if(tag1URL.value != '' && tag2URL.value != ''){
    var html='';
      html += '<div class="col-md-4" style="margin:auto;">'+
      '<div class="card">'+
      '<div class="card-body">'+
      '<p class="card-text">'+
      '<a href="'+tag1URL.value+'" target="_blank">'+tag1name.value+'</a>'+
      '</p>'+
      '<p class="card-text">'+
      '<a href="'+tag2URL.value+'" target="_blank">'+tag2name.value+'</a>'+
      '</p>'+
      '</div>'+
      '</div>'+
      '</div>';
      $("#Tags-div").empty();
      $("#Tags-div").append(html);
  }
  else if(tag1URL.value != ''){
    var html='';
      html += '<div class="col-md-4" style="margin:auto;">'+
      '<div class="card">'+
      '<div class="card-body">'+
      '<h5 class="card-title">'+
      '<a href="'+tag1URL.value+'" target="_blank">'+tag1name.value+'</a>'+
      '</h5>'+
      '</div>'+
      '</div>'+
      '</div>';
      console.log(html);
      $("#Tags-div").empty();
      $("#Tags-div").append(html);
  }


  // console.log(tag1name.value);
  // console.log(tag2name.value);
  // console.log(tag3name.value);
  // console.log(tag1URL.value);
  // console.log(tag2URL.value);
  // console.log(tag3URL.value);

  
}