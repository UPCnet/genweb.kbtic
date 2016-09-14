$(document).ready(function () {

// Tags select2 field
$('#searchbytagkbtic').select2({
    tags: [],
    tokenSeparators: [","],
    minimumInputLength: 1,
    ajax: {
        url: portal_url + '/getVocabulary?name=plone.app.vocabularies.Keywords',
        data: function (term, page) {
            return {
                query: term.toLowerCase(),
                page: page // page number
            };
        },
        results: function (data, page) {
            return data;
        }
    }
});

// Tags search
$('#searchbytagkbtic').on("change", function(e) {
    var query = $('#searchinputcontentkbtic .searchInput').val();
    var path = $(this).data().name;
    var tags = $('#searchbytagkbtic').val();
    var obsolete = $('#include_obsolets:checked').val();
    $('.listingBar').hide();
    tags = decodeURI(tags.replace(/=/g,'%'));
    $.get(path + '/search_filtered_content', { q: query, t: tags, o: obsolete}, function(data) {
        $('#tagslist').html(data);
    });
});

// Content search
$('#searchinputcontentkbtic .searchInput').on('keydown', function(event) {
    if (event.keyCode == 13) {
        var query = $(this).val();
        var path = $(this).data().name;
        var tags = $('#searchbytagkbtic').val();
        var obsolete = $('#include_obsolets:checked').val();
        $('.listingBar').hide();
        $.get(path + '/search_filtered_content', { q: query, t: tags, o: obsolete }, function(data) {
            $('#tagslist').html(data);
        });
    }
});

$('#searchinputcontentkbtic #include_obsolets').click( function(event){

    var query = $('#searchInput').val();
    var path = $(location).attr('href');
    var tags = $('#searchbytagkbtic').val();
    var obsolete = $('#include_obsolets:checked').val();
    $('.listingBar').hide();
    $.get(path + '/search_filtered_content', { q: query, t: tags, o: obsolete }, function(data) {
        $('#tagslist').html(data);
    });
});

$("a.CatItem").on("click", function (event) {
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    var category = $(this).attr("value");

    if ($("#searchbytagkbtic").val() == ''){
        $('#searchbytagkbtic').select2({
            tags: [],
            tokenSeparators: [","],
            minimumInputLength: 1,
            ajax: {
                url: portal_url + '/getVocabulary?name=plone.app.vocabularies.Keywords',
                data: function (term, page) {
                    return {
                        query: term.toLowerCase(),
                        page: page // page number
                    };
                },
                results: function (data, page) {
                    return data;
                }
            },
            initSelection: function (element, callback) {
                callback({id: category, text: category });
            }
        }).select2('val', []);

        $("#searchbytagkbtic").val(category).trigger("change");
    }
    else{

        var catSelect = $("#searchbytagkbtic").val().split(",");
         $('#searchbytagkbtic').select2({
            tags: [],
            tokenSeparators: [","],
            minimumInputLength: 1,
            ajax: {
                url: portal_url + '/getVocabulary?name=plone.app.vocabularies.Keywords',
                data: function (term, page) {
                    return {
                        query: term.toLowerCase(),
                        page: page // page number
                    };
                },
                results: function (data, page) {
                    return data;
                }
            },
            initSelection: function (element, callback) {

                var data = [];

                for(var i = 0; i < catSelect.length; i++){
                    data.push({id:catSelect[i],text:catSelect[i]});
                }
                data.push({id: category, text: category});
                callback(data);

            }
        }).select2('val', []);

        var catToSearch = $("#searchbytagkbtic").val();
        $("#searchbytagkbtic").val(catToSearch).trigger("change");
    }

});


// ========================================================================== //

    (function($) {
        $.getValue = function(key)   {
            key = key.replace(/[\[]/, '\\[');
            key = key.replace(/[\]]/, '\\]');
            var pattern = "[\\?&]" + key + "=([^&#]*)";
            var regex = new RegExp(pattern);
            var url = decodeURI(window.location.href);
            var results = regex.exec(url);
            if (results === null) {
                return null;
            } else {
                return results[1];
            }
        }
    })(jQuery);

var getVal = $.getValue("cat");

$("a.searchRedirect").on("click", function (event) {
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    var category = $(this).attr("value");
    var host = $(location).attr('host');
    var pathname = $(location).attr('pathname');
    var root_path = 'http://' + host + pathname;
    $(location).attr('href',root_path+'/kbtic-rin/?cat='+category);
});



if (getVal != null) {
    var category = getVal
    if ($("#searchbytagkbtic").val() == ''){
        $('#searchbytagkbtic').select2({
            tags: [],
            tokenSeparators: [","],
            minimumInputLength: 1,
            ajax: {
                url: portal_url + '/getVocabulary?name=plone.app.vocabularies.Keywords',
                data: function (term, page) {
                    return {
                        query: term.toLowerCase(),
                        page: page // page number
                    };
                },
                results: function (data, page) {
                    return data;
                }
            },
            initSelection: function (element, callback) {
                callback({id: category, text: category });
            }
        }).select2('val', []);
        $("#searchbytagkbtic").val(category).trigger("change");
    }

    else{

        var catSelect = $("#searchbytagkbtic").val().split(",");
         $('#searchbytagkbtic').select2({
            tags: [],
            tokenSeparators: [","],
            minimumInputLength: 1,
            ajax: {
                url: portal_url + '/getVocabulary?name=plone.app.vocabularies.Keywords',
                data: function (term, page) {
                    return {
                        query: term.toLowerCase(),
                        page: page // page number
                    };
                },
                results: function (data, page) {
                    return data;
                }
            },
            initSelection: function (element, callback) {

                var data = [];

                for(var i = 0; i < catSelect.length; i++){
                    data.push({id:catSelect[i],text:catSelect[i]});
                }
                data.push({id: category, text: category});
                callback(data);

            }
        }).select2('val', []);

        var catToSearch = $("#searchbytagkbtic").val();
        $("#searchbytagkbtic").val(catToSearch).trigger("change");
    }

}

});
