/**
 * Based on Wookmark's endless scroll.
 */
$(window).ready(function () {
    var apiURL = '/api/v1/pin/?album='+album_id+'&format=json&offset='
    var page = 0;
    var handler = null;
    var isLoading = false;
    
    /**
     * When scrolled all the way to the bottom, add more tiles.
     */
    function onScroll(event) {
      if(!isLoading) {
          var closeToBottom = ($(window).scrollTop() + $(window).height() > $(document).height() - 100);
          if(closeToBottom) loadData();
      }
    };
    
    function applyLayout() {
      $('#pins').imagesLoaded(function() {
          // Clear our previous layout handler.
          if(handler) handler.wookmarkClear();
          
          // Create a new layout handler.
          handler = $('#pins .pin');
          handler.wookmark({
              autoResize: true,
              offset: 3,
              itemWidth: 242
          });
      });
    };
    
    /**
     * Loads data from the API.
     */
    function loadData() {
        isLoading = true;
        $('#loader').show();
        
        $.ajax({
            url: apiURL+(page*20),
            success: onLoadData
        });
    };
    
    /**
     * Receives data from the API, creates HTML for images and updates the layout
     */
    function onLoadData(data) {
        data = data.objects;
        isLoading = false;
        $('#loader').hide();
        
        page++;
        
        var html = '';
        var i=0, length=data.length, pin;
        for(; i<length; i++) {
          pin = data[i];
          html += '<div class="pin">';
          if (is_owner) {
              html += '<a class="pull-right" href="/albums/delete-pin/' + pin.id +'">&times;</a>';
          };
          html += '<a class="fancybox" rel="pins" href="'+pin.file+'">';
          html += '<img src="'+pin.thumbnail+'" width="200" >';
          html += '</a>';
          html += '<p>'+pin.description+'</p>';
          html += '</div>';
        }
        if (html === '') {
            tip = '<div class="alert alert-block fade in">';
            tip += '<a class="close" data-dismiss="alert" href="#">&times;</a>';
            tip += '这个相册里还没有照片,登录后点击右上角,可以批量上传哦~~';
            tip += '</div>';
            $('#pins').html(tip);
        };
        $('#pins').append(html);
        
        applyLayout();
    };
  
    $(document).ready(new function() {
        $(document).bind('scroll', onScroll);
        loadData();
    });

    /**
     * On clicking an image show fancybox original.
     */
    $('.fancybox').fancybox({
        openEffect: 'none',
        closeEffect: 'none'
    });
});
