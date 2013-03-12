$(window).ready(function() {
  $('.carousel').carousel({ interval: 10000 });
  $('.disabled').click(function(e) { e.preventDefault(); });
});
