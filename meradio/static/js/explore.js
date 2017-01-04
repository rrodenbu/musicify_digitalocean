/* Name: playInitialSong
   Author: Riley Rodenburg
   Description: Play the initial song already on the page in the HTML
   Input: n/a
   Output: Plays song as page is initially loaded.
   Version: 1.0.0
   Reviewer:
*/
function playInitialSong() {
    var audioPlayer = $("#id-music-player");
    var preview_url = $("#id-preview").val();
    audioPlayer.attr("src", preview_url);
}

/* Name: likeSong
   Author: Riley Rodenburg
   Description: Save current song to users "liked" playlist
                Request another song (provided by JSON)
                Update explore html to new song, play new song
   Input: n/a
   Output: Requests and plays next song. Updates album
           cover, artist and title.
   Version: 1.0.0
   Reviewer:
*/
function likeSong() {
  var audioPlayer = $("#id-music-player");

  // Animations
  $(".album-details").removeClass("no").addClass("yes");

  // Current song to save to "liked"
  var track_id = $("#id-track").val();
  
  // Save to to "liked" playlist and request and play new song
  $.get("/musicify/like/"+track_id)
      .done(function(data) {
	      $("#id-cover").attr("src", data.cover);
	      $("#id-name").text(parseHtmlEnteties(data.name));
	      $("#id-artist").text(parseHtmlEnteties(data.artist));
	      $("#id-track").val(data.track_id);
	      audioPlayer.attr("src", data.preview);
        $(".album-details").removeClass("yes");
	  })
      .fail(function() {
	      alert("No more songs.");
	  });
}


/* Name: dislikeSong
   Author: Riley Rodenburg
   Description: Save current song to users "disliked" playlist
                Request another song (provided by JSON)
                Update explore html to new song, play new song
   Input: n/a
   Output: Requests and plays next song. Updates album
           cover, artist and title.
   Version: 1.0.0
   Reviewer:
*/
function dislikeSong() {
  var audioPlayer = $("#id-music-player");
  
  // Animations
  $(".album-details").removeClass("yes").addClass("no");

  // Current song to save to "dislike" songs
  var track_id = $("#id-track").val();
  
  // Save to "disliked" playlist and request and play new song
  $.get("/musicify/dislike/"+track_id)
      .done(function(data) {
	      $("#id-cover").attr("src", data.cover);
	      $("#id-name").text(parseHtmlEnteties(data.name));
	      $("#id-artist").text(parseHtmlEnteties(data.artist));
	      $("#id-track").val(data.track_id);
	      audioPlayer.attr("src", data.preview);
        $(".album-details").removeClass("no");
	  })
      .fail(function() {
	      alert("No more songs.");
	  });
}

/* Name: parseHtmlEnteties
   Author: Riley Rodenburg
   Description: Reads numbers as a normal number, helps parse ASCII
   Input: str
   Output: 
   Version: 1.0.0
   Reviewer:
*/
function parseHtmlEnteties(str) {
    str = str.replace("&amp;", '&');
    str = str.replace("&gt;", '>');
    str = str.replace("&lt;", '<');
    str = str.replace("&quot;", '"');
    str = str.replace("&#39;", "'");
    return str;
}

/* Name: playPauseSong
   Author: Riley Rodenburg
   Description: Play or pause current song.
   Input: n/a
   Output: Pauses song if playing or plays song if paused
   Version: 1.0.0
   Reviewer:
*/
function playPauseSong() {
    var audioPlayer = $("#id-music-player");
    var hoverImage = $("#id-hover-image");
    var currentSong = audioPlayer[0];
    
    if (currentSong.paused) {
        currentSong.play();
        hoverImage.removeClass('glyphicon-play').addClass('glyphicon-pause');
    } else {
        currentSong.pause();
        hoverImage.removeClass('glyphicon-pause').addClass('glyphicon-play');
    } 
}

// https://docs.djangoproject.com/en/1.10/ref/csrf/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    // Put this on top to make sure csrf is ready for AJAX
	// https://docs.djangoproject.com/en/1.10/ref/csrf/
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


	playInitialSong();
	
	$(document).on('click', "#id-like-button", likeSong);
	$(document).on('click', "#id-dislike-button", dislikeSong);
	$(document).on('click', "#id-overlay", playPauseSong);

    // Using spacebar to pause and play the current song
    $(document).keydown(function(e) {
              if (e.keyCode == '32') {
                e.preventDefault();
                playPauseSong()
              }
    });
});