/**
 * Name: search
 * Author: Nguyen Dinh
 * Description: search for all users in the system and display the result
 * Input: n/a
 * Output: display result onto the search result area, inside Find
 * Version: 1.0.0
 * Reviewer:
 */
function search(){
    var text = $('#id-input-search').val();
    $.get("/musicify/search-users/" + text)
       .done(function(data) {
           // Remove the current result to populate new data
           $('#id-search-result').remove();

           var search_div = $('<div></div>');
           search_div.attr({
               'id': 'id-search-result',
               'class': 'sidepanel-body'
           });

           var groupFavorites = $('<p><b>Favorites</b></p>');
           var groupActive = $('<p><b>Active</b></p>');
           var groupInactive = $('<p><b>Inactive</b></p>');

           $('#id-start-of-search-result').after(search_div);

           // Convert each object into a line and append to the place holder
           for (var i = 0; i < data.length; i++){

               // Wrapper for each line
               var search_div_each_user = $('<div></div>');
               search_div_each_user.attr('class', 'friend');

               // Display the follow or unfollow btn based on context
               var current_username = $('b:first').text();
               // If the current user returned as result,
               // don't display favorite and unfavorite button
               if (current_username !== data[i]['username']){
                   var favorite_btn = $('<button></button>');
                   favorite_btn.attr({
                       'type': 'button',
                       'class': 'btn btn-default favorite-btn'
                   });
                   if (data[i]['in_favorite'] === 'yes'){
                       favorite_btn.attr('id', data[i]['username'] + '/unfavorite');
                       favorite_btn.html('<span class="glyphicon glyphicon-star" aria-hidden="true">');
                   } else {
                       favorite_btn.attr('id', data[i]['username'] + '/favorite');
                       favorite_btn.html('<span class="glyphicon glyphicon-star-empty" aria-hidden="true"></span>');
                   }
               }
               search_div_each_user.append(favorite_btn);

               // Display the user's name
               var name = $('<a></a>');
               name.text(data[i]['first_name'] + ' ' + data[i]['last_name']);
               name.attr('href', '/musicify/'+data[i]['username']+'/');
               search_div_each_user.append(name);

               // Display the status dot
               var status_dot = $('<img>');
               status_dot.attr({
                   'class': 'status-dot',
                   'width': '8px'
               });
               if (data[i]['status'] === 'loggedin') {
                   // Display if user is in his station or not
                   if (data[i]['is_live'] === 'yes'){
		       var live_status = $("<img alt='LIVE' width='50px'>");
		       live_status.attr('src', "/static/images/live_icon.gif");
                       search_div_each_user.append(live_status);
                   } else {
                       status_dot.attr('src', '/static/images/green-dot.png');
                   }
               } else {
                   status_dot.attr('src', '/static/images/gray-dot.png');
               }
               search_div_each_user.append(status_dot);



               // Display the hr element
               var search_hr = $('<hr>');
               search_hr.attr('class', 'no-space');
               search_div_each_user.append(search_hr);

               // Connect the outter wrapper to the inner one
               if (data[i]['status'] === 'loggedin') {
                   if (data[i]['in_favorite'] === 'yes'){
                       groupFavorites.append(search_div_each_user);
                   } else {
                       groupActive.append(search_div_each_user);
                   }
               } else {
                    groupInactive.append(search_div_each_user);
               }
           }
           // Only display the categories if they have results
           if (groupFavorites.children("div").length > 0){
               search_div.append(groupFavorites);
           }
           if (groupActive.children("div").length > 0){
               search_div.append(groupActive);
           }
           if (groupInactive.children("div").length > 0){
               search_div.append(groupInactive);
           }
       })
}


/**
 * Name: refreshSearch
 * Author: Nguyen Dinh
 * Description: refresh search result
 * Input: n/a
 * Output: n/a
 * Version: 1.0.0
 * Reviewer:
 **/
function refreshSearch(){
    if ($('#id-input-search').val() !== ''){
        search();
    }
}


/**
 * Name: getFavorites
 * Author: Nguyen Dinh
 * Description: Retrieve and display user's favorites
 * Input: n/a
 * Output: n/a
 * Version: 1.0.0
 * Reviewer:
 **/
function getFavorites(){
    $.get("/musicify/get-favorites")
        .done(function(data){
            $('#id-favorite-loading').hide();
            var favoriteResultsWrapper = $('#id-favorite-results');
            favoriteResultsWrapper.empty();
            for (var i = 0; i < data.length; i++){
                var favorite_wrapper = $('<div class="friend"></div>');

                // Display the avatar
                var favorite_avatar = $('<img>');
                favorite_avatar.attr({
                    'class': 'user-avatar',
                    'src': '/musicify/get-avatar/'+data[i]['username']
                });
                favorite_wrapper.append(favorite_avatar);

                // Display user's name
                var favorite_name = $('<a></a>');
                favorite_name.text(data[i]['first_name'] + ' ' + data[i]['last_name']);
                favorite_name.attr('href', '/musicify/'+data[i]['username']+'/');
                favorite_wrapper.append(favorite_name);

                // Display user's status
                var favorite_status_dot = $('<img>');
                favorite_status_dot.attr({
                    'class': 'status-dot',
                    'width': '8px'
                });
                if (data[i]['status'] === 'loggedout') {
                    favorite_status_dot.attr('src', '/static/images/gray-dot.png');
                    favorite_wrapper.append(favorite_status_dot);
                } else {
                    // Display if user is in his station or not
                    if (data[i]['is_live'] === 'yes'){
			var favorite_live_status = $("<img alt='LIVE' width='50px'>");
			favorite_live_status.attr('src', "/static/images/live_icon.gif");
			favorite_wrapper.append(favorite_live_status);
                    } else {
                        favorite_status_dot.attr('src', '/static/images/green-dot.png');
                        favorite_wrapper.append(favorite_status_dot);
                    }

                }

                var favorite_hr = $('<hr class="no-space">');
                favorite_wrapper.append(favorite_hr);

                favoriteResultsWrapper.append(favorite_wrapper);
            }
        })
}


/**
 * Name: toggleFavorite
 * Author: Nguyen Dinh
 * Description: Either favorite or unfavorite a user based on context
 * Input: n/a
 * Output: n/a
 * Version: 1.0.0
 * Reviewer:
 **/
function toggleFavorite(){
    var idActionArr = this.id.split("/");

    // Get whatever after the last "/" as the action
    var action = idActionArr[idActionArr.length - 1];

    // Get whatever before the last "/" as the username
    var username = this.id.split("/", idActionArr.length - 1).join("/");

    // If action is invalid, alert the user
    if (action === "favorite" || action ==="unfavorite"){
        $.get("/musicify/"+username+"/"+action+"/")
            .done(function(){
                // When done, refresh the search result and favorites
                getFavorites();
                refreshSearch();
            })
            // If username is invalid or any other reason, alert the user
            .fail(function(){
                alert("Unable to "+action+" "+username+".");
            })
    } else {
        alert(action + " is not a valid action.");
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

    getFavorites();

    // Update the result every 2 seconds
    // In case user changes his status
    setInterval(refreshSearch, 2000);

    // Update the favorite in 2 seconds
    setInterval(getFavorites, 2000);

    // Set favorite and unfavorite a user
    $(document).on('click', ".btn.btn-default.favorite-btn", toggleFavorite);

    // When user finishes hitting a key, fire the function
    $('#id-input-search').on({
        // Prevent the enter key to submit the form
        keydown: function(e) {
            if (e.which === 13) {
                e.preventDefault();
            }
        },
        keyup: function(){
            if ($('#id-input-search').val() === ''){
                $('#id-search-result').remove();
            } else {
                search();
            }
        }
    });
});