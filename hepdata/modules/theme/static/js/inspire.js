
var inspire_ds = (function () {

    return {
        get_inspire_data: function (inspire_id, callback) {
            $.ajax({
                dataType: "json",
                url: '/inspire/search?id=' + inspire_id,
                method: 'GET',
                processData: false,
                cache: true,
                success: function (data) {
                    console.log(data);
                    callback(data);
                }
            });
        },

        render_inspire_data: function (data) {
            if (data.status == 'success') {
                $("#inspire-retrieve-progress").addClass("hidden");

                var html = "<div class='alert alert-info'>A preview of the publication (not everything is displayed).</div>";
                html += '<p class="inspire-title"><a href="http://inspirehep.net/record/' + inspire_id + '" target="_blank">' + data.query.title[0] + '</a><p>';

                if (data.query.authors.length > 0) {
                    html += '<p class="inspire-authors">' + data.query.authors[0].full_name + (data.query.authors.length > 1 ? " et al." : " ") + '</p>';
                }

                if (data.query.journal_info != '') {
                    html += '<p class="inspire-journal">' + data.query.journal_info + '</p>';
                }

                html += '<p class="inspire-abstract">' + data.query.abstract + '</p><br/>';

                html += '<p style="font-weight: bolder;">If you\'re happy that this is the correct INSPIRE Id, you just need to click on \'confirm\'. If not, you can retrieve another record.</p>';

                $("#inspire-result").addClass("well well-sm");
                $("#inspire-result").html(html);
                $("#success").removeClass("hidden");
                $("#inspire-add-button").removeClass("hidden");
                MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
            } else {
                $("#inspire-add-button").addClass("hidden");
            }
        }
    }
})();