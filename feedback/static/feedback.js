$('.rating ul li').on('click', function () {
    let li = $(this),
        ul = li.parent(),
        rating = ul.parent(),
        last = ul.find('.current');

    if (!rating.hasClass('animate-left') && !rating.hasClass('animate-right')) {

        last.removeClass('current');

        ul.children('li').each(function () {
            let current = $(this);
            current.toggleClass('active', li.index() > current.index());
        });

        rating.addClass(li.index() > last.index() ? 'animate-right' : 'animate-left');
        rating.css({
            '--x': li.position().left + 'px'
        });
        li.addClass('move-to');
        last.addClass('move-from');

        setTimeout(() => {
            li.addClass('current');
            li.removeClass('move-to');
            last.removeClass('move-from');
            rating.removeClass('animate-left animate-right');
        }, 800);
    }
})

var data = {1:5,2:4,3:5}

function send_feedback() {
    data[4] = $('#q4').val()
    data['csrfmiddlewaretoken'] = $('input[name=csrfmiddlewaretoken').val()

    $.ajax({
        url: "/feedback/send",
        method: "POST",
        data: data,
        success: function(){
            location.replace("/feedback/submitted")
        }
    });

}

$('.star').on('click', function () {
    p = $(this).parent().attr("data-q")
    n = $(this).attr("data-id");
    data[p] = n;
})

