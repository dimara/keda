$(document).ready(function () {

  var $rows = $('#table tr');
  $('#search').keyup(function() {
      var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();

      $rows.show().filter(function() {
          var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
          return !~text.indexOf(val);
      }).hide();
  });



    if(window.location.href.indexOf("reservations") > -1) {
       $('#page-title').html('Reservation');
    }
    if(window.location.href.indexOf("th") > -1) {
       $('#page-title').html('T.H.');
    }
    if(window.location.href.indexOf("availability") > -1) {
       $('#page-title').html('Availability');
    }
    if(window.location.href.indexOf("test") > -1) {
       $('#page-title').html('Test Page');
    }
    if(window.location.href.indexOf("parousiologio") > -1) {
       $('#page-title').html('Παρουσιολόγιο');
    }
    if(window.location.href.indexOf("stats") > -1) {
       $('#page-title').html('Stats');
    }
    if(window.location.href.indexOf("damages") > -1) {
           $('#page-title').html('Damages');
    }
    if(window.location.href.indexOf("logistic") > -1) {
           $('#page-title').html('Logistic');
    }
    if(window.location.href.indexOf("info") > -1) {
           $('#page-title').html('Reservation Info');
    }
    if(window.location.href.indexOf("apartments") > -1) {
           $('#page-title').html('Apartments');
    }
    if(window.location.href.indexOf("persons") > -1) {
           $('#page-title').html('Persons');
    }



        $("#showstatus").click(function() {
            if($('#showstatus:checked').length) {
                $(".label").show();
            } else {
                $(".label").hide();
            }
        });

        $(".rltvs").click(function() {
            if($('.rltvs:checked').length) {
                $(".relatives").show();
            } else {
                $(".relatives").hide();
            }
        });

        $(".vhcls").click(function() {
            if($('.vhcls:checked').length) {
                $(".vehicles").show();
            } else {
                $(".vehicles").hide();
            }
        });

        $(".cntcts").click(function() {
            if($('.cntcts:checked').length) {
                $(".contacts").show();
            } else {
                $(".contacts").hide();
            }
        });

        $(".prd").click(function() {
            if($('.prd:checked').length) {
                $(".period").show();
            } else {
                $(".period").hide();
            }
        });

        $(".aprtmnt").click(function() {
            if($('.aprtmnt:checked').length) {
                $(".appartment").show();
            } else {
                $(".appartment").hide();
            }
        });

        $(".tp").click(function() {
            if($('.tp:checked').length) {
                $(".type").show();
            } else {
                $(".type").hide();
            }
        });

        $(".pd").click(function() {
            if($('.pd:checked').length) {
                $(".payed").show();
            } else {
                $(".payed").hide();
            }
        });

        $(".actv").click(function() {
            if($('.actv:checked').length) {
                $(".ea").show();
            } else {
                $(".ea").hide();
            }
        });

        $("#condensed").click(function() {
            if($('#condensed:checked').length) {
                $("#table").addClass("table table-hover table-condensed");
            } else {
                $("#table").removeClass("table-condensed");
            }
        });
        $("#errors").click(function() {
            if($('#errors:checked').length) {
                    $(".ok").hide();
                    $(".warnings").hide();
                    $(".danger").show();
                    $( "#warnings" ).prop( "checked", false );
                }
                else{
                    $(".ok").show();
                    $(".warnings").show();
                    }
        });
        $("#warnings").click(function() {
            if($('#warnings:checked').length) {
                    $(".ok").hide();
                    $(".danger").hide();
                    $(".warnings").show();
                    $( "#errors" ).prop( "checked", false );
                }
                else{
                    $(".ok").show();
                    $(".danger").show();
                    }
        });



$(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('.scrollup').fadeIn();
        } else {
            $('.scrollup').fadeOut();
        }
    });

$('.scrollup').click(function(){
    $("html, body").animate({ scrollTop: 0 }, 600);
    return false;
    });

});


