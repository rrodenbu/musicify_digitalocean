function animateScroll0() {
    var elem = document.getElementById("id-time-bar"); 
    var width = 3.3;
    var id = setInterval(frame, 1000); //30000 is 30 seconds
    function frame() {
        if (width >= 100) {
            clearInterval(id);
        } else {
            width += 3.3; 
            elem.style.width = width + '%'; 
        }
    }
}

function pauseCurrTime() {
    if (currentSong.paused) {
	// currently paused, toggle to play
	var incrementTime = window.setInterval(animateScroll0, 1000);
    } else {
	clearInterval(animateScroll0);
    }
}

function animateScroll1()
{
    var timeBar = $('#id-time-bar');
    timeBar.velocity({ width: '100%'}, 
		     { duration: 30000 },
		     { easing: 'linear' },
		     { complete: function() { resetScroll(); }
		     });		    
}

function resetScroll() 
{
    var timeBar = $('#id-time-bar');
    timeBar.attr("style", "width: 0%");
    timeBar.velocity({ width: '0%' },
		     { duration: 100 });
}

function pauseScroll() 
{
    var audioPlayer = $("#id-music-player");
    var currentSong = audioPlayer[0];
    var timeBar = $('#id-time-bar');

    if (currentSong.paused) {
	animateScroll1();
    } else {
	timeBar.stop(); // pause the animation
    }
}

function animateScroll2()
{
    //    $('.progress-bar-fill').velocity({ width: '100%' }, 
    //    $('.progress-bar-fill').css('width', '100%');
}

$(document).ready(function () {
	//	animateScroll0();
	animateScroll1();
	// animateScroll2();

        $(document).on('click', "#id-like-button", animateScroll1);
        $(document).on('click', "#id-dislike-button", animateScroll1);
        //$(document).on('click', "#id-play-pause-button", pauseScroll);
	$(document).on('click', "#id-overlay", pauseScroll);
    });