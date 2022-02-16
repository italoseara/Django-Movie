const video = $('video');

const back = $('#back');
const subtitle = $('#subtitles');

const playButton = $('#play-button');
const foward = $('#foward');
const backward = $('#backward');
const volume = $('#volume');

const toggleSubtitles = $('#captions');
const previous = $('#previous');
const next = $('#next');
const fullScreenButton = $('#full-screen');

const dot = $('#dot');
const watched = $('#watched');
const downloaded = $('#downloaded');
const timestamp = $('#timestamp');
const progress = $('#progress');

const hud = $('.hud');

function togglePlay() {
    const method = video.prop('paused') ? 'play' : 'pause';
    video[0][method]();
}

function updateButton() {
    playButton.toggleClass('fa-play');
    playButton.toggleClass('fa-pause');
}

function updateProgress() {
    const percent = (video.prop('currentTime') / video.prop('duration')) * 100;
    dot.css('margin-left', `${percent}%`);
    watched.css('width', `${percent}%`);
}

function updateTimestamp() {
    let seconds = Math.round(video.currentTime - video.duration) * -1;

    if (seconds >= 0) {
        let secondsFormat = new Date(seconds * 1000).toISOString();
        let regex = secondsFormat.match(/\d\d:(\d\d:\d\d)/);

        if (seconds >= 3600) timestamp.text(regex[0]);
        else timestamp.text(regex[1]);
    }
}

function goFoward() {
    const newTime = video.currentTime + 10;
    video.currentTime = newTime > video.duration ? video.duration : newTime;
}

function goBackward() {
    const newTime = video.currentTime - 10;
    video.currentTime = newTime < 0 ? 0 : newTime;
}

function mute() {
    video.muted = !video.muted;
    volume.toggleClass('fa-volume-up');
    volume.toggleClass('fa-volume-mute');
}

function fullScreen() {
    !document.fullscreenElement ? document.documentElement.requestFullscreen() : document.exitFullscreen();
    fullScreenButton.toggleClass('fa-expand');
    fullScreenButton.toggleClass('fa-compress');
}

function scrub(e) {
    const scrubTime = ((e.pageX - progress.offset().left) / progress.width()) * video.prop('duration');
    const percent = (scrubTime / video.prop('duration')) * 100;
    if (percent < 0) percent = 0;
    dot.css('margin-left', `${percent}%`);
    watched.css('width', `${percent}%`);
    
    video[0].currentTime = scrubTime;
}

function hideHud() {
    hud.addClass('hidden');
    back.addClass('hidden');
    subtitle.css('bottom', '1em');

    $('.video-content').addClass('hide-cursor');
}

function showHud() {
    hud.removeClass('hidden');
    back.removeClass('hidden');
    subtitle.css('bottom', '3em');

    $('.video-content').removeClass('hide-cursor');
}

function nextVideo(episode) {
    let pageUrl = window.location.href;
    if (pageUrl.includes('series')) {
        let pageUrlArray = pageUrl.toString().split('/');
        let episodeNumber = parseInt(pageUrlArray[pageUrlArray.length-2]);
        let nextEpisode = episodeNumber + episode;
        window.location.href = `${pageUrl.substring(0, pageUrl.length - episodeNumber.toString().length-1)}${nextEpisode}`;
    } else {
        window.location.href = '/browse';
    }
}

video.click(togglePlay);
video.dblclick(fullScreen);
video.on('timeupdate', () => { updateProgress(); updateTimestamp(); })
video.on('play', updateButton)
video.on('pause', updateButton);

$(document).on('keydown', (e) => {
    if (e.code === 'Space') togglePlay();
    else if (e.code === 'ArrowRight') goFoward();
    else if (e.code === 'ArrowLeft') goBackward();
    else if (e.code === 'KeyM') mute();
    else if (e.code === 'KeyF') fullScreen();
});

back.click(() => document.location.href = '/browse');

playButton.click(togglePlay);
backward.click(goBackward);
foward.click(goFoward);
volume.click(mute);

toggleSubtitles.click(() => { subtitle.toggleClass('hidden'); });
previous.click(() => nextVideo(-1));
next.click(() => nextVideo(1));
fullScreenButton.click(fullScreen);

let mousedownProgress = false;
progress.click(scrub);
progress.on('mousedown', () => mousedownProgress = true);
progress.on('mouseup', () => video[0].play());

$(document).on('mousemove', (e) => mousedownProgress && mousedown && scrub(e));

let mousedown = false;
$(document).on('mousedown', () => mousedown = true);
$(document).on('mouseup', () => {mousedown = false; mousedownProgress = false});

let timer = null
let mouseMoving = false;
$(document).on('mousemove', () => {
    mouseMoving = true;
    clearTimeout(timer);
    timer = setTimeout(function() {
        mouseMoving = false;
    }, 5000);
});
video.click(showHud);

let onHud = false;
hud.on('mouseenter', () => onHud = true);
hud.on('mouseleave', () => onHud = false);

setInterval(() => {
    if (!onHud &&
        !mouseMoving &&
        !video.prop('paused') && 
        !hud.hasClass('hidden')) {
        setTimeout(() => {}, 5000);
        hideHud();
    } else if (onHud || mouseMoving || video.prop('paused')) { 
        showHud();
    }
}, 100);


let previousTime = 0;
setInterval(() => {
    if (video.prop('currentTime') !== previousTime) {
        $.ajax({
            type: 'POST',
            url: '/api/update-video-time/',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            data: {
                videoId: video.data('id'),
                videoType: video.data('type'),
                time: video.prop('currentTime')
            },
        })
    }

    previousTime = video.prop('currentTime');
}, 5000);

function getCookie(c_name) {
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

if (video.prop('textTracks')) {
    let track = video.prop('textTracks')[0];

    track.mode = 'hidden';
    track.oncuechange = function() {
        let activeCues = track.activeCues;
        if (activeCues.length > 0) {
            let cue = activeCues[0];
            subtitle.html(cue.text);
        } else {
            subtitle.html('');
        }
    };
}