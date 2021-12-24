/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */
function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $('#imageResult')
        .attr('src', e.target.result);
    };
    reader.readAsDataURL(input.files[0]);
  }
}

$(function () {
  $('#upload').on('change', function () {
    readURL(input);
  });
});

function readURLCover(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $('#imageResultCover')
        .attr('src', e.target.result);
    };
    reader.readAsDataURL(input.files[0]);
  }
}

$(function () {
  $('#uploadCover').on('change', function () {
    readURLCover(input);
  });
});

function readURLSecret(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $('#imageResultSecret')
        .attr('src', e.target.result);
    };
    reader.readAsDataURL(input.files[0]);
  }
}

$(function () {
  $('#uploadSecret').on('change', function () {
    readURLSecret(input);
  });
});

/*  ==========================================
    SHOW UPLOADED IMAGE NAME
* ========================================== */
var input = document.getElementById('upload');
var infoArea = document.getElementById('upload-label');

input.addEventListener('change', showFileName);
function showFileName(event) {
  var input = event.srcElement;
  var fileName = input.files[0].name;
  infoArea.textContent = 'File name: ' + fileName;
}

var inputCover = document.getElementById('uploadCover');
var infoAreaCover = document.getElementById('upload-labelCover');

inputCover.addEventListener('change', showFileNameCover);
function showFileNameCover(event) {
  var input = event.srcElement;
  var fileName = input.files[0].name;
  infoArea.textContent = 'File name: ' + fileName;
}

var inputSecret = document.getElementById('uploadSecret');
var infoAreaSecret = document.getElementById('upload-labelSecret');

inputSecret.addEventListener('change', showFileNameSecret);
function showFileNameSecret(event) {
  var input = event.srcElement;
  var fileName = input.files[0].name;
  infoArea.textContent = 'File name: ' + fileName;
}

function copyClip() {
  var copyText = document.getElementById("exampleFormControlTextarea1");

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  // /* Copy the text inside the text field */
  navigator.clipboard.writeText(copyText.value);
  alert("Copied!")
}