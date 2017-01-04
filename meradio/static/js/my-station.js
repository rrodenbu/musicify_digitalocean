// global var to track the status of the song
var songPlayingStatus = 'Playing';
var pauseDuration = 0;
var pauseStartTime;

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
    var track_id = $("#id-track").val();
    $('.glyphicon-volume-up').removeClass('glyphicon-volume-up').addClass('');
    $("#play-icon-"+track_id).attr("class", "glyphicon glyphicon-volume-up")
    audioPlayer.attr("src", preview_url);
    songPlayingStaus = 'Playing';
}

/* Name: nextSong
   Author: Riley Rodenburg
   Description: Request another song (provided by JSON)
                Update explore html to new song, play new song.
   Input: n/a
   Output: Requests and plays next song. Updates album
           cover, artist and title.
   Version: 1.0.0
   Reviewer:
*/
function nextSong() {
  var audioPlayer = $("#id-music-player");
  
  // Current song
  var track_id = $("#id-track").val();
  var username = $("#id-username").val();

  // Request and play new song
  $.get("/musicify/next-song/"+track_id)
       .done(function(data) {
          $("#id-cover").attr("src", data.cover);
          $("#id-name").text(parseHtmlEnteties(data.name));
          $("#id-artist").text(parseHtmlEnteties(data.artist));
          $("#id-track").val(data.track_id);
          $('.glyphicon-volume-up').removeClass('glyphicon-volume-up').addClass('');
          $("#play-icon-"+data.track_id).attr("class", "glyphicon glyphicon-volume-up");
          audioPlayer.attr("src", data.preview);
          songPlayingStaus = 'Playing';
          $.get("/musicify/update-playing-status/Playing/0/");
       })
       .fail(function(){
	      console.log("Unable to play the next song.");
	   });
}

/* Name: prevSong
   Author: Riley Rodenburg
   Description: Request previous song (provided by JSON)
                Update explore html to new song, play new song.
   Input: n/a
   Output: Requests and plays previous song. Updates album
           cover, artist and title.
   Version: 1.0.0
   Reviewer:
*/
function prevSong() {
  var audioPlayer = $("#id-music-player");
  
  // Current song
  var track_id = $("#id-track").val();
  var username = $("#id-username").val();

  // check and play previous song
  $.get("/musicify/prev-song/"+track_id)
       .done(function(data) {
          $("#id-cover").attr("src", data.cover);
          $("#id-name").text(parseHtmlEnteties(data.name));
          $("#id-artist").text(parseHtmlEnteties(data.artist));
          $("#id-track").val(data.track_id);
          $('.glyphicon-volume-up').removeClass('glyphicon-volume-up').addClass('');
          $("#play-icon-"+data.track_id).attr("class", "glyphicon glyphicon-volume-up");
          audioPlayer.attr("src", data.preview);
          songPlayingStaus = 'Playing';
          $.get("/musicify/update-playing-status/Playing/0/");
       })
       .fail(function(){
	      console.log("Unable to play the previous song.");
	   });
}


/* Name: playSelectedSong
   Author: Judy Mai
   Description: Request song (provided by JSON)
                Update mystation html to new song, play song.
   Input: n/a
   Output: Requests and plays requested song. Updates album
           cover, artist and title.
   Version: 1.0.0
   Reviewer:
*/
function playSelectedSong() {
  var track_id = this.id;
  var audioPlayer = $("#id-music-player");
  var playPauseButton = $("#id-play-pause-button-span");
  
  // Current user station
  var username = $("#id-username").val();

  // Request and play new song
  $.get("/musicify/play-song/"+track_id)
       .done(function(data) {
          $("#id-cover").attr("src", data.cover);
          $("#id-name").text(parseHtmlEnteties(data.name));
          $("#id-artist").text(parseHtmlEnteties(data.artist));
          $("#id-track").val(data.track_id);
          $('.glyphicon-volume-up').removeClass('glyphicon-volume-up').addClass('');
          $("#play-icon-"+data.track_id).attr("class", "glyphicon glyphicon-volume-up")
	      playPauseButton.removeClass('glyphicon-play').addClass('glyphicon-pause');
          audioPlayer.attr("src", data.preview);
          songPlayingStaus = 'Playing';
          $.get("/musicify/update-playing-status/Playing/0/");
       })
       .fail(function(){
	      console.log("Unable to play selected song.");
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
   Author: Riley Rodenburg, Nguyen Dinh
   Description: Play or pause current song, then record the current status
   Input: n/a
   Output: Pauses song if playing or plays song if paused
   Version: 1.0.0
   Reviewer:
*/
function playPauseSong() {
  var audioPlayer = $("#id-music-player");
  var playPauseButton = $("#id-play-pause-button-span");
  var hoverImage = $("#id-hover-image");
  var currentSong = audioPlayer[0];

  if (currentSong.paused) {
      currentSong.play();
      playPauseButton.removeClass('glyphicon-play').addClass('glyphicon-pause');
      hoverImage.removeClass('glyphicon-play').addClass('glyphicon-pause');
      songPlayingStatus = 'Playing';
      pauseDuration = parseInt(new Date().getTime() / 1000 - pauseStartTime);
      pauseStartTime = 0;
  } else {
      currentSong.pause();
      playPauseButton.removeClass('glyphicon-pause').addClass('glyphicon-play');
      hoverImage.removeClass('glyphicon-pause').addClass('glyphicon-play');
      songPlayingStatus = 'Paused';
      pauseDuration = 0;
      pauseStartTime = new Date().getTime() / 1000;
  }

  $.get("/musicify/update-playing-status/"+songPlayingStatus+"/"+pauseDuration+"/")
}

/* Name: deleteFromLiked
   Author: Riley Rodenburg
   Description: Remove song from users liked playlist
   Input: n/a
   Output: Song removed from user's like playlist.
   Version: 1.0.0
   Reviewer:
*/
function deleteFromLiked() {
  var track_id = this.id;

  // Remove song from liked list
  $.get("/musicify/remove-song/"+track_id)
      .done(function(data) {
	      $("#"+track_id).remove();
	  })
      .fail(function(){
	      console.log("Can't remove song from your liked playlist.");
	  });
}

/* Name: startChart
   Author: Riley Rodenburg
   Description: Chat window implementation for messaging on
                various channels.
   Input: n/a
   Output: Display messages.
   Version: 1.0.0
   Reviewer:
*/

var $chatWindow = $('#messages');
var accessManager;
var messagingClient;
var curr_channel;
var username;
var channel;
var totalUsers;

function startChat() {
    var station_name = $("#id-channel-name").val();
    username= station_name;
    channel_name = station_name;
    createChat();
}
 
 
function createChat() {
  $.getJSON('/musicify/token', {identity: username, device: 'browser'}, function(data) {
    accessManager = new Twilio.AccessManager(data.token);
    messagingClient = new Twilio.IPMessaging.Client(accessManager);
    var promise = messagingClient.getChannelByUniqueName(channel_name);
    promise.then(function(channel) {
        curr_channel = channel;
        if (!curr_channel) {
            // If channel does not exist then create it
            messagingClient.createChannel({
                uniqueName: channel_name,
                friendlyName: channel_name
            }).then(function(channel) {

                curr_channel = channel;
                setupChannel();
            });
        } else {
            setupChannel();
            getCurrentListeners(curr_channel.sid);
        }
    });

  });

  function setupChannel() {
      // Join the general channel
      curr_channel.join().then(function(channel) {
          
      });
            
      // Listen for new messages sent to the channel
      curr_channel.on('messageAdded', function(message) {
          if(message.body != ""){
            printMessage(message.author, message.body);
          }
      });

      // Listen for members joining a channel
      curr_channel.on('memberJoined', function(member) {
        addListener(member.identity);

        Materialize.toast(member.identity + ' joined.', 2000, 'rounded')

      });

      // Listen for members leaving channel
      curr_channel.on('memberLeft', function(member) {
          removeListener(member.identity)
          Materialize.toast(member.identity + ' left.', 2000, 'rounded')
      });
  }
 
  // Send a new message to the general channel
  // https://www.twilio.com/docs/api/ip-messaging/guides/channels
  // https://www.twilio.com/blog/2015/12/city-chat-with-python-django-and-twilio-ip-messaging.html
  var $input = $('#chat-input');
  $input.keypress(function(e) {
      if (e.keyCode == 13) {
          e.preventDefault(); //Prevents page from reloading entirely.
          var message = $input.val()
          curr_channel.sendMessage(message)
          //printMessage(username, message);
          $input.val('');
      }
  });

}

// Helper function to print info messages to the chat window
function print(infoMessage, asHtml) {
    var $msg = $('<div class="info">');
    if (asHtml) {
        $msg.html(infoMessage);
    } else {
        $msg.text(infoMessage);
    }
    $chatWindow.append($msg);
}
 
// Helper function to print chat message to the chat window
function printMessage(fromUser, message) {
    var $user = $('<span class="username">').text(fromUser + ': ');
    if (fromUser === username) {
        $user.addClass('me');
    }
    var $message = $('<span class="message">').text(message);
    var $container = $('<div class="message-container">');
    $container.append($user).append($message);
    $chatWindow.append($container);

    // scroll down to most recent message
    var objDiv = document.getElementById("messages");
    objDiv.scrollTop = objDiv.scrollHeight;
}


/* Name: addListener
   Author: Riley Rodenburg
   Description: Get listeners info and add listener list
   Input: n/a
   Output: Listener first and last name and avatar displayed.
   Version: 1.0.0
   Reviewer:
*/
function addListener(username_of_new_listener) {
  listenerCount = $("#id_total_users")
  currentCount = parseInt(listenerCount.text())
  listenerCount.text(currentCount+1);
  // Retrieve user info
  $.get("/musicify/retrieve-user-info/"+username_of_new_listener)
      .done(function(data) {
	      /* // overlay stuff 
	      var person_div = $("<div></div>");
	      person_div.attr('id', 'id-listener-' + username_of_new_listener);
	      person_div.html(data.first_name + " " + data.last_name);
	      $("#listeners").append(person_div);
	      */
	      
	      var person_div = $("<div></div>");
	      person_div.attr('id', 'id-listener-' + username_of_new_listener);
	      person_div.html(data.first_name + " " + data.last_name);
	      //	      $("#listeners").append("<div id=id-listener-" + username_of_new_listener + ">" + data.first_name + " " + data.last_name"<hr class='small-space'></div>");
	      $("#listeners").append(person_div);
	      $("#listeners").append("<hr class='small-space'>");
	  }).fail(function(){
		  console.log("Can't get users info.");
	      });
}

/* Name: removeListener
   Author: Riley Rodenburg
   Description: Remove html for listener 
   Input: n/a
   Output: The "listeners" list should no longer have the passed in listener
   Version: 1.0.0
   Reviewer:
*/
function removeListener(username_of_listener) {
  listenerCount = $("#id_total_users")
  currentCount = parseInt(listenerCount.text())
  listenerCount.text(currentCount-1);

  // Retrieve user info
  $("#id-listener-"+username_of_listener).remove()
  
}


/* Name: getCurrentListeners
   Author: Riley Rodenburg
   Description: Request all member of current channel or station (provided by JSON)
                Update user-station html to display all active listeners
   Input: n/a
   Output: Requests and displays all active listeners.
   Version: 1.0.0
   Reviewer:
*/
function getCurrentListeners(channel_sid) {

    $.get("/musicify/listeners/"+channel_sid)
       .done(function(data) {
           $("#id_total_users").text(0);
           for (var i = 0; i < data.length; i++){
              addListener(data[i].username);
           }
       }).fail(function(){
         console.log("Can't retrieve listeners.")
       });
}


/* Name: getRecommendations
   Author: Nguyen Dinh
   Description: Load recommendations from the current user
   Input: n/a
   Output: recommendations.
   Version: 1.0.0
   Reviewer:
*/
function getRecommendations() {
    var recommended_wrapper = $('#recommended-songs');
    recommended_wrapper.empty();

    $('#id-loading').show();
   
    $.get("/musicify/get-recommendations")
       .done(function(data) {
           if (data.length > 0){
               $('#id-loading').hide();

	       for (var i = 0; i < data.length; i++) {
		   var recommended_li = $("<li class='playlist-li'></li>");
		   recommended_li.attr('id', data[i]['track_id']);
		   var recommended_span = $('<span></span>');
		   recommended_span.attr({
			   'id': 'play-icon-'+ data[i]['track_id'],
			       'class': ''
			       });
		   var recommended_dislike = $('<button></button>');
		   recommended_dislike.attr({
			   'id': data[i]['track_id'],
			       'type': 'button',
			       'class': 'glyphicon glyphicon-remove-sign btn btn-default recommend-dislike-btn',
			       });
		   var recommended_track_info =  $('<button></button>');
		   recommended_track_info.attr({
			   'id': data[i]['track_id'],
			       'class': 'btn-link play-song-btn',
			       });
		   var recommended_track_info_name = $('<span class="text-song"></span>');
		   recommended_track_info_name.text(parseHtmlEnteties(data[i]['name']));
		   var recommended_track_info_artist = $('<span class="text-artist"></span>');
		   recommended_track_info_artist.text(parseHtmlEnteties(data[i]['artist']));
		   recommended_track_info.append(recommended_track_info_name);
		   recommended_track_info.append(recommended_track_info_artist);

		   var recommended_like = $('<button></button>');
		   recommended_like.attr({
			   'id': data[i]['track_id'],
			       'type': 'button',
			       'class': 'glyphicon glyphicon-ok-sign btn btn-default recommend-like-btn right'
			       });

		   recommended_li.append(recommended_span);
		   recommended_li.append(recommended_dislike);
		   recommended_li.append(recommended_track_info);
		   recommended_li.append(recommended_like);
		   
		   recommended_wrapper.append(recommended_li);
	       }
           }})
	.fail(function(){
		console.log("Can't retrieve recommendations.");
	    });
}


/* Name: likeSelectedSong
   Author: Nguyen Dinh
   Description: Like a recommended song and refresh the playlists based on new result
   Version: 1.0.0
   Reviewer:
*/
function likeSelectedSong(){
    var currentItem = this;
    var track_id = currentItem.id;
    var liked_track_info_btn = $('#'+track_id+'.play-song-btn');

    $.get("/musicify/like/"+track_id)
      .done(function(data) {
          // Add liked song to the current liked playlist
	      
	  var liked_li = $("<li class='playlist-li'></li>");
	  liked_li.attr('id', track_id);
          var liked_span = $('<span></span>');
          liked_span.attr('id', 'play-icon-'+track_id);

          var liked_delete_btn = $('<button></button>');
          liked_delete_btn.attr({
              'id': track_id,
              'type': 'button',
              'class': 'glyphicon glyphicon-remove-sign right btn btn-default delete-song-btn'
          });
          liked_li.append(liked_span);
          liked_li.append(liked_track_info_btn);
          liked_li.append(liked_delete_btn);
          $('#liked-songs').append(liked_li);

          // Remove it from the recommended playlist
          currentItem.closest("li").remove();

          // Get a new set of recommendations if the list is empty
          if ($('#recommended-songs').is(':empty')){
                getRecommendations();
          }
      })
      .fail(function() {
	      console.log("Unable to like this track.");
	  });
}


/* Name: dislikeSelectedSong
   Author: Nguyen Dinh
   Description: dislike a recommended song and remove it from the recommendations
   Version: 1.0.0
   Reviewer:
*/
function dislikeSelectedSong(){
    var currentItem = this;
    var track_id = currentItem.id;

    $.get("/musicify/dislike/"+track_id)
      .done(function(data) {
          currentItem.closest("li").remove();

          // Get a new set of recommendations if the list is empty
          if ($('#recommended-songs').is(':empty')){
                getRecommendations();
          }
      })
      .fail(function() {
	      console.log("Unable to dislike this track.");
	  });
}

/* Name: showPlaylist
   Author: Riley Rodenburg
   Description: Reveal the playlists: reccomended or liked.
   Version: 1.0.0
   Reviewer:
*/
function showPlaylist(){
    if ($("#liked-songs").is(":hidden")){
      $("#liked-songs").show();
    }
    else {
      $("#liked-songs").hide();
    }
    
}

/* Name: showLikedPlaylist
   Author: Riley Rodenburg, Judy Mai
   Description: Show liked playlist.
   Version: 1.0.0
   Reviewer:
*/
function showLikedPlaylist(){
    $("#liked-songs").show();
    $("#id-recommended-playlist").hide();
    $("#id-recommended-btn").removeClass('selected');
    $("#id-liked-btn").addClass('selected');
}

/* Name: showRecommendedPlaylist
   Author: Riley Rodenburg, Judy Mai
   Description: Show recommended playlist
   Version: 1.0.0
   Reviewer:
*/
function showRecommendedPlaylist(){
    $("#liked-songs").hide();
    $("#id-recommended-playlist").show(); 
    $("#id-recommended-btn").addClass('selected');
    $("#id-liked-btn").removeClass('selected');
}

/* Name: showMessagesListeners
   Author: Judy Mai
   Description: Reveal either messages or listeners
   Version: 1.0.0
   Reviewer:
*/
function showMessagesListeners(){
    if ($("#messages-panel").is(":hidden")){
        $("#messages-panel").show();
        $("#listeners").hide();
        $("#listeners-icon").removeClass('selected');
        $("#messages-label").addClass('selected');
    }
    else {
        $("#messages-panel").hide();
        $("#listeners").show();
        $("#listeners-icon").addClass('selected');
        $("#messages-label").removeClass('selected');
    }
}

/* Name: showMessagesPanel
   Author: Judy Mai
   Description: Show messages panel
   Version: 1.0.0
   Reviewer:
*/
function showMessagesPanel(){
    $("#messages-panel").show();
    $("#listeners").hide();
    $("#listeners-icon").removeClass('selected');
    $("#messages-label").addClass('selected');
    
}

/* Name: changeDescription
   Author: Judy Mai
   Description: Replaces description with a description form
   Version: 1.0.0
   Reviewer:
*/
function changeDescription(e) {
    var descriptionDiv = $('#description-row');
    var description = $('#description');

    descriptionDiv.empty();

    var descriptionForm = $('<form class="form-inline" action="javascript:void(0)"></form>');
    var descriptionInput = $('<textarea></textarea>');
    descriptionInput.attr({
	    'class': 'form-control',
		'id': 'description-field',
		'max_length': '120',
		'value': description.text(),
	});
    descriptionInput.html(description.text());
    var submitButton = $('<button></button>');
    submitButton.attr({
	    'type': 'submit',
		'id': 'description-btn',
		'class': 'btn btn-sm btn-primary',
	});
    submitButton.html('submit');

    descriptionForm.append(descriptionInput);
    descriptionForm.append(submitButton);    
    descriptionDiv.append(descriptionForm);
    
    document.getElementById('description-btn').addEventListener('click', function(e) {
	    submitDescription(e);
	});
}

/* Name: submitDescription
   Author: Judy Mai
   Description: Uses django form to set new description to user
   Version: 1.0.0
   Reviewer:
*/
function submitDescription(e) {
    var descriptionForm = $('#description-form');
    var descriptionField = $('#description-field');
    var descriptionDiv = $('#description-row');

    $.post("/musicify/change-description", {'description': descriptionField.val()})
	.done(function(data) {
		displayDescription(data);
		descriptionField.val("").focus();
	    })
	.fail(function(data) {
		console.log("Can't change description");
    });
   
}

/* Name: displayDescription
   Author: Judy Mai
   Description: displays description and edit button
   Version: 1.0.0
   Reviewer:
*/
function displayDescription(descriptionText) {
    var descriptionDiv = $('#description-row');
    descriptionDiv.empty();

    var description = $('<i></i>');
    description.attr({
	    'id': 'description',
    });
    description.html(descriptionText);
    if (descriptionText == '') {
	description.html('Add description');
    }

    var editButton = $('<button><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></button>');
    editButton.attr({
            'type': 'button',
                'id': 'id-edit-btn',
                'class': 'btn btn-default edit-btn',
                });
  
    descriptionDiv.append(description);
    descriptionDiv.append(editButton);

    document.getElementById('id-edit-btn').addEventListener('click', function(e) {
            changeDescription(e);
        });
}

// https:/Add description/docs.djangoproject.com/en/1.10/ref/csrf/
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


  $.get("/musicify/update-playing-status/Playing/0/");
  playInitialSong();
  startChat();
  $(document).on('click', "#id-play-pause-button", playPauseSong);
  $(document).on('click',"#id-overlay", playPauseSong);
  $(document).on('click', "#id-next-song-button", nextSong);
  $(document).on('click', "#id-prev-song-button", prevSong);
  $(document).on('click', ".delete-song-btn", deleteFromLiked);
  $(document).on('click', ".play-song-btn", playSelectedSong);
  $(document).on('click', ".recommend-like-btn", likeSelectedSong);
  $(document).on('click', ".recommend-dislike-btn", dislikeSelectedSong);

  $(document).on('click', "#id-liked-btn", showLikedPlaylist);
  $(document).on('click', "#id-recommended-btn", showRecommendedPlaylist);

  $(document).on('click', "#id-recommended-btn", getRecommendations);

  $(document).on('click', "#messages-label", showMessagesPanel);
  $(document).on('click', "#listeners-icon", showMessagesListeners);
  
  $("#id-edit-btn").click(function(e) {
	  changeDescription(e);
  });


  $("#id-music-player").on('ended', nextSong); //Song ended, auto to next one

  // Press space bar to pause an unpause unless it is in chat input
  $(document).keydown(function(e) {
      if (!$("#chat-input").is(":focus") && !$("#description-field").is(":focus")) {
        if (e.keyCode == '32') {
            e.preventDefault();
            playPauseSong();
        }
      }
  });

});

$(window).unload(function(){
    curr_channel.leave().then(function(leftChannel) {
            console.log('left ' + leftChannel.friendlyName);
    });
    $.ajax({
        type: 'GET',
        url: '/musicify/update-playing-status/Stopped/0/',
        async:false, //IMPORTANT, the call will be synchronous
        data: {}
    }).done(function(data) {
        console.log('complete');
    });
});