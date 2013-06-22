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
});