window.load_table_data = function(pagenum_selector, page) {
        var sel = $(pagenum_selector);
        var pagenum_id = '#'+sel.attr('id');
        var filterval = window[sel.attr('data-table-filter-func')]();
        var tbody_id = sel.attr('data-table-body-id');
        var tname = sel.attr('data-table-name');
        $.ajax({
                url: '/render-table-pagenums/'+tname+'/'+page+'?filters='+filterval,
                success: function(data) {
                        $(pagenum_id).html(data);
                }
        });
        $.ajax({
                url: '/render-table-page/'+tname+'/'+page+'?filters='+filterval,
                success: function(data) {
                        $(tbody_id).html(data);
                }
        });
};

$("a.page-num-anchor").live('click', function(){
        var pagenum_id = '#'+$(this).parent().attr('id');
        var page = $(this).attr('data-page-num');
        window['load_table_data'](pagenum_id, page);
});