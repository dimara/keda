$ = django.jQuery;

function update_row(tds, boxes) {
        tds[1].innerHTML = boxes.length;
        tds[2].innerHTML = boxes.filter(':checked').length;
        tds[3].innerHTML = boxes.filter(':not(:checked)').length;
}

function update(){
    for (var i=0; i<4; i++){
        tds = $("#summary tr#" + i + " td")
        boxes = $('.' + i)
        update_row(tds, boxes)
    }
    tds = $("#summary tr#4 td")
    boxes = $('#staff td input[type="checkbox"]')
    update_row(tds, boxes)

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

})


