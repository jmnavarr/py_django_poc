$(document).ready(function() {
    $('.prevent-default').on('click', function(e) {
        e.preventDefault();
    });

    $('#btn-select-all-search-results').on('click', function() {
       $('.search-result-checkbox').prop('checked', true);
    });

    $('#btn-export-csv-search-results').on('click', function() {
        href = $(this).attr('href');
        checkboxes = $('.search-result-checkbox');
        ids = '';

        $.each(checkboxes, function(index, value) {
            ids += $(value).data('search-result-id') + ',';
        });
        ids = ids.substring(0, ids.length - 1); // remove last comma

        $(this).attr('href', href + '?ids=' + ids);

        return true;
    });
});