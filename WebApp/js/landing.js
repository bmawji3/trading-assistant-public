/* Theme Name: Tradify - Landing page Template
   Author: CoderBoys
   Version: 1.0.0
*/

"use strict"; 
/*-----------------------------------------------------------------------------------*/
/*  LOADING
/*-----------------------------------------------------------------------------------*/
$(window).load(function() {
    $('body').delay(350).css({
        'overflow': 'visible'
    });
});

/* ==============================================
Smooth Scroll To Anchor
=============================================== */
//jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('.navbar-nav a').on('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top - 0
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});
/*-------------------------------------------------*/
/* =  Full-window section
/*-------------------------------------------------*/

var windowHeight = $(window).height(),
    topSection = $('.home-fullscreen');
topSection.css('height', windowHeight);

$(window).resize(function() {
    var windowHeight = $(window).height();
    topSection.css('height', windowHeight);
});


//sticky header on scroll
$(window).load(function() {
    $(".sticky").sticky({
        topSpacing: 0
    });
});

/* ==============================================
Magnific Popup
=============================================== */
$(document).ready(function() {
    $('.popup-video').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        fixedContentPos: false,
        fixedBgPos: true,

        overflowY: 'auto',

        closeBtnInside: true,
        preloader: false,

        midClick: true,
        removalDelay: 300,
        mainClass: 'my-mfp-zoom-in'
    });
});