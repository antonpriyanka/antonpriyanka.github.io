$.ajax({
  type: "POST",
  url: "~/othello_gui.py",
  data: { param: text}
}).done(function( o ) {
   // do something
});
