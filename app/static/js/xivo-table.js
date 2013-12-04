$(function() {

  $.extend($.tablesorter.themes.bootstrap, {
    table      : 'table table-bordered',
    caption    : 'caption',
    header     : 'bootstrap-header',
    sortNone   : 'bootstrap-icon-unsorted',
    sortAsc    : 'icon-chevron-up glyphicon glyphicon-chevron-up',
    sortDesc   : 'icon-chevron-down glyphicon glyphicon-chevron-down',
  });


  var $table = $("table").tablesorter({
    theme : "bootstrap",
    widthFixed: true,
    headerTemplate : '{content} {icon}', 
    widgets : [ "uitheme", "filter", "zebra" ],

    widgetOptions : {
      zebra : ["even", "odd"],
      filter_anyMatch : true,
      filter_liveSearch : true,
      filter_columnFilters: false,
      filter_reset : ".reset"

    }
  })
  .tablesorterPager({
      container: $(".ts-pager"),
      cssGoto  : ".pagenum",
      removeRows: false,
      output: '{startRow} - {endRow} / {filteredRows} ({totalRows})'
  });

  $.tablesorter.filter.bindSearch($table, $('.search'));

});
