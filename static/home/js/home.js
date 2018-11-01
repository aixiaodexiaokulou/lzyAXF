$(function () {
    // 隐藏滚动条后导致页面加宽的处理
    $('.home').width(innerWidth);
    new Swiper('#topSwiper', {
        pagination: '.swiper-pagination',
        // nextButton: '.swiper-button-next',
        // prevButton: '.swiper-button-prev',
        paginationClickable: true,
        spaceBetween: 0,
        centeredSlides: true,
        autoplay: 2500,
        autoplayDisableOnInteraction: false,
        loop: true,
    });
    new Swiper('#mustbuySwiper', {
        paginationClickable: true,
        spaceBetween: 0,
        centeredSlides: true,
        autoplay: 2500,
        autoplayDisableOnInteraction: false,
        slidesPerView: 3,
        loop: true,
    });
})