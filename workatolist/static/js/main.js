function makeUL(list, categories) {
    var ul = document.createElement("ul");
    list.appendChild(ul);
    ul = list.querySelectorAll('ul')[0];
    for (var i = 0; i < categories.length; i++) {
        var category = categories[i];
        var li = "<li class='channel' data-categoryId='"+category.uuid+"'>"
                    +"<label for='"+slugify(category.name)+category.uuid+"' class='menu_label'>"+category.name
                    +"<a class='call-api' href='/approachone/rest/category/?uuid="+category.uuid+"'>=></a>"
                    +"</label>"
                    +"<input type='checkbox' id='"+slugify(category.name)+category.uuid+"' />"
                +"</li>";
        ul.insertAdjacentHTML('beforeend', li);
        if (category.children.length) {
            li = document.querySelector("*[data-categoryId='"+category.uuid+"']");
            makeUL(li, category.children);
        }
    }
}

function slugify(text) {
    return text.toString().toLowerCase()
        .replace(/\s+/g, '-')           // Replace spaces with -
        .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
        .replace(/\-\-+/g, '-')         // Replace multiple - with single -
        .replace(/^-+/, '')             // Trim - from start of text
        .replace(/-+$/, '');            // Trim - from end of text
}

/*  AJAX */

var ajax = {
    send: function(url, method, data, async, callback) {
        if (async === undefined) {
            async = true;
        }
        var xhr = new XMLHttpRequest();

        xhr.addEventListener("load", function(e){
            callback(xhr);

        }, false);

        xhr.addEventListener("error", function(e){
            callback(xhr);
        }, false);

        if ( xhr.upload ) {
            xhr.upload.onprogress = function(e) {
                var done = e.position || e.loaded, total = e.totalSize || e.total;
                var progress = ~~(Math.floor(done/total*1000)/10);
                moveProgressBar(progress);
                console.log("Progress: "+progress);
            };
        }

        xhr.open(method, url, async);
        xhr.send(data);
    },
};

// Send request to the API to retrieve all channels available
function updateChannels() {
    var overlay = document.querySelector(".tree-wrapper-overlay");
    overlay.style.display = 'block';
    ajax.send('/approachone/rest/channels/', 'GET', null, true, function(data){
        if (data.status === 200) {
            var data = JSON.parse(data.responseText);
            var channelsUL = document.getElementById("channels");
            channelsUL.innerHTML = '';
            channels = data.data;
            for (var i = 0; i < channels.length; i++) {
                var channel = channels[i];
                var li = "<li class='channel' data-idChannel='"+channel.uuid+"'>"
                            +"<label for='"+slugify(channel.channelName)+channel.uuid+"' class='menu_label'>"+channel.channelName
                            +"<a class='call-api' href='/approachone/rest/channel/?uuid="+channel.uuid+"'>=></a>"
                            +"</label>"
                            +"<input type='checkbox' id='"+slugify(channel.channelName)+channel.uuid+"' />"
                        +"</li>";
                channelsUL.insertAdjacentHTML('beforeend', li);
                if (channel.categories.length) {
                    li = document.querySelector("*[data-idChannel='"+channel.uuid+"']");
                    makeUL(li, channel.categories);
                }
            }
        } else {
            var tree_wrapper = document.querySelector('#tree-wrapper');
            tree_wrapper.innerHTML = "<span class='error'>("+data.status+") Failed to retrieve data from API</span>";
        }
        overlay.style.display = 'none';

        var buttons = document.getElementsByClassName('call-api');
        for (var i=0; i < buttons.length; i++) {
            buttons[i].addEventListener('click', function(event){
                event.preventDefault();
                var api_url = this.href;
                ajax.send(api_url, 'GET', null, true, function(data){
                    if (data.status === 200) {
                        $('#api-response').JSONView(data.responseText, {
                            collapsed: true, nl2br: true, recursive_collapser: false
                        });
                        $('#api-url').attr("href", api_url);
                        $('#api-url').html(api_url);
                        $('#api-url').css('display', 'block');
                    } else {

                    }
                });
            });
        }
        $('#channels li:last-child').addClass('last');
    });
}

updateChannels();

var input = document.querySelector('#sendfile');
input.addEventListener('click', function(event) {
    event.preventDefault();
    //var form = document.querySelector('form')[0];
    var formData = new FormData();
    var csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
    try{
        var file = document.querySelector("#id_file").files[0];
    }catch(err) {
        var file = null;
    }
    var channel = document.querySelector("#id_channel");
    var channel_val = channel.value;
    formData.append('channel', channel_val);
    formData.append('file', file);
    formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken);
    channel.disabled = true;
    ajax.send('/approachone/', 'POST', formData, true, function(data){
        if (data.status === 200) {
            document.querySelector("#form-fields-container").innerHTML = data.responseText;
            updateChannels();
            updateStatus('success', data.status);
        } else {
            updateStatus('error', data.status);
        }
        channel.disabled = false;
    });
});

function updateStatus(status, status_code) {
    var el = document.querySelector(".status");
    el.style.display = 'block';
    if (status === 'success') {
        removeClass(el, 'error');
        addClass(el, 'success');
        el.innerHTML = 'Upload complete!';
    } else {
        removeClass(el, 'success');
        addClass(el, 'error');
        el.innerHTML = '('+status_code+') Upload error!';
    }
}

function addClass(el, className) {
    if (el.classList) {
      el.classList.add(className);
    } else {
      el.className += ' ' + className;
    }
}

function removeClass(el, className) {
    if (el.classList) {
        el.classList.remove(className);
    } else {
        el.className = el.className.replace(new RegExp('(^|\\b)' + className.split(' ').join('|') + '(\\b|$)', 'gi'), ' ');
    }
}

function toggleModal() {
    var form_modal = document.querySelector('.form-upload');
    var overlay = document.querySelector('.overlay');
    if (~~form_modal.style.opacity) {
        overlay.style.display = 'none';
        form_modal.style.transform = 'scale(0)';
        form_modal.style.opacity = '0';
        document.body.style.overflow = 'auto';
    } else {
        overlay.style.display = 'block';
        form_modal.style.transform = 'scale(1)';
        form_modal.style.opacity = '1';
        document.body.style.overflow = 'hidden';
    }
}

var buttons = document.querySelectorAll(".upload-button, .close-button");
for(var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', toggleModal);
}

function moveProgressBar(percentage) {
    var progress = document.getElementById("progress");
    var bar = document.getElementById("bar");
    bar.style.visibility = 'visible';
    progress.style.width = percentage + '%';
    progress_val = document.querySelector('#progress-value');
    if (percentage <= 50) {
        progress_val.style.color = '#4f83be';
    } else {
        progress_val.style.color = '#FFFFFF';
    }
    progress_val.innerHTML = percentage+"%";
}
