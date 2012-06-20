/**
 * Based on Wookmark's endless scroll.
 */
$(window).ready(function () {
    var apiURL = '/api/v1/album/?format=json&offset='
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
      $('#albums').imagesLoaded(function() {
          // Clear our previous layout handler.
          if(handler) handler.wookmarkClear();
          
          // Create a new layout handler.
          handler = $('#albums .pin');
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
        var i=0, length=data.length;
        for(; i<length; i++) {
          album = data[i];
          html += '<div class="pin">';
          html += '<p><b>'+album.name +'</b><small>(' + album.count + '张)</small></p>';
          html += '<a class="" rel="pins" href="'+album.id+'">';
          html += '<img src="' + STATIC_URL + 'album.png" width="200" >';
          html += '</a>';
          html += '<p>by <b>' + album.username + '</b></p>';
          html += '<p>at <i>' + album.create + '</i></p>';
          html += '</div>';
        }
        $('#albums').append(html);
        
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
