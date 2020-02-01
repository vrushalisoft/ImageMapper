var enrolled_data = []
var paged_enrolled_data = []
var predicted_data = []
var enroll_per_page = 50

var image_list_data = []
var default_campaign = {
  list_image: "",
  enroll_image: "",
}
var enrol_pager = {};

var current_working_set = ''
$('#previousEnrollButton').hide()
$('#nextEnrollButton').hide()

var predictionContainer = "#prediction_container"
var listConatainer = "#list_container"
var enrollContainer = "#enroll_container"

function getEnrolledDataUrl() {
  return used_host + '/enroll_data'
}

function getEnrolledData(querry) {
  $.ajax({
    cache: false,
    type: 'GET',
    url: getEnrolledDataUrl(),
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
          console.error('Serverside Error While Geting Enrolled Data');
          console.error(json.message)
        }
        else {
          enrolled_data = json.details
          setPage(enrol_pager.currentPage);
          if(enrol_pager.currentPage >= enrol_pager.totalPages) {
            $('#nextEnrollButton').hide()
          } else {
            $('#nextEnrollButton').show()
          }

        }
    },
    error: function (data) {
        console.log("Error While Getting Enrolled Data");
        console.log(data);
    }
  });
}

function initEnrolled(edata) {
  var images = []
  $.each(edata, function (indx, data) {
    var enrol_dom = '<div class="col-sm-2">'
    enrol_dom+='<img class="img-fluid enroll_image" class="enroll_image" src="'+data+'" alt="Photo" id="enrol_'+indx+'" onClick="enrollImageClicked(\''+data+'\','+indx+')">'
    var name = data.split('/')[3]
    enrol_dom+='<label for="enrol_'+indx+'">'+name+'</label>'
    enrol_dom+='</div>'
    images.push(enrol_dom) 
  })
  $(enrollContainer).html(images)
}
function getPredictionDataUrl() {
  return used_host + '/prediction_data'
}
function getMappingUrl() {
  return used_host + '/mapper'
}

function getPredictionData(querry) {
  $.ajax({
    cache: false,
    type: 'GET',
    url: getPredictionDataUrl(),
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
          console.error('Serverside Error While Geting Prediction Data');
          console.error(json.message)
        }
        else {
          predicted_data = json.details
          initPrediction(predicted_data[current_page-1])
          if(current_page >= predicted_data.length) {$('#previousButton').show();  $('#nextButton').hide()}
          if(current_page <= 1) {$('#previousButton').hide(); $('#nextButton').show()}
          else { $('#previousButton').show(); $('#nextButton').show() }
        }
    },
    error: function (data) {
        console.log("Error While Getting Prediction Data");
        console.log(data);
    }
  });
}

function postMapingData(data) {
  $.ajax({
    cache: false,
    type: 'POST',
    url: getMappingUrl(),
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
          notifyUser('danger', 'Server Error Mapping Image')
          console.error('Serverside Error While Posting Image Map');
          console.error(json.message)
        }
        else {
          notifyUser('success', 'Map Saved Successfully')
          getPredictionData()
          // predicted_data = json.details
          // initPrediction(predicted_data[0])
        }
    },
    error: function (data) {
        console.log("Error While Posting Image Map");
        console.log(data);
    }
  });
}

function initPrediction(pdata) {
  var prediction_list_dom = []
  var prediction_image_dom = '<a href="'+pdata.image_path+'" data-toggle="lightbox" data-title="Image Used for Prediction" data-gallery="gallery">'
  prediction_image_dom += '<img class="img-fluid" src="'+pdata.image_path+'" alt="Photo"></img>'
  prediction_image_dom += '<a/>'
  $(predictionContainer).html(prediction_image_dom)
  
  $.each(pdata.recognised_images, function (indx,image_data) {
    var predict_dom = '<div class="col-md-12">'
    predict_dom+='<img class="img-fluid enroll_image" class="enroll_image" src="'+image_data.recognised_image+'" alt="Photo" id="list_'+indx+'" onClick="imageListClicked(\''+image_data.mapped_image+'\','+indx+')">'
    var name = image_data.recognised_image.split('/')[3]
    predict_dom+='<label for="list_'+indx+'">'+name+'</label>'
    predict_dom+='</div>'
    var done = image_data.mapped_image!='TBD'?'done':''
    prediction_list_dom.push(predict_dom)
  })
  $(listConatainer).html(prediction_list_dom)
}
function enrollImageClicked(data, indx) {
  // $(enrollContainer+'>div>img').removeClass('active')
  // $('#enrol_'+indx).hasClass('active')?$('#enrol_'+indx).removeClass('active'):$('#enrol_'+indx).addClass('active')
}
function imageListClicked(data, indx) {
  // $(listConatainer+'>img').removeClass('active')
  // $('#list_'+indx).hasClass('active')?$('#list_'+indx).removeClass('active'):$('#list_'+indx).addClass('active')
  // $(enrollContainer+'>div>img').removeClass('active')
  // if($(enrollContainer+'>div>img[src$="'+data+'"]').length>0) {
  //   $(enrollContainer+'>div>img[src$="'+data+'"]').addClass('active')
  //   $('html, body').animate({
  //       scrollTop: $(enrollContainer+'>div>img[src$="'+data+'"]').offset().top
  //   }, 100);
  // }
 
}
function mapImageClicked() {
  var enroll_image = ''
  var list_image = ''
  if($(enrollContainer+'>div>img.active').length==1){
    enroll_image = $(enrollContainer+'>div>img.active').attr('src')
  }
  if($(listConatainer+'>img.active').length==1){
    list_image = $(listConatainer+'>img.active').attr('src')
  }
  if(!list_image) {
    notifyUser('error','Please Select Predicted Image!')
  }
  else if(!enroll_image) {
    notifyUser('error','Please Select Enrolled Image!')
  } else {
    var data = {
      image_path: $(predictionContainer+'>a>img').attr('src'),
      recognised_image: list_image.toString(),
      mapped_image: enroll_image.toString()
    }
    postMapingData(data)
  }
}
var current_page = 1;
function predictionImageNextClicked() {
  if(current_page == predicted_data.length) {
    notifyUser('error', 'Already Showing Last Entry!')
  } else {
    current_page++;
    $('#previousButton').show()
    if(current_page == predicted_data.length) $('#nextButton').hide()
    else $('#nextButton').show()
    initPrediction(predicted_data[current_page-1])
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
    initPrediction(predicted_data[current_page-1])
  }
  
}

function enrollImageNextClicked() {
  var page_to_set = enrol_pager.currentPage + 1
  setPage(page_to_set)
  if(page_to_set >= enrol_pager.totalPages) {
    $('#nextEnrollButton').hide()
  } else if(page_to_set >= 2) {
    $('#previousEnrollButton').show()
  }
}
function enrollImagePreviousClicked() {
  var page_to_set = enrol_pager.currentPage - 1
  setPage(page_to_set)
  if(page_to_set < 2) {
    $('#previousEnrollButton').hide()
  } else if(page_to_set < enrol_pager.totalPages) { 
    $('#nextEnrollButton').show()
  }
}

function setPage(page, reset = false) {
  if (page < 1 || page > this.enrol_pager.totalPages && !reset) {
    console.log('Returning');
    return;
  }
  // get pager object from service
  enrol_pager = getPager(enrolled_data.length, page, enroll_per_page);

  // get current page of items
  paged_enrolled_data = enrolled_data.slice(enrol_pager.startIndex, enrol_pager.endIndex + 1);
  initEnrolled(paged_enrolled_data)
  $('#showing_enrolled').html(`<b>Total Images: ${enrolled_data.length}<b/>`)
  $('#perpage_enrolled').html(`<b>Images Per Page: ${enroll_per_page}<b/> |`)
}

function refresh() {
  getPredictionData()
  current_page = 1;
}
function refreshEnrolled() {
  getEnrolledData()
}

refresh()

function getPager(totalItems, currentPage = 1, pageSize = 3) {
  // calculate total pages
  var totalPages = Math.ceil(totalItems / pageSize);

  // ensure current page isn't out of range
  if (currentPage < 1) {
      currentPage = 1;
  } else if (currentPage > totalPages) {
      currentPage = totalPages;
  }

  var startPage, endPage;
  if (totalPages <= 10) {
      // less than 10 total pages so show all
      startPage = 1;
      endPage = totalPages;
  } else {
      // more than 10 total pages so calculate start and end pages
      if (currentPage <= 6) {
          startPage = 1;
          endPage = 10;
      } else if (currentPage + 4 >= totalPages) {
          startPage = totalPages - 9;
          endPage = totalPages;
      } else {
          startPage = currentPage - 5;
          endPage = currentPage + 4;
      }
  }

  // calculate start and end item indexes
  var startIndex = (currentPage - 1) * pageSize;
  var endIndex = Math.min(startIndex + pageSize - 1, totalItems - 1);

  // create an array of pages to ng-repeat in the pager control
  var pages = Array.from(Array((endPage + 1) - startPage).keys()).map(i => startPage + i);

  // return object with all pager properties required by the view
  return {
      totalItems: totalItems,
      currentPage: currentPage,
      pageSize: pageSize,
      totalPages: totalPages,
      startPage: startPage,
      endPage: endPage,
      startIndex: startIndex,
      endIndex: endIndex,
      pages: pages
  };
}
