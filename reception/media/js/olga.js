$ = django.jQuery;

function update(){
    var c = $('#staff td input').length;
    var p = $('#staff td input:checked').length;
    var a = c-p;
    var c1 = $('#staff td input#id_paron_1').length;
    var c2 = $('#staff td input#id_paron_2').length;
    var c3 = $('#staff td input#id_paron_3').length;
    var c4 = $('#staff td input#id_paron_4').length;
    var p1 = $('#staff td input#id_paron_1:checked').length;
    var p2 = $('#staff td input#id_paron_2:checked').length;
    var p3 = $('#staff td input#id_paron_3:checked').length;
    var p4 = $('#staff td input#id_paron_4:checked').length;
    var a1 = c1 - p1;
    var a2 = c2 - p2;
    var a3 = c3 - p3;
    var a4 = c4 - p4;
    $('#c').html(c);
    $('#p').html(p);
    $('#a').html(a);
    $('#c1').html(c1);
    $('#c2').html(c2);
    $('#c3').html(c3);
    $('#c4').html(c4);
    $('#p1').html(p1);
    $('#p2').html(p2);
    $('#p3').html(p3);
    $('#p4').html(p4);
    $('#a1').html(a1);
    $('#a2').html(a2);
    $('#a3').html(a3);
    $('#a4').html(a4);
}


$(document).ready(function(){

        update();
        var checkbox1 = $('#staff td input[type="checkbox"]');
        checkbox1.click(function() {
          if ($(this).is(':checked')) {
              $(this).parents('tr').find('select').hide();
          } else {
                  $(this).parents('tr').find('select').show();
          }
          update()
        });

        var idx1 = $('#staff tr td#idx');
        idx1.mouseover(function() {
          $(this).parents('tr').find('td#idx').html($(this).parents('tr')[0].rowIndex);
        });

})


