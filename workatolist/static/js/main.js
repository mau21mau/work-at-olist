function makeUL(list, categories) {
    var ul = document.createElement("ul");
    list.appendChild(ul);
    ul = list.querySelectorAll('ul')[0];
    for (var i = 0; i < categories.length; i++) {
        //var li = "<li data-categoryId='"+categories[i].uuid+"'>"+categories[i].name+"</li>";
        var li = "<li class='channel' data-categoryId='"+categories[i].uuid+"'>"
                    +"<label for='"+slugify(categories[i].name)+categories[i].uuid+"' class='menu_label'>"+categories[i].name
                    +"<a class='call-api' href='/approachone/rest/category/?uuid="+categories[i].uuid+"'>=></a>"
                    +"</label>"
                    +"<input type='checkbox' id='"+slugify(categories[i].name)+categories[i].uuid+"' />"
                +"</li>";
        ul.insertAdjacentHTML('beforeend', li);
        if (categories[i].children.length) {
            li = document.querySelector("*[data-categoryId='"+categories[i].uuid+"']");
            makeUL(li, categories[i].children);
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
        /*
        xhr.addEventListener('progress', function(e) {
            var done = e.position || e.loaded, total = e.totalSize || e.total;
            console.log('xhr progress: ' + (Math.floor(done/total*1000)/10) + '%');
            moveProgressBar()
        }, false);
         */
        xhr.addEventListener("load", function(e){
            callback(xhr);

        }, false);


        xhr.addEventListener("error", function(e){
            callback(xhr);
        }, false);

        if ( xhr.upload ) {
            xhr.upload.onprogress = function(e) {
                var done = e.position || e.loaded, total = e.totalSize || e.total;
                //console.log('xhr.upload progress: ' + done + ' / ' + total + ' = ' + (Math.floor(done/total*1000)/10) + '%');
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
    ajax.send('/approachone/rest/channels/', 'GET', null, true, function(data){
        data = JSON.parse(data.responseText);
        var channels = document.getElementById("channels");
        channels.innerHTML = '';
        for (var i = 0; i < data.length; i++) {
            var li = "<li class='channel' data-idChannel='"+data[i].uuid+"'>"
                        +"<label for='"+slugify(data[i].channelName)+data[i].uuid+"' class='menu_label'>"+data[i].channelName
                        +"<a class='call-api' href='/approachone/rest/channel/?uuid="+data[i].uuid+"'>=></a>"
                        +"</label>"
                        +"<input type='checkbox' id='"+slugify(data[i].channelName)+data[i].uuid+"' />"
                    +"</li>";
            channels.insertAdjacentHTML('beforeend', li);
            if (data[i].categories.length) {
                li = document.querySelector("*[data-idChannel='"+data[i].uuid+"']");
                makeUL(li, data[i].categories);
            }
        }

        var buttons = document.getElementsByClassName('call-api');
        for (var i=0; i < buttons.length; i++) {
            buttons[i].addEventListener('click', function(event){
                event.preventDefault();
                var api_url = this.href;
                ajax.send(api_url, 'GET', null, true, function(data){
                    $('#api-response').JSONView(data.responseText, { collapsed: true, nl2br: true, recursive_collapser: false });
                    $('#api-url').attr("href", api_url);
                    $('#api-url').html(api_url);
                    $('#api-url').css('display', 'block');
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

    var channel = document.querySelector("#id_channel").value;
    formData.append('channel', channel);
    formData.append('file', file);
    formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken);
    ajax.send('/approachone/', 'POST', formData, true, function(data){
        debug = data;
        if (data.status === 200) {
            document.querySelector("#form-fields-container").innerHTML = data.responseText;
            updateChannels();
            updateStatus('success');
        } else {
            updateStatus('error');
        }
    });
});

function updateStatus(status) {
    var el = document.querySelector(".status");
    el.style.display = 'block';
    if (status === 'success') {
        removeClass(el, 'error');
        addClass(el, 'success');
        el.innerHTML = 'Upload complete!';
    } else {
        removeClass(el, 'success');
        addClass(el, 'error');
        el.innerHTML = 'Upload error!';
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
