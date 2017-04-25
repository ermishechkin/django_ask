function set_mark(g, val) {
  label = g.find('.badge');
  btn_like = g.find('.btn-like');
  btn_dislike = g.find('.btn-dislike');
  if (val > 0) {
    btn_dislike.attr('set', 0);
    btn_like.attr('set', 1);
  }
  else if (val == 0) {
    btn_dislike.attr('set', 0);
    btn_like.attr('set', 0);
  }
  else {
    btn_dislike.attr('set', 1);
    btn_like.attr('set', 0);
  }
  label.html(total);
}

function send_question_mark(qid, m) {
  $.ajax({
    url: '/my_ask/mark_q',
    datatype: 'json',
    type: 'post',
    data: {
      qid: qid,
      mark: m,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    }
  }).done(function(rsp) {
    status = rsp.status;
    if (status != 'ok')
      return;
    qid = rsp.qid;
    mark = rsp.mark;
    total = rsp.total;
    g = $('.question-mark-group[data-qid='+qid+']');
    set_mark(g, mark);
  });
}

function mark_question() {
  qid = $(this).parents('.question-mark-group').data().qid;
  mark = $(this).data().val;
  send_question_mark(qid, mark);
  return false;
}

$(document).ready(function() {
  $('.btn-question-mark').on('click', mark_question);
})
