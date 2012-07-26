$(document).ready(function() {
    var delayTime  = 3000,
        alerts     = $('.alert');

    delayTime = delayTime + (alerts.length * 250);

    alerts.each(function() {
        $(this).delay(delayTime).fadeOut('slow');
        delayTime -= 250;
        console.log(delayTime);
    });
    handler = $('#id_albums li');
    handler.wookmark({
        container: $('#id_albums'),
        autoResize: true,
        offset: 3,
        itemWidth: 242
    });
});
