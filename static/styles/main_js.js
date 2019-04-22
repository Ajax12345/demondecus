$(document).ready(function(){
      function get_notes(){
        var result = [];
        $('.main_note_display').each(function(){
          result.push({'note':$(this).data('note'), 'line':parseInt($(this).data('line')), 'position':parseInt($(this).data('position')), 'count':parseInt($(this).data('notecount')), 'step':$(this).data('step')});
        });
        return result;
      }
      var note_count = 1;
      var note_block_count = 1;
      var line_number = 1;
      var step = 'no_step';
      var reset_flag = false;
      var selected_note = 'quarter_note';
      function step_class(){
        if (step === 'no_step'){
          return 'no_step';
        }
        if (selected_note === 'whole_note'){
          return 'whole_note_step';
        }
        return step;
      }
      function get_step_val(_note, step){
        if (step){
          if (_note === 'whole'){
            return 'whole_note_step';
          }
          return 'has_step';
        }
        return 'no_step';

      }
      for (var i = 1; i < 8; i++){
        var html = `
        <table style='margin:0 auto;' data-line='${i}' id='music_table${i}'>
        <tr>
          <td><div class='clef'></div></td>
          <td>
          <div class='music_line' data-line='${i}' id='music_line${i}'>
            <div class='music_bar no_border1' data-bar='1' data-parent='${i}'>
              <table><tr id='music_bar_${i}_1'></tr></table>
            </div>
            <div class='music_bar no_border1' data-bar='2' data-parent='${i}'>
              <table><tr id='music_bar_${i}_2'></tr></table>
            </div>
            <div class='music_bar no_border1 no_border2' data-bar='3' data-parent='${i}'>
              <table><tr id='music_bar_${i}_3'></tr></table>
            </div>
            <div class='music_bar' data-bar='4' data-parent='${i}'>
              <table><tr id='music_bar_${i}_4'></tr></table>
            </div>
            <div class='music_bar' data-bar='5' data-parent='${i}'>
              <table><tr id='music_bar_${i}_5'></tr></table>
            </div>
            <div class='music_bar' data-bar='6' data-parent='${i}'>
              <table><tr id='music_bar_${i}_6'></tr></table>
            </div>
            <div class='music_bar' data-bar='7' data-parent='${i}'>
              <table><tr id='music_bar_${i}_7'></tr></table>
            </div>
            <div class='music_bar no_border' data-bar='8' data-parent='${i}'>
              <table><tr id='music_bar_${i}_8'></tr></table>
            </div>
            <div class='music_bar no_border' data-bar='9' data-parent='${i}'>
              <table><tr id='music_bar_${i}_9'></tr></table>
            </div>
            <div class='music_bar no_border' data-bar='10' data-parent='${i}'>
              <table><tr id='music_bar_${i}_10'></tr></table>
            </div>
          </div>
          </td>
        </tr>
        </table>
        <div style='height:50px;'></div>
        `;
        $('.composition').append(html);

      }
      for (var i = 1; i < 11; i++){
        var html = `
        <td><div class='note_block' style='margin-left:60px;' data-blockcount="${note_block_count}" data-position="${i}"></div></td>
        `;
        $("#music_bar_"+line_number.toString()+"_"+i.toString()).append(html);
      }
      note_block_count++;
      $('.header').on('click', '.select_datasets', function(){
        if ($('.composer_pannel').css('display') === 'none'){
          $('.composer_pannel').css('display', 'block');
        }
        else{
          $('.composer_pannel').css('display', 'none');
        }
      });
      $('.composer_pannel').on('click', '.pannel_composer', function(){
        var _id = parseInt($(this).data('composer'));
        var ref = $(this);
        $('.pannel_composer').each(function(){
          $(this).attr('class', 'pannel_composer');
        });
        ref.attr('class', 'pannel_composer selected');
      });
      $('.composition').on('click', '.note_block', function(){
        var ref = $(this);
        var flag = true;
        var count = parseInt(ref.data('blockcount'));
        var _position = ref.data('position');
        $('.note_block').each(function(){
          if (parseInt($(this).data('blockcount')) === count){
            $(this).css('background-color', 'white');
            var pos = parseInt($(this).data('position'));
            if (3 > pos || pos > 7 ){
              $(this).css('border-bottom-color', 'white');
            }

            $(this).html('');
          }
        });
        if (count+1 === note_block_count){
          for (var i = 1; i < 11; i++){
            if (reset_flag){
              var html = `
              <td><div class='note_block' data-blockcount="${note_block_count}" data-position="${i}" style='margin-left:60px;'></div></td>
              `;

            }
            else{
              var html = `
              <td><div class='note_block' data-blockcount="${note_block_count}" data-position="${i}"></div></td>
              `;
            }

            $("#music_bar_"+line_number.toString()+"_"+i.toString()).append(html);
          }
          reset_flag= false;
          note_block_count++;
        }
        var new_html = `
          <div class='${selected_note} main_note_display ${step_class()}' data-line='${line_number}' data-note='${selected_note}' data-position='${_position}' data-notecount='${note_count}' data-step='${step}'></div>
        `;
        note_count++;
        if (note_count%39===0){
          reset_flag = true;
          line_number++;
        }
        ref.append(new_html);
      });
      $(document).on({

          mouseenter: function () {
            if ($(this).css('background-color') != 'rgb(255, 255, 255)'){
              $(this).css( 'cursor', 'pointer' );
              $(this).css('background-color', '#FC9FB4');
            }


          },
          mouseleave: function () {
            if ($(this).css('background-color') != 'rgb(255, 255, 255)'){
              $(this).css( 'cursor', 'default' );
              $(this).css('background-color', '#F46A8A');
            }

          }
      }, ".note_block");
      $('.note_choices').on('click', '.pallete_note', function(){
        var ref = $(this);
        $('.pallete_note').each(function(){

          $(this).attr('class', 'pallete_note');

        });
        selected_note = ref.data('note');
        ref.attr('class', 'pallete_note pallete_selected');

      });
      $('.note_choices').on('click', '.step_selection', function(){
        var ref = $(this);
        $('.step_selection').each(function(){
          $(this).attr('class', 'step_selection');
        });
        step = $(this).data('step');
        ref.attr('class', 'step_selection step_selected');
      });
      $('.outer_predict_wrapper').on('click', '.predict_note', function(){

          var selected;
          $('.pannel_composer').each(function(){
            if ($(this).prop('class').match('selected')){
              selected = $(this).data('composer');
            }
          });
          $.ajax({
            url: "/predict_note",
            type: "get",
            data: {'notes': JSON.stringify(get_notes()), 'composer':selected},
            success: function(response) {
              var converter = {'eighth': 'eighth_note', 'quarter': 'quarter_note', '16th': 'sixteenth_note', 'half': 'half_note', 'whole': 'whole_note'};
              note_count++;
              var step_val = get_step_val(response.result.note.type, response.result.note.step);
              var new_html = `
                <div class='${converter[response.result.note.type]} main_note_display ${step_val}' data-line='${line_number}' data-note='${converter[response.result.note.type]}' data-position='${response.result.note.line}' data-notecount='${note_count}' data-step='${step_val}'></div>
              `;
              $('.note_block').each(function(){
                if (parseInt($(this).data('blockcount')) === note_block_count-1){
                  $(this).css('background-color', 'white');
                  var pos = parseInt($(this).data('position'));
                  if (3 > pos || pos > 7 ){
                    $(this).css('border-bottom-color', 'white');
                  }
                  if (parseInt($(this).data('position')) === response.result.note.line){
                    $(this).html(new_html);
                  }
                }
              });
              note_block_count++;
              if (note_count%39===0){
                reset_flag = true;
                line_number++;
              }
              for (var i = 1; i < 11; i++){
                if (reset_flag){
                  var html = `
                  <td><div class='note_block' data-blockcount="${note_block_count}" data-position="${i}" style='margin-left:60px;'></div></td>
                  `;

                }
                else{
                  var html = `
                  <td><div class='note_block' data-blockcount="${note_block_count}" data-position="${i}"></div></td>
                  `;
                }

                $("#music_bar_"+line_number.toString()+"_"+i.toString()).append(html);
              }

              reset_flag= false;
              note_block_count++;
            },
            error: function(xhr) {
              //Do Something to handle error
            }
          });

      });
    });
