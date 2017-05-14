
$(document).ready(function(){

  $('.ingredients').hide();

  $('.to_fave').click(function() {
    var fave_id = $(this).attr('id');
    console.log(fave_id);
    $('#fave_form').append('<input type="hidden" name="id_input" id="id_input" value="' + fave_id + '"/>');
    $('#' + fave_id).hide();
    $('#fave_img_' + fave_id).show();
    $('#fave_form').submit();
    $('#id_input').remove();
  });

  $('#fave_form').submit(function(e){
    e.preventDefault();
    $.ajax({
      url: '/favorite',
      method: 'post',
      data: $(this).serialize(),
      success: function(serverResponse){
      }
    });
  });

  $('.fave_img').click(function() {
    var full_id = $(this).attr('id');
    var fave_id = full_id.substring(9);
    $('#unfave_form').append('<input type="hidden" name="id_input" id="id_input" value="' + fave_id + '"/>');
    $('#' + fave_id).show();
    $('#fave_img_' + fave_id).hide();
    $('#unfave_form').submit();
    $('#id_input').remove();
  });

  $('#unfave_form').submit(function(e){
    e.preventDefault();
    $.ajax({
      url: '/unfavorite',
      method: 'post',
      data: $(this).serialize(),
      success: function(serverResponse){
      }
    });
  });

  $('.ingredient_show').click(function() {
    var full_id = $(this).attr('id');
    var recipe_id = full_id.substring(11);
    if ( $('#ingredients_all_' + recipe_id).is(':hidden') ) {
      $('#ingredients_all_' + recipe_id).show();
      $('#ingredient_' + recipe_id).text('Hide Ingredients');
    } else {
      $('#ingredients_all_' + recipe_id).hide();
      $('#ingredient_' + recipe_id).text('Show Ingredients');
    }
  });

  $('#filter').change(function() {
    var cat = $(this).val();
    if (cat == 'all') {
      $('.category').show();
      $('.divider').show();
    }
    else {
      $('#' + cat).siblings().hide();
      $('.divider').hide();
      $('#' + cat).show();
    }
  });
});
