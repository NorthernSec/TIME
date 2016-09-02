function loading(target, page, query){
  $("body").css("cursor", "progress");
  $(target).load(page, query, function(){$("body").css("cursor", "default");});
}

$(function() {
  $("[data-toggle='toggle']").click(function() {
    $($(this).data("target")).toggleClass('in');
  });
});
