// Global var to store the current track id on this page
var current_track_id;
var host = $('#id-station-username').text();
var isUserLeftChannel = true;

/* Name: syncUserSong
   Author: Nguyen Dinh
   Description: Play current song with
   Input: song, start_time
   Output: Plays song as page is initially loaded.
   Version: 1.0.0
   Reviewer:
*/
function syncUserSong() {
    $.get("/musicify/sync-user-song/"+host)
       .done(function(data) {
          var audioPlayer = $("#id-music-player");
          var currentSong = audioPlayer[0];

          // The song only plays when the user is in his channel
          if (data.track_id !== '' && !isUserLeftChannel && parseInt(data.start_time) <= parseInt(data.length)){
            $('#id-loading').hide();
            $('#id-waiting-content').hide();
            $('#id-not-live-icon').hide();
            $('#id-live-icon').show();
            $("#id-page-content").show();
            $("#messaging-content").removeClass('col-md').addClass('col-md-6');
            if (current_track_id !== data.track_id){
              $("#id-cover").attr("src", data.cover);
              $("#id-name").text(parseHtmlEnteties(data.name));
              $("#id-artist").text(parseHtmlEnteties(data.artist));
              $("#id-track").val(data.track_id);
              current_track_id = data.track_id;
              $("#id-page-content").show();
              start_time = parseInt(data.start_time);

              // Play song from current data
              audioPlayer.attr("src", data.preview);
              currentSong.currentTime = data.start_time;
            }

            if (data.status !== 'Playing' && currentSong.played){
                currentSong.pause();
            } else if (data.status === 'Playing' && currentSong.paused) {
                // Use this to avoid the race condition between play() and pause()
                setTimeout(function () {
                    currentSong.play();
                }, 150);
            }
          } else { // User NOT in their channel:
              $('#id-loading').show();
              $("#id-page-content").hide();
              $("#messaging-content").removeClass('col-md-6').addClass('col-md');
              $('#id-waiting-content').show();
              $('#id-not-live-icon').show();
              $('#id-live-icon').hide();
              if (currentSong.played){
                    currentSong.pause();
              }
          }
       })
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
    return str.replace(/&#([0-9]{1,3});/gi, function(match, numStr) {
        var num = parseInt(numStr, 10); // read num as normal number
        return String.fromCharCode(num);
    });
}

/* Name: muteUnmuteSong
   Author: Judy Mai
   Description: Mute or unmute current song from another user's station
   Input: n/a
   Output: Mutes song if unmuted or vice versa
   Version: 1.0.0
   Reviewer:
*/
function muteUnmuteSong() {
  var audioPlayer = $("#id-music-player");
  var muteUnmuteButton = $("#id-mute-unmute-button-span");
  var hoverImage = $("#id-hover-image");
  var currentSong = audioPlayer[0];

  if (currentSong.muted) {
      // if currently muted, then unmute it
      currentSong.muted = false;
      muteUnmuteButton.removeClass('glyphicon-volume-off').addClass('glyphicon-volume-up');
      hoverImage.removeClass('glyphicon-volume-off').addClass('glyphicon-volume-up');
  } else {
      // currently unmuted, mute it
      currentSong.muted = true;
      muteUnmuteButton.removeClass('glyphicon-volume-up').addClass('glyphicon-volume-off');
      hoverImage.removeClass('glyphicon-volume-up').addClass('glyphicon-volume-off');
  }
}

/* Name: startChat
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

function startChat() {
    var station_name = $("#id-station-username").text();
    curr_user_username = $("#id-logged-in-user").val();

    username= curr_user_username;
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
      var username = $("#id-logged-in-user").val();

      
      curr_channel.join().then(function(channel) {

      });

      // Listen for new messages sent to the channel
      curr_channel.on('messageAdded', function(message) {
          if(message.body != ""){
            printMessage(message.author, message.body);
          }
      });

      // Listen for members joining channel
      curr_channel.on('memberJoined', function(member) {
        addListener(member.identity)
        Materialize.toast(member.identity + ' joined.', 2000, 'rounded')
          // If the user is the station's owner
          // notify everybody
          if (member.identity == host){
              isUserLeftChannel = false;
          }
      });

      // Listen for members leaving channel
      curr_channel.on('memberLeft', function(member) {
          removeListener(member.identity);
          Materialize.toast(member.identity + ' left.', 2000, 'rounded')

          // If the user is the station's owner
          // notify everybody
          if (member.identity == host){
              isUserLeftChannel = true;
          }
      });
  }
 
  // Send a new message to the general channel
  // https://www.twilio.com/docs/api/ip-messaging/guides/channels
  // https://www.twilio.com/blog/2015/12/city-chat-with-python-django-and-twilio-ip-messaging.html
  var $input = $('#chat-input');
  $input.keypress(function(e) {
      if (e.keyCode == 13) {
          e.preventDefault(); //Prevents page from reloading entirely.
          var message = $input.val();
	  curr_channel.sendMessage(message);
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

  // Retrieve user info
  $.get("/musicify/retrieve-user-info/"+username_of_new_listener)
      .done(function(data) {
        var person_div = $("<div></div>");
        person_div.attr('id', 'id-listener-' + username_of_new_listener);
        person_div.html(data.first_name + " " + data.last_name);
        //        $("#listeners").append("<div id=id-listener-" + username_of_new_listener + ">" + data.first_name + " " + data.last_name"<hr class='small-space'></div>");
        $("#listeners").append(person_div);
        $("#listeners").append("<hr class='small-space'>");
    }).fail(function(){
        console.log("Can't get users info.");
    });

  listenerCount = $("#id_total_users")
  currentCount = parseInt(listenerCount.text())
  listenerCount.text(currentCount+1);


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
  // Retrieve user info
  $("#id-listener-"+username_of_listener).remove()

  listenerCount = $("#id_total_users")
  currentCount = parseInt(listenerCount.text())
  listenerCount.text(currentCount-1);
  
}

/* Name: toggleFavorite
   Author: Judy Mai
   Description: Sets the user to the logged in user's favorites or removes.
   Input: n/a
   Output: Favorites or unfavorites the user
   Version: 1.0.0
   Reviewer:
*/
function toggleFavorite() {
    var favorite_btn = $("#id-favorite-btn-span");
    var username = $("#id-username").val();

    var favorite_class = document.getElementById("id-favorite-btn-span").classList;
    if (favorite_class.contains("glyphicon-star-empty")) {
        // empty star, favorite and switch
        favorite_btn.removeClass("glyphicon-star-empty").addClass("glyphicon-star");
        $.get("/musicify/"+username+"/favorite/")
            // If username is invalid or any other reason, alert the user                        
            .fail(function(){
                console.log("Unable to favorite "+username+".");
            });
    } 
    else {
	// full star, unfavorite and switch
	favorite_btn.removeClass("glyphicon-star").addClass("glyphicon-star-empty");
	$.get("/musicify/"+username+"/unfavorite/")
            // If username is invalid or any other reason, alert the user                        
	    .fail(function(){
		    console.log("Unable to unfavorite "+username+".");
		});
    }
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
           // If the host is not in chat => he's not in his station
           for (var i = 0; i < data.length; i++){
               if (data[i]['username'] == host){
                    isUserLeftChannel = false;
               }
               addListener(data[i].username);
           }
       }).fail(function(){
         console.log("Can't retrieve listeners.")
       });
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

/* Name: showListenersPanel
   Author: Judy Mai
   Description: Show listeners panel
   Version: 1.0.0
   Reviewer:
*/
function showListenersPanel(){
    $("#messages-panel").hide();
    $("#listeners").show(); 
    $("#listeners-icon").addClass('selected');
    $("#messages-label").removeClass('selected');
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


  setInterval(syncUserSong, 1000);
  startChat();
  $(document).on('click',"#id-overlay", muteUnmuteSong);
  $(document).on('click', "#id-mute-unmute-button", muteUnmuteSong);
  $(document).on('click', "#id-favorite-btn", toggleFavorite);
  $(document).on('click', "#messages-label", showMessagesPanel);
  $(document).on('click', "#listeners-icon", showMessagesListeners);

  setInterval(syncUserSong, 1000);


});

$(window).bind('beforeunload', function(){

  curr_channel.leave().then(function(leftChannel) {
        console.log('left ' + leftChannel.friendlyName);
  });
  
});
