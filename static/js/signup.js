
function cmp_passwords() {
  if ($('#password_again')[0].value == '') {
    $('#password_mismatch')[0].style['display'] = 'none';
    return;
  }
  $('#password_mismatch')[0].style['display'] = '';

  if ($('#password_id')[0].value != $('#password_again')[0].value) {
    // $('#password_mismatch')[0].style['display'] = '';
    $('#password_mismatch').toggleClass('text-danger', true);
    $('#password_mismatch').toggleClass('text-success', false);
    $('#password_mismatch').text('Пароли не совпадают');
  }
  else {
    // $('#password_mismatch')[0].style['display'] = 'none';
    $('#password_mismatch').toggleClass('text-danger', false);
    $('#password_mismatch').toggleClass('text-success', true);
    $('#password_mismatch').text('Пароли совпадают');
  }
}

$(document).ready(function() {
  $('#password_id').on('input', cmp_passwords);
  $('#password_again').on('input', cmp_passwords);
});
