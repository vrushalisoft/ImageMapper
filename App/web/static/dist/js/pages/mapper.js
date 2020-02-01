var nmatch_data = []
var predicted_data = []

var current_page = 1
var current_data = {}

function nearMatchImgClicked(image_id) {
  $('.person_images, .enrolled_images').removeClass('active_img');
  $('#'+image_id).addClass('active_img');
  console.log('#'+image_id);
}

function nMapClick() {
  var img_path = $('#predictimage').attr('src')
  $('#nMatchContainer').html('')
  $.each(nmatch_data, function (indx, row) {
    console.log("nMap get clicked");
    console.log(img_path, row[1]);
    console.log(row[1]==img_path);
    if (row[1]==img_path) {
      var html = `
      <div class="col-sm-2" style="text-align: center;">
        <a href="#" onclick="nearMatchImgClicked('near_${indx}')">
        <img class="img-fluid person_images"  src="${row[2]}" alt="Photo" id='near_${indx}' >
        </a>
        <label style="display: flow-root;" for="near_${indx}" >
        ${row[2].split('/')[(row[2].split('/').length)-2]}
        </label>
      </div>
      `
      $('#nMatchContainer').append(html)
    } 
  
    
  })
  

}

function postData(data) {
  $.ajax({
    cache: false,
    type: 'POST',
    url: getMapperUrl(),
    dataType: 'json',
    data: data,
    xhrFields: {
        // The 'xhrFields' property sets additional fields on the XMLHttpRequest.
        // This can be used to set the 'withCredentials' property.
        // Set the value to 'true' if you'd like to pass cookies to the server.
        // If this is enabled, your server must respond with the header
        // 'Access-Control-Allow-Credentials: true'.
        withCredentials: false
    },
    success: function (json) {
        if (!json.status) {
          notifyUser('error', 'Server Error in Mapping')
          console.log('Serverside Error');
          console.log(json.msg)
        }
        else {
          notifyUser('success', json.msg)
        }
    },
    error: function (data) {
      notifyUser('error', 'Error Saving Mapping')
        console.log("Error Saving Mapping");
        console.log(data);
    }
  });
}
  
function Mapper(){
  var values = getValues(false, false, false)
  postData(values)
}
function MapperSkip(){
  var values = getValues(true, false, true)
  postData(values)
}
function MapperNotEnrolled(){
  var values = getValues(false, true, true)
  postData(values)
}
function getValues(isSkip, isNotEnrolled, isEnrollPathBlank){
  return{
    cid: $('#cid').val(),
    pid: $('#pid').val(),
    prediction_img_path:$('#predictimage').attr('src'),
    enroll_img_path:isEnrollPathBlank?'':$('.active_img').attr('src'),
    isSkipped: isSkip,
    isNotEnrolled:isNotEnrolled
  }
}

function  getNmapDataUrl() {
  return used_host + '/nmap'
}

function getnmapdata(){
  $.ajax({
    cache: false,
    type: 'GET',
    url: getNmapDataUrl(),
    xhrFields: {
        // The 'xhrFields' property sets additional fields on the XMLHttpRequest.
        // This can be used to set the 'withCredentials' property.
        // Set the value to 'true' if you'd like to pass cookies to the server.
        // If this is enabled, your server must respond with the header
        // 'Access-Control-Allow-Credentials: true'.
        withCredentials: false
    },
    success: function (json) {
        if (!json.status) {
          console.error('Serverside Error While Geting Nmatched Data');
          console.error(json.message)
        }
        else {
          nmatch_data = json.data
          console.log(nmatch_data)
        }
    },
    error: function (data) {
        console.log("Error While Getting Nmatched Data");
        console.log(data);
    }
  });
}

function  getPredictDataUrl() {
  return used_host  + '/api'+'/person'+'/'+$('#cid').val() +'/'+ $('#pid').val()
}

function getPredictData(){
  $.ajax({
    cache: false,
    type: 'GET',
    url: getPredictDataUrl(),
    xhrFields: {
        // The 'xhrFields' property sets additional fields on the XMLHttpRequest.
        // This can be used to set the 'withCredentials' property.
        // Set the value to 'true' if you'd like to pass cookies to the server.
        // If this is enabled, your server must respond with the header
        // 'Access-Control-Allow-Credentials: true'.
        withCredentials: false
    },
    success: function (json) {
        if (!json.status) {
          console.error('Serverside Error While Geting Predict Data');
          console.error(json.message)
        }
        else {
          predicted_data = json.data
          console.log(predicted_data)
          initPrediction()
          if(current_page >= predicted_data.length) {$('#previousButton').show();  $('#nextButton').hide()}
          if(current_page <= 1) {$('#previousButton').hide(); $('#nextButton').show()}
          else { $('#previousButton').show(); $('#nextButton').show() }
        }
    },
    error: function (data) {
        console.log("Error While Getting predict Data");
        console.log(data);
    }
  });
}

function initPrediction() {
  current_page = 1
  current_data = predicted_data[current_page-1]
  $('#previousButton').hide()
  renderPredictionImage()
}

function renderPredictionImage() {
  $('#predictimage').attr('src', current_data[3])
  var image_parts = current_data[3]?current_data[3].split('/'):[]
  var name = image_parts.length>0?image_parts[image_parts.length-1]:''
  $('#predictlabel').html(name)
  nMapClick()
}

function predictionImageNextClicked() {
  if(current_page == predicted_data.length) {
    notifyUser('error', 'Already Showing Last Entry!')
  } else {
    current_page++;
    
    $('#previousButton').show()
    if(current_page == predicted_data.length) $('#nextButton').hide()
    else $('#nextButton').show()
    current_data = predicted_data[current_page-1]
    renderPredictionImage()
  }
}
function predictionImagePreviousClicked() {
  if(current_page == 1) {
    notifyUser('error', 'Already Showing First Entry!')
  } else {
    current_page--;
    $('#nextButton').show()
    if(current_page == 1) $('#previousButton').hide()
    else $('#previousButton').show()
    current_data = predicted_data[current_page-1]
    renderPredictionImage()
  }
  
}

getPredictData()
getnmapdata()