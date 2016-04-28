$(function () {

    var id = $(this).attr('data-channelId');
    $.ajax({
        url: '/approachone/rest/channels/',
        beforeSend: function(xhr) {
            xhr.overrideMimeType( "application/json; charset=utf-8" );
        }
    })
    .done(function(data) {
        for (var i = 0; i < data.length; i++) {
            var li = "<li class='channel' data-idChannel='"+data[i].uuid+"'>"
                        +"<label for='c"+data[i].uuid+"' class='menu_label'>"+data[i].channelName
                        +"<a class='call-api' href='/approachone/rest/channel/?uuid="+data[i].uuid+"'>=></a>"
                        +"</label>"
                        +"<input type='checkbox' id='c"+data[i].uuid+"' />"
                    +"</li>";
            $('#channels').append(li);
            if (data[i].categories.length) {
                li = $("*[data-idChannel='"+data[i].uuid+"']");
                makeUL(li, data[i].categories);
            }
        }
        $('#channels li:last-child').addClass('last');
    });

    function makeUL(list, categories) {
        var ul = "<ul></ul>";
        $(list).append(ul);
        ul = $($(list).children("ul").get(0));
        for (var i = 0; i < categories.length; i++) {
            //var li = "<li data-categoryId='"+categories[i].uuid+"'>"+categories[i].name+"</li>";
            var li = "<li class='channel' data-categoryId='"+categories[i].uuid+"'>"
                        +"<label for='c"+categories[i].uuid+"' class='menu_label'>"+categories[i].name
                        +"<a class='call-api' href='/approachone/rest/category/?uuid="+categories[i].uuid+"'>=></a>"
                        +"</label>"
                        +"<input type='checkbox' id='c"+categories[i].uuid+"' />"
                    +"</li>";
            ul.append(li);
            if (categories[i].children.length) {
                li = $("*[data-categoryId='"+categories[i].uuid+"']");
                makeUL(li, categories[i].children);
            }
        }
    }

    $(document).on('click', '.call-api', function(event){
        event.preventDefault();
        var api_url = $(this).attr('href');
        $.ajax({
            url: api_url,
            beforeSend: function(xhr) {
                xhr.overrideMimeType( "application/json; charset=utf-8" );
            }
        })
        .done(function(data) {
            //$('#response-text').html(JSON.stringify(data));
            $('#api-response').JSONView(data, { collapsed: true, nl2br: true, recursive_collapser: false });
            $('#api-url').attr("href", api_url);
            $('#api-url').html(api_url);
            $('#api-url').css('display', 'block');
        });
    });

});
