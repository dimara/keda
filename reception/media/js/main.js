// $(function(){
//     var url = window.location.pathname,
//         urlRegExp = new RegExp(url.replace(/\/$/,''));    
//         $('.nav li a').each(function(){
//         if(urlRegExp.test($(this).attr('href'))){
//             $(this).addClass('active');
//         }
//         });
// });​


$(document).ready(function () {
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

        $("#condensed").click(function() {
            if($('#condensed:checked').length) {
                $("#table").addClass("table table-hover table-condensed");
            } else {
                $("#table").removeClass("table-condensed");
            }
        });

});

