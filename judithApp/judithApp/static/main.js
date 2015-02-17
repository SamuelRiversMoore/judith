
$(document).ready(function() {
  // on form submission ...
  chitchat("judith", "Salut!" );

  $('form').on('submit', function() {
    // grab values
    userStr = $('input[name="user"]').val();
    chitchat("user", userStr );
    $('input[name="user"]').val('');

    $.ajax({
      type: "POST",
      url: "/",
      data : { 'first': userStr },
      success: function(results) {
        chitchat("judith", results );
      }
    });
  });
});

var chitchat = function(talkerID, text){
  if (text.indexOf("<-continuer->") >= 0){
    text = text.split("<-continuer->")
  }
  if (talkerID == "user"){
    reading = 0;
    time = 0;
  } else {
    reading = 2000;
    time = reading + text.length*150;
    typing();
  }
  if (jQuery.type(text) == "string"){
    setTimeout(function() {
      $('<div class="message">'+text+'</div>').addClass(talkerID).hide().appendTo('#message-wrapper').fadeIn("fast");
      console.log(text);
      deleteMessage();
      scrolling();
    }, time);
  }
  if (jQuery.type(text) == "array"){
    var count = 0
    $.each(text, function() {
      setTimeout(function() {
        $('<div class="message">'+text[count]+'</div>').addClass(talkerID).hide().appendTo('#message-wrapper').fadeIn("fast");
        console.log(text[count]);
        deleteMessage();
        scrolling();
        count += 1
      }, time);
    });   
  }
}
var typing = function(){
  setTimeout(function() {
    $('#typing').show();
  }, reading);
  setTimeout(function() {
    $('#typing').hide();
  }, time);      
}
var scrolling = function(){
  $('#container').animate({ scrollTop: $(document).height() }, 100);
}
var deleteMessage = function(){
  var messages = $('#message-wrapper').children('.message');
  if ( messages.length > 15 ){
    messages.first().remove();
  }
}