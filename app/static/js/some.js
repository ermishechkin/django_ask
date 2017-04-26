
$(document).ready(function() {
  $('button').on('click', function() {
    console.log('click');
    var $form = $(this).parents('form');
    console.log($form.find('input[name=username]').val());

    $.ajax({
      url: '/login2/',
      datatype: 'json',
      type: 'post',
      data: {
        username: $form.find('input[name=username]').val(),
        password: $form.find('input[name=password]').val(),
        csrfmiddlewaretoken: $form.find('input[name=csrfmiddlewaretoken]').val(),
      }
    }).done(function(rsp) {
      console.log(rsp);
    });
    return false;
  })
})
