function nearMatchImgClicked(image_id) {
  $('.person_images, .enrolled_images').removeClass('active_img');
  $('#'+image_id).addClass('active_img');
  console.log('#'+image_id);
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
  var values = getValues()
  postData(values)
}
function getValues(){
  return{
    cid: $('#cid').val(),
    pid: $('#pid').val(),
    prediction_img_path:$('#predict_image').attr('src'),
    enroll_img_path:$('.active_img').attr('src')
  }
}

