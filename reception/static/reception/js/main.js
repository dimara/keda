var ntf = {"n0":"Regular visitor without agent!", "n1":"Regular visitor without book reference!", "n10":"Booking period started but not arrived!", "n11":"Booking period over but still staying!", "n12":"Booking period over but never arrived!", "n13":"Left without paying!"};

$(".n0").attr("title",ntf["n0"]);
$(".n1").attr("title",ntf["n1"]);
$(".n10").attr("title",ntf["n10"]);
$(".n11").attr("title",ntf["n11"]);
$(".n12").attr("title",ntf["n12"]);
$(".n13").attr("title",ntf["n13"]);
$(".n0.n1").attr("title",ntf["n1"]+ntf["n13"]);
$(".n1.n13").attr("title",ntf["n1"]+ntf["n13"]);
$(".n10.n1").attr("title",ntf["n10"]+ntf["n1"]);
$(".n10.n12").attr("title",ntf["n10"]+ntf["n12"]);
$(".n11.n1").attr("title",ntf["n11"]+ntf["n1"]);
$(".n0.n1.13").attr("title",ntf["n0"]+ntf["n1"]+ntf["n13"]);

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
                $(".nodanger").show();
                $(".danger").show();  
                $("#ra0,#ra1,#ra2,#ra3,#ra4,#rt0,#rt1,#rt2,#rt3,#rt4,#rt5").prop('checked', true);
                $("#cntr").html($(".nodanger,.danger").length);
            }
            else{
                $(".ok").show();
                $("#cntr").html($(".ok,.nodanger,.danger").length);
                }
    });

    $("#cntr").html($(".shw").length);
    $("#ecntr").html($(".danger,.nodanger").length);

    $("#rt0,#rt1,#rt2,#rt3,#rt4,#rt5").click(function() {
        var y=0;
        for (var i = 0; i < 6; i++) {
            if($("#rt"+i).is(':checked')){
                if (!$("#ra0").is(':checked')||!$("#ra1").is(':checked')||!$("#ra2").is(':checked')||!$("#ra3").is(':checked')||!$("#ra4").is(':checked')) {
                    $("#ra0,#ra1,#ra2,#ra3,#ra4").prop('checked', true);
                    $("#ra0,#ra1,#ra2,#ra3,#ra4").show();
                }
                $(".rt"+i).show();
                $(".rt"+i).addClass( "shw" );
            }
            else{
                $(".rt"+i).hide();      
                $(".rt"+i).removeClass( "shw" );      
            }
        };
    $("#ecntr").html($(".danger,.nodanger").length);
    $("#cntr").html($(".shw").length);
    });

    $("#ra0,#ra1,#ra2,#ra3,#ra4").click(function() {
        var x=0;
        for (var i = 0; i < 5; i++) {
            if($("#ra"+i).is(':checked')){
                if (!$("#rt0").is(':checked')||!$("#rt1").is(':checked')||!$("#rt2").is(':checked')||!$("#rt3").is(':checked')||!$("#rt4").is(':checked')||!$("#rt5").is(':checked')) {
                    $("#rt0,#rt1,#rt2,#rt3,#rt4,#rt5").prop('checked', true);
                    $("#rt0,#rt1,#rt2,#rt3,#rt4,#rt5").show();
                }
                    $(".ra"+i).show();
                    $(".ra"+i).addClass( "shw" );
            }
                else{
                    $(".ra"+i).hide();
                    $(".ra"+i).removeClass( "shw" );   
                }          
        };
    $("#ecntr").html($(".danger,.nodanger").length);
    $("#cntr").html($(".shw").length);
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


