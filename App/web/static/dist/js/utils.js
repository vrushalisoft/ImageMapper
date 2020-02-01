var local = 'http://127.0.0.1:5000'
var online = 'https://laptopsoft.herokuapp.com'
var used_host = local
const Toast = Swal.mixin({
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 3000
});

function notifyUser(type, message) {
  Toast.fire({
    type: type,
    title: message
  })
}

function getMapperUrl() {
  return used_host + '/mapper'
}