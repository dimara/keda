$ = django.jQuery;

$(document).ready(function(){

  col = $('.nested-inline-row td').parent().prev().children().length;
  $('.nested-inline-row td').first().attr("colspan", col);

})
