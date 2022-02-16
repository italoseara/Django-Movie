const movie_posters = $('.poster');

$.each(movie_posters, function() {
    let bottom = $(this).find('.bottom');

    $(this).on('mouseenter', () => {
        bottom.css('opacity', 1);
        playButton.css('opacity', 1);
        removeButton.css('opacity', 1);
    });

    $(this).on('mouseleave', () => {
        bottom.css('opacity', 0);
    });

    $(this).on('contextmenu', (e) => {
        e.preventDefault();
    });
});

$(document).ready(function() {
    $('.progress').each(function() {
        var watched = $(this).data('watched');
        $(this).find('.watched').css('width', watched + '%');
    });
});

$('.row-title span').click(function() {
    $.ajax({
        type: 'POST',
        url: '/api/clear-watching/',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        data: {},
        success: function(data) {
            location.reload();
        }
    })
});

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + '=');
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(';', c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return decodeURI(document.cookie.substring(c_start, c_end));
        }
    }
    return '';
}

function isOverflowing(element) {
    return element.width() - parseInt($(element).parent().css('margin')) > window.innerWidth;
}

$('.content').mouseenter(function() {
    if (isOverflowing($(this).find('.row'))) {
        $(this).find('.arrow').css('opacity', 1);
    }
});
$('.content').mouseleave(function() {
    $(this).find('.arrow').css('opacity', 0);
});

$('.arrow-right').click(function() {
    if (isOverflowing($(this).parent().find('.row'))) {
        $(this).parent().find('.row').css("transform", `translateX(${window.innerWidth}px)`);
        $(this).css("transform", `translateX(${window.innerWidth}px)`);
        $(this).parent().find('.arrow-left').css("transform", `translateX(${window.innerWidth}px)`);
    }
});

$('.arrow-left').click(function() {
    if (isOverflowing($(this).parent().find('.row'))) {
        $(this).parent().find('.row').css("transform", `translateX(0px)`);
        $(this).css("transform", `translateX(0px)`);
        $(this).parent().find('.arrow-left').css("transform", `translateX(0px)`);
    }
});
