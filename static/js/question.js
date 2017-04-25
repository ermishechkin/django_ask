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

function send_answer_mark(aid, m) {
  $.ajax({
    url: '/my_ask/mark_a',
    datatype: 'json',
    type: 'post',
    data: {
      aid: aid,
      mark: m,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    }
  }).done(function(rsp) {
    status = rsp.status;
    if (status != 'ok')
      return;
    aid = rsp.aid;
    mark = rsp.mark;
    total = rsp.total;
    g = $('.answer-mark-group[data-aid='+aid+']');
    set_mark(g, mark);
  });
}

function mark_answer() {
  aid = $(this).parents('.answer-mark-group').data().aid;
  mark = $(this).data().val;
  send_answer_mark(aid, mark);
  return false;
}

function send_answer() {
  qid = $(this).data().qid; //attr('qid');
  content = $(this).parents('form').find('#content').val();

  $.ajax({
    url: '/my_ask/answer',
    datatype: 'json',
    type: 'POST',
    data: {
      qid: qid,
      content: content,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    }
  });

  $(this).parents('form').find('#content').val('');
  return false;
}

function subscribe_answers() {
  qid = $('.btn-question-mark').parents('.question-mark-group').data('qid');
  $.get("/my_ask/sub?id="+qid, function(data) {
    container = $('.answers_container').append(data);
    container.children('.btn-answer-mark').last().on('click', mark_answer);
    subscribe_answers();
  });
}

$(document).ready(function() {
  $('.btn-question-mark').on('click', mark_question);
  $('.btn-answer-mark').on('click', mark_answer);
  $('#submit-button').on('click', send_answer);
  subscribe_answers();
})
