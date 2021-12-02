$(function(){
    var $tabContent = $('#tabContent div');
    $('#tab input:first-child').addClass('selectedItem');
    $('#tab input').on('click', function(){
        var index = $(this).index();
        $('#tab input').removeClass('selectedItem');
        $(this).addClass('selectedItem');
        console.log(index)
        $tabContent.css('display','none');
        $tabContent.eq(index).css('display','block');
    });
});
