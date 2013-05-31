$ = django.jQuery;

function update_row(tds, p, a) {
        tds[1].innerHTML = p.length;
        tds[2].innerHTML = p.filter(':checked').length;
        tds[3].innerHTML = a.filter(':checked').length;
}

function update(){
    for (var i=0; i<4; i++){
        tds = $("#summary tr#" + i + " td")
        p = $('.p' + i)
        a = $('.a' + i)
        update_row(tds, p, a)
    }
    tds = $("#summary tr#4 td")
    p = $('#staff td input[name="paron"]')
    a = $('#staff td input[name="apon"]')
    update_row(tds, p, a)

}


$(document).ready(function(){

        update();
        var paron = $('#staff td input[name="paron"]');
        paron.click(function() {
          if ($(this).is(':checked')) {
              $(this).parents('tr').find('input[name="apon"]').hide();
          } else {
              $(this).parents('tr').find('input[name="apon"]').show();
          }
          update()
        });
        var apon = $('#staff td input[name="apon"]');
        apon.click(function() {
          if ($(this).is(':checked')) {
              $(this).parents('tr').find('select').show();
              $(this).parents('tr').find('input[name="paron"]').hide();
          } else {
              $(this).parents('tr').find('select').hide();
              $(this).parents('tr').find('input[name="paron"]').show();
          }
          update()
        });

})


